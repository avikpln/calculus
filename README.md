# Calculus

![CI](https://github.com/avikpln/calculus/actions/workflows/ci.yml/badge.svg)

A Python library for representing and manipulating finite and infinite
sequences through lazy evaluation.

## Vision

The Calculus package aims to provide a collection of reusable
abstractions for discrete and continuous mathematics.

The current implementation provides a generic `Sequence[T]`
abstraction together with the specialized `NumericSequence` subclass,
serving as the foundation for future components such as recurrences,
series, and function abstractions.

## Features

-   Generic `Sequence[T]` implementation.
-   `NumericSequence` with element-wise arithmetic.
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

Install development dependencies with:

```bash
pip install -r requirements-dev.txt
```

## Project layout

``` text
├── .github
│   └── workflows
│       └── ci.yml                    # GitHub Actions CI workflow
├── calculus
│   ├── __init__.py                   # Package public API
│   ├── numeric_sequence.py           # NumericSequence implementation
│   ├── sequence.py                   # Generic Sequence implementation
│   ├── test_numeric_sequence.py      # Pytest test suite
│   ├── test_sequence.py              # Pytest test suite
│   └── utils.py                      # Shared validation helpers
├── .gitignore
├── LICENSE
├── NOTES.md                          # Design rationale and architectural decisions
├── README.md
├── requirements-dev.txt              # Development and CI dependencies
├── STYLE.md                          # Project coding and documentation conventions
└── TODO.md                           # Planned enhancements
```

## Example

```python
from calculus import NumericSequence

# Infinite sequence of perfect squares.
squares = NumericSequence(lambda n: n ** 2)

print(squares[3])
# 9

print(squares.head(5))
# ⟨1, 4, 9, 16, 25⟩

# Unary arithmetic.
print(-squares.head(5))
# ⟨-1, -4, -9, -16, -25⟩

# Absolute value.
print(abs(-squares.head(5)))
# ⟨1, 4, 9, 16, 25⟩

# Element-wise addition.
evens = NumericSequence(lambda n: 2 * n)
print((squares + evens).head(5))
# ⟨3, 8, 15, 24, 35⟩

# Element-wise multiplication.
print((squares * evens).head(5))
# ⟨2, 16, 54, 128, 250⟩

# Exponentiation.
nonnegints = NumericSequence(lambda n: n, first_index=0)
print(2 ** nonnegints)
# ⟨1, 2, 4, 8, 16, ...⟩
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
git diff --cached --check
```

## Documentation

-   `STYLE.md` describes the project's coding and documentation
    standards.
-   `NOTES.md` records design decisions and implementation rationale.

## License

See `LICENSE`.
