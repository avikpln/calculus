"""Tests for utils.

Run with:
    pytest tests/test_utils.py -v
"""
import pytest

from calculus.utils import validate_callable, validate_int, validate_range

# -- CALLABLE VALIDATION

def test_validate_callable_accepts_callable() -> None:
    validate_callable(lambda n: n)


def test_validate_callable_rejects_non_callable() -> None:
    with pytest.raises(TypeError):
        validate_callable("not callable")


# -- INTEGER VALIDATION

def test_validate_int_accepts_int() -> None:
    validate_int(5)


def test_validate_int_accepts_bool_by_default() -> None:
    validate_int(True)


def test_validate_int_rejects_bool() -> None:
    with pytest.raises(TypeError):
        validate_int(True, allow_bool=False)


def test_validate_int_rejects_none() -> None:
    with pytest.raises(TypeError):
        validate_int(None)


def test_validate_int_accepts_none_when_allowed() -> None:
    validate_int(None, allow_none=True)


def test_validate_int_rejects_noninteger() -> None:
    with pytest.raises(TypeError):
        validate_int("5")  # type: ignore[arg-type]


# -- RANGE VALIDATION

def test_validate_range_accepts_valid_range() -> None:
    validate_range(1, 10, 2)


def test_validate_range_accepts_all_none() -> None:
    validate_range(None, None, None)


def test_validate_range_accepts_bool() -> None:
    validate_range(True, False, True)


def test_validate_range_rejects_noninteger_start() -> None:
    with pytest.raises(TypeError):
        validate_range("1", 10, 2)  # type: ignore[arg-type]


def test_validate_range_rejects_noninteger_stop() -> None:
    with pytest.raises(TypeError):
        validate_range(1, "10", 2)  # type: ignore[arg-type]


def test_validate_range_rejects_noninteger_step() -> None:
    with pytest.raises(TypeError):
        validate_range(1, 10, "2")  # type: ignore[arg-type]


def test_validate_range_rejects_zero_step() -> None:
    with pytest.raises(ValueError):
        validate_range(1, 10, 0)
