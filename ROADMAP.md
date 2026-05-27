# Dali Public Roadmap

This roadmap covers the public layer of the Dali standards project.
Private implementation milestones are tracked separately.

---

## Versioning philosophy

Each version ships an **open standard milestone** — a named, versioned artifact
that legal AI systems can implement against. The goal is that other tools can
claim *"Dali-compatible"* by emitting conformant Evidence JSON.

Versions are not product releases. They are specification milestones.

---

## v0 — Benchmark (shipped)

**Status:** Complete

- Citation integrity benchmark with 25+ annotated prompt/citation pairs
- Drift detection engine (weekly re-check of cited sources)
- Existence + support scoring methodology
- Public corpus under `synthetic/` and `data/public/`

---

## v1 — Normalize (Q3 2026)

**Status:** In progress

**Public deliverables:**
- eyecite integration as the parser of record
- Evidence JSON v1.0 RFC (`specs/evidence-json-v1.md`) — versioned contracts
  for `EvidenceBundle`, `CitationIntegrityResult`, future `SemanticSupportResult`
  and `ReplayArtifact`
- Canonical citation schema (`schemas/canonical-citation.schema.json`)
- Corpus expanded to 150+ prompts (US federal + UK/Commonwealth + Brazil +
  adversarial)
- Stanford CodeX + Harvard CAP partnership program launched

**Milestone framing:** *"Citation integrity has a normalization standard."*

---

## v2 — Connect (Q4 2026 – Q1 2027)

**Status:** Planned

**Public deliverables:**
- Citation relationship graph schema
- Jurisdiction hierarchy definitions
- **Treatment ontology v1** — 3 categories only:
  `cited_approvingly` | `contradicted` | `neutral_reference`
- Treatment classifier training dataset (open data, CC-licensed)
- Treatment classifier evaluation methodology + benchmark results

**Milestone framing:** *"First open legal citation graph + treatment dataset
outside Westlaw."*

Note: Model weights and production classifier remain in the private implementation.
The open dataset + open ontology + open evaluation methodology is the public
deliverable. See `specs/authority-treatment-v1.md` (forthcoming).

---

## v3a — Verify, narrow scope (Q2–Q3 2027)

**Status:** Planned

**Public deliverables:**
- Proposition extraction schema (3 classes):
  `supported` | `partially_supported` | `not_supported`
- Pinpoint validation contract
- Evidence JSON v2.0 with `SemanticSupportResult` defined

**Scope:** US federal courts + litigation memos only.

**Milestone framing:** *"The evidentiary integrity layer for legal AI."*

---

## v3b — Verify, continuous refinement (Q4 2027 – ongoing)

**Status:** Research track, no fixed end date

Multi-hop citations, statutory interplay, cross-authority synthesis, temporal
semantic validity. Each refinement produces a measurable accuracy improvement
on the public benchmark.

---

## v4 — Temporalize (Q1 2028)

**Status:** Planned

- Temporal snapshot schema
- Law-versioning standard
- `state-as-of` query contract

---

## v5 — Globalize (2028 H2)

**Status:** Planned

**Jurisdictions:** US + UK/Commonwealth + Brazil. EU deferred until v3
semantic verification is hardened on common + civil law.

- Cross-jurisdiction adapter SDK
- AGLC / BlueBook unifier
- Portuguese-language ontology stubs for Brazilian civil law

---

## v6 — Platform (early 2029)

**Status:** Planned

- Verification API specification (open)
- Audit replay RFC (open)
- Evidence bundle format v3

---

## What is not on this roadmap

- Hosted inference (private implementation decision)
- Enterprise RBAC, SSO, multi-tenant (private)
- Treatment classifier weights (private — see v2 notes)
- Any feature gated on a commercial arrangement
