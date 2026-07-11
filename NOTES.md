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

## Numeric arithmetic via mixin, not multiple inheritance

When designing `NumericSequence`, the natural next thought was a
future `NumericRecurrence(NumericSequence, Recurrence)` — numeric
arithmetic plus recursive evaluation, combined the obvious way any
object-oriented instinct would reach for: multiple inheritance.

This was rejected, for reasons worth recording since they weren't
obvious until worked through.

**The `__slots__` problem.** `NumericSequence` and `Recurrence` both
descend from `Sequence`, forming a diamond. If both branches declare
non-empty `__slots__` (as `Recurrence` does, for `_basis`), Python
raises `TypeError: multiple bases have instance lay-out conflict` at
class-definition time. This isn't a style concern — the class
literally cannot be defined.

**The type-preservation problem, which is the deeper issue.** Even
setting `__slots__` aside, `combine()` returning `type(self)` — the
obvious way to make `NumericSequence.combine()` yield a
`NumericSequence` instead of a bare `Sequence[Number]` — is unsound in
general. A `Recurrence`'s identity *is* its recursive rule and basis;
the elementwise sum of two recurrences is not, in general, itself
expressible as some recursion with some basis. It is simply a sequence
evaluable independently at each index. Forcing `type(self)` here would
either silently produce a broken `Recurrence` or require reconstructing
a valid recursion for the result, which isn't generally possible.
`NumericSequence` itself is the special case where this danger doesn't
apply — it carries no extra structure beyond "numbers indexed by a
rule," so there is nothing for `combine()` to fail to preserve.

**Resolution: a mixin, not a shared base.** `ArithmeticMixin` provides
the arithmetic dunders (`__add__`, `__sub__`, etc.) without inheriting
from `Sequence` at all. It assumes only that `self` supports `map()`
and `combine()` — enforced via a `Protocol`, not runtime inheritance —
and its helper always constructs a plain `NumericSequence` as the
result, regardless of what class it's mixed into. This means:

- No diamond: a class like a future `NumericRecurrence` would inherit
  from `Recurrence` alone and mix in `ArithmeticMixin` separately, so
  its only path to `Sequence` is through `Recurrence` — ordinary
  single inheritance.
- No `__slots__` conflict: the mixin declares `__slots__ = ()`,
  contributing no instance layout.
- No type-preservation trap: arithmetic on any mixed-in class
  correctly downgrades to `NumericSequence`, since that's the most
  specific type any elementwise numeric result can honestly claim to
  be — a sum of two recurrences was never going to still be a
  recurrence.

**Trade-off accepted.** The mixin's methods depend on `self` already
having `combine()`/`map()`, which is a structural (`Protocol`-based)
rather than an inheritance-based requirement. This is intentional:
the whole point of the mixin is to add capability without adding a
base class, so the dependency has to be expressed as "shape," not
"ancestry."

> **Note:** this section needs revisiting in light of the following item.

------------------------------------------------------------------------

## Redesign: subtype preservation across transformations

### Motivation

While expanding `NumericSequence`, an issue was discovered during the
preparation of the README examples:

```python
(-squares).head(4)   # Works.
-squares.head(4)     # Fails.
```

The problem is that transformation methods inherited from `Sequence`
(e.g., `head()`, slicing, `map()`) construct and return a `Sequence`,
causing subclasses such as `NumericSequence` to lose their type. As a
result, arithmetic operators are no longer available after such
operations.

This is a general design issue affecting all future subclasses
(`Recurrence`, `NumericRecurrence`, etc.), and therefore warranted an
architectural redesign.

### Considered solutions

#### 1. Override every transformation method

Override all methods in `NumericSequence` that return a `Sequence` so
that they instead return a `NumericSequence`.

**Rejected.**

Although straightforward, this introduces a large amount of duplicated
code, is difficult to maintain, and would require every future subclass
to repeat the same pattern.

#### 2. Preserve construction arguments

Store the additional constructor arguments required by each subclass and
allow `Sequence` to reconstruct objects using a pattern similar to:

```python
return type(self)(
    rule,
    size,
    first_index=self.first_index,
    **self._constructor_kwargs()
)
```

**Rejected.**

This significantly reduces duplication, but still forces `Sequence` to
know that reconstruction is performed by forwarding constructor
arguments. The abstraction remains unnecessarily tied to one particular
construction mechanism.

#### 3. Use decorators

Move the reconstruction logic into decorators applied to transformation
methods.

**Rejected.**

Although technically feasible, decorators hide an important part of the
control flow and make the implementation less explicit. The additional
complexity is not justified.

#### 4. Introduce a protected factory method

