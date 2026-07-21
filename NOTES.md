# NOTES

**Purpose.** This document records design decisions and implementation
rationale for the `Sequence` library. It is intended as a long-term
memory of *why* certain choices were made, especially when the obvious
implementation was rejected.

Only decisions that may influence future development belong here.

## API Design

### `Sequence.__repr__`

`__repr__` intentionally returns the same value as `__str__`.

A conventional representation such as

``` python
Sequence(rule=<function <lambda> at 0x...>, ...)
```

is technically more faithful but usually provides little useful
information. Displaying a preview of the sequence is considerably more
informative.

This intentionally favors practicality over convention.

------------------------------------------------------------------------

### Shifting semantics

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

### Forward-only iteration

`subiter()` supports only forward iteration (`step > 0`).

Although supporting negative steps would mimic `range()`, reverse
iteration complicates the implementation, provides little practical
benefit, and conflicts with the intended design of future recurrence-
based sequences.

General reindexing remains available through `subsequence()`.

------------------------------------------------------------------------

### `map()` and `combine()`

`map()` and `combine()` are instance methods.

Although `combine()` is mathematically symmetric, the instance-method
API is more fluent and naturally defines which sequence contributes
properties such as `size` and `first_index`.

This decision may be revisited if the library evolves toward a more
functional API.

------------------------------------------------------------------------

### `constant()` and `from_iterable()` stay `@staticmethod`

Both factory methods remain `@staticmethod`, hardcoding their own
class name rather than becoming `classmethod`s that construct via
`cls`.

A `classmethod` version would let every subclass automatically
"inherit" a correctly-typed factory for free, since `cls` resolves to
whichever class the method was actually called on. This works safely
only as long as a subclass's constructor accepts nothing beyond
`rule`, `size`, and `first_index`. `NumericSequence` satisfies this,
but classes such as `Recurrence` do not: `Recurrence` requires an
additional `basis` argument, so `cls(rule, size, first_index)` would
either raise `TypeError` or, worse, succeed in some degenerate form
that only accidentally means what its class name suggests. This
concern is real: `Recurrence(rule=lambda x: c, basis=(None,))`
is a valid constructor call for a constant sequence-shaped
`Recurrence`, so a naive `cls`-based factory could quietly hand back a
technically-legal but conceptually vestigial `Recurrence` — a constant
sequence is not, in the mathematical sense the library cares about,
"a recurrence." Mistaking a qualification (e.g. calling
`Recurrence.constant()` instead of `NumericSequence.constant()`) would
then fail silently rather than loudly.

Keeping `constant()`/`from_iterable()` as `@staticmethod`s with each
class hardcoding its own type avoids this trap entirely: only classes
that explicitly override the method claim a construction type; every
other class in the hierarchy falls through, via ordinary MRO, to the
nearest ancestor that did. No class is responsible for judging whether
some other, possibly future, subclass is "safe" to auto-construct —
each class only ever states what it itself returns.

Concretely: `Sequence` defines the base implementation, returning
`Sequence`. `NumericSequence` overrides it to return `NumericSequence`,
since `NumericSequence` adds no constructor parameters beyond
`Sequence`'s own and is therefore safe to construct generically.
`Recurrence` defines no override, so it inherits `Sequence`'s version
and returns a plain `Sequence` — never attempting, and never risking,
a malformed or misleadingly-typed `Recurrence`. `NumericRecurrence`
(inheriting from both `Recurrence` and `NumericSequence`) also defines
no override; by MRO, it inherits `NumericSequence`'s version and
correctly returns a `NumericSequence`, with no code required on its
part.

This does mean `constant()`'s and `from_iterable()`'s bodies are
near-duplicated between `Sequence` and `NumericSequence` — identical
logic, differing only in the hardcoded class name. This is an accepted
cost, consistent with the per-class duplication already accepted for
`_resize()`/`_reindex()`.

------------------------------------------------------------------------

### Exposing the evaluation rule

The internal `_rule` object remains private.

A public property would simplify inspection, but would also constrain
future subclasses whose evaluation depends on mutable internal state
(e.g. cached recurrences).

Reconsider this only if a genuine use case emerges.

------------------------------------------------------------------------

### Restricted `first_index`

`first_index` was originally unrestricted, accepting any integer. It is
now constrained to `FIRST_INDEX_OPTIONS = (0, 1)`.

An arbitrary `first_index` was rarely useful in practice: the only
real use cases are thinking in one-indexed mathematical terms (`a_1,
a_2, ...`) or zero-indexed programming terms (`a_0, a_1, ...`).
Supporting arbitrary starting points added complexity — an unbounded
validation range, and a `combine()` mismatch check with no natural
"correct" resolution — without a corresponding benefit.

Negative indexing (`seq[-1]`) remains gated on `first_index == 0`,
since it is a zero-based convention inherited from Python sequences
and has no natural meaning for one-indexed sequences. This is simply
a consequence of `first_index == 0`, not a design goal in itself —
the `{0, 1}` restriction is justified on its own terms above, and
does not depend on negative indexing as motivation.

`first_index` remains immutable, and every operation deriving a new
sequence (i.e. constructing a new sequence based on the rule of an
existing one) continues to preserve the original `first_index`.

