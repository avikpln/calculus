# Design

This document describes the core abstractions of the `calculus` package and the
reasoning behind them.

## The Sequence Abstraction

A sequence is represented purely through the rule that produces its elements,
rather than through a stored collection of values. An element is computed only
when it is actually requested.

This is what makes infinite sequences representable at all: a sequence of
natural numbers, or a recursively defined sequence such as the Fibonacci
numbers, never materializes its elements, so its size can be genuinely
unbounded rather than merely large.

## Immutability

Sequences are immutable: no operation modifies an existing sequence in place,
and every transformation produces a new one instead. This is a deliberate
consequence of representing a sequence purely through its evaluation rule, and
it is treated as a firm invariant throughout the package, rather than an
incidental property.

## Indexing

Every sequence has an explicit first index, rather than always starting
implicitly at zero. Only two conventions are supported: the zero-indexed
convention familiar from programming, and the one-indexed convention familiar
from mathematical notation. An arbitrary starting index would offer little
practical benefit over these two conventions, while complicating both
validation and the combination of sequences that start at different indices.

A sequence's first index is fixed once it is created, and every operation that
derives a new sequence from an existing one preserves it.

## Type Preservation Through Reconstruction

Operations that derive a new sequence from an existing one do not all have the
same preservation semantics. Operations that only change the representation of
a sequence, such as taking a finite prefix, must preserve the concrete sequence
type. For example, taking the first elements of a numeric sequence must not
silently discard its numeric behavior. A specialized kind of sequence unable to
preserve itself through such an operation has no place in the hierarchy: this
is treated as a requirement every specialized sequence must satisfy, not merely
a default that happens to hold in the common case.

Reindexing operations are different. Changing the evaluation mapping may or may
not preserve the meaning represented by a specialized sequence. A subsequence,
shift, or tail may therefore preserve the specialized type when the subclass
supports it, or intentionally fall back to a more general sequence when the
operation would invalidate the subclass's own invariants.

This distinction avoids forcing every sequence type into the same preservation
strategy: resizing is required to preserve type, while reindexing preserves
type only when doing so remains semantically valid.

## Rule Propagation

Whenever a new sequence is derived from an existing one, it must obtain its own
evaluation rule. For a rule with no internal memory, reusing the original rule
is entirely safe. For a rule that remembers previously computed values,
however, sharing that same rule between two sequences would let evaluating one
silently affect the other.

Recursively defined sequences and series both rely on remembering previous
computations to remain efficient, so every sequence derived from either kind
receives its own independent memory, entirely decoupled from the sequence it
was derived from. What each remembers differs, shaped by how each is actually
computed, but both follow the same principle: efficiency must never come at the
cost of two sequences silently sharing state.

## Numeric and Boolean Sequences

A numeric sequence extends the base abstraction with arithmetic and comparison
operations over real numbers.

Comparisons produce a boolean sequence, rather than a numeric sequence of ones
and zeros. A dedicated boolean type allows expressing which elements of a
sequence's domain satisfy some condition, for instance an infinite subset of
the natural numbers, and combining such conditions logically as first-class
objects, while keeping numeric sequences purely numeric. A boolean sequence can
be converted to its numeric, zero/one representation explicitly, when that
interpretation is actually wanted.

A sequence that is both numeric and recursively defined combines both sets of
behavior at once, rather than choosing one or reducing one to the other. Both
are independent aspects of what such a sequence is, and neither is treated as
more fundamental than the other.

## Recurrences and Series

A recurrence represents a sequence whose terms are computed from a fixed number
of preceding terms, rather than from a closed-form rule. A series is a related
but distinct idea: it represents the accumulated partial sums of an underlying
numeric sequence.

Although a series is self-referential in a similar sense (each partial sum
depends on the one before it), it is not modeled as a kind of recurrence. A
recurrence's efficiency comes from needing only a bounded window of prior terms
to compute the next one; a series happens to satisfy this same property in a
different shape, but the two are efficient for different underlying reasons. No
single general abstraction currently covers both faithfully without weakening
one of them, so they remain distinct, unrelated kinds of sequence.
