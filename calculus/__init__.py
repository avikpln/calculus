"""The Calculus package."""

from .boolean_sequence import BooleanSequence
from .numeric_recurrence import NumericRecurrence
from .numeric_sequence import NumericSequence
from .recurrence import Recurrence
from .sequence import Sequence
from .series import Series

__version__ = "0.6.0"

__all__ = [
    "BooleanSequence",
    "NumericRecurrence",
    "NumericSequence",
    "Recurrence",
    "Sequence",
    "Series",
]