**Considered alternative: `one_indexed: bool`.** Replacing the public
`first_index: int` parameter with a boolean `one_indexed` was
considered, since a two-valued choice reads more clearly as a flag
than as a raw integer. This was rejected for two reasons.

First, `bool` does not truly correspond to what is being represented.
`first_index` is fundamentally an integer-valued property; restricting
it to two options is a validation choice, not evidence that the
underlying concept is binary. A boolean parameter would have no way to
express a third indexing scheme if one were ever needed, whereas an
`int` validated against a widening set requires only a validation
change.

Second, `one_indexed` would have required a conversion at every
internal reconstruction site (`_resize()`, `_reindex()`, `map()`,
`combine()`, and their `NumericSequence` counterparts), each of which
currently forwards `first_index=self.first_index` unchanged. Under a
boolean parameter, each of these would instead need
`one_indexed=bool(self.first_index)`, immediately converted back to
`int` inside `__init__` — a round trip with no computational benefit,
repeated at every call site.

------------------------------------------------------------------------

### `Recurrence` currently hardcodes `first_index=0`

Unlike `Sequence` and `NumericSequence`, `Recurrence` does not expose
`first_index` as a constructor parameter at all; it always constructs
with `first_index=0`.

This is the current implementation, not a settled design ruling: no
sound rationale has been established for restricting `Recurrence` to
`first_index=0` specifically, as opposed to allowing `first_index=1`
as an option like `Sequence` and `NumericSequence` do. See `TODO.md`
for revisiting this and allowing `Recurrence` to optionally start
from `first_index=1`.

------------------------------------------------------------------------

### `Series` does not hard-enforce `first_index`

Unlike `Recurrence`, `Series` does not hard-enforce a single
`first_index` value. It inherits `NumericSequence`'s behavior,
accepting either value in `FIRST_INDEX_OPTIONS`.

No mechanism internal to `Series` forces a specific `first_index`:
unlike `Recurrence`, it has no cache mechanism or lookup that depends
on indices starting at a particular value. Hardcoding a single
`first_index` for `Series` would therefore be an arbitrary
restriction rather than a necessity, so `Series` is left free to
accept either option, like `Sequence` and `NumericSequence`
themselves.

`Series` defaults to `first_index=1`, matching the standard mathematical
convention of summing from the first term. This default is not enforced;
`first_index=0` remains a valid, accepted choice.

------------------------------------------------------------------------

### Three-argument `pow()` is not supported

`__pow__` implements only the two-operand form of exponentiation
(`x ** y`), not Python's three-argument `pow(x, y, mod)` protocol,
which computes `(x ** y) % mod` efficiently for modular
exponentiation.

This is a deliberate omission, not an oversight: `**` alone only
ever calls `__pow__(self, other)`, never the three-argument form,
so no code path in `NumericSequence` currently reaches it. Supporting
it properly would require accepting an optional third operand
across `_binary()`, which is designed for strictly binary
operations, and modular exponentiation is a specialized numeric
technique of unclear relevance to a general-purpose sequence
library.

If a concrete use case emerges, this can be revisited; until then,
`NumericSequence` relies on Python's own `TypeError` for `pow(seq, y, m)`
calls, consistent with the project's EAFP philosophy elsewhere.

------------------------------------------------------------------------

### In-place operators are not implemented

`NumericSequence` does not implement `__iadd__`, `__imul__`, or any
other in-place arithmetic dunder.

Sequences are immutable by design: no method anywhere in `Sequence` or
`NumericSequence` mutates an existing instance, and every
transformation returns a new sequence. Implementing in-place operators
would be inconsistent with that model.

Python's default fallback — using the corresponding binary operator
(`__add__`, `__mul__`, etc.) when no in-place counterpart exists — is
therefore the correct and sufficient behavior, requiring no additional
code.

------------------------------------------------------------------------

### Naming: `naturals`, `progression`, `geometric`

`identity` was rejected as the name for the sequence of natural
numbers. It describes the underlying rule (`f(n) = n`), not the
sequence a caller actually wants — someone reaching for this
library thinks "give me 1, 2, 3, ...", not "give me the sequence
whose rule is the identity function." `naturals` names the result,
not the mechanism.

A `start_at` parameter, letting `naturals()` begin at an arbitrary
value, was considered and rejected. Crossed against the existing
`first_index` parameter (0 or 1), it produces four combinations
that are confusing to reason about, and a sequence with an
arbitrary starting value is no longer really "the natural numbers"
— it degenerates into an arithmetic progression with a fixed common
difference of 1. That capability, if wanted, belongs to
`progression()`, not as a bolt-on to `naturals()`.

`progression`, not `arithmetic_progression`, mirrors the choice
already made for `geometric`: both name the sequence type in full
mathematical terms, without redundantly restating "progression"
once the qualifying adjective already implies it. Keeping the two
names parallel (`geometric`, `progression`) avoids the asymmetry of
one method spelling out "progression" and the other not.

------------------------------------------------------------------------

### Naming: `T` over `SequenceT`

A descriptive name like `SequenceT` was considered for `T`. Not
adopted: `Sequence` is a simple generic container, the same category
as `list[T]`, where short names are the standard convention.

------------------------------------------------------------------------

### Default `first_index` for `progression()` and `geometric()`

