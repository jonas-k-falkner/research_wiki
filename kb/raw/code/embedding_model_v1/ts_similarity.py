#
import logging
import math
from collections.abc import Callable
from typing import ClassVar

import numpy as np
import torch
from torch import Tensor

from .soft_dtw_torch import SoftDTW

logger = logging.getLogger(__name__)
DEFAULT_DEVICE_MEMORY = 32 * 1e8
EPS = 1.5 * float(np.finfo(np.float32).eps)


class SimilarityFunction:
    """Base class for similarity functions."""

    repr_args: ClassVar[list] = []

    def __init__(self, missing_value_strategy: str = "drop", max_nan_frac: float = 0.1, raise_on_nan: bool = True, **kwargs):
        self.nan_strategy = missing_value_strategy.lower()
        if self.nan_strategy == "drop":
            self._resolve_nan = self.drop_nan_periods
        elif self.nan_strategy == "mean":
            self._resolve_nan = self.impute_mean
        else:
            raise ValueError(f"unknown missing_value_strategy: '{missing_value_strategy}'")
        self.max_nan_frac = max_nan_frac
        self.raise_on_nan = raise_on_nan
        self.cuda = False

    def to(self, device: str | torch.device, **kwargs):
        if "cuda" in str(device) and torch.cuda.is_available():
            self.cuda = True

    def __repr__(self):
        sup_repr = f"nan={self.nan_strategy}, nan_frac={self.max_nan_frac}"
        self_repr = ", ".join([f"{arg}={getattr(self, arg)}" for arg in self.repr_args])
        return f"{self.__class__.__name__}({self_repr[2:]}, {sup_repr})"

    @staticmethod
    def slice_x_into_batches(x: Tensor, num_batches: int):
        n = x.shape[0]
        bs = math.ceil(n / num_batches)
        i = 0
        while i < num_batches:
            yield x[(bs * i) : (bs * (i + 1))]
            i += 1

    @staticmethod
    def impute_mean(x: Tensor, **kwargs) -> Tensor:
        """Missing value imputation simply replacing with series mean."""
        x = x.squeeze(-1)
        mask = torch.isnan(x)
        return x.masked_scatter_(mask, torch.nanmean(x, dim=1).repeat_interleave(repeats=mask.sum(-1), dim=0)).unsqueeze(-1)

    @staticmethod
    def drop_nan_periods(x: Tensor, **kwargs):
        """Drop every period in which there is at least one NaN value."""
        # x: (BS, T, ...) - second dim is period
        bs, _t, d = x.shape
        return x[(~torch.isnan(x).any(dim=0))[None, :, :].expand((bs, -1, -1))].view(bs, -1, d)

    @staticmethod
    def resolve_nan(resolve_nan_fn: Callable, x: Tensor, y: Tensor, max_nan_frac: float = 0.1, raise_on_nan: bool = True, **kwargs) -> tuple[Tensor, Tensor]:
        x_bs = x.shape[0]
        if x.shape[1] != y.shape[1]:
            # items of different length
            t_min = min(x.shape[1], y.shape[1])
            x = x[:, :t_min, :]
            y = y[:, :t_min, :]
        # join and resolve
        z = torch.cat((x, y), dim=0)
        # check if there are any nans to resolve
        nan_mask = torch.isnan(z)
        if not nan_mask.any():
            return x, y
        # check fraction of nans
        _n, t, d = z.shape
        assert d == 1
        nan_per_sample = nan_mask.sum(dim=1).sum(-1) / t
        if (nan_per_sample > max_nan_frac).any():
            if raise_on_nan:
                raise RuntimeError(f"Encountered too many nan values to impute: {nan_per_sample[nan_per_sample > max_nan_frac]} > {max_nan_frac}")
            else:
                # check if there is any data
                no_data = nan_per_sample == 1.0
                if no_data.any():
                    raise RuntimeError("There are some time series with no data what so ever!")

        z = resolve_nan_fn(z, **kwargs)
        # split back into x, y
        return z[:x_bs], z[x_bs:]

    def _forward(self, *args, **kwargs) -> Tensor:
        raise NotImplementedError

    def forward(self, x: Tensor, y: Tensor, resolve_nan: bool = True, raise_on_nan: bool = True, **kwargs) -> Tensor:
        if len(x.shape) != 3:
            raise ValueError(f"expected x with 3 dimensions but got {x.shape}")
        if len(y.shape) != 3:
            raise ValueError(f"expected y with 3 dimensions but got {y.shape}")

        if resolve_nan:
            x, y = self.resolve_nan(self._resolve_nan, x, y, max_nan_frac=self.max_nan_frac, raise_on_nan=self.raise_on_nan and raise_on_nan, **kwargs)
        return self._forward(x, y, **kwargs)


