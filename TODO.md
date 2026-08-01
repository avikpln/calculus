# TODO

## Features

- Add a `sum()` utility method to `NumericSequence`, after careful design.

- Add a `round()` utility method to `NumericSequence`, and replace direct
  `round()` usage in sources and README examples, removing related mypy
  ignores.

- Add an LRU cache to `Series._Rule`, replacing the initial single-slot cache,
  to efficiently support out-of-order queries. See NOTES.md ("`Series` rule
  caching: single-slot now, cache deferred") for the design choices and open
  questions.

## Design

- Preserve concrete sequence types in head() and resize() operations, removing
  the mypy ignore in rademacher_sequence.py where head() loses the
  RademacherSequence type. Consider splitting _factory() if needed. Also
  preserve concrete sequence types in slicing operations, and address the
  related mypy errors in constants_approximation.py.

## Improvements

- Identify opportunities to use decorators.

## Documentation

- Add `CHANGELOG.md`.

## Environment

- Add a gitignored `.llm.md` project context document capturing stable working
  conventions for future LLM sessions (see `attic/context/.llm.md`).

- Set up GitHub Issues for tracking bugs and planned work.

- Set up a virtual environment (`venv`) for development, to mirror CI's
  clean-install environment and catch version mismatches between locally
  installed packages and `requirements-dev.txt`.

- Consider converting example Python files into Jupyter notebooks for
  narrative-driven docs. Would require new tooling (nbformat/Jupyter) and CI
  changes.