`progression()` and `geometric()` default to `first_index=0`,
diverging from the library's general default of 1. Both sequences
are conventionally written in `a_0, a_1, a_2, ...` notation in
standard mathematical usage, so defaulting to 0 matches how these
sequences are actually expressed rather than forcing a translation
step. `constant()` and `naturals()` keep the library's general
default of 1, since neither has a comparable, universally
recognized zero-indexed convention pulling them the other way.

------------------------------------------------------------------------

### No private helper needed for special sequences

Unlike `constant()` and `from_iterable()`, which are duplicated
across `Sequence` and `NumericSequence` because both classes must
construct their own type from the same rule-building logic,
`naturals()`, `progression()`, and `geometric()` exist only on
`NumericSequence`. There is no second class needing to share this
logic, so there is no reason to factor it into a private helper —
each rule is built directly inside its own factory method.

## Construction

### Default construction

`Sequence()` currently constructs an infinite sequence returning `None`.

This is convenient for placeholders and testing, but the long-term
semantics remain open.

Future work:

-   determine whether `Sequence()` should instead represent an empty
    sequence;
-   reconsider this together with the semantics of truthiness and
    default construction.

------------------------------------------------------------------------

### Default rule and typing

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

### Lazy validation

`Sequence.__init__()` eagerly validates its primary callable because it
establishes the object's core invariant.

Transformation methods such as `subsequence()`, `map()`, and `combine()`
do **not** eagerly validate their callables. Errors surface naturally
when the transformed sequence is evaluated, following the same EAFP
philosophy used elsewhere in the implementation.

## Validation

### Validation ownership: public API vs. private methods

Argument validation belongs to the public API layer: public methods
validate their own parameters before proceeding.

Private methods may assume that these preconditions already hold and
do not perform independent validation of their own. However, a
private method may still raise an exception as a natural consequence
of implementing the documented behavior of the public method(s) that
call it — this is not "validation," it is the method doing its job.

This distinction is about ownership, not about where an exception
happens to be physically raised. The deciding question is: do all
current callers of the private method agree on what it should reject?

-   If every current caller wants identical behavior (e.g.
    `_combiner()`, used identically by `combine()` and
    `NumericSequence`'s arithmetic dunders; or `_index_sequence()`,
    which currently has one caller), the check may live inside the
    private method itself.
-   If callers genuinely diverge (e.g. `subiter()` forbids both negative
    and zero step, while `__getitem__()`'s slice handling forbids only
    zero), no single private method can own the check correctly for
    both; validation must move out to each public caller instead.

Internal invariants that are guaranteed by the class's own code (not
by caller input) remain the domain of `assert`, not exceptions, and
current type checkers not being able to infer such invariants is
never in itself a reason to make an assertion.

**Considered alternative: exposing `binary()`/`unary()`.** Making
`NumericSequence`'s `_binary()`/`_unary()` public was considered, so
that each of the 14 arithmetic dunders could visibly own the
first_index validation at a true public entry point. This was
rejected once the ownership question was reframed around caller
agreement rather than public/private visibility: since every current
caller of `_combiner()` (`combine()` and all of `NumericSequence`'s
dunders via `_binary()`) wants identical first_index behavior, no
caller-specific validation is actually needed, and exposing
`binary()`/`unary()` would have added public surface area for no
behavioral benefit.

## Documentation

### Private methods

Private methods use block comments rather than docstrings.

Public APIs are documented for users; private helpers are documented for
maintainers. Internal comments should explain implementation decisions
and invariants rather than duplicate the method signature.

------------------------------------------------------------------------

### Delegating methods

Methods that internally construct a new `Sequence` document only the
exceptions they can actually propagate.

Their docstrings should not simply refer readers to
`Sequence.__init__()`, because each delegating method reaches only part
of the constructor's validation logic.

## Development

### Local verification

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

------------------------------------------------------------------------

### Trailing whitespace checking

No dedicated package is used to detect trailing whitespace.
`pycodestyle` (W291/W293) only covers `.py` files, since it implements
PEP 8, which has no jurisdiction over Markdown or other text files.

Git already provides a file-type-agnostic mechanism: `git diff --check`
reports whitespace errors (trailing whitespace, space before tab,
etc.). To check an entire tree rather than just a diff, compare
against the fixed, well-known empty-tree SHA:

```bash
git diff --check 4b825dc642cb6eb9a060e54bf8d69288fbee4904 HEAD
```

This is run as a CI step alongside `mypy --strict`, `pyflakes`,
`pydocstyle`, and `pytest`. No `pycodestyle` or `pre-commit` framework
is used for this; whitespace checking stays native to Git.

------------------------------------------------------------------------

### Project layout

Tests were moved out of the `calculus/` package into a top-level
`tests/` directory, once the project grew to four modules and a
substantially larger test suite:

```text
calculus/
    __init__.py
    sequence.py
    utils.py

tests/
    test_sequence.py
```

Since `tests/` sits outside the package, imports in test files are
absolute (`from calculus.sequence import Sequence`) rather than
relative. A root-level `pytest.ini` (`pythonpath = .`) makes
`calculus` importable without installing it, avoiding the need for
packaging.

------------------------------------------------------------------------

### Packaging

The project is not yet packaged for installation.

Once the public API has stabilized, add a `pyproject.toml` and support
standard installation workflows such as:

