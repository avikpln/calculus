"""Common utility functions for validating inputs across the project.

Functions:
    validate_callable: Validate that a value is callable.
    validate_int: Validate integer values, with configurable options.
    validate_range: Validate range arguments.
"""

__all__ = ["validate_callable", "validate_int", "validate_range"]


def validate_callable(value: object) -> None:
    """Validate that a value is callable.

    Args:
        value (object): The value to validate.

    Raises:
        TypeError: If ``value`` is not callable.
    """
    if not callable(value):
        raise TypeError(f"'{type(value).__name__}' object is not callable")


def validate_int(
    value: int | None,
    name: str = "value",
    allow_none: bool = False,
    allow_bool: bool = False,
) -> None:
    """Validate that a value is an integer.

    By default, only integers are accepted. The accepted values can be
    extended to include None or boolean values using the corresponding
    flags.

    Args:
        value (int | None): The value to validate.
        name (str): The variable name for error messages.
        allow_none (bool): Whether None is accepted. Defaults to False.
        allow_bool (bool): Whether boolean values are accepted. Defaults
            to False.

    Raises:
        TypeError: If ``value`` is not of an accepted type.
    """
    if value is None:
        if not allow_none:
            raise TypeError(
                f"'{name}' must be an integer, but got NoneType."
            )
    elif isinstance(value, bool):
        if not allow_bool:
            raise TypeError(
                f"'{name}' must be an integer, but got bool."
            )
    elif not isinstance(value, int):
        raise TypeError(
            f"'{name}' must be an integer, but got {type(value).__name__}."
        )


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
    validate_int(start, "start", allow_none=True, allow_bool=True)
    validate_int(stop, "stop", allow_none=True, allow_bool=True)
    validate_int(step, "step", allow_none=True, allow_bool=True)
    if step is not None and step == 0:
        raise ValueError(f"step ({step}) cannot be zero")
