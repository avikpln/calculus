"""Generic abstraction for finite and infinite sequences.

A Sequence maps indices to values through a lazy evaluation rule.

Classes:
    Sequence: A finite or infinite sequence of arbitrary objects.
"""
from __future__ import annotations

__all__ = ["Sequence"]
__version__ = '0.2.0'
__author__ = 'Avi Kaplan'

from collections.abc import Callable, Iterable
from typing import Generic, TypeVar, Generator, overload

from .utils import validate_int, validate_optional_int

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")

# Number of elements to display for infinite sequences.
DISPLAY_HEAD = 5

# Special symbols used for display.
_LEFT_SEQUENCE_BRACKET = "\N{mathematical left angle bracket}"
_RIGHT_SEQUENCE_BRACKET = "\N{mathematical right angle bracket}"
_INFINITY_SYMBOL = "\N{infinity}"

#=======================================================================
# Sequence {aₙ}
#=======================================================================

class _Rule(Generic[T]):
    # This class represents a sequence rule mapping integers to values.

    __slots__ = ("_func",)

    _func: Callable[[int], T]

    def __init__(self, func: Callable[[int], T]) -> None:
        # Initialize a new rule instance.
        if not callable(func):
            raise TypeError(f"'{type(func).__name__}' object is not callable")
        self._func = func

    def __call__(self, n: int) -> T:
        # Invoke the rule function on the given input.
        validate_int(n, "n")
        return self.func(n)

    @property
    def func(self) -> Callable[[int], T]:
        # The function defining the rule.
        return self._func


class Sequence(Generic[T], Iterable[T]):
    """A class representing infinite (and finite) sequences of objects.

    Attributes:
        size (int | None): The size of the sequence (None if infinite).
        finite (bool): True if the sequence is finite, otherwise False.
        first_index (int): The first index of the sequence.
        last_index (int | None): The last index of the sequence (None
            if infinite).

    Methods:
        subsequence(subfunc, size):
            Construct a subsequence by reindexing the current sequence.
        shift_by(offset):
            Shift the evaluation rule by a fixed offset.
        shift_to(where):
            Shift the evaluation rule to a given starting index.
        head(size):
            Return the first elements of the sequence.
        tail(size):
            Return the last elements of a finite sequence.
        map(op):
            Apply a unary operation element-wise.
        combine(other, op):
            Apply a binary operation element-wise.
    """

# -- INITIALIZATION

    __slots__ = ("_size", "_first_index", "_last_index", "_rule")

    # The default first index of a sequence.
    DEFAULT_FIRST_INDEX = 1

    @staticmethod
    def _none(n: int) -> None:
        # Default rule: returns None for all indices.
        return None

    def __init__(
        self,
        func: Callable[[int], T] | None = None,
        size: int | None = None, *,
        first_index: int = DEFAULT_FIRST_INDEX
    ) -> None:
        """Initialize a new sequence object.

        Args:
            func (Callable[[int], T]): The rule governing the sequence.
                If None, uses a default rule that returns None for
                every index.
            size (int | None): The size of the sequence. Defaults to
                None, which corresponds to an infinite sequence.
            first_index (int): The first index of the sequence.
                Defaults to DEFAULT_FIRST_INDEX. A read-only keyword
                parameter.

        Raises:
            TypeError: If ``func`` is not callable, if size is not None
                or an integer, or if ``first_index`` is not an integer.
            ValueError: If ``size`` is negative.
        """
        if func is None:
            func = self._none  # type: ignore[assignment]
        if not callable(func):
            raise TypeError(f"'{type(func).__name__}' object is not callable")
        if size is not None:
            validate_int(size, "size")
            if size < 0:
                raise ValueError(
                    f"expected nonnegative size, got {size} instead"
                )
        validate_int(first_index, "first_index")
        self._size = size
        self._first_index = first_index
        self._last_index = None if size is None else first_index + size - 1
        self._set_rule(func)

    def _set_rule(self, func: Callable[[int], T]) -> None:
        # Establish the rule of the sequence.
        self._rule = _Rule(func)

    def _resize(self, size: int | None) -> Sequence[T]:
        # Construct a new sequence of the same type with the given size.

        return Sequence(self._rule, size=size, first_index=self.first_index)

    def _reindex(
        self,
        func: Callable[[int], T] | None,
        size: int | None = None,
    ) -> Sequence[T]:
        # Construct a new sequence with the given rule and size.

        return Sequence(func, size=size, first_index=self.first_index)

# -- PROPERTIES

    @property
    def size(self) -> int | None:
        """The size of the sequence (None if infinite)."""
        return self._size

    @property
    def finite(self) -> bool:
        """True if and only if the sequence is finite."""
        return self._size is not None

    @property
    def first_index(self) -> int:
        """The first index of the sequence."""
        return self._first_index

    @property
    def last_index(self) -> int | None:
        """The last index of the sequence (None if infinite)."""
        return self._last_index

