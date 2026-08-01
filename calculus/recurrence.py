"""Generic abstraction for infinite recurrences.

This module extends the generic Sequence class to model sequences whose
elements are computed recursively from preceding terms.

Classes:
    Recurrence: A sequence whose elements are defined recursively.
"""
from __future__ import annotations

__all__ = ["Recurrence"]
__author__ = "Avi Kaplan"

from collections import deque
from collections.abc import Callable, Iterable
from typing import Any, Self, TypeVar

from .sequence import INFINITY, Intfinity, Rule, Sequence
from .utils import validate_callable

T = TypeVar("T")

# Special symbols used for display.
_EMPTY_SET_SYMBOL = '\N{empty set}'

# ======================================================================
# Recurrence {aₙ}
# ======================================================================

class Recurrence(Sequence[T]):
    """A class representing infinite (and finite) recurrences.

    This subclass inherits all functionality from Sequence. Each element
    is computed from a fixed number of preceding elements via a transition
    function, seeded by a set of initial base cases.

    Methods:
        look_and_say():
            Return the Look-and-Say sequence by John Horton Conway.
        von_neumann():
            Return the Von Neumann ordinals sequence.
    """

    class _Rule:
        # Callable recurrence rule.

        __slots__ = ("basis", "cache", "first_index", "func", "order")

        def __init__(
            self,
            func: Callable[[int, tuple[T, ...]], T],
            basis: Iterable[T],
            first_index: int,
        ) -> None:
            # Initialize a new recurrence rule instance.

            self.func = func
            self.basis = tuple(basis)
            self.order = len(self.basis)
            self.first_index = first_index
            self.cache: tuple[int, tuple[T, ...]] | None = None

        def __call__(self, n: int) -> Any:
            # Return the term at n, advancing and caching as needed.
            #
            # NOTE: Due to limitations in Mypy's handling of nested
            # generic scopes, 'Any' is used here (and in the 'advance'
            # method) to keep the implementation simple. This might be
            # revisited if a cleaner approach is found.

            # Check if the input corresponds to one of the base cases.
            relative_index = n - self.first_index
            if relative_index < self.order:
                return self.basis[relative_index]

            # Check the cache before calculating the requested value.
            if self.cache is not None and self.cache[0] <= n:
                start, seed = self.cache
            else:
                start, seed = self.first_index + self.order, self.basis

            # Advance basis the required number of times.
            window = deque(seed, maxlen=self.order)
            index = start
            for _ in range(n - start):
                # NOTE: deque supports the ordered indexing func needs;
                # converting tuple(window) would waste an O(order) copy.
                item = self.func(index, window)  # type: ignore[arg-type]
                window.append(item)
                index += 1
            new_seed = tuple(window)

            # Update cache, and return the result.
            self.cache = (n, new_seed)
            return self.func(n, new_seed)

# -- INITIALIZATION

    __slots__ = ("_basis", "_func", "_order")

    def __init__(
        self,
        func: Callable[[int, tuple[T, ...]], T],
        basis: Iterable[T],
        size: Intfinity = INFINITY,
        *,
        first_index: int = 0,
    ) -> None:
        """Initialize a new recurrence object.

        Args:
            func (Callable[[int, tuple[T, ...]], T]): The transition
                function computing the next term from its index and
                a fixed number of preceding terms.
            basis (Iterable[T]): The initial base case values.
            size (Intfinity): The size of the sequence. Defaults to
                INFINITY.
            first_index (int): The first index of the sequence. Defaults
                to 0. A read-only keyword parameter.

        Raises:
            TypeError: If ``func`` is not callable, if ``basis`` is not
                iterable, if ``size`` is not INFINITY or an integer, or
                if ``first_index`` is not an integer.
            ValueError: If ``basis`` is empty, if ``size`` is negative,
                or if ``first_index`` is not in
                ``sequence.FIRST_INDEX_OPTIONS``.
        """
        validate_callable(func)
        if not isinstance(basis, Iterable):
            raise TypeError(f"'{type(basis).__name__}' object is not iterable")
        basis = tuple(basis)
        if len(basis) == 0:
            raise ValueError("basis cannot have zero length")
        rule = self._rule_factory_produce(func, basis, first_index)
        super().__init__(rule, size=size, first_index=first_index)
        self._func = func
        self._basis = basis
        self._order = len(basis)
        self._first_index = first_index

# -- FACTORY

    def _rule_factory_produce(
        self,
        func: Callable[[int, tuple[T, ...]], T],
        basis: Iterable[T],
        first_index: int,
    ) -> Rule[T]:
        # Core producer. For details, see _rule_factory().

        return self._Rule(func, basis, first_index)

    def _rule_factory(self) -> Rule[T]:
        # Produce the rule for a newly derived sequence.

        return self._rule_factory_produce(
            self._func, self._basis, self._first_index
        )

    def _factory(self, size: Intfinity = INFINITY) -> Self:
        # Produce a new sequence of the same type and rule.

        return type(self)(
            self._func, self._basis, size=size, first_index=self._first_index
        )

# -- PROPERTIES

    @property
    def basis(self) -> tuple[T, ...]:
        """The basis of the recurrence."""
        return self._basis

    @property
    def order(self) -> int:
        """The order of the recurrence."""
        return self._order

# -- SPECIAL RECURRENCES

    @staticmethod
    def von_neumann() -> Recurrence[str]:
        """Return the Von Neumann ordinals sequence.

        The result is a fixed, infinite sequence whose elements
        represent pure sets constructed inductively from the empty set.

        Returns:
            Recurrence[str]: The Von Neumann ordinals sequence.
        """
        def von_neumann_func(n: int, a: tuple[str, ...]) -> str:
            return '{' + ((a[-1][1:-1] + ', ') if n > 1 else '') + a[-1] + '}'

        return Recurrence(von_neumann_func, (_EMPTY_SET_SYMBOL,))

    @staticmethod
    def look_and_say() -> Recurrence[str]:
        """Return the Look-and-Say sequence by John Horton Conway.

        The result is a fixed, infinite sequence whose elements
        are generated by reading the digits of the previous term.

        Returns:
            Recurrence[str]: The Look-and-Say sequence.
        """
        def say_term(term: str) -> str:
            string_builder = []
            curr_digit, count = term[0], 1

            for i, digit in enumerate(term[1:]):
                if term[i+1] != term[i]:
                    string_builder.append(str(count) + curr_digit)
                    curr_digit, count = digit, 1
                else:
                    count += 1

            string_builder.append(str(count) + curr_digit)
            return "".join(string_builder)

        return Recurrence(lambda n, a: say_term(a[-1]), ("1",))
