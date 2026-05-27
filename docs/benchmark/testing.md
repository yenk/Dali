# Benchmark Testing

This page records the exact verification steps used to confirm that the public benchmark repository `Dali` runs standalone.

## What was verified

- Direct script execution from the repo root
- Deterministic Tier 1 evaluation
- Unit tests for the public benchmark contract
- Output artifact shape and result stability

## Smoke test run

1. Run the Tier 1 evaluator directly from the repo root:

   ```bash
   python runners/run_integrity.py \
       --corpus data/public/citation_failure_cases.json \
       --output results/demo/integrity.json
   ```

   Observed result:

   - Corpus loaded: 4 total, 3 scoring-eligible, 1 needs-verification
   - Output written successfully
   - 3 result records produced

2. Run the public benchmark test set:

   ```bash
   python -m pytest tests/test_policy.py tests/test_run_integrity.py -q
   ```

   Observed result:

   - `27 passed`

## Notes

- The runner now bootstraps the repo root, so direct execution works without setting `PYTHONPATH`.
- The public benchmark does not require external services, API keys, or production persistence to validate Tier 1.
- The smoke artifact returned a top-level object with these keys:
  - `cross_version_aggregation`
  - `evaluator`
  - `policy_version`
  - `policy_versions_present`
  - `results`
  - `run_timestamp`
  - `summary`
