# TODO

## Features

- Implement comparison operators (`__eq__`, `__lt__`, etc.), returning
  0/1 `NumericSequence` results rather than `Sequence[bool]`; record
  the decision in `NOTES.md` once implemented.

- Add an `example/` top-level folder. Ideas: `e_and_pi.py` (π/e
  approximation via `Series`), `integral.py` (Riemann-sum
  approximation sequences, Simpson, etc.).

## Testing

- Add a unit test suite for `utils.py`.

- Test extensively beyond the pytest suite, e.g. manual
  exploration, edge cases, unusual input combinations.

## Documentation

- Add a scalar broadcasting example to `README.md`:

```python
  # Scalar broadcasting.
  print((squares + 1).head(5))
  # ⟨2, 5, 10, 17, 26⟩
```

- Add a thematic/visual header image to `README.md` — general
  calculus-themed imagery, not an architecture diagram.

- Add `CHANGELOG.md`.

- Once `Series` exists, extend "Restricted `first_index`" in
  `NOTES.md`. If `Series` hard-enforces `first_index=1` (verify
  this first), note that `FIRST_INDEX_OPTIONS = (0, 1)` is now
  validated by two concrete cases: `Recurrence` enforcing 0 and
  `Series` enforcing 1.

## Style

- Revise `STYLE.md` (see `attic/style/missing.txt`).

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

- Add a script to clean generated artifacts (e.g. `__pycache__`).

## Open Questions

- Should a `PowerSeries` abstraction be added?

- Should `BinarySequence`/`RandomSequence` abstractions be added?
