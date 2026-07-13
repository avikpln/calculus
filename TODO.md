# TODO

## Features

- Implement comparison operators (`__eq__`, `__lt__`, etc.), returning
  0/1 `NumericSequence` results rather than `Sequence[bool]`; record
  the decision in `NOTES.md` once implemented.

## Testing

- Move test files into a `test/` directory, separating them from the
  package sources.

- Add a unit test suite for `utils.py`.

## Documentation

- Add a scalar broadcasting example to `README.md`:

```python
  # Scalar broadcasting.
  print((squares + 1).head(5))
  # ⟨2, 5, 10, 17, 26⟩
```

- Add a UML class diagram documenting the package architecture and
  relationships between public classes.

## Style

- Revise `STYLE.md` (see `attic/style/missing.txt`; also consider the
  error-delegation question).

- Decide and standardize a single line-break style for wrapped method
  signatures and call expressions. At least three styles currently
  coexist in the codebase: (1) grouped, multiple arguments per line
  wrapped at a fixed width; (2) one argument per line; (3) a hanging
  indent, with initial arguments on the opening line and continuation
  wrapped below. Pick one and apply it consistently project-wide.

- Standardize PEP 8 spacing around arithmetic operators (e.g. `a + b`
  vs. `a+b`; note that `**` is already decided to use no spaces for
  simple operands, e.g. `n**2`); record the decision in `NOTES.md`
  once resolved.

- Modernize typing imports: `Callable`, `Iterable`, `Generator` from
  `collections.abc`; `Generic`, `TypeVar`, `Protocol`, `overload`,
  `Self` from `typing`.

- Rename section-comment delimiters in `numeric_sequence.py` and
  `test_numeric_sequence.py` to include ARITHMETIC (e.g. `UNARY` →
  `UNARY ARITHMETIC`, `ADDITIVE` → `ADDITIVE ARITHMETIC`) for
  consistency across `UNARY`, `ADDITIVE`, `MULTIPLICATIVE`, and
  `EXPONENTIATION`.

## Environment

- Add a gitignored `.llm.md` project context document capturing stable
  working conventions for future LLM sessions (see
  `attic/context/.llm.md`).

- Add a gitignored `attic/` directory for retired ideas and discarded
  designs.

- Establish a tagging strategy for the project (e.g. tagging every
  version bump vs. deferring until the project has consumers or a
  `pyproject.toml` to pin against).

- Set up GitHub Issues for tracking bugs and planned work.

- Set up a virtual environment (`venv`) for development, to mirror
  CI's clean-install environment and catch version mismatches between
  locally installed packages and `requirements-dev.txt`.
