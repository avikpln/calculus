"""Infinite Boolean sequences.

This module extends the generic Sequence class to handle Boolean
elements.

Classes:
    BooleanSequence: An infinite sequence of Boolean values.
"""
from __future__ import annotations

__all__ = ["BooleanSequence"]
__author__ = "Avi Kaplan"

from .sequence import INFINITY, Intfinity, Rule, Sequence

#=======================================================================
# Boolean Sequence {bₙ}
#=======================================================================

class BooleanSequence(Sequence[bool]):
    """A class representing infinite Boolean sequences.

    This subclass inherits all functionality from Sequence.
    """

# -- INITIALIZATION

    __slots__ = ()

# -- FACTORY

    def _resize(self, size: Intfinity) -> BooleanSequence:
        # Produce a new sequence of the same type and given size.

        rule = self._rule_factory()
        return BooleanSequence(rule, size=size, first_index=self.first_index)

    def _reindex(
        self,
        rule: Rule[bool] | None,
        size: Intfinity = INFINITY,
    ) -> BooleanSequence:
        # Produce a new sequence with the given rule and size.

        return BooleanSequence(rule, size=size, first_index=self.first_index)
