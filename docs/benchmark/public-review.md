# Public Benchmark Review

This note summarizes the current public benchmark surface in a way that stays limited to the benchmark contract, reproducibility, and known methodological constraints.

## Why this is not just another citation checker

Dali is not only checking whether a citation exists. It is evaluating whether the AI-assisted workflow that produced the citation remains reconstructable, attributable, and defensible after the fact. That is the difference between citation checking and provenance infrastructure.

## What is strong

- The benchmark scope is well bounded.
- The separation between citation existence and claim support is correct.
- The corpus is replayable and versioned.
- The repository makes its limitations explicit instead of overstating conclusions.
- The prompt set is designed to be neutral rather than model-leading.

## What should stay bounded in interpretation

- The current corpus is small enough that results should be treated as exploratory rather than population-level.
- Support scoring should be interpreted with care when the scorer and subject model families overlap.
- Aggregate claims should stay tied to the current corpus size and versioned methodology.

## What could be improved in later versions

- Expand the corpus before making broader statistical claims.
- Add clearer confidence reporting around aggregate summaries.
- Keep the benchmark runner reproducible from the repository root.
- Keep any optional enrichment or archival mechanisms separate from the public contract.

## What should remain in scope for the public repo

- Corpus schemas
- Taxonomy and policy versioning
- Deterministic local evaluation
- Validation and anonymization
- Public methodology and testing notes
- Synthetic probes that are part of the benchmark standard

## What should remain out of scope for the public repo

- Implementation details that are outside the public benchmark contract
- Operational infrastructure fingerprints
- Exact hosted model selection details beyond what is needed to reproduce the benchmark
- Persistence or replay orchestration semantics outside the public benchmark contract

## Bottom line

The current benchmark is a credible, well-scoped public standard. Its main limitation is not design quality but sample size and the need to keep claims tightly aligned to what the corpus can actually support.
