"""Infinite Boolean sequences.

This module extends the generic Sequence class to handle Boolean
elements, enabling element-wise logical operations.

Classes:
    BooleanSequence: An infinite sequence of Boolean values.
"""
from __future__ import annotations

__all__ = ["BooleanSequence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable

from .sequence import INFINITY, Intfinity, Rule, Sequence

#=======================================================================
# Boolean Sequence {bₙ}
#=======================================================================

class BooleanSequence(Sequence[bool]):
    """A class representing infinite Boolean sequences.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise logical operations, exposed through the
    standard logical operators.
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
