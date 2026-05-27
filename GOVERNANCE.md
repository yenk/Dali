# Dali Governance

Dali is an open standards project for legal citation integrity infrastructure.
It is governed as a community-driven specification effort modeled on ECMA, IETF,
and the W3C process — not as a typical open-source library.

---

## Project scope

Dali defines:

- **Evidence JSON contracts** — versioned, RFC-style schemas for `EvidenceBundle`,
  `CitationIntegrityResult`, `SemanticSupportResult`, and `ReplayArtifact`.
- **Ontology definitions** — canonical enum values and semantics for
  `AuthorityTreatment`, `PropositionSupport`, `AuthorityType`, and
  `JurisdictionHierarchy`.
- **Reference implementations** — parsers, baseline evaluators, and benchmark
  runners that implement the contracts correctly (not optimally).
- **Benchmark corpus and evaluation methodology** — reproducible accuracy claims
  against a public prompt corpus.

Dali does **not** define:

- Production-grade verification engine internals
- Treatment classifier model weights or training data curation
- Enterprise orchestration, RBAC, multi-tenant infrastructure
- Hosted inference services

The governing principle: **public semantics, private implementation quality.**
Dali defines *what something is*. How to make it work well at scale is left to
implementors.

---

## Decision-making

### Specification changes

Changes to Evidence JSON contracts, ontology enum values, or schema definitions
follow a lightweight RFC process (see [RFC_PROCESS.md](RFC_PROCESS.md)):

1. Open an issue with the `rfc` label describing the problem.
2. Submit a PR adding a draft spec under `specs/`.
3. Two-week public comment period.
4. Maintainer merge after addressing substantive objections.

### Ontology discipline

**Through v3, a new ontology category is added only when an existing category
demonstrably collapses two distinct legal behaviors into the same bucket.**
The default answer to a proposed expansion is *no*. Ontology minimalism is a
first-class design constraint.

### Breaking changes

Evidence JSON contracts use semantic versioning. A `v1.x` change is backwards-
compatible. A `v2` change may break consumers of `v1` and requires a migration
guide and a 90-day deprecation window.

---

## Maintainers

| Name | Role |
|------|------|
| Yen Kha | Founding maintainer |

To propose yourself as a maintainer, open an issue. Maintainer status requires
sustained contribution across at least two released versions.

---

## Relationship to dali-agent

`yenk/dali-agent` is a private repository that contains a production
implementation of the Dali contracts. It consumes `yenk/Dali` schemas and
ontology definitions as a versioned dependency.

The relationship is analogous to:
- OpenTelemetry spec ↔ Datadog agent
- Kubernetes API spec ↔ managed GKE
- MCP protocol ↔ Anthropic's production models

`yenk/Dali` defines the interfaces. `yenk/dali-agent` provides one
implementation. Any other system that emits conformant Evidence JSON is
equally "Dali-compatible."

---

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
