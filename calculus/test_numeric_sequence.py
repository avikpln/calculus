"""Tests for NumericSequence arithmetic operations.

Run with:
    pytest test_numeric_sequence.py -v
"""
import pytest

from .numeric_sequence import NumericSequence

# -- UNARY ARITHMETIC

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


def test_abs_returns_elementwise_absolute_value() -> None:
    seq = NumericSequence(lambda n: (-1)**n * n, size=5, first_index=1)
    result = abs(seq)
    assert list(result) == [1, 2, 3, 4, 5]


def test_abs_returns_numeric_sequence() -> None:
    seq = NumericSequence(lambda n: -n, size=3)
    result = abs(seq)
    assert isinstance(result, NumericSequence)


# -- ADDITIVE ARITHMETIC

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


# -- MULTIPLICATIVE ARITHMETIC

def test_mul_scalar_returns_elementwise_product() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = seq * 10
    assert list(result) == [10, 20, 30]


def test_mul_sequence_returns_elementwise_product() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=1)
    b = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    result = a * b
    assert list(result) == [10, 40, 90]


def test_mul_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a * b
    assert isinstance(result, NumericSequence)


def test_mul_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a * b


def test_rmul_scalar_returns_elementwise_product() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = 10 * seq
    assert list(result) == [10, 20, 30]


def test_truediv_scalar_returns_elementwise_quotient() -> None:
    seq = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    result = seq / 10
    assert list(result) == [1.0, 2.0, 3.0]


def test_truediv_sequence_returns_elementwise_quotient() -> None:
    a = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    result = a / b
    assert list(result) == [10.0, 10.0, 10.0]


def test_truediv_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a / b
    assert isinstance(result, NumericSequence)


def test_truediv_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a / b


def test_rtruediv_scalar_returns_elementwise_quotient() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = 60 / seq
    assert list(result) == [60.0, 30.0, 20.0]


def test_floordiv_scalar_returns_elementwise_floor_quotient() -> None:
    seq = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    result = seq // 6
    assert list(result) == [1, 3, 5]


def test_floordiv_sequence_returns_elementwise_floor_quotient() -> None:
    a = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    b = NumericSequence(lambda n: n + 1, size=3, first_index=1)
    result = a // b
    assert list(result) == [5, 6, 7]


def test_floordiv_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a // b
    assert isinstance(result, NumericSequence)


def test_floordiv_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a // b


def test_rfloordiv_scalar_returns_elementwise_floor_quotient() -> None:
    seq = NumericSequence(lambda n: n + 1, size=3, first_index=1)
    result = 20 // seq
    assert list(result) == [10, 6, 5]


def test_mod_scalar_returns_elementwise_remainder() -> None:
    seq = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    result = seq % 6
    assert list(result) == [4, 2, 0]


def test_mod_sequence_returns_elementwise_remainder() -> None:
    a = NumericSequence(lambda n: n * 10, size=3, first_index=1)
    b = NumericSequence(lambda n: n + 1, size=3, first_index=1)
    result = a % b
    assert list(result) == [0, 2, 2]


def test_mod_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a % b
    assert isinstance(result, NumericSequence)


def test_mod_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a % b


def test_rmod_scalar_returns_elementwise_remainder() -> None:
    seq = NumericSequence(lambda n: n + 1, size=3, first_index=1)
    result = 20 % seq
    assert list(result) == [0, 2, 0]


# -- EXPONENTIATION ARITHMETIC

def test_pow_scalar_returns_elementwise_power() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = seq ** 2
    assert list(result) == [1, 4, 9]


def test_pow_sequence_returns_elementwise_power() -> None:
    a = NumericSequence(lambda n: n + 1, size=3, first_index=1)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    result = a ** b
    assert list(result) == [2, 9, 64]


def test_pow_returns_numeric_sequence() -> None:
    a = NumericSequence(lambda n: n, size=3)
    b = NumericSequence(lambda n: n, size=3)
    result = a ** b
    assert isinstance(result, NumericSequence)


def test_pow_mismatched_first_index_raises_value_error() -> None:
    a = NumericSequence(lambda n: n, size=3, first_index=0)
    b = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(ValueError):
        a ** b


def test_rpow_scalar_returns_elementwise_power() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    result = 2 ** seq
    assert list(result) == [2, 4, 8]


# -- COMPLEX OPERAND BEHAVIOR

def test_floordiv_with_complex_operand_raises_type_error() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(TypeError):
        list(seq // (1 + 2j))


def test_mod_with_complex_operand_raises_type_error() -> None:
    seq = NumericSequence(lambda n: n, size=3, first_index=1)
    with pytest.raises(TypeError):
        list(seq % (1 + 2j))


# -- SUBTYPE PRESERVATION

def test_head_preserves_numeric_subtype() -> None:
    squares = NumericSequence(lambda n: n * n)
    result = (-squares).head(4)
    assert isinstance(result, NumericSequence)
    assert list(result + 1) == [0, -3, -8, -15]


# -- SPECIAL SEQUENCES

def test_constant_returns_numeric_sequence() -> None:
    seq = NumericSequence.constant(7, size=3)
    assert isinstance(seq, NumericSequence)
    assert list(seq) == [7, 7, 7]


def test_from_iterable_returns_numeric_sequence() -> None:
    seq = NumericSequence.from_iterable([1, 2, 3])
    assert isinstance(seq, NumericSequence)
    assert list(seq) == [1, 2, 3]


def test_naturals_returns_correct_numeric_sequence() -> None:
    seq = NumericSequence.naturals(size=3)
    assert isinstance(seq, NumericSequence)
    assert list(seq) == [1, 2, 3]


def test_progression_returns_correct_numeric_sequence() -> None:
    seq = NumericSequence.progression(5, 3, size=4)
    assert isinstance(seq, NumericSequence)
    assert list(seq) == [5, 8, 11, 14]


def test_geometric_returns_correct_numeric_sequence() -> None:
    seq = NumericSequence.geometric(2, 3, size=4)
    assert isinstance(seq, NumericSequence)
    assert list(seq) == [2, 6, 18, 54]
