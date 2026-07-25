"""The Calculus package."""

from .sequence import Sequence
from .numeric_sequence import NumericSequence
from .recurrence import Recurrence
from .numeric_recurrence import NumericRecurrence
from .series import Series
from .boolean_sequence import BooleanSequence

__version__ = "0.6.0"

__all__ = [
    "Sequence",
    "BooleanSequence",
    "NumericSequence",
    "Recurrence",
    "NumericRecurrence",
    "Series",
]
