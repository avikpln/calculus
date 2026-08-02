"""Generic abstraction for infinite sequences.

A Sequence maps indices to values through a lazy evaluation rule.

Classes:
    Sequence: An infinite sequence of arbitrary objects.
"""
from __future__ import annotations

__all__ = ["Sequence"]
__author__ = "Avi Kaplan"

from collections.abc import Callable, Generator, Iterable, Iterator
from typing import Final, Generic, Self, TypeVar, overload

from .utils import validate_callable, validate_int, validate_range

Intfinity = int | None
"""Type representing an extended integer."""

INFINITY: Final = None
"""Represents positive infinity."""

# Type of sequence elements.
T = TypeVar("T")
# Type of returned sequence elements.
R = TypeVar("R")

Rule = Callable[[int], T]
"""Type representing a mapping from integers to objects."""

FIRST_INDEX_OPTIONS = (0, 1)
"""The allowed first indices of a sequence."""

DISPLAY_HEAD = 5
"""Number of elements to display for infinite sequences."""

# Special symbols used for display.
_LEFT_SEQUENCE_BRACKET = "\N{mathematical left angle bracket}"
_RIGHT_SEQUENCE_BRACKET = "\N{mathematical right angle bracket}"
_INFINITY_SYMBOL = "\N{infinity}"

# ======================================================================
# Sequence {aₙ}
# ======================================================================

class Sequence(Iterable[T], Generic[T]):
    """A class representing infinite (and finite) sequences.

    Attributes:
        size (Intfinity): The size of the sequence (INFINITY if
            infinite).
        finite (bool): True if the sequence is finite, otherwise False.
        first_index (int): The first index of the sequence.
        last_index (Intfinity): The last index of the sequence (INFINITY
            if infinite).

    Methods:
        combine(other, op):
            Combine element-wise with another sequence or scalar.
        constant(value, size, first_index):
            Return a constant sequence.
        from_iterable(iterable, first_index):
            Return a sequence from an iterable.
        get_rule():
            Return a fresh copy of the sequence's rule.
        head(size):
            Return the first elements of the sequence.
        map(op):
            Apply an operation element-wise.
        subiter(start, stop, step):
            Return an iterator over a subsequence.
        subsequence(subrule, size):
            Construct a subsequence by reindexing the current sequence.
        tail(size):
            Return the last elements of a finite sequence.
    """

