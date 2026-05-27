# Architecture

This page describes the public benchmark layers, artifact flow, and the boundary between the benchmark standard and optional extended evaluation.

## Layers

| Layer | Name | Purpose |
|---|---|---|
| **1** | **Canonical Case Corpus** | Court-documented citation failures with deterministic scoring |
| **2** | **Synthetic Probes** | Shipped prompt set plus user-supplied prompt directories for extended evaluation |
| **3** | **Replay Tests** | Private operational capability unless separately released |
| **4** | **Workflow Audits** | Private operational capability unless separately released |

## Public benchmark flow

1. The Tier 1 evaluator loads `data/public/citation_failure_cases.json`.
2. The runner applies the workflow-centric defensibility rubric deterministically.
3. The output is written as a JSON result artifact.
4. Optional reachability checks can be enabled for source validation.
5. Tier 2 prompt runs compare model behavior over the shipped prompt set or a user-supplied JSONL directory.

## Public artifacts

- `results/demo/integrity.json` for local Tier 1 evaluation
- `results/v0.2/{date}/integrity.json` for versioned Tier 1 runs
- `results/v0.2/{date}/synthetic.json` for Tier 2 runs
- `results/v0.2/{date}/methodology.json` for run metadata

## Boundary

The public repo defines the benchmark standard, corpus contract, validation rules, and reproducible local evaluation behavior.

Private implementation details may add archival, replay, persistence, and production verification layers, but those are intentionally outside the public benchmark contract.

## Related docs

- [README.md](../README.md)
- [docs/examples.md](examples.md)
- [docs/benchmark/testing.md](benchmark/testing.md)
- [docs/benchmark/public-review.md](benchmark/public-review.md)
