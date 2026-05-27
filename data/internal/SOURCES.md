# Canonical Case Corpus — Sources & Curation Provenance

This document records where each record in `citation_failure_cases.json` came from, when it was retrieved, and what verification still needs to be done.

## Curation policy

- Every scoring-eligible record requires a verifiable `source_url`.
- Records lacking a verifiable URL are flagged `needs_verification: true` and are excluded from scoring aggregates by `corpus/validator.py`.
- Records are seeded primarily from **Damien Charlotin's AI Hallucination Cases database** ([damiencharlotin.com/hallucinations](https://www.damiencharlotin.com/hallucinations/)), supplemented by hand-curated additions of high-profile incidents where the public court record is well-documented.

## Records — provenance log

### mata-v-avianca-2023

- **Source type:** sanctions order
- **Curation source:** hand-curated
- **Retrieval date:** 2026-05-25
- **Primary source URL:** CourtListener docket — Mata v. Avianca, Inc., No. 22-cv-1461 (S.D.N.Y.)
- **Verification status:** annotation_confidence = `high`. The case is one of the most widely documented AI-citation sanctions in U.S. legal history; facts cross-referenced against multiple sanctions-order excerpts and contemporaneous news reporting.
- **Outstanding verification:** `source_document_hash` is null pending an archival run of the sanctions order PDF through the public benchmark snapshot flow.

### us-v-cohen-2023

- **Source type:** judicial opinion + reported coverage of the citation incident
- **Curation source:** hand-curated
- **Retrieval date:** 2026-05-25
- **Primary source URL:** CourtListener docket — United States v. Cohen, S.D.N.Y.
- **Verification status:** annotation_confidence = `high` for the workflow-attribution facts (client-supplied AI citations, counsel filed without verification). Exact list of fabricated citations is not reproduced here pending verification against the underlying court orders.
- **Outstanding verification:** Need to confirm exact docket number for the supervised-release motion; `source_document_hash` not yet populated.

### park-v-kim-2024

- **Source type:** published Second Circuit opinion
- **Curation source:** hand-curated
- **Retrieval date:** 2026-05-25
- **Primary source URL:** CourtListener — Park v. Kim (2d Cir. 2024)
- **Verification status:** annotation_confidence = `medium`. The general fact pattern (AI-generated nonexistent citations in an appellate brief, referral to Grievance Panel) is documented in public commentary; specific fabricated case names and exact procedural posture need confirmation against the published opinion.
- **Outstanding verification:** Marked `needs_verification: true`. Until the published opinion is read end-to-end and quoted, this record is loadable for inspection but **does not count toward scoring aggregates**.

### mata-derivative-reporter-swap-001

- **Source type:** synthetic Tier-2 probe derived from `mata-v-avianca-2023`
- **Curation source:** hand-curated
- **Retrieval date:** 2026-05-25
- **Provenance:** Internal probe constructed by altering the reporter of the Mata-fabricated citation (F.3d → F.2d). Documented in this corpus to demonstrate that Tier-2 synthetic probes can carry full lineage attribution back to a Tier-1 canonical case.
- **Verification status:** annotation_confidence = `high` (it is a deliberate, documented mutation).
- **Outstanding verification:** None — by construction.

## Expansion plan

The v0.2 ship targets 4–6 high-confidence records. v0.3 expands to 15–25 records pulled programmatically from the Charlotin database (with retrieval dates recorded per-record), plus any hand-additions deemed materially important to the corpus narrative.

## Attribution

If the Charlotin database is used as a primary curation source for v0.3+, the README and METHODOLOGY documents must:

1. Cite the database by URL with retrieval date
2. Note that curation provenance is per-record (`curation_source: "charlotin_db"`)
3. Offer reciprocal credit if Charlotin requests it
