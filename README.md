# Calculus

A Python library for representing and manipulating finite and infinite
sequences through lazy evaluation.

## Vision

The Calculus package aims to provide a collection of reusable
abstractions for discrete and continuous mathematics.

The current implementation provides a generic `Sequence[T]`
abstraction, which serves as the foundation for future components such
as numeric sequences, recurrences, series, and function abstractions.

## Features

-   Generic `Sequence[T]` implementation.
-   Finite and infinite sequences.
-   Lazy evaluation via user-defined rules.
-   Arbitrary starting indices.
-   Element access and slicing.
-   Forward iteration over subsequences.
-   Sequence transformations (`map`, `combine`, `shift_by`, `shift_to`).
-   Factory methods for constant sequences and sequences built from
    iterables.
-   Fully type-annotated (`mypy --strict`).

## Dependencies

Calculus has no runtime dependencies beyond the Python standard
library.

Development requires:

- `mypy` for static type checking
- `pyflakes` for static analysis
- `pydocstyle` for docstring style checking
- `pytest` for unit testing

## Project layout

``` text
├── calculus
│   ├── __init__.py      # Package public API
│   ├── sequence.py      # Generic Sequence implementation
│   ├── test_sequence.py # Pytest test suite
│   └── utils.py         # Shared validation helpers
├── .gitignore
├── LICENSE
├── NOTES.md             # Design rationale and architectural decisions
├── README.md
├── STYLE.md             # Project coding and documentation conventions
└── TODO.md              # Planned enhancements
```

## Example

```python
from calculus import Sequence

# Infinite sequence of perfect squares.
squares = Sequence(lambda n: n**2)

print(squares[3])
# 9

print(squares.head(5))
# ⟨1, 4, 9, 16, 25⟩
```

## Development

The project emphasizes:

- clean API design;
- strict static typing;
- comprehensive documentation;
- thorough unit testing.

Before committing, run:

```text
mypy --strict calculus
pyflakes calculus
pydocstyle calculus
pytest
```

## Documentation

-   `STYLE.md` describes the project's coding and documentation
    standards.
-   `NOTES.md` records design decisions and implementation rationale.

## License

See `LICENSE`.
