"""Tests for Recurrence construction and evaluation.

Run with:
    pytest tests/test_recurrence.py -v
"""
import pytest

from calculus.sequence import Sequence
from calculus.recurrence import Recurrence

# -- CONSTRUCTION & VALIDATION

def test_construction_with_func_and_basis() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib.first_index == 0
    assert fib.finite is False


def test_construction_with_size_is_finite() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=5)
    assert fib.finite is True
    assert fib.size == 5
    assert fib.last_index == 4


def test_noncallable_func_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Recurrence("not callable", basis=(0, 1))  # type: ignore[arg-type]


def test_noniterable_basis_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Recurrence(lambda n, a: 2 * a[-1], basis=1)  # type: ignore[arg-type]


def test_empty_basis_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Recurrence(lambda n, a: 2 * a[-1], basis=())


def test_first_index_is_always_zero() -> None:
    seq = Recurrence(lambda n, a: 2 * a[-1], basis=(1,))
    assert seq.first_index == 0


# -- PROPERTIES

def test_basis_returns_original_values() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib.basis == (0, 1)


def test_order_returns_basis_length() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib.order == 2


# -- EVALUATION

def test_basis_values_are_returned_directly() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[0] == 0
    assert fib[1] == 1


def test_recurrence_relation_computes_later_terms() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[2] == 1
    assert fib[3] == 2
    assert fib[4] == 3
    assert fib[10] == 55


def test_iter_yields_expected_terms() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=7)
    assert list(fib) == [0, 1, 1, 2, 3, 5, 8]


def test_single_term_basis_recurrence() -> None:
    doubling = Recurrence(lambda n, a: 2 * a[-1], basis=(1,), size=5)
    assert list(doubling) == [1, 2, 4, 8, 16]


def test_shift_by_computes_correct_values() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=10)
    shifted = fib.shift_by(2)
    assert list(shifted) == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


# -- CACHING BEHAVIOR

def test_revisiting_same_index_returns_same_value() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[20] == fib[20]


def test_out_of_order_access_still_computes_correctly() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[10] == 55
    assert fib[5] == 5
    assert fib[15] == 610


def test_sequential_access_uses_cache_fast_path() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[50] == 12586269025
    assert fib[51] == 20365011074
    assert fib[52] == 32951280099


# -- SUBTYPE PRESERVATION

def test_head_preserves_recurrence_subtype() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    prefix = fib.head(5)
    assert isinstance(prefix, Recurrence)
    assert list(prefix) == [0, 1, 1, 2, 3]


# -- FALLBACK TO PLAIN SEQUENCE

def test_shift_by_returns_plain_sequence() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    shifted = fib.shift_by(2)
    assert isinstance(shifted, Sequence)
    assert not isinstance(shifted, Recurrence)


def test_tail_returns_plain_sequence() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=6)
    suffix = fib.tail(3)
    assert isinstance(suffix, Sequence)
    assert not isinstance(suffix, Recurrence)


def test_subsequence_returns_plain_sequence() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    sub = fib.subsequence(lambda k: k * 2, size=4)
    assert isinstance(sub, Sequence)
    assert not isinstance(sub, Recurrence)


# -- RULE INDEPENDENCE

def test_rule_factory_produces_independent_caches() -> None:
    fib = Recurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    first = fib.shift_by(0)
    second = fib.shift_by(0)
    assert first._rule is not second._rule
    assert first[20] == second[20]


# -- SPECIAL RECURRENCES

def test_von_neumann() -> None:
    seq = Recurrence.von_neumann()
    assert tuple(seq.head(4)) == (
        "\N{EMPTY SET}",
        "{\N{EMPTY SET}}",
        "{\N{EMPTY SET}, {\N{EMPTY SET}}}",
        "{\N{EMPTY SET}, {\N{EMPTY SET}}, {\N{EMPTY SET}, {\N{EMPTY SET}}}}",
    )

def test_look_and_say() -> None:
    seq = Recurrence.look_and_say()
    assert tuple(seq.head(6)) == ("1", "11", "21", "1211", "111221", "312211")