Provide a protected factory method responsible for constructing the
result of transformations. Transformation methods simply delegate object
creation to this hook, while subclasses override it when additional
construction state is required.

**Current direction.**

This keeps `Sequence` completely agnostic to subclass constructor
signatures and delegates reconstruction to the subclass itself. The
resulting design is simpler, more extensible, and avoids duplicated
overrides while providing a single, well-defined extension point for all
future subclasses.

### Classifying classes and methods

The `_make()` factory alone is not sufficient. Further analysis showed
that the problem is deeper than object construction: **both classes and
transformation methods must be classified**, since not every
transformation can honestly preserve every subclass's structure.

A **preserving class** carries no mathematical structure beyond its
evaluation rule. Returning `type(self)` from `_make()` is always
correct.

Examples:

* `Sequence`
* `NumericSequence`

A **non-preserving class** carries additional mathematical structure
that cannot generally survive arbitrary transformations.

Example:

* future `Recurrence`

Transformation methods fall into three categories:

* **Preserving methods** preserve the representation and require no
  subclass-specific mathematics.
  Example: `head()`.

* **Non-preserving methods** change the representation, but only
  through *reindexing* — the underlying rule is still evaluated
  through the original sequence, just at different indices.
  Examples: `subsequence()`, slicing.

* **Mathematically preserving methods** preserve the representation,
  but only through subclass-specific mathematics.
  Examples: future `tail()` and `shift()` for `Recurrence`.

* **Strictly non-preserving methods** compute genuinely new *values*
  via a rule, not merely a reindexing of existing ones. No class can
  meaningfully preserve its subtype through them, so they always
  return a plain `Sequence`, regardless of class.
  Examples: `map()`, `combine()`.

The distinguishing question for the last category is not "does the
class carry extra structure?" but "does the result even correspond to
the same kind of mathematical object?" A `Recurrence`'s elementwise sum
with another sequence is not, in general, itself expressible as some
recursion with some basis — it is simply values indexed by a rule. The
same holds for `NumericSequence`, which has no extra structure to
preserve in the first place, so preservation is never available at
this category regardless of the class doing the calling.

### The `_make()` factory and the `preserve` flag

`_make()` is invoked with a `preserve` flag set by the calling method's
category, not by the class:

* Preserving methods call `self._make(preserve=True)`.
* Non-preserving methods call `self._make(preserve=False)`.
* Mathematically preserving methods (once a subclass overrides them to
  compute the new representation) call `self._make(preserve=True)`.
* Strictly non-preserving methods bypass `_make()` entirely and
  construct a plain `Sequence` directly.

`_make()` itself decides what to do with the flag, based on the class:

```python
if preserve:
    return self._make(...)      # type(self), always correct
else:
    return super()._make(...)   # defer to the nearest preserving ancestor
```

A preserving class ignores the flag — `type(self)` is correct either
way. A non-preserving class honors it: `preserve=True` still builds
`type(self)`, but `preserve=False` defers to `super()._make()`. If the
superclass is itself non-preserving, its `_make()` performs the same
check, so the call chain walks up the MRO — no matter how many
non-preserving classes are stacked — until it reaches the nearest
preserving ancestor.

This resolves the motivating example: `head()` is a preserving method,
so `(-squares).head(4)` correctly stays a `NumericSequence` via
`_make(preserve=True)`.

### Summary table

| Method category | Preserving class | Non-preserving class |
| --- | --- | --- |
| Preserving (`head()`) | `_make()` → `type(self)` | `_make()` → `type(self)` |
| Non-preserving (`subsequence()`, slicing) | `_make()` → `type(self)` (flag has no effect) | `_make()` → `super()._make()` chain → nearest preserving ancestor |
| Mathematically preserving (future `Recurrence.tail()`/`shift()`) | `_make()`, no override needed | subclass override computes representation, then `_make(preserve=True)` |
| Strictly non-preserving (`map()`, `combine()`) | plain `Sequence`, no `_make()` call | plain `Sequence`, no `_make()` call |

### Consequences

`_make()` is intentionally **only a factory**. It constructs an object
once the necessary data has already been derived; it never performs
representation-specific mathematics itself. That responsibility
belongs to the transformation methods (or subclass overrides of them)
that call it.

`map()` and `combine()` are deliberately excluded from the `_make()`
mechanism altogether: since they always return a plain `Sequence`,
there is no subtype to preserve, no `_make()` call to make, and (for
`combine()` specifically) no ambiguity over which operand's class
should govern the result — neither one's subtype survives regardless.
This is consistent with `NumericSequence`'s arithmetic mixin, which
never routes through `self.combine()`/`self.map()` for its own
construction and therefore has no reason to override either.
