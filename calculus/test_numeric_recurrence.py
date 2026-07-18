"""Tests for NumericRecurrence construction and evaluation.

Run with:
    pytest test_numeric_recurrence.py -v
"""
from .numeric_sequence import NumericSequence
from .recurrence import Recurrence
from .numeric_recurrence import NumericRecurrence

# -- CONSTRUCTION

def test_construction_with_func_and_basis() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib.first_index == 0
    assert fib.basis == (0, 1)
    assert fib.order == 2


def test_recurrence_relation_computes_later_terms() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    assert fib[2] == 1
    assert fib[3] == 2
    assert fib[10] == 55


# -- ARITHMETIC

def test_add_scalar_returns_elementwise_sum() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=5)
    result = fib + 10
    assert list(result) == [10, 11, 11, 12, 13]


def test_neg_returns_elementwise_negation() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1), size=5)
    result = -fib
    assert list(result) == [0, -1, -1, -2, -3]


def test_arithmetic_returns_numeric_sequence() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    result = fib + 1
    assert isinstance(result, NumericSequence)
    assert not isinstance(result, NumericRecurrence)


# -- SUBTYPE PRESERVATION

def test_head_preserves_numeric_recurrence_subtype() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    prefix = fib.head(5)
    assert isinstance(prefix, NumericRecurrence)
    assert list(prefix) == [0, 1, 1, 2, 3]


# -- FALLBACK TO PLAIN NUMERIC SEQUENCE

def test_shift_by_returns_numeric_sequence_not_recurrence() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    shifted = fib.shift_by(2)
    assert isinstance(shifted, NumericSequence)
    assert not isinstance(shifted, NumericRecurrence)
    assert not isinstance(shifted, Recurrence)


def test_tail_returns_numeric_sequence_not_recurrence() -> None:
    fib = NumericRecurrence(
        lambda n, a: a[-1] + a[-2], basis=(0, 1), size=6,
    )
    suffix = fib.tail(3)
    assert isinstance(suffix, NumericSequence)
    assert not isinstance(suffix, NumericRecurrence)
    assert not isinstance(suffix, Recurrence)


# -- RULE INDEPENDENCE

def test_rule_factory_produces_independent_caches() -> None:
    fib = NumericRecurrence(lambda n, a: a[-1] + a[-2], basis=(0, 1))
    first = fib.shift_by(0)
    second = fib.shift_by(0)
    assert first._rule is not second._rule
    assert first[20] == second[20]


# -- SPECIAL RECURRENCES

def test_fibonacci() -> None:
    seq = NumericRecurrence.fibonacci()
    assert tuple(seq.head(8)) == (0, 1, 1, 2, 3, 5, 8, 13)


def test_factorial() -> None:
    seq = NumericRecurrence.factorial()
    assert tuple(seq.head(6)) == (1, 1, 2, 6, 24, 120)


def test_double_factorial() -> None:
    seq = NumericRecurrence.double_factorial()
    assert tuple(seq.head(6)) == (1, 1, 2, 3, 8, 15)


def test_catalan() -> None:
    seq = NumericRecurrence.catalan()
    assert tuple(seq.head(6)) == (1, 1, 2, 5, 14, 42)
