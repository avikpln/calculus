"""Tests for Sequence construction and validation.

Run with:
    pytest test_sequence.py -v
"""
import pytest

from .sequence import Sequence

# -- CONSTRUCTION & VALIDATION

def test_default_construction_is_infinite_with_none_rule() -> None:
    seq: Sequence[None] = Sequence()
    assert seq.size is None
    assert seq.finite is False
    assert seq.first_index == 1
    assert seq[1] is None


def test_construction_with_rule_size_and_first_index() -> None:
    seq = Sequence(lambda n: n * 2, size=3, first_index=0)
    assert seq.size == 3
    assert seq.finite is True
    assert seq.first_index == 0
    assert seq.last_index == 2
    assert seq[0] == 0
    assert seq[1] == 2
    assert seq[2] == 4


def test_size_zero_is_allowed() -> None:
    seq = Sequence(lambda n: n, size=0)
    assert seq.size == 0
    assert seq.finite is True
    assert bool(seq) is False


def test_noncallable_rule_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Sequence(rule="not callable")  # type: ignore[arg-type]


def test_noninteger_size_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Sequence(lambda n: n, size="three")  # type: ignore[arg-type]


def test_negative_size_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Sequence(lambda n: n, size=-1)


def test_noninteger_first_index_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Sequence(lambda n: n, first_index="zero")  # type: ignore[arg-type]


def test_first_index_out_of_range_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Sequence(lambda n: n, first_index=2)


# -- PROPERTIES

def test_properties_reflect_construction_arguments() -> None:
    seq = Sequence(lambda n: n, size=4, first_index=0)
    assert seq.size == 4
    assert seq.finite is True
    assert seq.first_index == 0
    assert seq.last_index == 3


def test_properties_for_infinite_sequence() -> None:
    seq = Sequence(lambda n: n)
    assert seq.size is None
    assert seq.finite is False
    assert seq.last_index is None


# -- ITERATION

def test_iter_yields_elements_of_finite_sequence() -> None:
    seq = Sequence(lambda n: n * n, size=4, first_index=1)
    assert list(seq) == [1, 4, 9, 16]


def test_iter_on_infinite_sequence_is_unbounded_but_lazy() -> None:
    seq = Sequence(lambda n: n)
    it = iter(seq)
    assert [next(it) for _ in range(3)] == [1, 2, 3]


def test_subiter_with_explicit_start_stop_step() -> None:
    seq = Sequence(lambda n: n, size=10, first_index=0)
    assert list(seq.subiter(start=2, stop=8, step=2)) == [2, 4, 6]


def test_subiter_defaults_to_full_range() -> None:
    seq = Sequence(lambda n: n * 2, size=3, first_index=1)
    assert list(seq.subiter()) == [2, 4, 6]


def test_subiter_negative_step_raises_value_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(ValueError):
        list(seq.subiter(step=-1))


def test_subiter_zero_step_raises_value_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(ValueError):
        list(seq.subiter(step=0))


def test_subiter_noninteger_start_raises_type_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(TypeError):
        list(seq.subiter(start="0"))  # type: ignore[arg-type]


# -- REPRESENTATION

def test_str_of_finite_sequence_shows_all_elements() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    assert str(seq) == "\N{mathematical left angle bracket}1, 2, 3\N{mathematical right angle bracket}"


def test_str_of_infinite_sequence_shows_head_and_ellipsis() -> None:
    seq = Sequence(lambda n: n, first_index=1)
    assert str(seq) == (
        "\N{mathematical left angle bracket}1, 2, 3, 4, 5, ...\N{mathematical right angle bracket}"
    )


def test_repr_matches_str() -> None:
    seq = Sequence(lambda n: n, size=3)
    assert repr(seq) == str(seq)


# -- INDEXING & SLICING (SUBSCRIPTION)

def test_integer_index_returns_element() -> None:
    seq = Sequence(lambda n: n * 10, size=5, first_index=1)
    assert seq[3] == 30


def test_integer_index_on_infinite_sequence() -> None:
    seq = Sequence(lambda n: n)
    assert seq[100] == 100


def test_index_out_of_range_raises_index_error_on_finite_sequence() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(IndexError):
        seq[4]


def test_index_below_first_index_raises_index_error_on_infinite_sequence() -> None:
    seq = Sequence(lambda n: n, first_index=1)
    with pytest.raises(IndexError):
        seq[0]


def test_negative_index_on_zero_based_finite_sequence() -> None:
    seq = Sequence(lambda n: n * n, size=4, first_index=0)
    assert seq[-1] == 9
    assert seq[-4] == 0


def test_negative_index_out_of_range_raises_index_error() -> None:
    seq = Sequence(lambda n: n, size=4, first_index=0)
    with pytest.raises(IndexError):
        seq[-5]


def test_slice_returns_subsequence() -> None:
    seq = Sequence(lambda n: n, size=10, first_index=0)
    sub = seq[2:6]
    assert isinstance(sub, Sequence)
    assert list(sub) == [2, 3, 4, 5]


def test_slice_with_step_returns_subsequence() -> None:
    seq = Sequence(lambda n: n, size=10, first_index=0)
    sub = seq[0:10:2]
    assert isinstance(sub, Sequence)
    assert list(sub) == [0, 2, 4, 6, 8]


def test_slice_on_infinite_sequence_without_stop_is_infinite() -> None:
    seq = Sequence(lambda n: n, first_index=1)
    sub = seq[5:]
    assert isinstance(sub, Sequence)
    assert sub.finite is False
    # sub keeps seq's own first_index (1); it does not restart at 5.
    assert sub[1] == 5
    assert sub[2] == 6


