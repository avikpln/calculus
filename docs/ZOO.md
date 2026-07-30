# Sequence Type Ideas

This file collects ideas for new sequence types that could extend the package.
These are open invitations, not commitments: anyone is welcome to pick one up,
adapt it, or propose something entirely new.

## `RandomSequence`

A sequence backed by a user-supplied random rule (e.g. a lambda calling
`random.random()`), with each generated value recorded the first time its index
is queried - not for performance, but because without recording, the same index
would silently return a different value on every call. Design details,
including why derived sequences should share rather than fork their recorded
values, and the proposed `{rₙ}` symbol, are recorded in NOTES.md.

## `RationalSequence`

A sequence of exact rational numbers, built on Python's `Fraction` (or a pair
of `NumericSequence`s representing the numerator and denominator). Since every
real number can be approximated by a sequence of rational numbers, this
provides a path toward representing real values computationally through
convergent sequences rather than finite-precision approximations.

## `ComplexSequence`

A sequence of complex numbers, restoring the `complex` support that was dropped
from `NumericSequence`'s `Number` (renamed later to `Real`) type, as comparison
operators are undefined for `complex`. Would need its own arithmetic and,
likely, no ordering operators at all.

## Memoized wrapper sequence

A sequence that wraps any existing rule and caches every computed value in a
dict, so repeated access to the same index skips recomputation. A pure
performance optimization, in contrast to `RandomSequence`'s recording, which
exists for correctness rather than speed.

## Query-counting sequence

A sequence that wraps a rule and tracks how many times each index has been
queried. No mathematical content - a minimal, purely pedagogical demonstration
of a stateful `_Rule`.

## `PrimeSequence`

The sequence of prime numbers, generated incrementally (e.g. via a growing
sieve or trial division), where each new prime depends on retaining the primes
found so far. Unlike `Recurrence`, its state isn't fixed-order or reducible to
a small window of prior terms.
