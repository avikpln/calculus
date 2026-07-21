"""Infinite numeric series.

This module extends NumericSequence with support for series, whose
elements are the partial sums of an underlying term sequence.

Classes:
    Series: A numeric sequence whose elements are partial sums of a term
        sequence.
"""
from __future__ import annotations

__all__ = ["Series"]
__author__ = "Avi Kaplan"

from collections.abc import Callable

from .numeric_sequence import Number, NumericSequence
from .utils import validate_callable

#=======================================================================
# Series {Sₙ}
#=======================================================================

class Series(NumericSequence):
    """A numeric sequence whose elements are partial sums of terms.

    This subclass inherits all functionality from NumericSequence.
    Each element is the accumulated sum of an underlying term rule,
    starting from the sequence's first index.

    Methods:
        alternating_harmonic():
            Return the alternating harmonic series.
        basel():
            Return the Basel problem series.
        harmonic():
            Return the harmonic series.
        leibniz():
            Return the Leibniz series.
    """

    class _Rule:
        # Callable series rule, caching the last computed partial sum.

        __slots__ = ("cache", "first_index", "term_rule")

        def __init__(
            self,
            term_rule: Callable[[int], Number],
            first_index: int,
        ) -> None:
            # Initialize a new series rule instance.

            self.term_rule = term_rule
            self.first_index = first_index
            self.cache: tuple[int, Number] | None = None

        def __call__(self, n: int) -> Number:
            # Return the partial sum at index n.

            # Check the cache before calculating the requested value.
            if self.cache is not None and self.cache[0] <= n:
                index, value = self.cache
            else:
                index = self.first_index
                value = self.term_rule(index)

            # Calculate the target sum.
            while index < n:
                index += 1
                value += self.term_rule(index)

            # Update cache, and return the result.
            self.cache = (n, value)
            return value

# -- INITIALIZATION

    __slots__ = ("_term_rule",)

    def __init__(
        self,
        term_rule: Callable[[int], Number],
        size: int | None = None,
        *,
        first_index: int = 1,
    ) -> None:
        """Initialize a new series object.

        Args:
            term_rule (Callable[[int], Number]): The rule governing the
                terms being summed.
            size (int | None): The size of the sequence. Defaults to
                None, which corresponds to an infinite sequence.
            first_index (int): The first index of the sequence. Defaults
                to 1. A read-only keyword parameter.

        Raises:
            TypeError: If ``term_rule`` is not callable, if ``size`` is
                not None or an integer, or if ``first_index`` is not an
                integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        validate_callable(term_rule)
        rule = self._rule_factory_produce(term_rule, first_index)
        super().__init__(rule, size=size, first_index=first_index)
        self._term_rule = term_rule

# -- FACTORY

    def _rule_factory_produce(
        self,
        term_rule: Callable[[int], Number],
        first_index: int,
    ) -> Callable[[int], Number]:
        # Core producer. For details, see _rule_factory().

        return self._Rule(term_rule, first_index)

    def _rule_factory(self) -> Callable[[int], Number]:
        # Produce the rule for a newly derived sequence.

        return self._rule_factory_produce(self._term_rule, self.first_index)

    def _resize(self, size: int | None) -> Series:
        # Produce a new sequence of the same type and given size.

        return Series(self._term_rule, size=size, first_index=self.first_index)

    def _reindex(
        self,
        rule: Callable[[int], Number] | None,
        size: int | None = None,
    ) -> NumericSequence:
        # Produce a new sequence with the given rule and size.

        return NumericSequence._reindex(self, rule, size)
