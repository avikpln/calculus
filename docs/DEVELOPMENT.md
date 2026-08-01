# Development Guide

## Local Verification

Before every commit, run `scripts\verify.bat`.

This same sequence is automated by the project's CI workflow, which uses the
empty-tree hash to check every file in the repository rather than just staged
changes.

## Tagging Strategy

Tags mark major feature milestones, e.g. a new module landing.

Starting from `v0.5.0`, tags are annotated with a real message
(`git tag -a vX.Y.Z -m "..."`), rather than lightweight. Existing tags
(`v0.0.0`–`v0.4.0`) are not retroactively rewritten to add messages, since
force-replacing a published tag changes its identity and can conflict with
anyone who already fetched it.

## Code Cleanliness

Avoid speculative imports, constants, and infrastructure.

Unused code should be introduced only when a concrete feature requires it,
keeping static analysis clean and reducing maintenance overhead.

## Feature Implementation Protocol

To keep development consistent and incremental, each feature should be
implemented using the following workflow:

1. **Implement:**
   - Implement the feature.
   - Keep the implementation focused on the current feature only.

2. **Document:**
   - Add or update method docstrings.
   - Update the class docstring if the public API has changed.
   - Update the module docstring if appropriate.

3. **Test:**
   - Add or update the relevant tests.
   - Ensure the test suite reflects only the public API.

4. **Publish:**
   - Update `README.md` to document the new feature.
   - Add or update usage examples where appropriate.

5. **Record:** *(only if warranted)*
   - Update `ARCHITECTURE.md` when the high-level class hierarchy changes.
   - Update `DESIGN.md` when core abstractions or the conceptual model change.
   - Record important design decisions or rationale in `NOTES.md`.
   - Avoid documenting routine implementation details.

**IMPORTANT!** Run the project's verification tools **before committing**. Only
commit once all checks pass.

## Checklist for Adding a New Verification Tool

- Add the tool to `requirements-dev.txt`.

- Add the verification step to CI (`.github/workflows/ci.yml`).

- Add a local verification step to `scripts/verify.bat`.

- Update `README.md`:
  - Development section: update the verification steps.
  - Dependencies section: update the requirements list.
  - Project Layout section: add any new configuration files.

- Update the Local Verification section in `docs/DEVELOPMENT.md`.

- Remove the corresponding `TODO.md` entry if the verification task was
  tracked as planned work.