# -- INITIALIZATION

    __slots__ = ("_first_index", "_last_index", "_rule", "_size")

    @staticmethod
    def _none(n: int) -> None:
        # Default rule: returns None for all indices.
        return None

    def __init__(
        self,
        rule: Rule[T] | None = None,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> None:
        """Initialize a new sequence object.

        Args:
            rule (Rule[T]): The rule governing the sequence. If None,
                uses a default rule that returns None for every index.
            size (Intfinity): The size of the sequence. Defaults to
                INFINITY.
            first_index (int): The first index of the sequence.
                Defaults to 1. A read-only keyword parameter.

        Raises:
            TypeError: If ``rule`` is not callable, if size is not
                INFINITY or an integer, or if ``first_index`` is not an
                integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        if rule is None:
            # Callable[[int], None] is not assignable to Callable[[int], T].
            resolved_rule: Rule[T] = self._none  # type: ignore[assignment]
        else:
            validate_callable(rule)
            resolved_rule = rule
        if size is not INFINITY:
            validate_int(size, "size", allow_bool=False)
            if size < 0:
                raise ValueError(
                    f"expected nonnegative size, got {size} instead"
                )
        validate_int(first_index, "first_index", allow_bool=False)
        if first_index not in FIRST_INDEX_OPTIONS:
            raise ValueError(
                f"first_index must be in {FIRST_INDEX_OPTIONS}, "
                f"got {first_index} instead"
            )

        self._size = size
        self._first_index = first_index
        self._last_index = (
            INFINITY if size is INFINITY else first_index + size - 1
        )
        self._rule = resolved_rule

# -- FACTORY

    def _rule_factory(self) -> Rule[T]:
        # Produce the rule for a newly derived sequence.
        #
        # Subclasses with a stateful rule should override this method to
        # return an independent copy. Otherwise, derived sequences will
        # silently share the same rule object and its internal state.

        return self._rule

    def _reindex_rule_factory(self, subrule: Callable[[int], int]) -> Rule[T]:
        # Produce the rule for a newly derived subsequence.

        rule = self._rule_factory()
        return lambda k: rule(subrule(k))

    def _factory(self, size: Intfinity = INFINITY) -> Self:
        # Produce a new sequence of the same type and rule.
        #
        # Subclasses MUST override this method to preserve their type
        # through type preserving operations.

        rule = self._rule_factory()
        return type(self)(rule, size=size, first_index=self.first_index)

    def _reindex_factory(
        self,
        subrule: Callable[[int], int],
        size: Intfinity = INFINITY,
    ) -> Sequence[T]:
        # Produce a new reindexed sequence of the same type.
        #
        # Subclasses should override this method if reindexing preserves
        # their invariants. Otherwise, the default implementation falls back
        # to a more general type.

        rule = self._reindex_rule_factory(subrule)
        return Sequence(rule, size=size, first_index=self.first_index)

# -- PROPERTIES

    @property
    def size(self) -> Intfinity:
        """The size of the sequence."""
        return self._size

    @property
    def finite(self) -> bool:
        """True if and only if the sequence is finite."""
        return self._size is not INFINITY

    @property
    def first_index(self) -> int:
        """The first index of the sequence."""
        return self._first_index

    @property
    def last_index(self) -> Intfinity:
        """The last index of the sequence."""
        return self._last_index

# -- ITERATION

    def _process_range(
        self,
        start: int | None = None,
        stop: int | None = None,
        step: int | None = None,
    ) -> tuple[int, int, Intfinity]:
        # Normalize a range into start, step, and resulting size.

        # Handle start index, stop index, and step.
        step = 1 if step is None else step
        if step > 0:
            start = (
                self.first_index if start is None
                else max(start, self.first_index)
            )
            if self.last_index is not INFINITY:
                if stop is None:
                    stop = self.last_index + 1
                else:
                    stop = min(stop, self.last_index + 1)
        elif step < 0:
            if self.last_index is not INFINITY:
                if start is None:
                    start = self.last_index
                else:
                    start = min(start, self.last_index)
            else:
                # An infinite sequence with a negative step and no
                # finite stop has no well-defined bounds, so it
                # gracefully yields an empty range.
                start = self.first_index - 1 if start is None else start
            stop = (
                self.first_index - 1 if stop is None
                else max(stop, self.first_index - 1)
            )
        else:
            assert False

        # Evaluate size.
        size = INFINITY
        if stop is not None:
            size = len(range(start, stop, step))

        return start, step, size

    def subiter(
        self,
        start: int | None = None,
        stop: int | None = None,
        step: int | None = None,
    ) -> Generator[T, None, None]:
        """Return an iterator over a subsequence.

        Args:
            start (int | None): The first index to iterate from.
                Defaults to first_index.
            stop (int | None): The index at which to stop (exclusive).
                Defaults to one past the last index (or indefinitely if
                infinite).
            step (int | None): The step between successive indices.
                Defaults to 1.

        Raises:
            TypeError: If ``start``, ``stop``, or ``step`` is not an
                integer or None.
            ValueError: If ``step`` is zero or negative.
        """
        validate_range(start, stop, step)
        if step is not None and step < 0:
            raise ValueError(f"step ({step}) cannot be negative")

        start, step, size = self._process_range(start, stop, step)

        index = start
        while size is None or size > 0:
            yield self._rule(index)
            index += step
            if size is not None:
                size -= 1

    def __iter__(self) -> Iterator[T]:
        """Return an iterator for the sequence.

        Returns:
            Iterator[T]: An iterator for the sequence.
        """
        return self.subiter()

# -- REPRESENTATION

    def __str__(self) -> str:
        """Return a user-friendly sequence string representation.

        The string representation of an infinite sequence is given in
        the format 〈a1, a2, a3, a4, a5, ...〉, where the number of
        elements displayed is determined by the global constant
        DISPLAY_HEAD. For a finite sequence, its string representation
        includes all of its elements; e.g., 〈1, 2, 3〉.

        Returns:
            str: A user-friendly string representation of the sequence.
        """
        size = self.size if self.finite else DISPLAY_HEAD
        assert size is not None  # mypy
        headiter = self.subiter(stop=self.first_index + size)
        string = (
            f"{_LEFT_SEQUENCE_BRACKET}"
            f"{', '.join(str(item) for item in headiter)}"
            f"{_RIGHT_SEQUENCE_BRACKET}"
        )
        if not self.finite:
            string = string[:-1] + ", ..." + string[-1]
        return string

    def __repr__(self) -> str:
        """Return the official string representation of the sequence.

        Returns:
            str: The official string representation of the sequence.
        """
        # Intentionally return the same representation as __str__.
        # Although __repr__ is conventionally unambiguous, displaying
        # a preview of the sequence is more useful than displaying the
        # underlying callable, whose repr typically contains only a
        # memory address.
        #
        # Zen of Python:
        #   [1] Beautiful is better than ugly.
        #   [9] Although practicality beats purity.
        return self.__str__()

# -- INDEXING & SLICING (SUBSCRIPTION)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Self: ...

    def __getitem__(self, subscript: int | slice) -> T | Sequence[T]:
        """Return the specified element or subsequence.

        If subscript is an integer, the corresponding element is
        returned. If subscript is a slice, the corresponding
        subsequence is returned. Zero-indexed finite sequences also
        support negative indexing and slicing.

        Args:
            subscript (int | slice): The index or slice specifying the
                requested element or subsequence.

        Returns:
            T | Sequence[T]: The specified element or subsequence.

        Raises:
            TypeError: If ``subscript`` is neither an integer nor a slice,
                or if a slice's start, stop, or step is not an integer or
                None.
            ValueError: If a slice's step is zero.
            IndexError: If ``subscript`` is an integer index outside the
                valid range of the sequence.
        """
        if isinstance(subscript, int):
            return self._index_sequence(subscript)
        if isinstance(subscript, slice):
            validate_range(subscript.start, subscript.stop, subscript.step)
            return self._slice_sequence(subscript)
        raise TypeError(
            "sequence indices must be integers or slices, "
            f"not {type(subscript).__name__}"
        )

    def _index_sequence(self, index: int) -> T:
        # Return the element at the specified index.

        if self.finite:
            assert self.last_index is not None  # mypy

            if self.first_index <= index <= self.last_index:
                return self._rule(index)
            # Allow Python-style negative indexing for finite sequences
            # starting at index 0.
            effective_first_index = self.first_index
            if self.first_index == 0:
                effective_first_index = -(self.last_index + 1)
                if effective_first_index <= index < 0:
                    return self._rule(index - effective_first_index)
            raise IndexError(
                f"index {index} is out of range "
                f"[{effective_first_index}, {self.last_index}]"
            )
        else:
            if self.first_index <= index:
                return self._rule(index)
            raise IndexError(
                f"index {index} is out of range "
                f"[{self.first_index}, {_INFINITY_SYMBOL})"
            )

    def _slice_sequence(self, slice_: slice) -> Sequence[T]:
        # Return the subsequence specified by the given slice.

        # Allow Python-style negative indexing for finite sequences
        # starting at index 0.
        start, stop, step = slice_.start, slice_.stop, slice_.step
        if self.last_index is not INFINITY and self.first_index == 0:
            effective_first_index = -(self.last_index + 1)
            def adjust_negative_index(index: int) -> int:
                index = max(index, effective_first_index)
                index = index - effective_first_index
                return index
            if start is not None and start < 0:
                start = adjust_negative_index(start)
            if stop is not None and stop < 0:
                stop = adjust_negative_index(stop)

        start, step, size = self._process_range(start, stop, step)

        def subrule(k: int) -> int:
            return start + (k - self.first_index)*step

        return self.subsequence(subrule, size)

    def subsequence(
        self,
        subrule: Callable[[int], int],
        size: Intfinity = INFINITY,
    ) -> Sequence[T]:
        """Return the subsequence defined by the specified index map.

        Args:
            subrule (Callable[[int], int]): A function that maps
                indices of the subsequence to indices of this
                sequence.
            size (Intfinity): The size of the subsequence. Defaults to
                INFINITY.

        Returns:
            Sequence[T]: The specified subsequence.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer.
            ValueError: If ``size`` is negative.
        """
        return self._reindex_factory(subrule, size)

# -- UTILITY

    def __bool__(self) -> bool:
        """Return whether the sequence is non-empty.

        Returns:
            bool: True if the sequence contains at least one element,
                otherwise False.
        """
        return self.size != 0

    def __len__(self) -> int:
        """Return the number of elements in the sequence.

        Returns:
            int: The number of elements in the sequence.

        Raises:
            TypeError: If the sequence is infinite.
        """
        if not self.finite:
            raise TypeError("infinite sequences have no length")
        assert self.size is not None  # mypy

        return self.size

    def __reversed__(self) -> Generator[T, None, None]:
        """Return a reverse iterator over the sequence.

        Returns:
            Generator[T, None, None]: An iterator over the elements of
                the sequence in reverse order.

        Raises:
            TypeError: If the sequence is infinite.
        """
        # This method is not strictly necessary. Without it, reversed()
        # falls back to __len__() and __getitem__(), but that fails for
        # infinite sequences because __len__() raises TypeError.
        if not self.finite:
            raise TypeError("infinite sequences cannot be reversed")
        assert self.last_index is not None  # mypy

        for index in range(self.last_index, self.first_index - 1, -1):
            yield self._index_sequence(index)

    def get_rule(self) -> Rule[T]:
        """Return a fresh copy of the sequence's rule.

        Returns:
            Rule[T]: The rule of the sequence.
        """
        return self._rule_factory()

    def head(self, size: int) -> Self:
        """Return a sequence containing the first elements.

        Args:
            size (int): The number of elements to include.

        Returns:
            Sequence[T]: A sequence containing the first size elements.

        Raises:
            TypeError: If ``size`` is not an integer.
            ValueError: If ``size`` is negative.
        """
        validate_int(size, "size", allow_bool=False)
        if size < 0:
            raise ValueError(f"head size ({size}) cannot be negative")
        if self.finite:
            assert self.size is not None  # mypy
            size = min(size, self.size)
        return self._factory(size=size)

    def tail(self, size: int) -> Sequence[T]:
        """Return a sequence containing the last elements.

        Args:
            size (int): The number of elements to include.

        Returns:
            Sequence[T]: A sequence containing the last size elements.

        Raises:
            TypeError: If the sequence is infinite or if ``size``
                is not an integer.
            ValueError: If ``size`` is negative.
        """
        if not self.finite:
            raise TypeError("infinite sequences have no tail")
        validate_int(size, "size", allow_bool=False)
        if size < 0:
            raise ValueError(f"tail size ({size}) cannot be negative")
        if self.finite:
            assert self.size is not None  # mypy
            size = min(size, self.size)
        tail_offset = self.size - size
        return self._reindex_factory(lambda n: n + tail_offset, size)

    @staticmethod
    def _mapper(
        seq: Sequence[T],
        op: Callable[[T], R],
    ) -> Callable[[int], R]:
        # Return the rule obtained by applying an operation to a rule.

        rule = seq._rule_factory()
        return lambda n: op(rule(n))

    def map(self, op: Callable[[T], R]) -> Sequence[R]:
        """Apply an operation element-wise.

        The returned sequence inherits the size and first index of the
        current sequence.

        Args:
            op (Callable[[T], R]): The operation to apply.

        Returns:
            Sequence[R]: The sequence obtained by applying op to each
                element.

        Raises:
            TypeError: If ``op`` is not callable.
        """
        validate_callable(op)
        rule = self._mapper(self, op)
        return Sequence(rule, self.size, first_index=self.first_index)

    @staticmethod
    def _combiner(
        first: Sequence[T],
        second: T | Sequence[T],
        op: Callable[[T, T], R],
    ) -> tuple[Callable[[int], R], Intfinity]:
        # Return the rule and size defining the combined sequence.

        size = first.size
        if isinstance(second, Sequence):
            if first.first_index != second.first_index:
                raise ValueError(
                    "cannot combine sequences with different first indices "
                    f"({first.first_index} != {second.first_index})"
                )
            first_rule = first._rule_factory()
            second_rule = second._rule_factory()

            def combine_rule(n: int) -> R:
                return op(first_rule(n), second_rule(n))

            if second.size is not INFINITY:
                size = (
                    second.size if first.size is INFINITY
                    else min(first.size, second.size)
                )
        else:
            first_rule = first._rule_factory()

            def combine_rule(n: int) -> R:
                return op(first_rule(n), second)
        return combine_rule, size

    def combine(
        self,
        other: T | Sequence[T],
        op: Callable[[T, T], R],
    ) -> Sequence[R]:
        """Combine element-wise with another sequence or scalar.

        The returned sequence preserves the first index of the current
        sequence. Its size is the minimum of the operand sizes.

        Args:
            other (T | Sequence[T]): The sequence or scalar to combine
                with the current sequence.
            op (Callable[[T, T], R]): The operation to apply.

        Returns:
            Sequence[R]: The sequence obtained by applying op
                element-wise.

        Raises:
            TypeError: If ``op`` is not callable.
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        validate_callable(op)
        rule, size = self._combiner(self, other, op)
        return Sequence(rule, size, first_index=self.first_index)

# -- SPECIAL SEQUENCES

    @staticmethod
    def _constant_rule(value: T) -> Rule[T]:
        # Return the rule that yields a constant value for every index.
        return lambda n: value

    @staticmethod
    def constant(
        value: T,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
    ) -> Sequence[T]:
        """Return a constant sequence.

        Args:
            value (T): The constant value of each sequence element.
            size (Intfinity): The number of elements in the sequence.
                Defaults to INFINITY.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            Sequence[T]: A sequence whose elements are all equal to
                value.

        Raises:
            TypeError: If ``size`` is not INFINITY or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in FIRST_INDEX_OPTIONS.
        """
        return Sequence(
            Sequence._constant_rule(value), size=size, first_index=first_index,
        )

    @staticmethod
    def _iterable_rule(
        iterable: Iterable[T],
        first_index: int,
    ) -> tuple[Rule[T], int]:
        # Return the rule and size defining a sequence from an iterable.
        table = tuple(iterable)
        return lambda n: table[n - first_index], len(table)

    @staticmethod
    def from_iterable(
        iterable: Iterable[T],
        *,
        first_index: int = 1,
    ) -> Sequence[T]:
        """Return a sequence from an iterable.

        Args:
            iterable (Iterable[T]): The iterable providing the sequence
                elements.
            first_index (int): The index of the first sequence element.
                Defaults to 1.

        Returns:
            Sequence[T]: A finite sequence containing the elements of
                iterable.

        Raises:
            TypeError: If ``first_index`` is not an integer.
            ValueError: If ``first_index`` is not in
                FIRST_INDEX_OPTIONS.

        Examples:
            >>> Sequence.from_iterable("Hello, world!")
            ⟨'H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!'⟩
        """
        rule, size = Sequence._iterable_rule(iterable, first_index)
        return Sequence(rule, size=size, first_index=first_index)
