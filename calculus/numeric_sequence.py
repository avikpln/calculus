"""Infinite numeric sequences with element-wise arithmetic.

This module extends the generic Sequence class to handle numeric
elements, enabling element-wise arithmetic operations.

Classes:
    NumericSequence: An infinite sequence of numeric values.
"""
from __future__ import annotations

__all__ = ["NumericSequence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable, Iterable

from .sequence import INFINITY, Intfinity, Rule, Sequence
from .utils import validate_callable

# A type for representing a number.
Number = int | float | complex

#=======================================================================
# Numeric Sequence {aₙ}
#=======================================================================

class NumericSequence(Sequence[Number]):
    """A class representing infinite numeric sequences.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise arithmetic operations, exposed through the
    standard arithmetic operators.

    Methods:
        constant(value, size, first_index):
            Return a constant numeric sequence.
        from_iterable(iterable, first_index):
            Return a numeric sequence from an iterable.
        geometric(first_term, common_ratio, size, first_index):
            Return a geometric sequence.
        map(op):
            Return an element-wise mapped numeric sequence.
        naturals(size, first_index):
            Return the sequence of natural numbers.
        progression(first_term, common_difference, size, first_index):
            Return an arithmetic progression.
    """

# -- INITIALIZATION

    __slots__ = ()

# -- FACTORY

    def _resize(self, size: Intfinity) -> NumericSequence:
        # Produce a new sequence of the same type and given size.

        rule = self._rule_factory()
        return NumericSequence(rule, size=size, first_index=self.first_index)

    def _reindex(
        self,
        rule: Rule[Number] | None,
        size: Intfinity = INFINITY,
    ) -> NumericSequence:
        # Produce a new sequence with the given rule and size.

        return NumericSequence(rule, size=size, first_index=self.first_index)

# -- UTILITY

    def _apply(self, op: Callable[[Number], Number]) -> NumericSequence:
        # Return the sequence obtained by applying op to each element.

        validate_callable(op)
        rule = self._mapper(self, op)
        return NumericSequence(rule, self.size, first_index=self.first_index)

    # Unlike Sequence.map(), which works with any element type,
    # override assumes op to both accept and return a Number, and
    # returns a NumericSequence rather than a generic Sequence.
    def map(  # type: ignore[override]
        self,
        op: Callable[[Number], Number],
    ) -> NumericSequence:
        """Return an element-wise mapped numeric sequence.

        Args:
            op (Callable[[Number], Number]): The operation to apply.

        Returns:
            NumericSequence: The sequence obtained by applying ``op`` to
                each element.

        Raises:
            TypeError: If ``op`` is not callable.
        """
        return self._apply(op)

# -- ARITHMETIC HELPERS

    def _unary(self, op: Callable[[Number], Number]) -> NumericSequence:
        # Return the sequence obtained by applying a unary operation.

        return self._apply(op)

    def _binary(
        self,
        other: Number | NumericSequence,
        op: Callable[[Number, Number], Number],
    ) -> NumericSequence:
        # Return the sequence obtained by applying a binary operation.

        if not isinstance(other, Number | NumericSequence):
            raise TypeError(
                f"unsupported type ({type(other).__name__}) for other "
                "operand in binary operation"
            )

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
        # // is undefined for complex; Python raises TypeError at
        # runtime, consistent with the project's EAFP philosophy.
        return self._binary(
            other, lambda x, y: x // y,  # type: ignore[operator]
        )

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
        # Same rationale as __floordiv__: // is undefined for complex.
        return self._binary(
            other, lambda x, y: y // x,  # type: ignore[operator]
        )

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
        # Same rationale as __floordiv__: % is undefined for complex.
        return self._binary(
            other, lambda x, y: x % y,  # type: ignore[operator]
        )

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
        # Same rationale as __floordiv__: % is undefined for complex.
        return self._binary(
            other, lambda x, y: y % x,  # type: ignore[operator]
        )

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

# -- SPECIAL NUMERIC SEQUENCES

    @staticmethod
    def constant(
        value: Number,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return a constant sequence.

        Args:
            value (Number): The constant value of each sequence element.
            size (Intfinity): The number of elements in the sequence, or
                None for an infinite sequence. Defaults to None.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            NumericSequence: A sequence whose elements are all equal to
                value.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
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
                Defaults to 1.

        Returns:
            NumericSequence: A finite numeric sequence containing the
                elements of iterable.

        Raises:
            TypeError: If ``first_index`` is not an integer.
            ValueError: If ``first_index`` is not in
                ``sequence.FIRST_INDEX_OPTIONS``.
        """
        rule, size = Sequence._iterable_rule(iterable, first_index)
        return NumericSequence(rule, size=size, first_index=first_index)

    @staticmethod
    def naturals(
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return the sequence of natural numbers.

        Args:
            size (Intfinity): The number of elements in the sequence.
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
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        return NumericSequence(lambda n: n, size=size, first_index=first_index)

    @staticmethod
    def progression(
        first_term: Number,
        common_difference: Number,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return an arithmetic progression.

        Args:
            first_term (Number): The first term of the progression.
            common_difference (Number): The constant difference
                between consecutive terms.
            size (Intfinity): The number of elements in the sequence.
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
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        rule = lambda n: first_term + common_difference*(n - first_index)
        return NumericSequence(rule, size=size, first_index=first_index)

    @staticmethod
    def geometric(
        first_term: Number,
        common_ratio: Number,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return a geometric sequence.

        Args:
            first_term (Number): The first term of the sequence.
            common_ratio (Number): The constant ratio between
                consecutive terms.
            size (Intfinity): The number of elements in the sequence.
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
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        rule = lambda n: first_term * common_ratio**(n - first_index)
        return NumericSequence(rule, size=size, first_index=first_index)
