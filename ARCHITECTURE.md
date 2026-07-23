# Architecture

This document records the class hierarchy of the `calculus` package
and the relationships between its classes.

## Class diagram

```mermaid
classDiagram
    class Sequence~T~ {
        +finite
        +first_index
        +last_index
        +size
        +combine(other, op)
        +head(size)
        +map(op)
        +shift_by(offset)
        +shift_to(where)
        +subsequence(subrule, size)
        +tail(size)
        +constant(value, size, first_index)$
        +from_iterable(iterable, first_index)$
        #_rule
    }

    class NumericSequence {
        +__add__(other)
        +__radd__(other)
        +__sub__(other)
        +__rsub__(other)
        +__mul__(other)
        +__rmul__(other)
        +__truediv__(other)
        +__rtruediv__(other)
        +__floordiv__(other)
        +__rfloordiv__(other)
        +__mod__(other)
        +__rmod__(other)
        +__pow__(other)
        +__rpow__(other)
        +__neg__()
        +__abs__()
        +map(op)
        +geometric(first_term, common_ratio, size, first_index)$
        +naturals(size, first_index)$
        +progression(first_term, common_difference, size, first_index)$
    }

    Sequence <|-- NumericSequence

    class Recurrence {
        +basis
        +order
    }

    Sequence <|-- Recurrence

    NumericSequence <|-- NumericRecurrence
    Recurrence <|-- NumericRecurrence

    NumericSequence <|-- Series
```

## Notes

- `$` is used in this diagram to denote a static method. The static
  methods shown here are factory methods.
- `Sequence` is the base abstraction for sequences in the package.
- `NumericSequence` inherits from `Sequence` and implements arithmetic
  operators through Python's special methods.
- `Recurrence` inherits from `Sequence`, representing sequences defined
  by recursive relations.
- `NumericRecurrence` inherits from both `Recurrence` and
  `NumericSequence`, combining numeric arithmetic with recursively
  defined elements.
- `Series` inherits from `NumericSequence`, representing partial sums of
  an underlying term sequence.
