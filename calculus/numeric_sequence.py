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
from fractions import Fraction
from typing import Self

from .boolean_sequence import BooleanSequence
from .sequence import INFINITY, Intfinity, Sequence
from .utils import validate_callable

Real = int | float | Fraction
"""A type for representing a real numeric value."""

# ======================================================================
# Numeric Sequence {aₙ}
# ======================================================================

class NumericSequence(Sequence[Real]):
    """A class representing infinite numeric sequences.

    This subclass inherits all functionality from Sequence and extends
    it with element-wise arithmetic operations, exposed through the
    standard arithmetic operators.

    Methods:
        constant(value, size, first_index):
            Return a constant numeric sequence.
        euler():
            Return the sequence defining e.
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

    def _factory(self, size: Intfinity = INFINITY) -> Self:
        # Produce a new sequence of the same type and rule.

        rule = self._rule_factory()
        return type(self)(rule, size=size, first_index=self.first_index)

    def _reindex_factory(
        self,
        subrule: Callable[[int], int],
        size: Intfinity = INFINITY,
    ) -> NumericSequence:
        # Produce a new reindexed sequence of the same type.

        rule = self._reindex_rule_factory(subrule)
        return NumericSequence(rule, size=size, first_index=self.first_index)

# -- UTILITY

    def _apply(self, op: Callable[[Real], Real]) -> NumericSequence:
        # Return the sequence obtained by applying op to each element.

        validate_callable(op)
        rule = self._mapper(self, op)
        return NumericSequence(rule, self.size, first_index=self.first_index)

    # Unlike Sequence.map(), which works with any element type,
    # override assumes op to both accept and return a Real, and returns
    # a NumericSequence rather than a generic Sequence.
    def map(  # type: ignore[override]
        self,
        op: Callable[[Real], Real],
    ) -> NumericSequence:
        """Return an element-wise mapped numeric sequence.

        Args:
            op (Callable[[Real], Real]): The operation to apply.

        Returns:
            NumericSequence: The sequence obtained by applying ``op`` to
                each element.

        Raises:
            TypeError: If ``op`` is not callable.
        """
        return self._apply(op)

# -- COMPARISON

    def _compare(
        self,
        other: Real | NumericSequence,
        op: Callable[[Real, Real], bool],
    ) -> BooleanSequence:
        # Return the sequence from applying a comparison operation.

        if not isinstance(other, Real | NumericSequence):
            raise TypeError(
                f"unsupported type ({type(other).__name__}) for other "
                "operand in comparison operation"
            )

        rule, size = self._combiner(self, other, op)
        return BooleanSequence(rule, size, first_index=self.first_index)

    # Deliberately deviates from object's scalar bool contract, matching
    # NumPy's elementwise array comparison behavior.
    def __eq__(  # type: ignore[override]
        self,
        other: Real | NumericSequence
    ) -> BooleanSequence:
        """Return the element-wise equality.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                equate with.

        Returns:
            BooleanSequence: The element-wise equality of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x == y)

    # Same rationale as __eq__: deliberate deviation from scalar bool.
    def __ne__(  # type: ignore[override]
        self,
        other: Real | NumericSequence
    ) -> BooleanSequence:
        """Return the element-wise non-equality.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                compare against.

        Returns:
            BooleanSequence: The element-wise non-equality of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x != y)

    def __lt__(self, other: Real | NumericSequence) -> BooleanSequence:
        """Return the element-wise less-than comparison.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                compare against.

        Returns:
            BooleanSequence: The element-wise less-than comparison of
                the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x < y)

    def __le__(self, other: Real | NumericSequence) -> BooleanSequence:
        """Return the element-wise less-than-or-equal comparison.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                compare against.

        Returns:
            BooleanSequence: The element-wise less-than-or-equal
                comparison of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x <= y)

    def __gt__(self, other: Real | NumericSequence) -> BooleanSequence:
        """Return the element-wise greater-than comparison.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                compare against.

        Returns:
            BooleanSequence: The element-wise greater-than comparison of
                the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x > y)

    def __ge__(self, other: Real | NumericSequence) -> BooleanSequence:
        """Return the element-wise greater-than-or-equal comparison.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                compare against.

        Returns:
            BooleanSequence: The element-wise greater-than-or-equal
                comparison of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._compare(other, lambda x, y: x >= y)

# -- ARITHMETIC HELPERS

    def _unary(self, op: Callable[[Real], Real]) -> NumericSequence:
        # Return the sequence obtained by applying a unary operation.

        return self._apply(op)

    def _binary(
        self,
        other: Real | NumericSequence,
        op: Callable[[Real, Real], Real],
    ) -> NumericSequence:
        # Return the sequence obtained by applying a binary operation.

        if not isinstance(other, Real | NumericSequence):
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
        return self._unary(lambda x: x.__abs__())

# -- ADDITIVE ARITHMETIC

    def __add__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise sum.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                add.

        Returns:
            NumericSequence: The element-wise sum of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x + y)

    def __radd__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise sum.

        Args:
            other (Real | NumericSequence): The scalar or sequence to be
                added.

        Returns:
            NumericSequence: The element-wise sum of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y + x)

    def __sub__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise difference.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                subtract.

        Returns:
            NumericSequence: The element-wise difference of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x - y)

    def __rsub__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise difference.

        Args:
            other (Real | NumericSequence): The scalar or sequence from
                which to subtract.

        Returns:
            NumericSequence: The element-wise difference of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y - x)

# -- MULTIPLICATIVE ARITHMETIC

    def __mul__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise product.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                multiply.

        Returns:
            NumericSequence: The element-wise product of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x * y)

    def __rmul__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise product.

        Args:
            other (Real | NumericSequence): The scalar or sequence to be
                multiplied.

        Returns:
            NumericSequence: The element-wise product of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y * x)

    def __truediv__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise quotient.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
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
        other: Real | NumericSequence,
    ) -> NumericSequence:
        """Return the element-wise quotient.

        Args:
            other (Real | NumericSequence): The scalar or sequence to be
                divided by the current sequence.

        Returns:
            NumericSequence: The element-wise quotient of the operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y / x)

    def __floordiv__(
        self,
        other: Real | NumericSequence,
    ) -> NumericSequence:
        """Return the element-wise floor quotient.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                divide by.

        Returns:
            NumericSequence: The element-wise floor quotient of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x // y)

    def __rfloordiv__(
        self,
        other: Real | NumericSequence,
    ) -> NumericSequence:
        """Return the element-wise floor quotient.

        Args:
            other (Real | NumericSequence): The scalar or sequence to be
                divided by the current sequence.

        Returns:
            NumericSequence: The element-wise floor quotient of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y // x)

    def __mod__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise remainder.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                divide by.

        Returns:
            NumericSequence: The element-wise remainder of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x % y)

    def __rmod__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise remainder.

        Args:
            other (Real | NumericSequence): The scalar or sequence to be
                divided by the current sequence.

        Returns:
            NumericSequence: The element-wise remainder of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: y % x)

