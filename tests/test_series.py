"""Tests for Series construction and evaluation.

Run with:
    pytest tests/test_series.py -v
"""
from calculus.numeric_sequence import NumericSequence
from calculus.series import Series

# -- CONSTRUCTION

def test_construction_with_term_rule() -> None:
    series = Series(lambda n: n)
    assert series.first_index == 1
    assert series.finite is False


def test_construction_with_size_is_finite() -> None:
    series = Series(lambda n: n, size=5)
    assert series.finite is True
    assert series.size == 5


def test_construction_with_first_index_zero() -> None:
    series = Series(lambda n: n, first_index=0)
    assert series.first_index == 0


# -- EVALUATION

def test_partial_sums_computed_correctly() -> None:
    series = Series(lambda n: n)
    assert list(series.head(5)) == [1, 3, 6, 10, 15]


def test_first_index_zero_partial_sums() -> None:
    series = Series(lambda n: n, first_index=0)
    assert list(series.head(5)) == [0, 1, 3, 6, 10]


def test_single_term_size_returns_first_term() -> None:
    series = Series(lambda n: n, size=1)
    assert list(series) == [1]


# -- CACHING BEHAVIOR

def test_revisiting_same_index_returns_same_value() -> None:
    series = Series(lambda n: n)
    assert series[20] == series[20]


def test_out_of_order_access_still_computes_correctly() -> None:
    series = Series(lambda n: n)
    assert series[10] == 55
    assert series[5] == 15
    assert series[15] == 120


def test_sequential_access_uses_cache_fast_path() -> None:
    series = Series(lambda n: n)
    assert series[50] == 1275
    assert series[51] == 1326
    assert series[52] == 1378


# -- SUBTYPE PRESERVATION

def test_head_preserves_series_subtype() -> None:
    series = Series(lambda n: n)
    prefix = series.head(5)
    assert isinstance(prefix, Series)
    assert list(prefix) == [1, 3, 6, 10, 15]


# -- FALLBACK TO PLAIN NUMERIC SEQUENCE

def test_shift_by_returns_numeric_sequence_not_series() -> None:
    series = Series(lambda n: n)
    shifted = series.shift_by(2)
    assert isinstance(shifted, NumericSequence)
    assert not isinstance(shifted, Series)


def test_tail_returns_numeric_sequence_not_series() -> None:
    series = Series(lambda n: n, size=6)
    suffix = series.tail(3)
    assert isinstance(suffix, NumericSequence)
    assert not isinstance(suffix, Series)


def test_subsequence_returns_numeric_sequence_not_series() -> None:
    series = Series(lambda n: n)
    sub = series.subsequence(lambda k: k * 2, size=4)
    assert isinstance(sub, NumericSequence)
    assert not isinstance(sub, Series)


# -- RULE INDEPENDENCE

def test_rule_factory_produces_independent_caches() -> None:
    series = Series(lambda n: n)
    first = series.shift_by(0)
    second = series.shift_by(0)
    assert first._rule is not second._rule
    assert first[20] == second[20]

# -- SPECIAL SERIES

def test_harmonic() -> None:
    seq = Series.harmonic()
    assert list(seq.head(4)) == [1, 1.5, 1 + 1/2 + 1/3, 1 + 1/2 + 1/3 + 1/4]


def test_alternating_harmonic() -> None:
    seq = Series.alternating_harmonic()
    assert list(seq.head(4)) == [1, 0.5, 1 - 1/2 + 1/3, 1 - 1/2 + 1/3 - 1/4]


def test_basel() -> None:
    seq = Series.basel()
    assert list(seq.head(3)) == [1, 1 + 1/4, 1 + 1/4 + 1/9]


def test_leibniz() -> None:
    seq = Series.leibniz()
    assert list(seq.head(3)) == [1, 1 - 1/3, 1 - 1/3 + 1/5]
