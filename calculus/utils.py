"""Common utility functions for validating inputs across the project.

Functions:
    validate_int: Validate that a value is an int and not a boolean.
    validate_optional_int: Validate int or None, rejecting booleans.
"""

__all__ = ["validate_int", "validate_optional_int", "validate_range"]


def validate_int(value: int, name: str = "value") -> None:
    """Validate that a value is an integer and not a boolean.

    Args:
        value (int): The value to validate.
        name (str): The variable name for error messages.

    Raises:
        TypeError: If ``value`` is a bool or not an instance of int.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"'{name}' must be an integer, but got {type(value).__name__}."
        )


def validate_optional_int(value: int | None, name: str = "value") -> None:
    """Validate that a value is an integer or None, rejecting booleans.

    If not None, it delegates to validate_int for strict checking.

    Args:
        value (int | None): The value to check.
        name (str): The variable name for error messages.

    Raises:
        TypeError: If ``value`` is neither None nor a valid integer.
    """
    if value is not None:
        validate_int(value, name=name)


def validate_range(
    start: int | None,
    stop: int | None,
    step: int | None
) -> None:
    """Validate that start, stop, and step form a valid range.

    Args:
        start (int | None): The start of the range.
        stop (int | None): The end of the range.
        step (int | None): The step of the range.

    Raises:
        TypeError: If ``start``, ``stop``, or ``step`` is not an
            integer or None.
        ValueError: If ``step`` is zero.
    """
    validate_optional_int(start, "start")
    validate_optional_int(stop, "stop")
    validate_optional_int(step, "step")
    if step is not None and step == 0:
        raise ValueError(f"step ({step}) cannot be zero")
