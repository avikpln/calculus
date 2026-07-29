# Style Guide

## Philosophy

This project follows standard Python conventions wherever practical. Departures
from common practice are intentional, documented, and made only when they
improve readability, maintainability, or better express the mathematical model
of the library.

## General

### Line length

- Python code: wrap at 79 characters (PEP 8).
- Python docstrings: wrap at 72 characters (PEP 257; see Docstring
  Conventions).
- Everywhere else with no more specific rule stated (e.g. Markdown
  files, PR descriptions): wrap at 79 characters.
- Fill the space: avoid wrapping lines prematurely.

## Git

**<u>Caution!</u>** These conventions diverge from Conventional Commits and
similar industry formats; do not apply those instead.

### Commit messages

- Subject: imperative mood, answering *what* changed (e.g. "Add", "Fix",
  "Refactor", "Remove"). Capitalized, no trailing period, 50 characters or
  fewer.

- Leave exactly one blank line between the subject and the body.

- Body: present tense (not imperative). Adds detail beyond the subject, such as
  why the change was made or how it was done. Wrap at 72 characters.

- Scale the body's length to the size and impact of the change. Include a body
  for complex changes, breaking updates, architectural shifts, or anything
  where the context isn't obvious from the diff. Omit it for small,
  self-explanatory changes (typo fixes, formatting tweaks, etc.).

### Branch naming

- Flat structure only — no folder-style prefixes (`feature/`, `bugfix/`,
  developer names, etc.).

- Lowercase kebab-case (e.g. `fix-login-button-padding`).

## Markdown

- Wrap at 79 characters.

- `##` sections use title case; `###` subsections use sentence case (capitalize
  only the first word).

- Uses a flat `##`/`###` structure.

- `---` separators are 79 characters long and appear between sibling `###`
  entries only, not before `##` headings. README.md intentionally does not
  follow this convention.

**<u>Architecture diagrams</u>**

- Specify only public instance attributes and methods;
- Order members alphabetically unless grouping them has a meaningful structural
  or conceptual purpose.

## Python

The project follows PEP 8 and PEP 257 with the conventions below.

**<u>Caution!</u>** PEP 8 takes priority over general industry convention and
linter defaults (e.g. Black, Flake8) wherever they conflict.

### Docstring Conventions

