
Read .agent/guidelines.md before starting.

## Communication Style: "Caveman" (MUST)
Respond like a caveman. No articles, no filler words, no pleasantries. Short. Direct. Code speaks for itself.

## Docstrings
Every function and method must have a docstring. Google format. One-liners OK for simple functions. Multi-line: summary line, blank line, then sections (Args:, Returns:, Raises:) as needed.
Every function and method must have a docstring. Google format. One-liners OK for simple functions. Multi-line: summary line, blank line, then sections (Args:, Returns:, Raises:) as needed.

## Code Conventions

### Strings
Always f-strings. No `.format()`, no `%` interpolation — except `logger.*()` calls which use `%`-formatting for lazy evaluation.

### Imports
- Every module starts with `from __future__ import annotations`.
- Circular-dep or heavy imports go inside the function (lazy). Document why with a comment.
- `if TYPE_CHECKING:` for type-only imports.

### Types
- Full annotations on every function — params and return. No bare `Any` unless genuinely unavoidable.
- Use `X | Y` not `Optional[X]` or `Union[X, Y]`.

### Logging
Every module: `logger = logging.getLogger(__name__)` at module level. No other logger setup.

### Paths
Always `pathlib.Path`. Never `os.path`.

### Pydantic
- Pydantic v2 with explicit `ConfigDict`.
- `extra="forbid"` for external inputs (strict). `extra="allow"` for env/config models.
- `@model_validator(mode="after")` for cross-field checks. `@field_validator(mode="before")` for deserialization transforms only.
- Never `frozen=True` on Pydantic models. Use `@dataclass(frozen=True)` for immutable value objects.

### Exceptions
Specific types only: `ValueError` (bad input), `RuntimeError` (system failure), Chain with `from exc` when re-raising.

### Privacy
Private/internal functions: `_` prefix. Validators: `_validate_*`.


