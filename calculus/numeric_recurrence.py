"""Infinite numeric sequences defined by recursion.

This module combines NumericSequence and Recurrence to represent
sequences that are both numeric and recursively defined.

Classes:
    NumericRecurrence: A numeric sequence whose elements are defined
        recursively.
"""
from __future__ import annotations

__all__ = ["NumericRecurrence"]
__author__ = "Avi Kaplan"

from typing import Self

from .numeric_sequence import NumericSequence, Real
from .recurrence import Recurrence
from .sequence import INFINITY, Intfinity, Rule

# ======================================================================
# Numeric Recurrence {aₙ}
# ======================================================================

class NumericRecurrence(NumericSequence, Recurrence[Real]):
    """A class representing infinite numeric recurrences.

    This subclass inherits all functionality from NumericSequence and
    Recurrence, combining element-wise arithmetic operations with
    recursively defined elements.

    Methods:
        catalan():
            Return the Catalan number sequence.
        double_factorial():
            Return the double factorial sequence.
        factorial():
            Return the factorial sequence.
        fibonacci():
            Return the Fibonacci sequence.
    """

# -- INITIALIZATION

    __slots__ = ()

# -- FACTORY

    def _rule_factory(self) -> Rule[Real]:
        # Produce the rule for a newly derived sequence.

        return Recurrence._rule_factory(self)

    def _factory(self, size: Intfinity = INFINITY) -> Self:
        # Produce a new sequence of the same type and rule.

        return type(self)(
            self._func, self._basis, size=size, first_index=self._first_index,
        )

# -- SPECIAL NUMERIC RECURRENCES

    @staticmethod
    def fibonacci() -> NumericRecurrence:
        """Return the Fibonacci sequence.

        The result is a fixed, infinite sequence where each term is the
        sum of the two preceding terms, beginning with 0 and 1.

        Returns:
            NumericRecurrence: The Fibonacci sequence.
        """
        return NumericRecurrence(lambda n, a: a[-1] + a[-2], (0, 1))

    @staticmethod
    def factorial() -> NumericRecurrence:
        """Return the factorial sequence.

        The result is a fixed, infinite sequence where each term is
        the product of all positive integers up to its index.

        Returns:
            NumericRecurrence: The factorial sequence.
        """
        return NumericRecurrence(lambda n, a: n * a[-1], (1,))

    @staticmethod
    def double_factorial() -> NumericRecurrence:
        """Return the double factorial sequence.

        The result is a fixed, infinite sequence where each term is the
        product of all positive integers up to its index that share its
        parity.

        Returns:
            NumericRecurrence: The double factorial sequence.
        """
        return NumericRecurrence(lambda n, a: n * a[-2], (1, 1))

    @staticmethod
    def catalan() -> NumericRecurrence:
        """Return the Catalan number sequence.

        The result is a fixed, infinite sequence of the Catalan numbers,
        which count structures such as balanced bracket sequences and
        binary tree shapes.

        Returns:
            NumericRecurrence: The catalan number sequence.
        """

        def catalan_func(n: int, a: tuple[Real, ...]) -> Real:
            return a[-1] * 2*(2*n-1) // (n+1)

        return NumericRecurrence(catalan_func, (1,))