# -- ITERATION

    def _process_range(
        self,
        start: int | None = None,
        stop: int | None = None,
        step: int | None = None,
    ) -> tuple[int, int, int | None]:
        # Normalize a range into start, step, and resulting size.

        validate_optional_int(start, "start")
        validate_optional_int(stop, "stop")
        validate_optional_int(step, "step")

        # Handle start index, stop index, and step.
        step = 1 if step is None else step
        if step > 0:
            start = (
                self.first_index if start is None
                else max(start, self.first_index)
            )
            if self.last_index is not None:
                if stop is None:
                    stop = self.last_index + 1
                else:
                    stop = min(stop, self.last_index + 1)
        elif step < 0:
            if self.last_index is not None:
                if start is None:
                    start = self.last_index
                else:
                    start = min(start, self.last_index)
            stop = (
                self.first_index - 1 if stop is None
                else max(stop, self.first_index - 1)
            )
        else:
            raise ValueError("range step cannot be zero")
        assert start is not None

        # Evaluate size.
        size = None
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
        if step is not None and step < 0:
            raise ValueError(f"step ({step}) must be positive")

        start, step, size = self._process_range(start, stop, step)

        index = start
        while size is None or size > 0:
            yield self._rule(index)
            index += step
            if size is not None:
                size -= 1

    def __iter__(self) -> Generator[T, None, None]:
        """Return an iterator for the sequence.

        Returns:
            Generator[T, None, None]: An iterator for the sequence.
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
        assert size is not None
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

    def __getitem__(self, subscript: int | slice) -> T | Sequence[T]:
        """Return the specified element or subsequence.

        If subscript is an integer, the corresponding element is
        returned. If subscript is a slice, the corresponding
        subsequence is returned.

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
            return self._slice_sequence(subscript)
        raise TypeError(
            "sequence indices must be integers or slices, "
            f"not {type(subscript).__name__}"
        )

    def _index_sequence(self, index: int) -> T:
        # Return the element at the specified index.

        if self.finite:
            assert self.last_index is not None

            if self.first_index <= index <= self.last_index:
                return self._rule(index)
            # Allow Python-style negative indexing for finite sequences
            # starting at index 0.
            if self.first_index == 0 and -(self.last_index + 1) <= index < 0:
                return self._rule(index + self.last_index + 1)
            raise IndexError(
                f"index {index} is out of range "
                f"[{self.first_index}, {self.last_index}]"
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

        start, step, size = self._process_range(
            slice_.start, slice_.stop, slice_.step
        )
        subrule = lambda k: start + (k - self.first_index) * step
        return self.subsequence(subrule, size)

    def subsequence(
        self,
        subfunc: Callable[[int], int],
        size: int | None = None
    ) -> Sequence[T]:
        """Return the subsequence defined by the specified index map.

        Args:
            subfunc (Callable[[int], int]): A function that maps
                indices of the subsequence to indices of this
                sequence.
            size (int | None): The size of the subsequence.
                Defaults to None, which corresponds to an infinite
                subsequence.

        Returns:
            Sequence[T]: The specified subsequence.

        Raises:
            TypeError: If ``size`` is not None or an integer.
            ValueError: If ``size`` is negative.
        """
        func = lambda k: self._rule(subfunc(k))
        return self._reindex(func, size)

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
        assert self.size is not None

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
        assert self.last_index is not None

        for index in range(self.last_index, self.first_index - 1, -1):
            yield self._index_sequence(index)

    def shift_by(self, offset: int) -> Sequence[T]:
        """Return a sequence with a shifted evaluation rule.

        The returned sequence preserves the size and first index of the
        current sequence.

        Args:
            offset (int): The offset by which to shift the evaluation
                rule.

        Returns:
            Sequence[T]: A sequence whose evaluation rule is shifted by
                ``offset``.

        Raises:
            TypeError: If ``offset`` is not an integer.
        """
        # This operation shifts the underlying evaluation rule while
        # preserving the sequence's size and first_index. For finite
        # sequences, the shifted rule may be evaluated outside the
        # original domain.
        validate_int(offset, "offset")
        func = lambda n: self._rule(n + offset)
        return self._reindex(func, self.size)

    def shift_to(self, where: int) -> Sequence[T]:
        """Shift the evaluation rule to a given index.

        Args:
            where (int): The index to which to shift the evaluation
                rule.

        Returns:
            Sequence[T]: A sequence whose evaluation rule is shifted to
                the given index.

        Raises:
            TypeError: If ``where`` is not an integer.
        """
        validate_int(where, "where")
        return self.shift_by(where - self.first_index)

    def head(self, size: int) -> Sequence[T]:
        """Return a sequence containing the first elements.

        Args:
            size (int): The number of elements to include.

        Returns:
            Sequence[T]: A sequence containing the first size elements.

        Raises:
            TypeError: If ``size`` is not an integer.
            ValueError: If ``size`` is negative.
        """
        validate_int(size, "size")
        if size < 0:
            raise ValueError(f"head size ({size}) cannot be negative")
        if self.finite:
            assert self.size is not None
            size = min(size, self.size)
        return self._resize(size)

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
        validate_int(size, "size")
        if size < 0:
            raise ValueError(f"tail size ({size}) cannot be negative")
        if self.finite:
            assert self.size is not None
            size = min(size, self.size)
        func = lambda n: self._rule(n + self.size - size)
        return self._reindex(func, size)

    @staticmethod
    def _mapper(
        seq: Sequence[T],
        op: Callable[[T], U]
    ) -> Callable[[int], U]:
        # Return the rule obtained by applying an operation to a rule.

        return lambda n: op(seq._rule(n))

    def map(self, op: Callable[[T], U]) -> Sequence[U]:
        """Return the sequence obtained by applying a unary operation.

        The returned sequence inherits the size and first index of the
        current sequence.

        Args:
            op (Callable[[T], U]): The unary operation to apply.

        Returns:
            Sequence[U]: The sequence obtained by applying op to each
                element.
        """
        rule = self._mapper(self, op)
        return Sequence(rule, self.size, first_index=self.first_index)

    @staticmethod
    def _combiner(
        first: Sequence[T],
        second: S | Sequence[S],
        op: Callable[[T, S], U]
    ) -> tuple[Callable[[int], U], int | None]:
        # Return the rule and size defining the combined sequence.

        size = first.size
        if isinstance(second, Sequence):
            if first.first_index != second.first_index:
                raise ValueError(
                    "cannot apply a binary operation on sequences with "
                    "different first index properties "
                    f"({first.first_index} != {second.first_index})"
                )
            rule = lambda n: op(first._rule(n), second._rule(n))
            if second.size is not None:
                size = (
                    second.size if first.size is None
                    else min(first.size, second.size)
                )
        else:
            rule = lambda n: op(first._rule(n), second)
        return rule, size

    @overload
    def combine(
        self, other: S, op: Callable[[T, S], U]
    ) -> Sequence[U]: ...

    @overload
    def combine(
        self, other: Sequence[S], op: Callable[[T, S], U]
    ) -> Sequence[U]: ...

    def combine(
        self,
        other: S | Sequence[S],
        op: Callable[[T, S], U]
    ) -> Sequence[U]:
        """Combine this sequence with another sequence or scalar.

        The returned sequence preserves the first index of the current
        sequence. Its size is the minimum of the operand sizes.

        Args:
            other (S | Sequence[S]): The sequence or scalar to combine
                with the current sequence.
            op (Callable[[T, S], U]): The binary operation to apply.

        Returns:
            Sequence[U]: The sequence obtained by applying op
                element-wise.

        Raises:
            ValueError: If ``other`` is a sequence with a different
                first index.
        """
        rule, size = self._combiner(self, other, op)
        return Sequence(rule, size, first_index=self.first_index)

# -- SPECIAL SEQUENCES

    @staticmethod
    def constant(
        value: T,
        size: int | None = None,
        *,
        first_index: int = DEFAULT_FIRST_INDEX
    ) -> Sequence[T]:
        """Return a constant sequence.

        Args:
            value (T): The constant value of each sequence element.
            size (int | None): The number of elements in the sequence,
                or None for an infinite sequence.
            first_index (int): The index of the first sequence element.

        Returns:
            Sequence[T]: A sequence whose elements are all equal to
                value.

        Raises:
            TypeError: If ``size`` is not None or an integer, or if
                ``first_index`` is not an integer.
            ValueError: If ``size`` is negative.
        """
        return Sequence(lambda n: value, size=size, first_index=first_index)

    @staticmethod
    def from_iterable(
        iterable: Iterable[T],
        *,
        first_index: int = DEFAULT_FIRST_INDEX
    ) -> Sequence[T]:
        """Return a sequence from an iterable.

        Args:
            iterable (Iterable[T]): The iterable providing the sequence
                elements.
            first_index (int): The index of the first sequence element.

        Returns:
            Sequence[T]: A finite sequence containing the elements of
                iterable.

        Raises:
            TypeError: If ``first_index`` is not an integer.

        Examples:
            >>> Sequence.from_iterable("Hello, world!")
            ⟨'H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!'⟩
        """
        table = tuple(iterable)
        return Sequence(lambda n: table[n - first_index], len(table),
                        first_index=first_index)
