# NOTES

## Purpose

This document records design decisions and implementation rationale for
the `Sequence` library. It is intended as a long-term memory of *why*
certain choices were made, especially when the obvious implementation
was rejected.

Only decisions that may influence future development belong here.

------------------------------------------------------------------------

# API Design

## `Sequence.__repr__`

`__repr__` intentionally returns the same value as `__str__`.

A conventional representation such as

``` python
Sequence(func=<function <lambda> at 0x...>, ...)
```

is technically more faithful but usually provides little useful
information. Displaying a preview of the sequence is considerably more
informative.

This intentionally favors practicality over convention.

------------------------------------------------------------------------

## Shifting semantics

`shift_by()` and `shift_to()` transform the underlying evaluation rule,
not the visible window of a sequence.

Consequences:

-   size is preserved;
-   `first_index` is preserved;
-   finite sequences may evaluate indices outside their original domain.

Domain-preserving operations belong to `head()` and `tail()` instead.

Future subclasses such as `Recurrence` or `Series` may override these
methods to prohibit shifts that are incompatible with their evaluation
mechanism.

------------------------------------------------------------------------

## Forward-only iteration

`subiter()` supports only forward iteration (`step > 0`).

Although supporting negative steps would mimic `range()`, reverse
iteration complicates the implementation, provides little practical
benefit, and conflicts with the intended design of future recurrence-
based sequences.

General reindexing remains available through `subsequence()`.

------------------------------------------------------------------------

## `map()` and `combine()`

`map()` and `combine()` are instance methods.

Although `combine()` is mathematically symmetric, the instance-method
API is more fluent and naturally defines which sequence contributes
properties such as `size` and `first_index`.

This decision may be revisited if the library evolves toward a more
functional API.

------------------------------------------------------------------------

## Exposing the evaluation rule

The internal `_rule` object remains private.

A public property would simplify inspection, but would also constrain
future subclasses whose evaluation depends on mutable internal state
(e.g. cached recurrences).

Reconsider this only if a genuine use case emerges.

# Construction

## Default construction

`Sequence()` currently constructs an infinite sequence returning `None`.

This is convenient for placeholders and testing, but the long-term
semantics remain open.

Future work:

-   determine whether `Sequence()` should instead represent an empty
    sequence;
-   reconsider this together with the semantics of truthiness and
    default construction.

------------------------------------------------------------------------

## Default rule and typing

The default rule is implemented as a private function returning `None`.

This requires a localized

``` python
# type: ignore[assignment]
```

because `Callable[[int], None]` is not compatible with arbitrary
`Callable[[int], T]`.

Alternative designs (factory methods, `Sequence[None]`, etc.) were
considered but currently provide less convenient APIs.

------------------------------------------------------------------------

## Lazy validation

`Sequence.__init__()` eagerly validates its primary callable because it
establishes the object's core invariant.

Transformation methods such as `subsequence()`, `map()`, and `combine()`
do **not** eagerly validate their callables. Errors surface naturally
when the transformed sequence is evaluated, following the same EAFP
philosophy used elsewhere in the implementation.

# Documentation

## Private methods

Private methods use block comments rather than docstrings.

Public APIs are documented for users; private helpers are documented for
maintainers. Internal comments should explain implementation decisions
and invariants rather than duplicate the method signature.

------------------------------------------------------------------------

## Delegating methods

Methods that internally construct a new `Sequence` document only the
exceptions they can actually propagate.

Their docstrings should not simply refer readers to
`Sequence.__init__()`, because each delegating method reaches only part
of the constructor's validation logic.

# Implementation

## `_Rule.func` property

`_Rule` exposes its callable through a read-only property even though
calling `_func` directly would be microscopically faster.

The property represents the logical interface while `_func` remains an
implementation detail. The overhead is negligible compared to the
user-supplied callable.

Optimize only if profiling ever demonstrates a measurable benefit.

------------------------------------------------------------------------

## Fixed `first_index`

`first_index` is immutable.

Every operation deriving a new sequence preserves the original
`first_index`.

Whether arbitrary starting indices justify their additional complexity
should be reconsidered after the library has matured.

------------------------------------------------------------------------

## Internal invariants

Several methods contain assertions such as

``` python
assert self.size is not None
```

or

``` python
assert self.last_index is not None
```

These are not runtime validation but documentation of internal
invariants that current type checkers cannot infer.

If the repetition becomes excessive, consider replacing them with
private helper properties that establish the invariant in one place.

------------------------------------------------------------------------

## Code cleanliness

Avoid speculative imports, constants, and infrastructure.

Unused code should be introduced only when a concrete feature requires
it, keeping static analysis clean and reducing maintenance overhead.

# Development

## Local verification

Before every commit, run:

1.  `mypy --strict`
2.  `pyflakes`
3.  `pydocstyle`
4.  `pytest`
5.  `git diff --cached --check`, to catch trailing whitespace in
    staged changes

All checks should pass before committing.

This same sequence is automated by the project's CI workflow, which
uses the empty-tree hash to check every file in the repository rather
than just staged changes.

## Project layout

The project currently keeps the test suite alongside the library
sources inside the `calculus/` package.

This is appropriate while the project is small. As the library grows,
consider adopting the more conventional layout:

```text
calculus/
    __init__.py
    sequence.py
    utils.py

tests/
    test_sequence.py
```

Separating tests from the package scales better, matches common Python
project structure, and makes it easier to add fixtures, integration
tests, and continuous integration.

No migration is currently necessary. Revisit this once the project
contains multiple modules or a substantially larger test suite.

## Packaging

The project is not yet packaged for installation.

Once the public API has stabilized, add a `pyproject.toml` and support
standard installation workflows such as:

```bash
pip install -e .
```

Packaging should be introduced together with project metadata,
dependency declarations, and continuous integration so that the
repository follows modern Python packaging conventions.