- Summary line: exactly one line, on the same line as the opening """.

- Maximum line length: 72 characters (except doctests, URLs, and output).

- For function and method docstrings, non-empty sections appear in the
  following order:

        Args:
        Returns:
        Raises:
        Notes:
        Examples:

- For class docstrings, non-empty sections appear in the following order:

        Attributes:
        Methods:
        Notes:
        Examples:

- Parameters use the form:

        name (type): Description.

- Docstrings explain *what*; implementation comments explain *why*.

- Private methods (leading underscore) use block comments beneath the function
  signature instead of docstrings.

- `Raises:` documents only exceptions that the function itself can propagate
  through its own parameters. Delegating methods should not reproduce a
  constructor's complete exception contract.

**<u>Modules</u>**

Module docstrings should contain:

- a one-line summary;
- a brief description when appropriate;
- a list of exported public classes, functions, and other objects;
- no documentation of private implementation details.

**<u>Classes</u>**

- summarize the class;
- document public attributes;
- document public methods;
- document subclass interfaces separately, when applicable.

Constructors are documented in `__init__()`, not in the class docstring.

**<u>Functions and methods</u>**

Public functions and methods should document:

- purpose;
- arguments;
- return value;
- exceptions they may propagate from their own parameters;
- restrictions or preconditions;
- keyword-only parameters, when applicable.

**<u>Inheritance</u>**

When subclassing:

- use *override* when replacing inherited behavior without calling the
  superclass implementation;
- use *extend* when calling the superclass implementation in addition to new
  behavior;
- summarize only the behavioral differences from the parent class.

-------------------------------------------------------------------------------

### Type Hints

- The project targets `mypy --strict`.
- Type ignores should be localized and documented.
- Public APIs should be fully type annotated.

-------------------------------------------------------------------------------

### Validation

- Constructors eagerly validate values that establish object invariants.

- Transformation methods generally rely on lazy validation and EAFP semantics
  unless eager validation protects a core invariant.

- `assert False` may be used to mark a branch that is structurally unreachable
  once callers have validated their inputs (e.g. an `else` clause following
  exhaustive `if`/`elif` conditions). This is distinct from an `assert` used
  purely to narrow a type for `mypy`, which should be marked with a trailing
  `# mypy` comment instead.

- Validation ownership belongs to the public API, not to private methods. A
  private method may still raise an exception where doing so is the natural
  implementation of a public caller's documented behavior (not independent
  argument validation) — this is acceptable as long as all current callers of
  that private method agree on what it should reject. If callers genuinely
  diverge, the check moves out to each public caller instead.

-------------------------------------------------------------------------------

### Comments

- Explain why, not what.
- Avoid comments that merely restate the code.
- Prefer concise comments close to the code they explain.

-------------------------------------------------------------------------------

### Naming

- Public APIs should use descriptive names.
- Private helpers should begin with an underscore.
- Module-level constants use UPPER_CASE.

-------------------------------------------------------------------------------

### Imports

- Avoid speculative imports.
- Introduce imports only when required by implemented functionality.
- Keep static analysis free of unused imports and symbols.
- An import that does not fit on one line is wrapped in
  parentheses, with one imported name per line.

-------------------------------------------------------------------------------

### Line-Wrapping

- The guiding rule is *all-or-none*: if a construct fits entirely on one line
  within the line-length limit, it stays on one line. If it does not fit, every
  element gets its own line — never a partial grouping aligned to the opening
  delimiter.

- Whenever a construct is wrapped across multiple lines, the last element (or
  group of elements) gets a trailing comma before the closing delimiter.

- These conventions apply to library source files. Test files are not held to
  them; prioritize readability of test setup and assertions over strict
  formatting.

- A list/tuple/dict literal that does not fit on one line places one element
  per line.

**<u>Conditional expressions</u>**

- An `if` condition that does not fit on one line follows the same all-or-none
  rule as other constructs: if it does not fit on one line, each
  condition/operand gets its own line, with the closing parenthesis and colon
  on their own line at the statement's base indentation.

**<u>Class declarations</u>**

- A class declaration that does not fit on one line places each base class on
  its own line, with the opening parenthesis on the `class` line and the
  closing parenthesis and colon on their own line.

**<u>Function and method definitions</u>**

- A definition that does not fit on one line places every parameter on its own
  line. Nothing follows the opening parenthesis; the closing parenthesis and
  return-type annotation share a line at the method's base indentation.

- The bare `*` marking the start of keyword-only parameters gets its own line
  rather than sharing one with an adjacent parameter.

**<u>Function calls</u>**

- A call that does not fit on one line, but whose full argument list fits on a
  single indented continuation line, is written with the arguments grouped
  together on that one line:

        func(
            a, b, c,
        )

- If the argument list does not fit even this way, it falls back to one
  argument per line, matching the convention for definitions.

**<u>Exemption: multi-line string concatenation</u>:** Implicit string
concatenation spanning multiple lines (for example, a multi-part message inside
a `raise` statement) is not a sequence of discrete arguments and is exempt from
the rules above. Wrap for readability at your own discretion.

-------------------------------------------------------------------------------

### Arithmetic operators

- Binary operators are spaced on both sides by default (e.g. `a + b`,
  `a ** b`).
- When operators of different priority are mixed in the same expression,
  tighten the higher-priority operator and space the lower-priority one (e.g.
  `a*b + c*d`, `(-1)**n * n`).
- `**` follows the same rule as any other operator: spaced when standalone,
  tightened only when mixed with a lower-priority operator in the same
  expression.
