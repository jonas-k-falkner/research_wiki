"""Skip all integration tests when fastembed is not installed."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _require_fastembed() -> None:
    """Skip the test if the [semantic] extra is absent."""
    try:
        import fastembed  # noqa: F401
    except ImportError:
        pytest.skip("fastembed not installed — run: uv sync --extra semantic")