```bash
pip install -e .
```

Packaging should be introduced together with project metadata,
dependency declarations, and continuous integration so that the
repository follows modern Python packaging conventions.

------------------------------------------------------------------------

### Tagging strategy

Tags mark major feature milestones, e.g. a new module landing.

Starting from `v0.5.0`, tags are annotated with a real message
(`git tag -a vX.Y.Z -m "..."`), rather than lightweight. Existing
tags (`v0.0.0`–`v0.4.0`) are not retroactively rewritten to add
messages, since force-replacing a published tag changes its
identity and can conflict with anyone who already fetched it.

------------------------------------------------------------------------

### Code cleanliness

Avoid speculative imports, constants, and infrastructure.

Unused code should be introduced only when a concrete feature requires
it, keeping static analysis clean and reducing maintenance overhead.

------------------------------------------------------------------------

### Feature implementation protocol

To keep development consistent and incremental, each feature should be
implemented using the following workflow:

1. **Implement**
   - Implement the feature.
   - Keep the implementation focused on the current feature only.

2. **Document**
   - Add or update method docstrings.
   - Update the class docstring if the public API has changed.
   - Update the module docstring if appropriate.

3. **Test**
   - Add or update the relevant tests.
   - Ensure the test suite reflects only the public API.

4. **Publish**
   - Update `README.md` to document the new feature.
   - Add or update usage examples where appropriate.

5. **Record** *(only if warranted)*
   - Record important design decisions, rejected alternatives, or
     implementation notes in `NOTES.md`.
   - Avoid documenting routine implementation details.

**IMPORTANT!** Run the project's verification tools
**before committing**. Only commit once all checks pass.

## Implementation

### `_Rule` removed entirely

The `_Rule` wrapper class is removed. `Sequence._rule` now holds the
raw callable directly, rather than a `_Rule` instance wrapping it.

`_Rule` originally existed to give every rule a uniform, polymorphic
`self._rule(n)` calling contract, and to validate `n` on every call
via `validate_int()`. Once the validation-ownership convention
established that private methods should not perform independent
argument validation (see the "Validation ownership" section above),
that per-call `validate_int(n)` check was dropped entirely. With it
gone, `_Rule` no longer did anything beyond storing a callable and
invoking it — exactly what a plain function reference already does.
Keeping the wrapper class around would have meant maintaining an
indirection layer with no remaining behavior of its own.

------------------------------------------------------------------------

### `Recurrence._Rule` is not a revival of the removed `_Rule` wrapper

`Recurrence` defines its own nested `_Rule` class. This is a distinct
class from the `Sequence`-level `_Rule` wrapper documented as removed
above, not a reversal of that decision.

The original `_Rule` was removed because, once per-call `validate_int`
was dropped, it did nothing beyond storing and invoking a callable —
exactly what a plain function reference already does, making the
indirection pointless.

`Recurrence._Rule` exists for a different reason: it must cache
previously computed terms so that evaluating a recurrence at large `n`
doesn't recompute the entire sequence from the basis every call. This
is genuine behavior a plain callable cannot express on its own, so the
wrapper is justified here in a way the original never was.
`_rule_factory()` constructs a fresh `_Rule` instance per derived
sequence specifically so that this cache is never silently shared
between a `Recurrence` and any sequence derived from it.

------------------------------------------------------------------------

### Internal invariants

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

### Floor division and modulo on complex operands

`__floordiv__`/`__rfloordiv__`/`__mod__`/`__rmod__` accept `Number`,
which includes `complex`, even though `//` and `%` are undefined for
complex numbers. This mirrors the project's EAFP philosophy already
used for zero-division: Python's own `TypeError` at runtime is the
enforcement mechanism, not eager static or runtime type-narrowing.
The resulting mypy errors are silenced with localized, documented
`# type: ignore[operator]` comments on each affected line.

------------------------------------------------------------------------

### Reversing the mixin decision

The mixin-based arithmetic design, previously used for
`NumericSequence`, was reversed: `NumericSequence` now defines its
arithmetic dunders directly, with a plain `Sequence[Number]` base and
no `_ArithmeticMixin`.

The reversal came from recognizing that `NumericRecurrence` is a
diamond: it is both a `NumericSequence` (numeric) and a `Recurrence`
(recursively constructed), and both of these are genuine is-a
relationships, not merely shared implementation. There is no
single-inheritance alternative that honestly captures both concepts at
once — reimplementing recursion internally on a `NumericSequence`
subclass would abandon the is-a relationship with `Recurrence` for no
real gain. The diamond (`Sequence` reached via two branches) was
therefore accepted as the correct design: `NumericRecurrence` inherits
from both `Recurrence` and `NumericSequence`.

Once the diamond was accepted, the mixin's purpose disappeared: it
existed solely to let `NumericSequence`'s arithmetic be mixed into a
class that also inherits `Sequence` through another branch, without a
`__slots__` conflict. But since the diamond itself was accepted instead
of avoided, that problem needs to be solved directly (through
`__slots__` and MRO handling) regardless of whether arithmetic comes
from a mixin or a base class — so the mixin no longer buys anything.
Defining arithmetic directly on `NumericSequence` is simpler and
removes the mixin's nontrivial typing cost: making `_ArithmeticMixin`
generic over its own concrete return type required splitting `Self`
into two `Protocol`/`TypeVar` pairs (`UnarySelf`/`_UnaryProtocol`,
`BinarySelf`/`_BinaryProtocol`), because `mypy --strict` could not
resolve a single shared `Self` across two protocol methods without
mistyping unrelated dunders. With no mixin, `self` is concretely
`NumericSequence` everywhere, and none of that machinery is needed.

