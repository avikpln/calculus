"""Numeric abstractions for finite and infinite recurrences.

This module combines NumericSequence and Recurrence to represent
sequences that are both numeric and recursively defined.

Classes:
    NumericRecurrence: A numeric sequence whose elements are defined
        recursively.
"""
from __future__ import annotations

__all__ = ["NumericRecurrence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable

from .numeric_sequence import Number, NumericSequence
from .recurrence import Recurrence

#========================================================================
# Numeric Recurrence {aₙ}
#========================================================================

class NumericRecurrence(Recurrence[Number], NumericSequence):
    """A numeric sequence whose elements are computed from prior terms.

    This subclass inherits all functionality from NumericSequence and
    Recurrence, combining element-wise arithmetic operations with
    recursively defined elements.
    """

# -- INITIALIZATION

    __slots__ = ()

    def _rule_factory(self) -> Callable[[int], Number]:
        # Return the rule used for numeric recurrence construction.

        return Recurrence._rule_factory(self)

    def _resize(self, size: int | None) -> NumericRecurrence:
        # Construct a new numeric recurrence of the given size.

        return NumericRecurrence(self._func, self._basis, size=size)

    def _reindex(
        self,
        rule: Callable[[int], Number] | None,
        size: int | None = None,
    ) -> NumericSequence:
        # Construct a new numeric recurrence of the given rule and size.

        return NumericSequence._reindex(self, rule, size)
