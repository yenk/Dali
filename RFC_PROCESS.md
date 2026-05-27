# RFC Process

This document describes how specification changes to Evidence JSON contracts,
ontology definitions, and schema primitives are proposed, reviewed, and ratified.

---

## When an RFC is required

An RFC is required for any change that:

- Adds, removes, or renames a field in an Evidence JSON contract
- Adds, removes, or renames an ontology enum value
- Changes the semantics of an existing field or value
- Introduces a new top-level schema or contract

Bug fixes, clarifications, and non-normative documentation changes do not
require an RFC. Open a regular PR for those.

---

## RFC lifecycle

```
DRAFT → COMMENT → ACCEPTED | WITHDRAWN
```

| Status | Meaning |
|--------|---------|
| `DRAFT` | Author is still working on the proposal |
| `COMMENT` | Open for public review (14-day minimum) |
| `ACCEPTED` | Merged into the spec; implementation may begin |
| `WITHDRAWN` | Author or maintainer closed the proposal |

---

## How to submit an RFC

1. **Open an issue** with the label `rfc` describing the problem the RFC solves.
   Include the motivation — why does the current spec fail to cover this?

2. **Create a branch** named `rfc/<short-title>` (e.g. `rfc/treatment-enum-v2`).

3. **Add a spec file** at `specs/<rfc-number>-<short-title>.md` using the
   template below. Number RFCs sequentially starting from the next available
   integer (check `specs/` for the current highest).

4. **Open a PR** against `main`. Add the `rfc` label. The PR description should
   link to the issue.

5. **Comment period begins** when the PR is marked `COMMENT` by a maintainer.
   The minimum comment period is 14 days. Controversial changes may be extended.

6. **Address objections.** Substantive objections must be addressed or explicitly
   rejected with reasoning before merge.

7. **Merge** — a maintainer merges the PR and updates the status to `ACCEPTED`.

---

## RFC template

```markdown
# RFC-NNN: Title

**Status:** DRAFT | COMMENT | ACCEPTED | WITHDRAWN
**Created:** YYYY-MM-DD
**Author:** Name

## Problem

What current gap or deficiency does this RFC address?

## Proposal

Precise description of the change. For schema changes, include before/after JSON.
For ontology changes, include enum values + normative definitions.

## Motivation

Why this change rather than alternatives?

## Alternatives considered

What other approaches were evaluated and why were they rejected?

## Backwards compatibility

Is this a breaking change? If so, what is the migration path?

## Open questions

List any unresolved issues explicitly.
```

---

## Ontology minimalism rule

For any RFC proposing a new ontology category (treatment type, proposition class,
authority type, jurisdiction abstraction):

> **An existing category must demonstrably collapse two distinct legal behaviors
> into the same bucket before a new one is added.**

The default answer to an expansion proposal is *no*. This rule is enforced
through v3. Reviewers should apply it actively.

---

## Versioning

Accepted RFCs that affect schemas or contracts increment the version according
to semantic versioning:

- **Patch** (x.y.Z) — clarification only, no behavioral change
- **Minor** (x.Y.0) — backwards-compatible addition
- **Major** (X.0.0) — breaking change; 90-day deprecation window required
