# TODO

## Design

- Create a DESIGN.md capturing distilled, per-class design decisions.
  See attic/design/ for discarded attempts.

## Features

- Add a `sum()` utility method to NumericSequence, after careful design.

- Add an LRU cache to `Series._Rule`, replacing the initial single-slot
  cache, to efficiently support out-of-order queries. See NOTES.md
  ("`Series` rule caching: single-slot now, cache deferred") for the
  design choices and open questions.

## Improvements

- Identify opportunities to use decorators.

## Testing

- Add a unit test suite for `utils.py`.

## Documentation

- Wrap markdown files at 79 instead of 72.

- Add a thematic/visual header image to `README.md` — general
  calculus-themed imagery, not an architecture diagram.

- Add `CHANGELOG.md`.

## Style

- Revise `STYLE.md` (see `attic/style/missing.txt`).

## Environment

- Add a gitignored `.llm.md` project context document capturing stable
  working conventions for future LLM sessions (see
  `attic/context/.llm.md`).

- Set up GitHub Issues for tracking bugs and planned work.

- Set up a virtual environment (`venv`) for development, to mirror
  CI's clean-install environment and catch version mismatches between
  locally installed packages and `requirements-dev.txt`.

- Add a script to clean generated artifacts (e.g. `__pycache__`).

- Consider converting example Python files into Jupyter notebooks for
  narrative-driven docs. Would require new tooling (nbformat/Jupyter)
  and CI changes (notebooks aren't covered by mypy/pyflakes/pytest the
  way .py files are).
