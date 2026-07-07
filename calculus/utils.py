"""Common utility functions for validating inputs across the project.

Functions:
    validate_int: Validate that a value is an int and not a boolean.
    validate_optional_int: Validate int or None, rejecting booleans.
"""

__all__ = ['validate_int', 'validate_optional_int']


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
