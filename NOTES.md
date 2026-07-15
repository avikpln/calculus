# NOTES

**Purpose.** This document records design decisions and implementation rationale for
the `Sequence` library. It is intended as a long-term memory of *why*
certain choices were made, especially when the obvious implementation
was rejected.

Only decisions that may influence future development belong here.

## API Design

### `Sequence.__repr__`

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
`func`, `size`, and `first_index`. `NumericSequence` satisfies this,
but classes such as `Recurrence` do not: `Recurrence` requires an
additional `basis` argument, so `cls(func, size, first_index)` would
either raise `TypeError` or, worse, succeed in some degenerate form
that only accidentally means what its class name suggests. This
concern isn't hypothetical: `Recurrence(func=lambda x: c, basis=(None,))`
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

Restricting to two values also clarifies negative indexing, which
remains gated on `first_index == 0`. This is deliberate, not an
oversight: negative indexing (`seq[-1]`) is a zero-based convention
inherited from Python sequences, and has no natural meaning for
one-indexed sequences. It is not offered as a general feature; its one
motivating use case is `Recurrence`, which defaults to `first_index=0`
so that base cases and negative-offset lookups behave predictably.

`first_index` remains immutable, and every operation deriving a new
sequence continues to preserve the original `first_index`.

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

### Three-argument `pow()` is not supported

`__pow__` implements only the two-operand form of exponentiation
(`x ** y`), not Python's three-argument `pow(x, y, mod)` protocol,
which computes `(x ** y) % mod` efficiently for modular
exponentiation.

This is a deliberate omission, not an oversight: `**` alone only
ever calls `__pow__(self, other)`, never the three-argument form,
so no code path in NumericSequence currently reaches it. Supporting
it properly would require accepting an optional third operand
across `_binary()`, which is designed for strictly binary
operations, and modular exponentiation is a specialized numeric
technique of unclear relevance to a general-purpose sequence
library.

If a concrete use case emerges, this can be revisited; until then,
NumericSequence relies on Python's own TypeError for `pow(seq, y, m)`
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

-   If every current caller wants identical behavior (e.g. `_combiner()`,
    used identically by `combine()` and `NumericSequence`'s arithmetic
    dunders; or `_index_sequence()`, which currently has one caller),
    the check may live inside the private method itself.
-   If callers genuinely diverge (e.g. `subiter()` forbids both negative
    and zero step, while `__getitem__()`'s slice handling forbids only
    zero), no single private method can own the check correctly for
    both; validation must move out to each public caller instead.

Internal invariants that are guaranteed by the class's own code (not
by caller input) remain the domain of `assert`, not exceptions, and
current type checkers not being able to infer such invariants is
never in itself a reason to make an assertion.

**Considered alternative: exposing `binary()`/`unary()`.** Making
NumericSequence's `_binary()`/`_unary()` public was considered, so
that each of the 14 arithmetic dunders could visibly own the
first_index validation at a true public entry point. This was
rejected once the ownership question was reframed around caller
agreement rather than public/private visibility: since every current
caller of `_combiner()` (`combine()` and all of NumericSequence's
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

**IMPORTANT!** Run the project's verification tools **before committing**.
Only commit once all checks pass.

## Implementation

### `_Rule.func` property removed

`_Rule` previously exposed its callable through a read-only `func`
property, used internally by `__call__()`. This was removed;
`__call__()` now calls `self._func` directly.

The property was originally kept for encapsulation, on the reasoning
that calling `_func` directly was only a negligible performance
difference. That reasoning undersold the risk: exposing `func`
externally invites callers to bypass a rule's `int -> T` calling
contract and reach into its internals directly. This surfaced
concretely when considering `_resize()`: the polymorphic contract
that lets `_resize()` work for any rule type (`_Rule`, and future
types such as `_RecursiveRule`) is `self._rule(n)`, not
`self._rule.func`. `_RecursiveRule.func`, for instance, is not an
`int -> T` callable at all, but the multi-argument combining function
(e.g. `lambda x, y: x + y` for a Fibonacci recurrence); calling it as
if it were `_Rule.func` would be a type mismatch, not just redundant
validation.

Removing the public property does not fully prevent this class of
mistake (a caller could still reach `self._rule._func` directly), but
it removes the specific, named affordance that made the mistake easy
to reach for, including in future optimization attempts.

------------------------------------------------------------------------

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

This supersedes the earlier "`_Rule.func` property removed" entry
above: that entry's concern (external callers bypassing `_Rule`'s
calling contract via `.func`) is now moot, since there is no `_Rule`
instance, or contract, left to bypass.

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
used for zero-division: Python's own TypeError at runtime is the
enforcement mechanism, not eager static or runtime type-narrowing.
The resulting mypy errors are silenced with localized, documented
`# type: ignore[operator]` comments on each affected line.

------------------------------------------------------------------------
Remove incorrect mixin decision from NOTES.md

Corrects NOTES.md, which recorded that NumericRecurrence adopts single
single inheritance from NumericSequence, reimplementing recursion
internally to avoid a diamond with Recurrence. This misstates the
actual decision: the diamond inheritance from both Recurrence and
NumericSequence was accepted as conceptually sound and adopted
directly, not avoided.
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

**Rejected.** Although straightforward, this introduces a large amount of duplicated
code, is difficult to maintain, and would require every future subclass
to repeat the same pattern.

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

**Rejected.** This significantly reduces duplication, but still forces `Sequence` to
know that reconstruction is performed by forwarding constructor
arguments. The abstraction remains unnecessarily tied to one particular
construction mechanism.

**3. Use decorators**

Move the reconstruction logic into decorators applied to transformation
methods.

**Rejected.** Although technically feasible, decorators hide an important part of the
control flow and make the implementation less explicit. The additional
complexity is not justified.

**4. Introduce protected factory methods**

Provide protected factory methods responsible for constructing the
result of transformations. Transformation methods simply delegate object
creation to these hooks, while subclasses override them when additional
construction state is required.

**Current direction.** This keeps `Sequence` completely agnostic to subclass constructor
signatures and delegates reconstruction to the subclass itself. The
resulting design is simpler, more extensible, and avoids duplicated
overrides while providing well-defined extension points for all
future subclasses.

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

* `_reindex(func, size)` — used by non-preserving (reindexing)
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

`map()` and `combine()` remain outside this mechanism entirely: since
they always return a plain `Sequence`, there is no subtype to
preserve and no call to `_resize()` or `_reindex()` to make. This is
consistent with `NumericSequence`'s arithmetic, which never routes
through `self.combine()`/`self.map()` for its own construction and
therefore has no reason to override either.

**<u>Consequences</u>**

`_resize()` and `_reindex()` are intentionally **only factories**. They
construct an object once the necessary data has already been derived;
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
