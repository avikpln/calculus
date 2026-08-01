"""Infinite power series.

Given a NumericSequence of coefficients c_0, c_1, c_2, ..., a power
series evaluates sum(c_n * x^n) at a given x, returning the result as an
infinite Series of partial sums.

Classes:
    PowerSeries: A power series defined by an infinite sequence of
        coefficients.
"""
from __future__ import annotations

from calculus import NumericSequence, Series
from calculus.numeric_sequence import Real

# ======================================================================
# Power Series
# ======================================================================

class PowerSeries:
    """A class representing a power series."""

# -- INITIALIZATION

    __slots__ = ("_coefficients",)

    def __init__(self, coefficients: NumericSequence) -> None:
        """Initialize a new power series object.

        Args:
            coefficients (NumericSequence): The coefficients of the
                power series, with coefficients[n] as the coefficient
                of x^n.

        Raises:
            TypeError: If ``coefficients`` is not a NumericSequence.
            ValueError: If ``coefficients``'s first_index is not 0.
        """
        if not isinstance(coefficients, NumericSequence):
            raise TypeError(
                "coefficients must be a NumericSequence object, "
                f"not {type(coefficients).__name__}"
            )
        if coefficients.first_index != 0:
            raise ValueError(
                "coefficients must have first_index=0, "
                f"got first_index={coefficients.first_index} instead"
            )
        self._coefficients = coefficients

    def __call__(self, x: Real) -> Series:
        """Evaluate the power series at x.

        Args:
            x (Real): The value at which to evaluate the power series.

        Returns:
            Series: The series of partial sums of the power series,
                evaluated at x.
        """
        coefficients = self._coefficients
        powers = NumericSequence.geometric(
            1.0, x, size=coefficients.size, first_index=0
        )
        return Series.from_sequence(coefficients * powers)


if __name__ == "__main__":
    # Create the power series representing 1/(1+x). For this series, the
    # coefficients are: 1, -1, 1, -1, ...
    alternating_series = PowerSeries(
        NumericSequence(lambda n: 1 if n % 2 == 0 else -1, first_index=0)
    )

    # Approximate 2.0 = 1/(1+(-0.5)).
    print("2.0 ≈ ", end="")
    print(alternating_series(-0.5))
    # 2.0 ≈ ⟨1.0, 1.5, 1.75, 1.875, 1.9375, ...⟩
