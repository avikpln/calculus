"""Tests for NumericSequence arithmetic operations.

Run with:
    pytest test_numeric_sequence.py -v
"""
import pytest

from .numeric_sequence import NumericSequence

# -- UNARY

def test_pos_returns_elementwise_identity() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    affirmed = +seq
    assert list(affirmed) == [1, 2, 3]


def test_pos_returns_numeric_sequence() -> None:
    seq = NumericSequence(lambda n: n, size=3)
    result = +seq
    assert isinstance(result, NumericSequence)


def test_neg_returns_elementwise_negation() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    negated = -seq
    assert list(negated) == [-1, -2, -3]


def test_neg_returns_numeric_sequence() -> None:
    seq = NumericSequence(lambda n: n, size=3)
    result = -seq
    assert isinstance(result, NumericSequence)


# -- ADDITIVE

def test_add_scalar_returns_elementwise_sum() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = seq + 10
    assert list(result) == [11, 12, 13]


def test_add_sequence_returns_elementwise_sum() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=1)
    b = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    result = a + b
    assert list(result) == [11, 22, 33]


def test_add_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a + b
    assert isinstance(result, NumericSequence)


def test_add_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a + b


def test_radd_scalar_returns_elementwise_sum() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = 10 + seq
    assert list(result) == [11, 12, 13]


def test_sub_scalar_returns_elementwise_difference() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = seq - 10
    assert list(result) == [-9, -8, -7]


def test_sub_sequence_returns_elementwise_difference() -> None:
    a = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    result = a - b
    assert list(result) == [9, 18, 27]


def test_sub_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a - b
    assert isinstance(result, NumericSequence)


def test_sub_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a - b


def test_rsub_scalar_returns_elementwise_difference() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = 10 - seq
    assert list(result) == [9, 8, 7]


# -- SUBTYPE PRESERVATION

def test_head_preserves_numeric_subtype() -> None:
    squares = NumericSequence(lambda n: n * n)
    result = (-squares).head(4)
    assert isinstance(result, NumericSequence)
    assert list(result + 1) == [0, -3, -8, -15]