**Lesson.** The original mixin decision was reasonable given what was
known at the time — multiple inheritance from two `Sequence` branches
is a real risk worth avoiding. But it solved the wrong problem: it
tried to route around the diamond's *implementation* conflicts
(`__slots__`, `type(self)` preservation) rather than confronting
whether the diamond itself was the correct model. Once
`NumericRecurrence` was recognized as genuinely both numeric and
recursively constructed, the diamond turned out to be the correct model,
and the mixin's generality cost more (in typing complexity) than it
returned (in reuse), since it currently has exactly one consumer.

------------------------------------------------------------------------

### Redesign: subtype preservation across transformations

**<u>Motivation</u>**

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

**<u>Considered Solutions</u>**

**1. Override every transformation method**

Override all methods in `NumericSequence` that return a `Sequence` so
that they instead return a `NumericSequence`.

**Rejected.** Although straightforward, this introduces a large amount
of duplicated code, is difficult to maintain, and would require every
future subclass to repeat the same pattern.

**2. Preserve construction arguments**

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

**Rejected.** This significantly reduces duplication, but still forces
`Sequence` to know that reconstruction is performed by forwarding
constructor arguments. The abstraction remains unnecessarily tied to one
particular construction mechanism.

**3. Use decorators**

Move the reconstruction logic into decorators applied to transformation
methods.

**Rejected.** Although technically feasible, decorators hide an
important part of the control flow and make the implementation less
explicit. The additional complexity is not justified.

**4. Introduce protected factory methods**

Provide protected factory methods responsible for constructing the
result of transformations. Transformation methods simply delegate object
creation to these hooks, while subclasses override them when additional
construction state is required.

**Current direction.** This keeps `Sequence` completely agnostic to
subclass constructor signatures and delegates reconstruction to the
subclass itself. The resulting design is simpler, more extensible, and
avoids duplicated overrides while providing well-defined extension
points for all future subclasses.

**<u>Classifying Classes and Methods</u>**

A single factory is not sufficient. Further analysis showed that the
problem is deeper than object construction: **both classes and
transformation methods must be classified**, since not every
transformation can honestly preserve every subclass's structure.

A **preserving class** carries no mathematical structure beyond its
evaluation rule. Constructing its own type from its own rule is always
correct.

Examples:

* `Sequence`
* `NumericSequence`

A **non-preserving class** carries additional mathematical structure
that cannot generally survive arbitrary transformations.

Example:

* future `Recurrence`

Transformation methods fall into three categories:

* **Preserving methods** vary only size, always reusing the calling
  instance's own rule unchanged.
  Example: `head()`.

* **Non-preserving methods** change the representation by supplying a
  new rule, but only through *reindexing* — the underlying rule is
  still evaluated through the original sequence, just at different
  indices.
  Examples: `subsequence()`, `shift_by()`, `tail()`, slicing.

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

**<u>`_resize()` and `_reindex()`</u>**

Preserving and non-preserving methods are backed by two separate
protected methods rather than a single factory with a flag:

* `_resize(size)` — used by preserving methods. Takes only `size`;
  always reuses the calling instance's own rule and constructs its
  own type by name. Every preserving class overrides this to name its
  own constructor; there is exactly one consumer today (`head()`).

* `_reindex(rule, size)` — used by non-preserving (reindexing)
  methods. Takes an explicit new rule and size. Each class states its
  construction target as a literal class name, not `type(self)`:
  `Sequence._reindex()` and `NumericSequence._reindex()` each
  construct their own type directly, while a future non-preserving
  class such as `Recurrence` overrides `_reindex()` to construct a
  plain `Sequence` instead, since an arbitrary reindexing generally
  isn't a valid recurrence.

An earlier version of this design used a single `_make()` method with
a `preserve` boolean, deferring non-preserving calls up the MRO via
`super()._make()` when a class wanted to fall back to its nearest
preserving ancestor. This was abandoned: `type(self)` inside a method
reached via `super()` still resolves to the *original* calling
instance's type, not the ancestor being deferred to, since `self` does
not change across a `super()` call. That made MRO deferral incompatible
with `type(self)`-based construction. Splitting into two explicitly
named methods removes the need for any deferral chain — each class
that needs non-default behavior for `_reindex()` overrides it directly
with its own literal target, rather than relying on `self`/`super()`
semantics to route the call correctly.

**<u>Consequences</u>**

`_resize()` and `_reindex()` are intentionally **only factories**. They
construct an object once the necessary data has already been produced;
they never perform representation-specific mathematics themselves.
That responsibility belongs to the transformation methods (or subclass
overrides of them) that call them.

