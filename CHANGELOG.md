# Changelog

## v0.7.0

### Added

- Added comparison operators to `NumericSequence`.
- Added one-based indexing support to `Recurrence`.
- Added a factory for building a `Series` from an existing sequence.
- Added `Fraction` support to the numeric type system.
- Added sequence rule retrieval.
- Added support for negative indexing in slice bounds for zero-indexed finite
  sequences.

### Changed

- Renamed the `Real` numeric type alias from `Number`.
- Restricted `combine()` to same-type operands.

### Removed

- Removed complex number support from `NumericSequence`.

### Fixed

- Fixed type-checking issues when applying arithmetic and slicing to derived
  sequences.
- Fixed reverse slicing of infinite sequences without an explicit stop.

## v0.6.0

### Added

- Added BooleanSequence for boolean-valued sequences.

## v0.5.0

### Added

- Added Series for partial-sum sequences.

## v0.4.0

### Added

- Added NumericRecurrence for recursively defined numeric sequences.

## v0.3.0

### Added

- Added Recurrence for sequences defined by recurrence rules.

## v0.2.0

### Added

- Added NumericSequence with arithmetic operations.

## v0.1.0

### Added

- Added the initial calculus package implementation.
