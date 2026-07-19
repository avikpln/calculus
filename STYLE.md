# Style Guide

## Philosophy

This project follows standard Python conventions wherever practical.
Departures from common practice are intentional, documented, and made
only when they improve readability, maintainability, or better express
the mathematical model of the library.

## Documentation

The project follows PEP 257 with the conventions below.

### Modules

Module docstrings should contain:

-   a one-line summary;
-   a brief description when appropriate;
-   a list of exported public classes, functions, and other objects;
-   no documentation of private implementation details.

------------------------------------------------------------------------

### Classes

Class docstrings should:

-   summarize the class;
-   document public attributes;
-   document public methods;
-   document subclass interfaces separately, when applicable.

Constructors are documented in `__init__()`, not in the class docstring.

------------------------------------------------------------------------

### Functions and methods

Public functions and methods should document:

-   purpose;
-   arguments;
-   return value;
-   exceptions they may propagate from their own parameters;
-   restrictions or preconditions;
-   keyword-only parameters, when applicable.

------------------------------------------------------------------------

### Inheritance

When subclassing:

-   use *override* when replacing inherited behavior without calling the
    superclass implementation;
-   use *extend* when calling the superclass implementation in addition
    to new behavior;
-   summarize only the behavioral differences from the parent class.

## Docstring conventions

-   Summary line: exactly one line, appearing on the same line as the
	opening """

-   Maximum line length: 72 characters (except doctests, URLs, and
    unavoidable output).

-   Sections appear, when applicable, in the following order:

        Args:
        Returns:
        Raises:
        Attributes:
        Methods:
        Notes:
        Examples:

-   Parameters use the form:

        name (type): Description.

-   Docstrings explain *what*; implementation comments explain *why*.

-   Private methods (leading underscore) use block comments beneath the
    function signature instead of docstrings.

-   `Raises:` documents only exceptions that the function itself can
    propagate through its own parameters. Delegating methods should not
    reproduce a constructor's complete exception contract.

## Type hints

-   The project targets `mypy --strict`.
-   Type ignores should be localized and documented.
-   Public APIs should be fully type annotated.

## Validation

-   Constructors eagerly validate values that establish object
    invariants.

-   Transformation methods generally rely on lazy validation and EAFP
    semantics unless eager validation protects a core invariant.

-   `assert False` may be used to mark a branch that is structurally
    unreachable once callers have validated their inputs (e.g. an
    `else` clause following exhaustive `if`/`elif` conditions). This
    is distinct from an `assert` used purely to narrow a type for
    `mypy`, which should be marked with a trailing `# mypy` comment
    instead.

-   Validation ownership belongs to the public API, not to private
    methods. A private method may still raise an exception where
    doing so is the natural implementation of a public caller's
    documented behavior (not independent argument validation) — this
    is acceptable as long as all current callers of that private
    method agree on what it should reject. If callers genuinely
    diverge, the check moves out to each public caller instead.

## Comments

-   Explain why, not what.
-   Avoid comments that merely restate the code.
-   Prefer concise comments close to the code they explain.

## Naming

-   Public APIs should use descriptive names.
-   Private helpers should begin with an underscore.
-   Module-level constants use UPPER_CASE.

## Line-wrapping

The guiding rule is *all-or-none*: if a construct fits entirely on
one line within the line-length limit, it stays on one line. If it
does not fit, every element gets its own line — never a partial
grouping aligned to the opening delimiter.

### General

-   Whenever a construct is wrapped across multiple lines, the
    last element (or group of elements) gets a trailing comma
    before the closing delimiter.

-   These conventions apply to library source files. Test files
    are not held to them; prioritize readability of test setup and
    assertions over strict formatting.

------------------------------------------------------------------------

### Class declarations

-   A class declaration that does not fit on one line places each
    base class on its own line, with the opening parenthesis on
    the `class` line and the closing parenthesis and colon on
    their own line.

------------------------------------------------------------------------

### Function and method definitions

-   A definition that does not fit on one line places every
    parameter on its own line. Nothing follows the opening
    parenthesis; the closing parenthesis and return-type
    annotation share a line at the method's base indentation.

-   The bare `*` marking the start of keyword-only parameters gets
    its own line rather than sharing one with an adjacent
    parameter.

------------------------------------------------------------------------

### Function calls

-   A call that does not fit on one line, but whose full argument
    list fits on a single indented continuation line, is written
    with the arguments grouped together on that one line:

        func(
            a, b, c,
        )

-   If the argument list does not fit even this way, it falls back
    to one argument per line, matching the convention for
    definitions.

------------------------------------------------------------------------

### Imports

-   An import that does not fit on one line is wrapped in
    parentheses, with one imported name per line.

------------------------------------------------------------------------

### `__all__` and other list literals

-   A list literal that does not fit on one line places one
    element per line.

------------------------------------------------------------------------

### Exemption: multi-line string concatenation

-   Implicit string concatenation spanning multiple lines (for
    example, a multi-part message inside a `raise` statement) is
    not a sequence of discrete arguments and is exempt from the
    rules above. Wrap for readability at your own discretion.

## Imports

-   Avoid speculative imports.
-   Introduce imports only when required by implemented functionality.
-   Keep static analysis free of unused imports and symbols.

## Arithmetic operators

-   Binary operators are spaced on both sides by default (e.g. `a + b`,
    `a ** b`).
-   When operators of different priority are mixed in the same
    expression, tighten the higher-priority operator and space the
    lower-priority one (e.g. `a*b + c*d`, `(-1)**n * n`).
-   `**` follows the same rule as any other operator: spaced when
    standalone, tightened only when mixed with a lower-priority
    operator in the same expression.

## Testing and quality

Before every commit, run:

1.  `mypy --strict`
2.  `pyflakes`
3.  `pydocstyle`
4.  `pytest`
5.  `git diff --cached --check` (trailing whitespace, staged changes)

All checks should pass before committing.

This same sequence is automated by the project's CI workflow, which
uses the empty-tree hash to check every file in the repository rather
than just staged changes.