`map()` and `combine()` are deliberately excluded from this mechanism
altogether: since they always return a plain `Sequence`, there is no
subtype to preserve, no `_resize()`/`_reindex()` call to make, and
(for `combine()` specifically) no ambiguity over which operand's class
should govern the result — neither one's subtype survives regardless.
This is consistent with `NumericSequence`'s arithmetic, which never
routes through `self.combine()`/`self.map()` for its own construction
and therefore has no reason to override either.

------------------------------------------------------------------------

### `_rule_factory()`: producing rules for transformed sequences

**Motivation**

`Sequence` represents a sequence solely by its evaluation rule. Most
rules are ordinary stateless callables, but future subclasses may
represent evaluation through callable objects carrying internal
state — a recurrence, for example, may cache previously computed
terms inside its rule object.

Whenever a transformation derives a new sequence from an existing
one, it must decide how the new sequence obtains its evaluation rule.
For stateless rules, simply reusing the existing callable is correct.
For stateful rules, however, sharing the same rule object would also
share its internal state, allowing evaluation of one sequence to
silently affect another.

**Mechanism**

`Sequence` provides the protected method `_rule_factory()`. Its
contract is intentionally semantic rather than implementation
specific: return an evaluation rule for a newly derived sequence that
is behaviorally equivalent to the current rule, honoring the same
`int -> T` calling contract as `self._rule`.

The base implementation simply returns `self._rule`, since stateless
rules require no further work. A subclass may override this method to
supply an equivalent rule with whatever independence guarantees its
own representation requires.

Every site that reconstructs a sequence from an existing rule —
`_resize()`, `subsequence()`, `shift_by()`, `tail()`, `_mapper()`, and
`_combiner()` — obtains that rule through `self._rule_factory()`
rather than referencing `self._rule` directly.

**Consequences**

This hook keeps `Sequence` agnostic to how a subclass represents
evaluation, regardless of whether the reconstructed object is that
subclass's own type or a plain `Sequence`. Stateless subclasses
inherit the base implementation unchanged; a subclass with a stateful
or non-trivial rule need only override `_rule_factory()`, without
touching `_resize()`, `_reindex()`, or any transformation method built
on top of them.

The mechanism governs only how evaluation rules propagate between
derived sequences. It does not determine the semantics of individual
transformations. If a subclass requires a transformation to behave
differently for mathematical reasons, it overrides that transformation
directly.

------------------------------------------------------------------------

### Overriding `_resize`/`_rule_factory` is optional but not free

Neither `_resize()` nor `_rule_factory()` is enforced as mandatory for
subclasses to override. A subclass author who forgets to override
`_resize()` gets no error: `head()`/`tail()` will simply return a
plain `Sequence` instead of the subclass's own type, silently losing
the subclass's methods. Similarly, forgetting to override
`_rule_factory()` on a subclass with a stateful rule silently shares
that state between the original and derived sequences instead of
giving each its own.

**Considered: `type(self) is not Sequence` check inside
`Sequence._resize()`.** Raising `NotImplementedError` whenever
`_resize()` runs on any subclass that hasn't overridden it would catch
the mistake the first time `head()`/`tail()` is actually called.
Rejected as the primary mechanism because it only fires at call time,
not at class-definition time, and it does not address
`_rule_factory()`, which has no comparable "identity" instance
attached to it and cannot be checked the same way.

**Considered: `__init_subclass__` enforcement.** Requiring every
`Sequence` subclass to define `_resize()` (or `_rule_factory()`) via
`__init_subclass__` would catch the omission immediately, at class
definition, before any instance is even created — a strictly earlier
and louder failure than the call-time check above. Rejected because it
would force every future subclass to override these methods even in
the (currently only hypothetical) case where a subclass is genuinely
content with plain-`Sequence` behavior, contradicting the project's
general preference for conventions enforced through documentation and
tests rather than structural runtime machinery.

**Decision.** No enforcement mechanism is added. Subclass authors are
expected to read the inline comments on `_resize()` and
`_rule_factory()` (see `sequence.py`) describing the consequence of
not overriding them, and existing tests such as
`test_head_preserves_numeric_subtype` are the intended guardrail for
each concrete subclass.

------------------------------------------------------------------------

### `Recurrence` does not override `shift_by()`, `tail()`, or `subsequence()`

`Recurrence` inherits these methods unchanged from `Sequence`. Since
`Recurrence` does not override `_reindex()`, all three fall through to
`Sequence._reindex()` and return a plain `Sequence`, not a `Recurrence`.

