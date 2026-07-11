"""Numeric abstractions for finite and infinite sequences.

This module extends the generic Sequence abstraction with support for
numeric sequences and element-wise arithmetic operations.

Classes:
    NumericSequence: A finite or infinite sequence of numeric values.
"""
from __future__ import annotations

__all__ = ["NumericSequence"]
__version__ = '0.2.0'
__author__ = 'Avi Kaplan'

from collections.abc import Callable

from .sequence import Sequence

# A type for representing a number.
Number = int | float | complex

#=======================================================================
# Numeric Sequence {aₙ}
#=======================================================================

class NumericSequence(Sequence[Number]):
    """A sequence whose elements are numeric values.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise arithmetic operations, exposed through the
    standard arithmetic operators.
    """

# -- INITIALIZATION

    def _make(
        self,
        func: Callable[[int], Number] | None = None,
        size: int | None = None, *,
        first_index: int = Sequence.DEFAULT_FIRST_INDEX,
        preserve: bool = False,
    ) -> NumericSequence:
        # Construct the result of a sequence transformation.

        return NumericSequence(func, size=size, first_index=first_index)

# -- ARITHMETIC HELPERS

    def _unary(self, op: Callable[[Number], Number]) -> NumericSequence:
        # Return the sequence obtained by applying a unary operation.

        rule = self._mapper(self, op)
        return NumericSequence(rule, self.size, first_index=self.first_index)

    def _binary(
        self,
        other: Number | NumericSequence,
        op: Callable[[Number, Number], Number]
    ) -> NumericSequence:
        # Return the sequence obtained by applying a binary operation.

        rule, size = self._combiner(self, other, op)
        return NumericSequence(rule, size, first_index=self.first_index)

# -- UNARY

    def __pos__(self) -> NumericSequence:
        """Return the element-wise unary plus.

        Returns:
            NumericSequence: The element-wise identity of the sequence.
        """
        return self._unary(lambda x: +x)

    def __neg__(self) -> NumericSequence:
        """Return the element-wise unary negation.

        Returns:
            NumericSequence: The element-wise negation of the sequence.
        """
        return self._unary(lambda x: -x)

# -- ADDITIVE

    def __add__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise sum.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                add.

        Returns:
            NumericSequence: The element-wise sum of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x + y)

    def __radd__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise sum.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                be added.

        Returns:
            NumericSequence: The element-wise sum of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y + x)

    def __sub__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise difference.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                subtract.

        Returns:
            NumericSequence: The element-wise difference of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x - y)

    def __rsub__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise difference.

        Args:
            other (Number | NumericSequence): The scalar or sequence
                from which to subtract.

        Returns:
            NumericSequence: The element-wise difference of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y - x)

# -- MULTIPLICATIVE

    def __mul__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise product.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                multiply.

        Returns:
            NumericSequence: The element-wise product of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x * y)

    def __rmul__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise product.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                be multiplied.

        Returns:
            NumericSequence: The element-wise product of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y * x)

    def __truediv__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise quotient.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                divide by.

        Returns:
            NumericSequence: The element-wise quotient of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x / y)

    def __rtruediv__(
        self,
        other: Number | NumericSequence
    ) -> NumericSequence:
        """Return the element-wise quotient.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                be divided by the current sequence.

        Returns:
            NumericSequence: The element-wise quotient of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y / x)

    def __floordiv__(
        self,
        other: Number | NumericSequence
    ) -> NumericSequence:
        """Return the element-wise floor quotient.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                divide by.

        Returns:
            NumericSequence: The element-wise floor quotient of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x // y)  # type: ignore[operator]

    def __rfloordiv__(
        self,
        other: Number | NumericSequence
    ) -> NumericSequence:
        """Return the element-wise floor quotient.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                be divided by the current sequence.

        Returns:
            NumericSequence: The element-wise floor quotient of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y // x)  # type: ignore[operator]

    def __mod__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise remainder.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                divide by.

        Returns:
            NumericSequence: The element-wise remainder of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x % y)  # type: ignore[operator]

    def __rmod__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise remainder.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                be divided by the current sequence.

        Returns:
            NumericSequence: The element-wise remainder of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y % x)  # type: ignore[operator]

# -- EXPONENTIATION

    def __pow__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise exponentiation.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                use as the exponent.

        Returns:
            NumericSequence: The element-wise exponentiation of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x ** y)

    def __rpow__(self, other: Number | NumericSequence) -> NumericSequence:
        """Return the element-wise exponentiation.

        Args:
            other (Number | NumericSequence): The scalar or sequence to
                use as the base.

        Returns:
            NumericSequence: The element-wise exponentiation of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y ** x)
