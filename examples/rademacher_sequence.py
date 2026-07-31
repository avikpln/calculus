"""Infinite Rademacher sequence.

This module extends NumericSequence to represent a sequence of
independent, identically distributed random variables, each taking the
values -1 and +1 with equal probability.

Classes:
    RademacherSequence: A numeric sequence of random +1/-1 values.
"""
from __future__ import annotations

import random

from calculus.sequence import INFINITY, Intfinity, Rule
from calculus.numeric_sequence import NumericSequence, Real
from calculus.utils import validate_callable, validate_int


# ======================================================================
# Rademacher Sequence
# ======================================================================

class RademacherSequence(NumericSequence):
    """A class representing infinite Rademacher sequences.

    This subclass inherits all functionality from NumericSequence. Each
    element is an independent random value of +1 or -1, generated with
    equal probability and recorded the first time its index is queried,
    so that later queries at the same index return the same value.
    """

    class _Rule:
        # Callable Rademacher sequence rule.

        __slots__ = ("rng", "values")

        def __init__(self, rng: random.Random) -> None:
            # Initialize a new Rademacher sequence rule instance.

            self.rng = rng
            self.values: dict[int, Real] = {}

        def __call__(self, n: int) -> Real:
            # Return the random value at index n.

            # Generate and record the value only on its first request.
            if n not in self.values:
                self.values[n] = self.rng.choice((-1, 1))
            return self.values[n]

# -- INITIALIZATION

    __slots__ = ("_random_rule",)

    def __init__(
        self,
        random_rule: _Rule | None = None,
        size: Intfinity = INFINITY,
        *,
        first_index: int = 1,
        seed: int | None = None,
    ) -> None:
        """Initialize a new Rademacher sequence object.

        Args:
            random_rule (Rule[Real] | None): The random rule used by the
                sequence to generate values. Defaults to None.
            size (Intfinity): The size of the sequence. Defaults to
                None, which corresponds to an infinite sequence.
            first_index (int): The first index of the sequence. Defaults
                to 1. A read-only keyword parameter.
            seed (int | None): The seed for the random number generator.
                Defaults to None.

        Raises:
            TypeError: If ``random_rule`` is not callable if ``size`` is
                not None or an integer, if ``seed`` is not None or an
                integer, or if ``first_index`` is not an integer.
            ValueError: If ``size`` is negative, or if ``first_index``
                is not in ``sequence.FIRST_INDEX_OPTIONS``.
        """
        if random_rule is None:
            validate_int(seed, "seed", allow_none=True)
            self._random_rule = self._Rule(random.Random(seed))
        else:
            validate_callable(random_rule)
            self._random_rule = random_rule
        super().__init__(self._random_rule, size=size, first_index=first_index)

# -- FACTORY

    def _rule_factory(self) -> Rule[Real]:
        # Produce the rule for a newly derived sequence.

        return self._random_rule

    def _factory(
        self,
        rule: Rule[Real],
        size: Intfinity,
        reindex: bool,
    ) -> RademacherSequence | NumericSequence:
        # Produce a new sequence from rule and size, considering mode.

        if reindex:
            return super()._factory(rule, size, reindex)
        return RademacherSequence(
            self._random_rule, size=size, first_index=self.first_index
        )


if __name__ == "__main__":
    import math

    # Generate the first 10,000 values of a Rademacher sequence.
    N = 10_000
    sample = RademacherSequence(seed=42).head(N)

    # Estimate the sample mean and standard deviation.
    mu = sum(sample) / N
    sigma = math.sqrt(
        sum((sample - mu) ** 2) / (N - 1)  # type: ignore[operator, arg-type]
    )

    print(f"Sample mean and standard deviation from {N} samples:")
    print(f"    {mu:.4f} ± {sigma:.4f}")
    # 0.0032 ± 1.0000