class TorchSoftDTW(SimilarityFunction):
    def __init__(
        self,
        bandwidth: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if torch.cuda.is_available():
            self.dev_cuda = torch.cuda.current_device()
            self.mem_cuda = int(torch.cuda.get_device_properties(self.dev_cuda).total_memory)
        else:
            self.dev_cuda = None
            self.mem_cuda = 0
        self.sdtw = SoftDTW(
            use_cuda=self.cuda,
            use_triton=self.cuda,
            # normalize to convert to valid distance
            normalize=True,
            bandwidth=bandwidth,
            **kwargs,
        )

    def to(self, device: str | torch.device, **kwargs):
        if "cuda" in str(device) and torch.cuda.is_available():
            self.cuda = True
            self.sdtw.use_cuda = True
            self.sdtw.use_triton = True

    def _forward(self, x: Tensor, y: Tensor, symmetric: bool = False, **kwargs):
        bs_x, t_x, _d_x = x.shape
        bs_y, t_y, _d_y = y.shape
        t = max(t_x, t_y)
        # this is some approximate memory requirement for the DTW forward pass
        # the main influence comes from the bs_y*bs_y distance matrix
        mem_req = ((bs_x * bs_y * t * 0.5) / (1 + symmetric)) * 10000
        mem = self.mem_cuda - torch.cuda.memory_allocated(self.dev_cuda) * 1.1 if self.cuda else DEFAULT_DEVICE_MEMORY

        # check if we need to split batches to keep memory in check
        split = mem_req > mem or (max(bs_x, bs_y) > 256 and t > 120)
        num_split_batches = max(math.ceil(mem_req / mem), 3)
        if symmetric and torch.equal(x, y):
            # Only compute upper triangle + diagonal
            indices = torch.triu_indices(bs_x, bs_x, offset=0, device=x.device)
            x_sub = x[indices[0]]
            y_sub = y[indices[1]]

            # Compute distances
            if split:
                n = x_sub.shape[0]
                bs_new = math.ceil(n / num_split_batches)
                distances = torch.cat([self.sdtw(x_sub[i : i + bs_new], y_sub[i : i + bs_new]) / t for i in range(0, n, bs_new)])
            else:
                distances = self.sdtw(x_sub, y_sub) / t

            # Fill full symmetric matrix
            result = torch.zeros(bs_x, bs_y, device=x.device, dtype=distances.dtype)
            result[indices[0], indices[1]] = distances
            result[indices[1], indices[0]] = distances  # Mirror to lower triangle
            return result
        else:
            if split:
                return torch.cat([soft_dtw(x_, y, sdtw=self.sdtw) for x_ in self.slice_x_into_batches(x, num_split_batches)], dim=0)
            else:
                return soft_dtw(x, y, sdtw=self.sdtw)


def soft_dtw(
    x: Tensor,
    y: Tensor,
    sdtw: SoftDTW,
) -> Tensor:
    """Compute the full n^2 soft dynamic time warping distance between x and y."""
    bs_x, t_x, d_x = x.shape
    bs_y, t_y, d_y = y.shape
    t = max(t_x, t_y)
    # expand such that every x is paired with all y
    x = x[:, None, :, :].expand(-1, bs_y, -1, -1).reshape(-1, t_x, d_x)
    y = y[None, :, :, :].expand(bs_x, -1, -1, -1).reshape(-1, t_y, d_y)
    assert x.shape == y.shape
    # normalize by seq len
    return sdtw(x, y).view(bs_x, bs_y) / t


def compute_similarity(sim_fn: SimilarityFunction, x: Tensor, y: Tensor, **kwargs):
    """Compute the provided sim function for the provided inputs."""
    # this is a bit of a redundant functionality, but serves to make the
    # calling for the similarity results consistent with how
    # the SimMemoryBuffer is called, where the sim_fn is
    # provided and not called directly
    return sim_fn.forward(x, y, **kwargs)


class MemoryBin:
    """Buffer wrapping functionality for a single
    time length bin of the SimMemoryBuffer."""

    def __init__(self):
        self.x = None
        self.z = None

    @torch.no_grad()
    def add(self, x: Tensor, z: Tensor):
        """add new records to the bin."""
        if self.x is None:
            assert self.z is None
            self.x = x
            self.z = z
        else:
            self.x = torch.cat((self.x, x), dim=0)
            self.z = torch.cat((self.z, z), dim=0)

    @torch.no_grad()
    def remove(self, n: int):
        """remove older records from bin"""
        n = min(n, self.size())
        self.x = self.x[n:]
        self.z = self.z[n:]

    def size(self):
        return 0 if self.x is None else self.x.shape[0]


class SimMemoryBuffer:
    """Memory buffer for similarity based SSL.

    Args:
        sim_fn: Combined similarity function.
        memory_size: maximum size of memory buffer.
        max_len_diff: maximum difference of length of series when sampling
        seed: seed for random number generation.
    """

    def __init__(
        self,
        sim_fn: SimilarityFunction,
        memory_size: int,
        seed: int = 369,
        **kwargs,
    ):
        self.sim_fn = sim_fn
        self.memory_size = memory_size
        self.seed = seed
        #
        self.rng = torch.Generator(device="cpu")
        self.rng.manual_seed(self.seed)
        self.memory = None
        self.cur_bin = None
        self.reset()

    def reset(self):
        """Reset, i.e. clear, memory and indices."""
        self.memory = None
        self.cur_bin = None

    @torch.no_grad()
    def add(self, x: Tensor, z: Tensor) -> None:
        """Add records to memory."""
        if self.memory_size is None or self.memory_size <= 0:
            # no memory
            return
        if len(x.shape) != 3:
            raise ValueError(f"expected x to be 3 dimensional but got {len(x.shape)} dimensions.")
        x, z = x.cpu().detach(), z.cpu().detach()
        bs, t, _d = x.shape

        if self.cur_bin is None or t != self.cur_bin:
            self.reset()
            self.cur_bin = t
            self.memory = MemoryBin()

        new_size = self.memory.size() + bs
        if new_size > self.memory_size:
            # remove old records if buffer is full
            n_trunc = new_size - self.memory_size
            self.memory.remove(n=n_trunc)

        # add to existing memory bin
        self.memory.add(x, z)

    @torch.no_grad()
    def sample(self, t: int, n: int) -> tuple[Tensor, Tensor] | tuple[None, None]:
        """Sample records from memory.

        Args:
            t: length of series to sample
            n: number of samples

        """
        # the goal is to only sample items with length similar to 't' if available
        if self.cur_bin is None or t != self.cur_bin:  # no samples with similar length available
            return None, None
        samp_idx = torch.randperm(n=self.memory.size(), generator=self.rng)[:n]
        return self.memory.x[samp_idx].detach(), self.memory.z[samp_idx].detach()

    @torch.no_grad()
    def compute_sim(self, x: Tensor, n_samples: int = 0, **kwargs) -> tuple[Tensor, Tensor | None, Tensor | None]:
        """
        calculate ts similarity between all series in x and
        optionally a number of samples from the buffer.

        Args:
            x: original time series (BS, T, D_org)
            n_samples: number of samples to retrieve from buffer

        """
        x_samp, z_samp = None, None
        if n_samples > 0:
            if self.memory_size is None or self.memory_size <= 0:
                raise RuntimeError("no memory specified on init. Cannot sample from 0 length memory.")
            x_samp, z_samp = self.sample(t=x.size(1), n=n_samples)

        # compute
        return (
            self.sim_fn.forward(x, x, symmetric=True, **kwargs),
            self.sim_fn.forward(x, x_samp.to(dtype=x.dtype, device=x.device), **kwargs) if x_samp is not None else None,
            z_samp.to(device=x.device) if z_samp is not None else None,
        )
