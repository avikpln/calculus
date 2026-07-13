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