This is intentional, not an oversight, and follows directly from the
preserving/non-preserving classification established earlier: `head()`
is a preserving method (same rule, smaller size), so `_resize()` is
overridden to keep returning a `Recurrence`. `shift_by()`, `tail()`, and
`subsequence()` are reindexing methods — they evaluate the original
rule at *different* indices — and an arbitrarily reindexed recurrence
rule is not, in general, itself expressible as some recursion with some
basis. Degrading to `Sequence` is therefore correct: `Recurrence`
correctly relies on the inherited `Sequence._reindex()` fallback here,
rather than needing an override of its own (see the "Redesign: subtype
preservation" note above).

The degraded `Sequence` remains fully correct to iterate: it is backed
by the same `Recurrence._Rule` instance (via `_rule_factory()`,
freshly constructed per derived sequence, so no cache-sharing occurs),
which computes values identically regardless of the wrapper class
calling it. A caller who only iterates forward may never notice the
type change.

**Future work.** Reconstructing a `Recurrence` for these cases
is possible in principle (the reindexing is simple enough algebraically
for `shift_by` and `tail`, and for `subsequence` when the subfunc is
affine with a positive integer step), but was left unimplemented since
no concrete use case has required it yet, consistent with the
project's general preference for avoiding speculative infrastructure.
Revisit once a use case appears, and prefer overriding `_reindex()`
directly rather than each of `shift_by()`/`tail()`/`subsequence()`
individually, keeping the override at the same architectural layer as
`_resize()`.

------------------------------------------------------------------------

### `Recurrence` rule caching: single-slot vs. windowed

`Recurrence._Rule` caches only a single position: the order
consecutive values immediately preceding the most recently computed
index, not a longer history.

**Why a non-consecutive (sparse) cache was rejected.** Storing
scattered previously-computed points, rather than one consecutive
position, would let arbitrary jumps between distant indices stay
partly cheap. This was rejected: it requires an eviction policy (which
points to keep as memory grows), a lookup structure to find the
nearest usable point below a queried index, and reasoning about
staleness across multiple disjoint basis windows. For a
general-purpose library with no visibility into callers' actual access
patterns, this complexity was judged disproportionate to the benefit.

**Why a sliding window cache is also problematic.** A wider but still
consecutive window (e.g. the last 1024 computed values instead of just
`order`) was also considered. Advancing such a window remains O(1) per
step, so it does not change the asymptotic cost of forward iteration.
However, it does not remove the fundamental cliff between "cheap" and
"expensive" backward queries — it only pushes that cliff further back.
A query one step behind the window's edge is exactly as expensive as a
query one step behind the current single-slot cache: both require a
full restart from `self.basis`. Choosing a window size is therefore a
judgment call with no clearly correct answer, since it only changes
where the cliff sits, not whether one exists.

**Decision.** Start with the simplest possible cache: exactly `order`
consecutive values, advanced one step at a time. This has no eviction
policy to design, no window size to choose, and covers the primary use
case (forward iteration) with minimal complexity. Backward queries
always restart from `self.basis`, which is a known and accepted
limitation, consistent with the library's existing forward-only
philosophy (see "Forward-only iteration" above). This can be revisited
if concrete usage patterns later show frequent backward or jumping
access.

------------------------------------------------------------------------

### `Series` rule caching: single-slot now, cache deferred

`Series._Rule` initially caches only a single `(n, S(n))` pair, the
most recently computed partial sum, mirroring `Recurrence._Rule`'s
single-slot approach.

**Why the two caches are not as symmetric as they first appear.**
`Recurrence._Rule` caches a *window* of `order` consecutive
predecessors, because a fixed-order transition function needs exactly
that window as input — advancing from a cached point means shifting
that window forward one step at a time. `Series._Rule` caches a
*single scalar value at an index*: `S(n) = S(n-1) + a(n)` needs only
the immediately preceding partial sum to advance, regardless of gap
size. This is a meaningful asymmetry, not a stylistic one: it means a
cache of scattered `(m, S(m))` points is directly usable for `Series`
(any cached point is sufficient to resume forward computation from),
whereas a cache of scattered *windows* for `Recurrence` would still
require additional reconstruction before resuming — the concern that
motivated rejecting a non-consecutive cache for `Recurrence` (see
above) does not transfer cleanly to `Series`, since `Series` has no
window to reconstruct.

**Decision.** Despite this asymmetry making a richer cache more
tractable for `Series` than it would be for `Recurrence`, the initial
implementation still starts with the simplest possible cache — a
single `(n, S(n))` slot — consistent with the project's general
preference for avoiding speculative infrastructure until a concrete
use case demands it. No current usage pattern requires efficient
support for out-of-order queries.

**Future work: LRU cache.** If usage patterns later show frequent
out-of-order queries poorly served by the single-slot cache, a richer
cache can be introduced without architectural changes elsewhere
(contained entirely within `Series._Rule`). Three design choices for
that future cache:

-   **Eviction policy:** LRU, evicting the least-recently-used
    cached entry once a size bound is reached.
-   **Recency tracking structure:** a deque, to track insertion/access
    order cheaply for the LRU policy.
-   **Floor lookup structure:** a balanced tree, to efficiently find
    the largest cached `m` with `1 <= m < n` when `S(n)` is not itself
    cached, falling back to `m = 1` (which is always cached, since
    `S(1) = a(1)` is trivially precomputed) if no such `m` exists.

**Unresolved questions.**

-   What should be the default cache size?
-   Should users be allowed to tune it? If so, should an unbounded
    cache be permitted?
-   Should the floor-lookup structure be a tree/ordered-map with
    O(log N) insertion (e.g. `sortedcontainers.SortedDict`, since
    Python's stdlib has no balanced-tree type — `OrderedDict` merely
    preserves insertion order), or a sorted array with `bisect`
    (O(N) insertion)? Choosing `bisect` implicitly signals the cache
    is meant to stay small and access patterns non-adversarial, since
    its O(N) insertion is only acceptable at small N and could be
    deliberately exploited by a caller driving repeated churn (e.g.
    many out-of-order jumps); a tree/ordered-map avoids that worst
    case but adds implementation complexity and (for
    `sortedcontainers`) a runtime dependency the project doesn't
    currently have.

------------------------------------------------------------------------

### `Series` builds its initial rule before calling `super().__init__()`

`Series.__init__` cannot call `self._rule_factory()` before
`super().__init__()` runs, because `_rule_factory()` needs
`self.first_index`, a property established only once `Sequence.__init__`
completes.

**Decision.** `Series` factors rule construction into
`_rule_factory_produce(term_rule, first_index)`, a helper taking both
arguments explicitly rather than reading them off `self`. `__init__`
calls it with its own local parameters, before `super().__init__()`
runs; `_rule_factory()` calls it with
`self._term_rule`/`self.first_index`, after construction completes.
Both call sites share the same construction logic without either one
depending on state that isn't yet available.

------------------------------------------------------------------------

### `NumericRecurrence`: explicit method resolution over MRO reliance

`NumericRecurrence(Recurrence, NumericSequence)` overrides `_resize()`,
`_reindex()`, and `_rule_factory()` explicitly, rather than leaving
any of them to fall through the MRO implicitly.

Base order matters here beyond arithmetic vs. recursion precedence:
`Recurrence.__init__` is the one that accepts `(func, basis, size)`
and enforces `first_index=0`; `NumericSequence` defines no `__init__`
override and would otherwise leave `Sequence.__init__` (which has no
`basis` parameter) resolved first. `Recurrence` must therefore come
first in the base list for construction to work at all.

`_resize()` must be overridden regardless, since it is the one method
responsible for naming the concrete return type (`NumericRecurrence`).

`_reindex()` and `_rule_factory()` are more subtle. With `Recurrence`
first, MRO resolution alone already produces the desired behavior:
`_rule_factory()` resolves to `Recurrence`'s version (which `Recurrence`
overrides, giving the caching implementation that avoids cache-sharing
between derived sequences), and `_reindex()` resolves to
`NumericSequence`'s version (since `Recurrence` does not override it,
falling through to the next class in the MRO that does). But this
correctness depends entirely on two things that aren't guaranteed to
stay true: the declared base class order in
`class NumericRecurrence(Recurrence, NumericSequence)`, and the
current absence of a `_reindex()` override on `Recurrence` itself.
Either could change for reasons unrelated to `NumericRecurrence` — a
future maintainer reordering bases, or `Recurrence` someday gaining its
own `_reindex()` override — and `NumericRecurrence` would silently pick
up the wrong parent's behavior with no error, only wrong values or
shared cache state discovered later.

