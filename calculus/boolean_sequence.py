"""Infinite Boolean sequences.

This module extends the generic Sequence class to handle Boolean
elements, enabling element-wise logical operations.

Classes:
    BooleanSequence: An infinite sequence of Boolean values.
"""
from __future__ import annotations

__all__ = ["BooleanSequence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING

from .sequence import INFINITY, Intfinity, Rule, Sequence

if TYPE_CHECKING:
    from .numeric_sequence import NumericSequence

#=======================================================================
# Boolean Sequence {bₙ}
#=======================================================================

class BooleanSequence(Sequence[bool]):
    """A class representing infinite Boolean sequences.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise logical operations, exposed through the
    standard logical operators.

    Methods:
        false(size, first_index):
            Return a Boolean sequence whose elements are all False.
        from_iterable(iterable, first_index):
            Return a Boolean sequence from an iterable.
        to_numeric:
            Return the corresponding NumericSequence of 0/1 values.
        true(size, first_index):
            Return a Boolean sequence whose elements are all True.
    """

# -- INITIALIZATION

    __slots__ = ()

# -- FACTORY

    def _factory(
        self,
        rule: Rule[bool],
        size: Intfinity,
        reindex: bool,
    ) -> Sequence[bool]:
        # Produce a new sequence from rule and size, considering mode.

        return BooleanSequence(rule, size=size, first_index=self.first_index)

# -- UTILITY

    def to_numeric(self) -> NumericSequence:
        """Return the corresponding NumericSequence of 0/1 values.

        Returns:
            NumericSequence: The element-wise conversion of the
                sequence's True/False values to 1/0.
        """
        from .numeric_sequence import NumericSequence
        boolean_rule = self._rule_factory()
        rule = lambda n: int(boolean_rule(n))
        return NumericSequence(
            rule, size=self.size, first_index=self.first_index
        )

# -- LOGICAL HELPERS

    def _unary(self, op: Callable[[bool], bool]) -> BooleanSequence:
        # Return the sequence obtained by applying a unary operation.

        rule = self._mapper(self, op)
        return BooleanSequence(rule, self.size, first_index=self.first_index)

    def _binary(
        self,
        other: bool | BooleanSequence,
        op: Callable[[bool, bool], bool],
    ) -> BooleanSequence:
        # Return the sequence obtained by applying a binary operation.

        if not isinstance(other, bool | BooleanSequence):
            raise TypeError(
                f"unsupported type ({type(other).__name__}) for other "
                "operand in binary operation"
            )

        rule, size = self._combiner(self, other, op)
        return BooleanSequence(rule, size, first_index=self.first_index)

# -- UNARY LOGICAL

    def __invert__(self) -> BooleanSequence:
        """Return the element-wise logical negation.

        Returns:
            BooleanSequence: The element-wise negation of the sequence.
        """
        return self._unary(lambda x: not x)

# -- BINARY LOGICAL

    def __or__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical OR.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to OR
                with.

        Returns:
            BooleanSequence: The element-wise logical OR of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x | y)

    def __ror__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical OR.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to OR
                with.

        Returns:
            BooleanSequence: The element-wise logical OR of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y | x)

    def __and__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical AND.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to
                AND with.

        Returns:
            BooleanSequence: The element-wise logical AND of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x & y)

    def __rand__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical AND.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to
                AND with.

        Returns:
            BooleanSequence: The element-wise logical AND of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y & x)

    def __xor__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical XOR.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to
                XOR with.

        Returns:
            BooleanSequence: The element-wise logical XOR of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x ^ y)

    def __rxor__(self, other: bool | BooleanSequence) -> BooleanSequence:
        """Return the element-wise logical XOR.

        Args:
            other (bool | BooleanSequence): The scalar or sequence to
                XOR with.

        Returns:
            BooleanSequence: The element-wise logical XOR of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y ^ x)

# -- SPECIAL BOOLEAN SEQUENCES

    @staticmethod
    def true(
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> BooleanSequence:
        """Return a Boolean sequence whose elements are all True.

        When interpreted as a subset of the natural numbers, this
        sequence represents the natural numbers.

        Args:
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            BooleanSequence: A sequence whose elements are all equal to
                True.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        return BooleanSequence(
            Sequence._constant_rule(True), size=size, first_index=first_index,
        )

    @staticmethod
    def false(
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> BooleanSequence:
        """Return a Boolean sequence whose elements are all False.

        When interpreted as a subset of the natural numbers, this
        sequence represents the empty set.

        Args:
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            BooleanSequence: A sequence whose elements are all equal to
                False.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        return BooleanSequence(
            Sequence._constant_rule(False), size=size, first_index=first_index,
        )

    @staticmethod
    def from_iterable(
        iterable: Iterable[bool],
        *,
        first_index: int = 1,
    ) -> BooleanSequence:
        """Return a Boolean sequence from a Boolean iterable.

        Args:
            iterable (Iterable[bool]): The iterable providing the
                sequence elements.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            BooleanSequence: A finite Boolean sequence containing the
                elements of iterable.

        Raises:
            TypeError: If ``first_index`` is not an integer.
            ValueError: If ``first_index`` is not in
                ``sequence.FIRST_INDEX_OPTIONS``.
        """
        rule, size = Sequence._iterable_rule(iterable, first_index)
        return BooleanSequence(rule, size=size, first_index=first_index)
