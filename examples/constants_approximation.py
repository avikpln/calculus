"""Two classic constants, approached two different ways.

e is easy: its defining sequence converges directly, and there's a
second, purely mechanical way to reach it by summing reciprocal
factorials. Comparing the two is a clean warm-up for the more
interesting story below.

pi is where it gets interesting. There's no single "the formula for
pi" - there's a lineage of them, each one answering the same question
a little better: how many terms before the answer stops embarrassing
you? We walk that lineage from a series needing millions of terms to
one needing only a handful.
"""
import math

from calculus import NumericSequence, NumericRecurrence, Series

# -- Euler's number ----------------------------------------------------

# The direct route: e is defined as the limit of (1 + 1/n)^n, also known
# as Euler's limit.
e_direct = NumericSequence.euler()

# The scenic route: e^1 = sum(1/n!), the Maclaurin series for e^x,
# around x = 0.
# NumericRecurrence.factorial() already knows how to generate n!;
# invert each term and let Series accumulate them. Factorial growth
# outpaces the limit sequence's convergence, which is why this route
# gets there so much faster.
e_series = Series.from_sequence(1 / NumericRecurrence.factorial())

print("e")
print(f"    {'Euler (1000 terms):':<28}{e_direct[1000]}")
print(f"    {'Maclaurin (17 terms):':<28}{e_series[17]}")
print("    " + "-" * 46)
print(f"    {'math.e reference:':<28}{math.e}")
# The series reaches useful precision in under 20 terms; the limit
# definition is still visibly settling even after a thousand.

# -- Pi: a lineage of approximations -----------------------------------

# (1) The Basel problem: sum of 1/n^2 converges to pi^2/6. Beautiful
# result, terrible algorithm - it converges so slowly that reaching
# single-digit accuracy already takes real patience.
basel = Series(lambda n: 1 / n**2)
pi_basel = (6 * basel[1_000_000]) ** 0.5

# (2) Leibniz's formula for pi/4: alternate the sign of 1/(2n+1).
# Elegant, and only marginally faster than Basel in practice.
leibniz = Series(lambda n: (-1)**n / (2*n + 1), first_index=0)
pi_leibniz = 4 * leibniz[100_000]

# (3) Nilakantha's series fixes Leibniz's biggest flaw: instead of
# alternating a single shrinking fraction from scratch, it starts
# from 3 and only needs to correct the remainder.
nilakantha = Series(
    lambda n: (-1)**(n - 1) * 4 / ((2*n) * (2*n + 1) * (2*n + 2)),
    first_index=1,
)
pi_nilakantha = 3 + nilakantha[10_000]

# (4) A StackExchange favorite: ratios of double factorials, scaled by a
# shrinking power of two. Not deep theory, just a sequence someone
# noticed converges fast - see the link below for the derivation.
# https://math.stackexchange.com/questions/14113/series-that-converge-to-pi-quickly
double_factorial = NumericRecurrence.double_factorial()
power_of_half = NumericSequence.geometric(1, 1 / 2, first_index=0)
ratio = (
    double_factorial[::2] / double_factorial[1::2]  # type: ignore[operator]
)
stackexchange_terms = ratio * power_of_half
pi_stackexchange = 2 * Series.from_sequence(stackexchange_terms)[49]

# (5) Chudnovsky's algorithm is where this story ends, though not where
# the search for better approximations does - each additional term buys
# roughly 14 more correct digits. It leans on the same factorial
# recurrence as e above, sliced three different ways.
factorial = NumericRecurrence.factorial()
factorial_3n = factorial[::3]
factorial_6n = factorial[::6]
chudnovsky_coefficients = NumericSequence(
    lambda n: (-1)**n * (545140134*n + 13591409) / 640320**(3*n + 3/2),
    first_index=0,
)
chudnovsky_terms = (
    (factorial_6n * chudnovsky_coefficients)  # type: ignore[operator]
    / (factorial_3n * factorial**3)  # type: ignore[operator]
)
pi_chudnovsky = 1 / (12 * Series.from_sequence(chudnovsky_terms)[2])

print()
print("pi")
print(f"    {'Basel (10^6 terms):':<28}{pi_basel}")
print(f"    {'Leibniz (10^5 terms):':<28}{pi_leibniz}")
print(f"    {'Nilakantha (10^4 terms):':<28}{pi_nilakantha}")
print(f"    {'StackExchange (49 terms):':<28}{pi_stackexchange}")
print(f"    {'Chudnovsky (2 terms):':<28}{pi_chudnovsky}")
print("    " + "-" * 46)
print(f"    {'math.pi reference:':<28}{math.pi}")
