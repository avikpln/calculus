"""Recurrence-based abstraction for sequences defined by prior terms.

This module extends the generic Sequence abstraction with support for
sequences whose elements are computed recursively from earlier terms.

Classes:
    Recurrence: A sequence whose elements are defined recursively.
"""
from __future__ import annotations

__all__ = ["Recurrence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable, Iterable
from typing import TypeVar, Any
from collections import deque

from .sequence import Sequence

R = TypeVar("R")

#========================================================================
# Recurrence {aₙ}
#========================================================================

class Recurrence(Sequence[R]):
    """A sequence whose elements are computed from prior terms.

    This subclass inherits all functionality from Sequence. Each element
    is computed from a fixed number of preceding elements via a transition
    function, seeded by a set of initial base cases.
    """

    class _Rule:
        # Callable recurrence rule, caching prior terms as it advances.

        __slots__ = ("func", "basis", "order", "cache")

        def __init__(
            self,
            func: Callable[[int, tuple[R,...]], R],
            basis: Iterable[R],
        ) -> None:
            # Initialize a new recurrence rule instance.

            self.func = func
            self.basis = tuple(basis)
            self.order = len(self.basis)
            self.cache: tuple[int, tuple[R,...]] | None = None

        def __call__(self, n: int) -> Any:
            # Return the term at n, advancing and caching as needed.
            #
            # NOTE: Due to limitations in Mypy's handling of nested
            # generic scopes, 'Any' is used here (and in the 'advance'
            # method) to keep the implementation simple. This might be
            # revisited if a cleaner approach is found.

            # Check if the input corresponds to one of the base cases.
            if n < self.order:
                return self.basis[n]

            # Check the cache before calculating the requested value.
            if self.cache is not None and self.cache[0] <= n:
                start, seed = self.cache
            else:
                start, seed = self.order, self.basis

            # Advance basis the required number of times.
            window = deque(seed, maxlen=self.order)
            index = start
            for _ in range(0, n - start):
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

    __slots__ = ("_func", "_basis", "_order")

    def __init__(
        self,
        func: Callable[[int, tuple[R,...]], R],
        basis: Iterable[R],
        size: int | None = None,
    ) -> None:
        """Initialize a new recurrence object.

        Args:
            func (Callable[[int, tuple[R,...]], R]): The transition
                function computing a term from its index and the
                preceding basis-many terms.
            basis (Iterable[R]): The initial base case values.
            size (int | None): The size of the sequence. Defaults to
                None, which corresponds to an infinite sequence.

        Raises:
            TypeError: If ``func`` is not callable, or if ``basis`` is
                not iterable.
            ValueError: If ``basis`` is empty.
        """
        if not callable(func):
            raise TypeError(f"'{type(func).__name__}' object is not callable")
        if not isinstance(basis, Iterable):
            raise TypeError(f"'{type(basis).__name__}' object is not iterable")
        basis = tuple(basis)
        if len(basis) == 0:
            raise ValueError("basis cannot have zero length")

        self._func = func
        self._basis = basis
        self._order = len(basis)
        rule = self._rule_factory()

        super().__init__(rule, size=size, first_index=0)

    def _rule_factory(self) -> Callable[[int], R]:
        # Return the rule used for recurrence construction.

        return self._Rule(self._func, self._basis)

    def _resize(self, size: int | None) -> Recurrence[R]:
        # Construct a new recurrence with the given rule and size.

        return Recurrence(self._func, self._basis, size=size)

# -- PROPERTIES

    @property
    def basis(self) -> tuple[R,...]:
        """The basis of the recurrence."""
        return self._basis

    @property
    def order(self) -> int:
        """The order of the recurrence."""
        return self._order

