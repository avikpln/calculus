# Calculus

![CI](https://github.com/avikpln/calculus/actions/workflows/ci.yml/badge.svg)

A Python library for representing and manipulating infinite sequences
through lazy evaluation.

## Vision

The Calculus package aims to provide a collection of reusable
abstractions for discrete and continuous mathematics.

The current implementation provides a generic `Sequence[T]` abstraction
together with the specialized `NumericSequence`, `Recurrence`,
`NumericRecurrence`, and `Series` subclasses.

## Features

-   Generic `Sequence[T]` implementation.
-   `NumericSequence` with element-wise arithmetic.
-   `Recurrence` for sequences defined by recursive relations.
-   `NumericRecurrence` combining numeric arithmetic with recursively
    defined elements.
-   `Series` for sequences defined by partial sums of an underlying
    term sequence.
-   Infinite (and finite) sequences.
-   Lazy evaluation via user-defined rules.
-   Support for zero- and one-indexed sequences.
-   Element access and slicing.
-   Forward iteration over subsequences.
-   `Sequence` transformations (`map`, `combine`, `shift_by`,
    `shift_to`).
-   Factory methods for constant sequences and sequences built from
    iterables.
-   Fully type-annotated (`mypy --strict`).

## Examples

### `Sequence`

```python
from calculus import Sequence

# Infinite sequence of uppercase letters, cycling through the alphabet.
alphabet = Sequence(lambda n: chr(65 + (n - 1) % 26))

print(alphabet.head(5))
# ⟨A, B, C, D, E⟩

print(alphabet[30])
# D

# map() works for any element type, not just numbers.
print(alphabet.map(str.lower).head(5))
# ⟨a, b, c, d, e⟩
```

### `NumericSequence`

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

### `Recurrence`

```python
from calculus import Recurrence

# Fibonacci sequence: each term is the sum of the two before it.
fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))

print(fib.head(8))
# ⟨0, 1, 1, 2, 3, 5, 8, 13⟩
```

### `NumericRecurrence`

```python
from calculus import NumericRecurrence

# Fibonacci sequence, with arithmetic operations available directly.
fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))

print((fib + 1).head(8))
# ⟨1, 2, 2, 3, 4, 6, 9, 14⟩

print((-fib).head(8))
# ⟨0, -1, -1, -2, -3, -5, -8, -13⟩

# Babylonian method sequence approximating the real-valued square root
# of 2. Formula: x_{n+1} = 0.5 * (x_n + 2 / x_n) starting with an
# initial guess of 2.0.
babylonian_sqrt2 = NumericRecurrence(
    lambda n, a: 0.5 * (a[-1] + 2.0 / a[-1]),
    basis=(2.0,)
)

print(babylonian_sqrt2.head(5))
# ⟨2.0, 1.5, 1.4166666666666665, 1.4142156862745097, 1.4142135623746899⟩
```

### `Series`

```python
from calculus import Series

# Triangular numbers: partial sums of the natural numbers.
triangular = Series(lambda n: n)

print(triangular.head(5))
# ⟨1, 3, 6, 10, 15⟩

# Leibniz series: partial sums approximating pi / 4.
leibniz = Series.leibniz()

print(leibniz.map(lambda x: round(x, 4)).head(5))
# ⟨1.0, 0.6667, 0.8667, 0.7238, 0.8349⟩

print(4 * leibniz[1000])
# 3.140592653839794
```

## Project Layout

``` text
├── .github
│   └── workflows
│       └── ci.yml                    # GitHub Actions CI workflow
├── calculus
│   ├── __init__.py                   # Package public API
│   ├── numeric_recurrence.py         # NumericRecurrence implementation
│   ├── numeric_sequence.py           # NumericSequence implementation
│   ├── recurrence.py                 # Recurrence implementation
│   ├── sequence.py                   # Sequence implementation
│   ├── series.py                     # Series implementation
│   └── utils.py                      # Shared validation helpers
├── tests
│   ├── test_numeric_recurrence.py    # Pytest test suite
│   ├── test_numeric_sequence.py      # Pytest test suite
│   ├── test_recurrence.py            # Pytest test suite
│   ├── test_sequence.py              # Pytest test suite
│   └── test_series.py                # Pytest test suite
├── .gitignore
├── ARCHITECTURE.md                   # Class hierarchy and relationships
├── DESIGN.md                         # Per-class technical design summary
├── LICENSE
├── NOTES.md                          # Design rationale and architectural decisions
├── pytest.ini                        # Adds project root to sys.path for tests
├── README.md
├── requirements-dev.txt              # Development and CI dependencies
├── STYLE.md                          # Project coding and documentation conventions
└── TODO.md                           # Planned enhancements
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

## Documentation

-   `STYLE.md` describes the project's coding and documentation
    standards.
-   `NOTES.md` records design decisions and implementation rationale.
-   `DESIGN.md` records the current, per-class technical design.

## License

See `LICENSE`.
