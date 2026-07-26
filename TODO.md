# TODO

## Design

- Create a DESIGN.md capturing distilled, per-class design decisions.
  See attic/design/ for discarded attempts.

## Features

- Add an `example/` top-level folder. Ideas: `e_and_pi.py` (π/e
  approximation via `Series`), `integral.py` (Riemann-sum
  approximation sequences, Simpson, etc.).

- Add an LRU cache to `Series._Rule`, replacing the initial single-slot
  cache, to efficiently support out-of-order queries. See NOTES.md
  ("`Series` rule caching: single-slot now, cache deferred") for the
  design choices and open questions.

## Improvements

- Identify opportunities to use decorators.

## Testing

- Change SPECIAL SEQUENCES to SPECIAL NUMERIC SEQUENCES in
  test_numeric_sequence.py.

- Review all test files for redundant, bloated, or missing tests.

- Add a unit test suite for `utils.py`.

- Test extensively beyond the pytest suite, e.g. manual
  exploration, edge cases, unusual input combinations.

## Documentation

- Fix Sequence.__init__'s docstring to add in ValueError:
  ", or if ``first_index`` is not in ``sequence.FIRST_INDEX_OPTIONS``.".

- Change "Boolean operators" to "logical operators" in ARCHITECTURE.md.

- Revise NOTES.md from top to bottom.

- Fix "Documentation" section in README.md.

- Fix "Feature implementation protocol" subsection in NOTES.md.

- Fix redundant comments about tests in README.md's project layout
  section.

- Review test module docstrings for accuracy.

- Wrap markdown files at 79 instead of 72.

- Add a scalar broadcasting example to `README.md`:

```python
  # Scalar broadcasting.
  print((squares + 1).head(5))
  # ⟨2, 5, 10, 17, 26⟩
```

- Add a thematic/visual header image to `README.md` — general
  calculus-themed imagery, not an architecture diagram.

- Add `CHANGELOG.md`.

- Review all docstrings and documentation comments.

## Style

- Convert type and constant comments to PEP 257 inline docstrings.

- Revise `STYLE.md` (see `attic/style/missing.txt`).

- Ensure that all Markdown files are not prematurely wrapped before 72
  characters.

## Environment

- Add a gitignored `.llm.md` project context document capturing stable
  working conventions for future LLM sessions (see
  `attic/context/.llm.md`).

- Set up GitHub Issues for tracking bugs and planned work.

- Set up a virtual environment (`venv`) for development, to mirror
  CI's clean-install environment and catch version mismatches between
  locally installed packages and `requirements-dev.txt`.

- Add a script to clean generated artifacts (e.g. `__pycache__`).

## Unresolved Questions

- Should a `ComplexSequence` class be added?

- Should a `PowerSeries` class be added?

- Should a `RandomSequence` class be added?

- Should `{rₙ}` be used to denote `Recurrence` and `NumericRecurrence`
  instead of `{aₙ}`?