# -- EXPONENTIATION ARITHMETIC

    def __pow__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise exponentiation.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
                use as the exponent.

        Returns:
            NumericSequence: The element-wise exponentiation of the
                operands.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        return self._binary(other, lambda x, y: x ** y)

    def __rpow__(self, other: Real | NumericSequence) -> NumericSequence:
        """Return the element-wise exponentiation.

        Args:
            other (Real | NumericSequence): The scalar or sequence to
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
        value: Real,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return a constant numeric sequence.

        Args:
            value (Real): The constant value of each sequence element.
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            NumericSequence: A sequence whose elements are all equal to
                value.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        return NumericSequence(
            Sequence._constant_rule(value), size=size, first_index=first_index,
        )

    @staticmethod
    def from_iterable(
        iterable: Iterable[Real],
        *,
        first_index: int = 1,
    ) -> NumericSequence:
        """Return a numeric sequence from a numeric iterable.

        Args:
            iterable (Iterable[Real]): The iterable providing the
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
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            NumericSequence: A sequence of natural numbers.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        return NumericSequence(lambda n: n, size=size, first_index=first_index)

    @staticmethod
    def progression(
        first_term: Real,
        common_difference: Real,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return an arithmetic progression.

        Args:
            first_term (Real): The first term of the progression.
            common_difference (Real): The constant difference between
                consecutive terms.
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 0.

        Returns:
            NumericSequence: The specified arithmetic progression.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        def progression_rule(n: int) -> Real:
            return first_term + common_difference*(n - first_index)

        return NumericSequence(
            progression_rule,
            size=size,
            first_index=first_index,
        )

    @staticmethod
    def geometric(
        first_term: Real,
        common_ratio: Real,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 0,
    ) -> NumericSequence:
        """Return a geometric sequence.

        Args:
            first_term (Real): The first term of the sequence.
            common_ratio (Real): The constant ratio between consecutive
                terms.
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 0.

        Returns:
            NumericSequence: The specified geometric sequence.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        def geometric_rule(n: int) -> Real:
            return first_term * common_ratio**(n - first_index)

        return NumericSequence(
            geometric_rule,
            size=size,
            first_index=first_index,
        )

    @staticmethod
    def euler() -> NumericSequence:
        """Return the sequence defining e.

        The result is an infinite sequence whose terms converge to e.

        Returns:
            NumericSequence: The sequence defining e.
        """
        def euler_rule(n: int) -> Real:
            return (1 + 1/n) ** n

        return NumericSequence(euler_rule, first_index=1)
