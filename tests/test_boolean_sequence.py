"""Tests for BooleanSequence.

Run with:
    pytest tests/test_boolean_sequence.py -v
"""
import pytest

from calculus.boolean_sequence import BooleanSequence
from calculus.numeric_sequence import NumericSequence

# -- UTILITY

def test_to_numeric_returns_numeric_sequence() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq.to_numeric()
    assert isinstance(result, NumericSequence)
    assert list(result) == [1, 0, 1, 0]


# -- UNARY LOGICAL

def test_invert_returns_elementwise_negation() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    negated = ~seq
    assert list(negated) == [False, True, False, True]


def test_invert_returns_boolean_sequence() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=3)
    result = ~seq
    assert isinstance(result, BooleanSequence)


# -- BINARY LOGICAL

def test_or_scalar_returns_elementwise_or() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq | False
    assert list(result) == [True, False, True, False]


def test_or_sequence_returns_elementwise_or() -> None:
    a = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    b = BooleanSequence(lambda n: n % 3 == 0, size=4, first_index=0)
    result = a | b
    assert list(result) == [True, False, True, True]


def test_or_returns_boolean_sequence() -> None:
    a = BooleanSequence(lambda n: True, size=3)
    b = BooleanSequence(lambda n: False, size=3)
    result = a | b
    assert isinstance(result, BooleanSequence)


def test_or_mismatched_first_index_raises_value_error() -> None:
    a = BooleanSequence(lambda n: True, size=3, first_index=0)
    b = BooleanSequence(lambda n: True, size=3, first_index=1)
    with pytest.raises(ValueError):
        a | b


def test_or_with_unsupported_operand_raises_type_error() -> None:
    seq = BooleanSequence(lambda n: True, size=3)
    with pytest.raises(TypeError):
        seq | "not a bool"


def test_ror_scalar_returns_elementwise_or() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = False | seq
    assert list(result) == [True, False, True, False]


def test_and_scalar_returns_elementwise_and() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq & True
    assert list(result) == [True, False, True, False]


def test_and_sequence_returns_elementwise_and() -> None:
    a = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    b = BooleanSequence(lambda n: n % 3 == 0, size=4, first_index=0)
    result = a & b
    assert list(result) == [True, False, False, False]


def test_and_returns_boolean_sequence() -> None:
    a = BooleanSequence(lambda n: True, size=3)
    b = BooleanSequence(lambda n: True, size=3)
    result = a & b
    assert isinstance(result, BooleanSequence)


def test_and_mismatched_first_index_raises_value_error() -> None:
    a = BooleanSequence(lambda n: True, size=3, first_index=0)
    b = BooleanSequence(lambda n: True, size=3, first_index=1)
    with pytest.raises(ValueError):
        a & b


def test_and_with_unsupported_operand_raises_type_error() -> None:
    seq = BooleanSequence(lambda n: True, size=3)
    with pytest.raises(TypeError):
        seq & "not a bool"


def test_rand_scalar_returns_elementwise_and() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = True & seq
    assert list(result) == [True, False, True, False]


def test_xor_scalar_returns_elementwise_xor() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq ^ True
    assert list(result) == [False, True, False, True]


def test_xor_sequence_returns_elementwise_xor() -> None:
    a = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    b = BooleanSequence(lambda n: n % 3 == 0, size=4, first_index=0)
    result = a ^ b
    assert list(result) == [False, False, True, True]


def test_xor_returns_boolean_sequence() -> None:
    a = BooleanSequence(lambda n: True, size=3)
    b = BooleanSequence(lambda n: False, size=3)
    result = a ^ b
    assert isinstance(result, BooleanSequence)


def test_xor_mismatched_first_index_raises_value_error() -> None:
    a = BooleanSequence(lambda n: True, size=3, first_index=0)
    b = BooleanSequence(lambda n: True, size=3, first_index=1)
    with pytest.raises(ValueError):
        a ^ b


def test_xor_with_unsupported_operand_raises_type_error() -> None:
    seq = BooleanSequence(lambda n: True, size=3)
    with pytest.raises(TypeError):
        seq ^ "not a bool"


def test_rxor_scalar_returns_elementwise_xor() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = True ^ seq
    assert list(result) == [False, True, False, True]


# -- SUBTYPE PRESERVATION

def test_head_preserves_boolean_subtype() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq.head(2)
    assert isinstance(result, BooleanSequence)
    assert list(result) == [True, False]


# -- SPECIAL BOOLEAN SEQUENCES

def test_true_returns_boolean_sequence_with_correct_values() -> None:
    seq = BooleanSequence.true(size=3)
    assert isinstance(seq, BooleanSequence)
    assert list(seq) == [True, True, True]


def test_true_negative_size_raises_value_error() -> None:
    with pytest.raises(ValueError):
        BooleanSequence.true(size=-1)


def test_false_returns_boolean_sequence_with_correct_values() -> None:
    seq = BooleanSequence.false(size=3)
    assert isinstance(seq, BooleanSequence)
    assert list(seq) == [False, False, False]


def test_false_negative_size_raises_value_error() -> None:
    with pytest.raises(ValueError):
        BooleanSequence.false(size=-1)


def test_from_iterable_returns_boolean_sequence_with_correct_values() -> None:
    seq = BooleanSequence.from_iterable([True, False, True])
    assert isinstance(seq, BooleanSequence)
    assert list(seq) == [True, False, True]
