"""Integral approximation.

This module demonstrates approximating a definite integral as a
NumericSequence of increasingly refined estimates, using Simpson's
rule.

Classes:
    Integral: An integral approximation of a function over an interval.
"""
from __future__ import annotations

from collections.abc import Callable

from calculus import NumericSequence
from calculus.numeric_sequence import Number
from calculus.utils import validate_callable

#=======================================================================
# Integral
#=======================================================================

class Integral:
    """A class for approximating integrals."""

# -- INITIALIZATION

    __slots__ = ("_integrand",)

    def __init__(self, integrand: Callable[[Number], Number]) -> None:
        """Initialize a new integral object.

        Args:
            integrand (Callable[[Number], Number]): The function to
                integrate.

        Raises:
            TypeError: If ``integrand`` is not callable.
        """
        validate_callable(integrand)
        self._integrand = integrand

    def integrate(self, lower: Number, upper: Number) -> NumericSequence:
        """Return a sequence of Simpson's rule integral approximations.

        Args:
            lower (Number): The lower endpoint of the integration
                interval.
            upper (Number): The upper endpoint of the integration
                interval.

        Returns:
            NumericSequence: The sequence of integral approximations.

        Raises:
            TypeError: If ``lower`` or ``upper`` is not a Number.
            ValueError: If ``lower`` is greater than ``upper``.
        """
        if not isinstance(lower, Number) or isinstance(lower, bool):
            raise TypeError(
                f"'lower' must be a Number, but got {type(lower).__name__}."
            )
        if not isinstance(upper, Number) or isinstance(upper, bool):
            raise TypeError(
                f"'upper' must be a Number, but got {type(upper).__name__}."
            )
        if lower > upper:
            raise ValueError(
                f"'lower' ({lower}) cannot exceed 'upper' ({upper})."
            )
        if lower == upper:
            return NumericSequence.constant(0.0, first_index=1)
        return self._simpson(self._integrand, lower, upper)

    @staticmethod
    def _simpson(
        f: Callable[[Number], Number],
        a: Number,
        b: Number,
    ) -> NumericSequence:
        # Return a sequence of Simpson's rule integral approximations.

        # Simpson's rule.
        simpson_rule = lambda n: ((b - a) / (6 * n)) * (
            f(a) + f(b)
            + 4 * sum(
                f(a + (2*i + 1) * (b - a) / (2 * n))
                for i in range(n)
            )
            + 2 * sum(
                f(a + 2*i * (b - a) / (2 * n))
                for i in range(1, n)
            )
        )

        return NumericSequence(simpson_rule, first_index=1)

if __name__ == "__main__":
    import math

    # Create an integral for f(x) = sin(x).
    integral = Integral(math.sin)

    # Approximate the integral of sin(x) from 0 to π.
    approximations = integral.integrate(0, math.pi)

    print("∫₀^π sin(x) dx ≈ ", end="")
    print(approximations.map(lambda x: round(x, 4)))
    # ∫₀^π sin(x) dx ≈ ⟨2.0944, 2.0046, 2.0009, 2.0003, 2.0001, ...⟩
