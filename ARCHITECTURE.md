# Architecture

This document records the class hierarchy of the `calculus` package
and the relationships between its classes.

## Class diagram

```mermaid
classDiagram
    class Sequence~T~ {
        +size
        +finite
        +first_index
        +last_index
        +subsequence(subrule, size)
        +shift_by(offset)
        +shift_to(where)
        +head(size)
        +tail(size)
        +map(op)
        +combine(other, op)
        +constant(value, size, first_index)$
        +from_iterable(iterable, first_index)$
        #_rule
    }

    class NumericSequence {
        +Arithmetic operators
        +naturals(size, first_index)$
        +progression(first_term, common_difference, size, first_index)$
        +geometric(first_term, common_ratio, size, first_index)$
    }

    Sequence <|-- NumericSequence

    class Recurrence {
        +basis
        +order
    }

    Sequence <|-- Recurrence

    NumericSequence <|-- NumericRecurrence
    Recurrence <|-- NumericRecurrence
```

## Notes

- `$` denotes a static method (a factory that does not operate on
  an existing instance).
- `NumericSequence`'s arithmetic operators are grouped rather than
  listed individually, since enumerating all fourteen dunder
  methods would add noise without adding information; see
  `numeric_sequence.py` for the complete list.
- `NumericRecurrence` inherits from both `Recurrence` and
  `NumericSequence`, combining numeric arithmetic with recursively
  defined elements.
