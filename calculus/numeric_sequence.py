"""Numeric abstractions for finite and infinite sequences.

This module extends the generic Sequence abstraction with support for
numeric sequences and element-wise arithmetic operations.

Classes:
    NumericSequence: A finite or infinite sequence of numeric values.
"""
from __future__ import annotations

__all__ = ["NumericSequence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable, Iterable

from .sequence import Sequence

# A type for representing a number.
Number = int | float | complex

#========================================================================
# Numeric Sequence {aₙ}
#========================================================================

class NumericSequence(Sequence[Number]):
    """A sequence whose elements are numeric values.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise arithmetic operations, exposed through the
    standard arithmetic operators.
    """

# -- INITIALIZATION

    def _resize(self, size: int | None) -> NumericSequence:
        # Construct a new sequence of the same type with the given size.

        rule = self._rule_factory()
        return NumericSequence(rule, size=size, first_index=self.first_index)

    def _reindex(
        self,
        rule: Callable[[int], Number] | None,
        size: int | None = None,
    ) -> NumericSequence:
        # Construct a new sequence with the given rule and size.

        return NumericSequence(rule, size=size, first_index=self.first_index)

# -- ARITHMETIC HELPERS

    def _unary(self, op: Callable[[Number], Number]) -> NumericSequence:
        # Return the sequence obtained by applying a unary operation.

        rule = self._mapper(self, op)
        return NumericSequence(rule, self.size, first_index=self.first_index)

    def _binary(
        self,
        other: Number | NumericSequence,
        op: Callable[[Number, Number], Number],
    ) -> NumericSequence:
        # Return the sequence obtained by applying a binary operation.

        rule, size = self._combiner(self, other, op)
        return NumericSequence(rule, size, first_index=self.first_index)

# -- UNARY ARITHMETIC

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

    def __abs__(self) -> NumericSequence:
        """Return the element-wise absolute value.

        Returns:
            NumericSequence: The element-wise absolute value of the
                sequence.
        """
        return self._unary(abs)

# -- ADDITIVE ARITHMETIC

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

# -- MULTIPLICATIVE ARITHMETIC

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
        other: Number | NumericSequence,
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
        other: Number | NumericSequence,
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
        other: Number | NumericSequence,
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

# -- EXPONENTIATION ARITHMETIC

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

# -- SPECIAL SEQUENCES

    @staticmethod
    def constant(
        value: Number,
        size: int | None = None,
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return a constant sequence.

        Args:
            value (Number): The constant value of each sequence element.
            size (int | None): The number of elements in the sequence,
                or None for an infinite sequence.
            first_index (int): The index of the first sequence element.

        Returns:
            NumericSequence: A sequence whose elements are all equal to
                value.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in FIRST_INDEX_OPTIONS.
        """
        return NumericSequence(
            Sequence._constant_rule(value), size=size, first_index=first_index,
        )

    @staticmethod
    def from_iterable(
        iterable: Iterable[Number],
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return a numeric sequence from a numeric iterable.

        Args:
            iterable (Iterable[Number]): The iterable providing the
                sequence elements.
            first_index (int): The index of the first sequence element.

        Returns:
            NumericSequence: A finite numeric sequence containing the
                elements of iterable.

        Raises:
            TypeError: If ``first_index`` is not an integer.
            ValueError: If ``first_index`` is not in
                FIRST_INDEX_OPTIONS.
        """
        rule, size = Sequence._iterable_rule(iterable, first_index)
        return NumericSequence(rule, size=size, first_index=first_index)

    @staticmethod
    def naturals(
        size: int | None = None,
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return the sequence of natural numbers.

        Args:
            size (int | None): The number of elements in the sequence.
                Defaults to None, which corresponds to an infinite
                sequence.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            NumericSequence: A sequence of natural numbers.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in FIRST_INDEX_OPTIONS.
        """
        return NumericSequence(lambda n: n, size=size, first_index=first_index)

    @staticmethod
    def progression(
        first_term: Number,
        common_difference: Number,
        size: int | None = None,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return an arithmetic progression.

        Args:
            first_term (Number): The first term of the progression.
            common_difference (Number): The constant difference
                between consecutive terms.
            size (int | None): The number of elements in the sequence.
                Defaults to None, which corresponds to an infinite
                sequence.
            first_index (int): The index of the first sequence element.
                Defaults to 0.

        Returns:
            NumericSequence: The specified arithmetic progression.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in FIRST_INDEX_OPTIONS.
        """
        rule = lambda n: first_term + common_difference*(n - first_index)
        return NumericSequence(rule, size=size, first_index=first_index)

    @staticmethod
    def geometric(
        first_term: Number,
        common_ratio: Number,
        size: int | None = None,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return a geometric sequence.

        Args:
            first_term (Number): The first term of the sequence.
            common_ratio (Number): The constant ratio between
                consecutive terms.
            size (int | None): The number of elements in the sequence.
                Defaults to None, which corresponds to an infinite
                sequence.
            first_index (int): The index of the first sequence element.
                Defaults to 0.

        Returns:
            NumericSequence: The specified geometric sequence.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in FIRST_INDEX_OPTIONS.
        """
        rule = lambda n: first_term * common_ratio**(n - first_index)
        return NumericSequence(rule, size=size, first_index=first_index)