**Decision.** Both methods are overridden explicitly, each calling the
intended parent's implementation directly by name:

```python
def _reindex(self, rule, size=None):
    return NumericSequence._reindex(self, rule, size)

def _rule_factory(self):
    return Recurrence._rule_factory(self)
```

This costs two trivial methods but removes any dependency on MRO
ordering or on a parent class's current (but not contractually
guaranteed) lack of an override. It also documents intent directly:
each override states, in code, which parent governs which behavior,
rather than requiring a reader to reconstruct that from the class
declaration and both parents' current implementations.

------------------------------------------------------------------------

### No abstraction for non-finite-history recurrences

`Series` (partial sums, `S(n) = S(n-1) + a(n)`) is not a subclass of
`Recurrence`, despite being self-referential. This is not a naming
accident to be fixed by a broader class; it is a fundamental
limitation of what a general "unbounded-history recurrence" base
class could offer.

`Recurrence`'s caching mechanism works because, for a fixed-order
recurrence, caching exactly `order` prior terms is *sufficient* to
compute the next one — bounded history and cheap advancement are the
same property by construction. A hypothetical base class for
recurrences depending on arbitrary prior history has no equivalent
guarantee: if a transition function genuinely needs the full history,
there is nothing generic to cache on the caller's behalf, and the
class degrades to storing everything, no better than recomputing from
scratch.

`Series` only appears to need unbounded history syntactically. It is
actually a fixed-order recurrence in disguise — order 1, over the pair
`(running sum, next term)` — and its efficiency comes from recognizing
that the accumulation itself is boundable, not from some generic
unbounded-history mechanism. This generalizes: whenever a recurrence
is efficiently cacheable, it is expressible as bounded-order, and is
therefore already covered by `Recurrence`. A class for the
"non-finite-history" case would only ever be useful for recurrences
that are *not* efficiently cacheable — meaning it could not deliver
the efficiency `Recurrence` itself was designed to provide.

**Decision.** No such abstraction is introduced. `Series` inherits
directly from `NumericSequence`, implementing its own efficient
accumulation, rather than through any `Recurrence`-family base class.

**Not a permanent ruling.** This decision is tied to efficiency being
a current design priority, not a timeless mathematical necessity.
Circumstances that weaken that priority could reasonably reopen it —
for example, hardware advances that make brute-force recomputation
cheap regardless of history size, or a user whose interest is bounded
in practice (e.g. only ever inspecting a `head()` of some fixed size),
for whom unbounded-history storage costs nothing they'd notice. Revisit
if such a concrete case emerges, rather than speculatively designing
for it now. If such an abstraction is ever introduced, `Series` should
be re-parented to inherit from it, so the inheritance hierarchy
reflects that `Series` genuinely is a (now-supported) kind of
recurrence, rather than leaving it a sibling for historical reasons.
