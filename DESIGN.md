# Design

This document records the current design of each class in the
`calculus` package. Each section is a dry, technical snapshot of what
the class does today — not why it does it. For rationale, rejected
alternatives, and historical context, see `NOTES.md`.

## Sequence

- **Inherits:** N/A (base class).
- **Constructor:** `Sequence(rule=None, size=None, *, first_index=1)`.
- **State:** `_rule`, `_size`, `_first_index`, `_last_index`.
- **first_index:** `0` or `1` (`FIRST_INDEX_OPTIONS`); defaults to `1`.
- **Evaluation:** direct call `self._rule(n)`; no caching.
- **_Rule:** N/A (no nested rule wrapper; `_rule` is a plain callable).
- **_resize:** constructs `Sequence`.
- **_reindex:** constructs `Sequence`.
- **_rule_factory:** returns `self._rule` directly (base case for
  stateless rules).
- **Special constructors:** `constant()`, `from_iterable()`.

## NumericSequence

- **Inherits:** `Sequence[Number]`.
- **Constructor:** none defined; inherits `Sequence.__init__` unchanged.
- **State:** none added.
- **first_index:** inherited from `Sequence`, unchanged.
- **Evaluation:** inherited from `Sequence`, unchanged; arithmetic
  dunders build on `_unary()`/`_binary()`.
- **_Rule:** N/A.
- **_resize:** overridden; constructs `NumericSequence`.
- **_reindex:** overridden; constructs `NumericSequence`.
- **_rule_factory:** inherited from `Sequence`, unchanged.
- **Special constructors:** `constant()`, `from_iterable()`,
  `naturals()`, `progression()`, `geometric()`.

## Recurrence

- **Inherits:** `Sequence[T]`.
- **Constructor:** `Recurrence(func, basis, size=None)`; `first_index`
  is not a parameter, always constructed as `0`.
- **State:** `_func`, `_basis`, `_order`.
- **first_index:** hardcoded to `0`.
- **Evaluation:** `func(n, window)`, where `window` holds the `order`
  preceding terms; computed via `_Rule`.
- **_Rule:** caches a single window of `order` consecutive preceding
  values; advances one step at a time from the cache, or from `basis`
  if no usable cache exists.
- **_resize:** overridden; constructs `Recurrence`.
- **_reindex:** inherited from `Sequence`, unchanged (returns plain
  `Sequence`).
- **_rule_factory:** overridden; returns a fresh `_Rule(func, basis)`.
- **Special constructors:** `von_neumann()`, `look_and_say()`.

## NumericRecurrence

- **Inherits:** `Recurrence[Number]`, `NumericSequence`.
- **Constructor:** none defined; inherits `Recurrence.__init__` (via
  MRO, `Recurrence` listed first).
- **State:** none added.
- **first_index:** inherited from `Recurrence`, hardcoded to `0`.
- **Evaluation:** inherited from `Recurrence`, unchanged.
- **_Rule:** inherited from `Recurrence`, unchanged.
- **_resize:** overridden; constructs `NumericRecurrence`.
- **_reindex:** overridden explicitly to `NumericSequence._reindex`
  (not left to MRO resolution).
- **_rule_factory:** overridden explicitly to
  `Recurrence._rule_factory` (not left to MRO resolution).
- **Special constructors:** `fibonacci()`, `factorial()`,
  `double_factorial()`, `catalan()`.

## Series

- **Inherits:** `NumericSequence`.
- **Constructor:** `Series(term_rule, size=None, *, first_index=1)`.
- **State:** `_term_rule`.
- **first_index:** `0` or `1`; not hard-enforced. Defaults to `1`.
- **Evaluation:** `S(n) = sum(term_rule(k) for k in
  range(first_index, n + 1))`, computed via `_Rule`.
- **_Rule:** caches a single `(n, S(n))` pair — the most recently
  computed partial sum. Resumes from the cache if `n >= cached_n`,
  else restarts from `first_index`.
- **_resize:** overridden; constructs `Series`.
- **_reindex:** overridden explicitly to `NumericSequence._reindex`
  (returns `NumericSequence`, not `Series`).
- **_rule_factory:** overridden; returns a fresh `_Rule` instance
  (independent cache per derived sequence).
- **Special constructors:** `harmonic()`, `alternating_harmonic()`,
  `basel()`, `leibniz()`.