def test_slice_zero_step_raises_value_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(ValueError):
        seq[::0]


def test_invalid_subscript_type_raises_type_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(TypeError):
        seq["not a subscript"]  # type: ignore[index]


# -- UTILITY

def test_bool_true_for_nonempty_finite_sequence() -> None:
    seq = Sequence(lambda n: n, size=1)
    assert bool(seq) is True


def test_bool_false_for_empty_sequence() -> None:
    seq = Sequence(lambda n: n, size=0)
    assert bool(seq) is False


def test_bool_true_for_infinite_sequence() -> None:
    seq = Sequence(lambda n: n)
    assert bool(seq) is True


def test_len_returns_size_of_finite_sequence() -> None:
    seq = Sequence(lambda n: n, size=7)
    assert len(seq) == 7


def test_len_on_infinite_sequence_raises_type_error() -> None:
    seq = Sequence(lambda n: n)
    with pytest.raises(TypeError):
        len(seq)


def test_reversed_yields_elements_in_reverse_order() -> None:
    seq = Sequence(lambda n: n, size=4, first_index=1)
    assert list(reversed(seq)) == [4, 3, 2, 1]


def test_reversed_on_infinite_sequence_raises_type_error() -> None:
    seq = Sequence(lambda n: n)
    # __reversed__ is a generator function: reversed(seq) alone only
    # builds the generator. The check inside only runs once iterated.
    with pytest.raises(TypeError):
        next(reversed(seq))


def test_shift_by_preserves_size_and_first_index() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    shifted = seq.shift_by(10)
    assert shifted.size == 3
    assert shifted.first_index == 1
    assert list(shifted) == [11, 12, 13]


def test_shift_to_shifts_rule_to_target_index() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    shifted = seq.shift_to(100)
    assert list(shifted) == [100, 101, 102]


def test_shift_by_noninteger_offset_raises_type_error() -> None:
    seq = Sequence(lambda n: n, size=3)
    with pytest.raises(TypeError):
        seq.shift_by("1")  # type: ignore[arg-type]


def test_head_returns_prefix_of_infinite_sequence() -> None:
    seq = Sequence(lambda n: n, first_index=1)
    prefix = seq.head(3)
    assert prefix.finite is True
    assert list(prefix) == [1, 2, 3]


def test_head_clips_to_available_size_on_finite_sequence() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    prefix = seq.head(10)
    assert prefix.size == 3


def test_head_negative_size_raises_value_error() -> None:
    seq = Sequence(lambda n: n, size=3)
    with pytest.raises(ValueError):
        seq.head(-1)


def test_tail_returns_suffix_of_finite_sequence() -> None:
    seq = Sequence(lambda n: n, size=5, first_index=1)
    suffix = seq.tail(2)
    assert list(suffix) == [4, 5]


def test_tail_on_infinite_sequence_raises_type_error() -> None:
    seq = Sequence(lambda n: n)
    with pytest.raises(TypeError):
        seq.tail(2)


def test_tail_negative_size_raises_value_error() -> None:
    seq = Sequence(lambda n: n, size=5)
    with pytest.raises(ValueError):
        seq.tail(-1)


def test_subsequence_reindexes_with_custom_map() -> None:
    seq = Sequence(lambda n: n, size=10, first_index=0)
    sub = seq.subsequence(lambda k: k * 2, size=5)
    assert list(sub) == [0, 2, 4, 6, 8]


def test_map_applies_unary_operation_elementwise() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    squared = seq.map(lambda x: x * x)
    assert list(squared) == [1, 4, 9]


def test_combine_two_sequences_elementwise() -> None:
    a = Sequence(lambda n: n, size=3, first_index=1)
    b = Sequence(lambda n: n * 10, size=3, first_index=1)
    combined = a.combine(b, lambda x, y: x + y)
    assert list(combined) == [11, 22, 33]


def test_combine_with_scalar_broadcasts() -> None:
    seq = Sequence(lambda n: n, size=3, first_index=1)
    combined = seq.combine(10, lambda x, y: x + y)
    assert list(combined) == [11, 12, 13]


def test_combine_size_is_minimum_of_operand_sizes() -> None:
    a = Sequence(lambda n: n, size=5, first_index=1)
    b = Sequence(lambda n: n, size=2, first_index=1)
    combined = a.combine(b, lambda x, y: x + y)
    assert combined.size == 2


def test_combine_mismatched_first_index_raises_value_error() -> None:
    a = Sequence(lambda n: n, size=3, first_index=0)
    b = Sequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a.combine(b, lambda x, y: x + y)


# -- SPECIAL SEQUENCES

def test_constant_sequence_repeats_value() -> None:
    seq = Sequence.constant(7, size=3)
    assert list(seq) == [7, 7, 7]


def test_constant_sequence_is_infinite_by_default() -> None:
    seq = Sequence.constant(7)
    assert seq.finite is False
    assert seq[1000] == 7


def test_constant_negative_size_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Sequence.constant(7, size=-1)


def test_from_iterable_builds_finite_sequence() -> None:
    seq = Sequence.from_iterable([10, 20, 30])
    assert seq.finite is True
    assert seq.size == 3
    assert list(seq) == [10, 20, 30]


def test_from_iterable_respects_first_index() -> None:
    seq = Sequence.from_iterable([10, 20, 30], first_index=0)
    assert seq[0] == 10
    assert seq[2] == 30


def test_from_iterable_noninteger_first_index_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Sequence.from_iterable([1, 2, 3], first_index="0")  # type: ignore[arg-type]
