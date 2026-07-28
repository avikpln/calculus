# Architecture

This document records the class hierarchy of the `calculus` package and the
relationships between its classes.

## Class Diagram

```mermaid
classDiagram
    class Sequence~T~ {
        %% Attributes
        +finite
        +first_index
        +last_index
        +size

        %% Methods
        +combine(other, op)
        +head(size)
        +map(op)
        +shift_by(offset)
        +shift_to(where)
        +subiter(start, stop, step)
        +subsequence(subrule, size)
        +tail(size)
    }

    class BooleanSequence {
        %% Methods
        +__or__(other)
        +__ror__(other)
        +__and__(other)
        +__rand__(other)
        +__xor__(other)
        +__rxor__(other)
        +__invert__()
        +to_numeric()
    }

    class NumericSequence {
        %% Methods
		+__eq__(other)
		+__ne__(other)
		+__lt__(other)
		+__le__(other)
		+__gt__(other)
		+__ge__(other)
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
    }

    Sequence <|-- BooleanSequence

    Sequence <|-- NumericSequence

    Sequence <|-- Recurrence

    NumericSequence <|-- NumericRecurrence
    Recurrence <|-- NumericRecurrence

    NumericSequence <|-- Series
```

## Notes

- `Sequence` is the base abstraction for sequences in the package.
- `BooleanSequence` inherits from `Sequence` and implements logical operators
  through Python's special methods.
- `NumericSequence` inherits from `Sequence` and implements arithmetic and
  comparison operators through Python's special methods.
- `Recurrence` inherits from `Sequence`, representing sequences defined by
  recursive relations.
- `NumericRecurrence` inherits from both `Recurrence` and `NumericSequence`,
  combining numeric arithmetic with recursively defined elements.
- `Series` inherits from `NumericSequence`, representing partial sums of an
  underlying term sequence.
