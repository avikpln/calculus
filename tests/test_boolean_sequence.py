"""Tests for BooleanSequence.

Run with:
    pytest tests/test_boolean_sequence.py -v
"""
from calculus.boolean_sequence import BooleanSequence

# -- TYPING

def test_head_preserves_boolean_subtype() -> None:
    seq = BooleanSequence(lambda n: n % 2 == 0, size=4, first_index=0)
    result = seq.head(2)
    assert isinstance(result, BooleanSequence)
    assert list(result) == [True, False]
