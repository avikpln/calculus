"""The Calculus package."""

from .sequence import Sequence
from .numeric_sequence import NumericSequence
from .recurrence import Recurrence
from .numeric_recurrence import NumericRecurrence
from .series import Series

__version__ = "0.5.0"

__all__ = [
    "Sequence",
    "NumericSequence",
    "Recurrence",
    "NumericRecurrence",
    "Series",
]
