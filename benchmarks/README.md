# benchmarks/

Benchmark assets for Dali, organized by evaluation tier.

```
benchmarks/
  tier1/    Canonical court-documented citation failure cases (deterministic ground truth)
  tier2/    Synthetic probe prompts for live model evaluation
```

## Tiers at a glance

| Tier | Contents | Runner | API keys needed |
|---|---|---|---|
| **Tier 1** | `tier1/corpus/citation_failure_cases.json` | `runners/run_integrity.py` | No |
| **Tier 2** | `tier2/{legal,research,adversarial}/` | `runners/run_synthetic.py` | Yes |

Tier 1 is the evidentiary standard. Tier 2 extends evaluation to live model behavior.

## Quick start

```bash
# Tier 1 — no network, no API key:
python runners/run_integrity.py \
  --corpus benchmarks/tier1/corpus/citation_failure_cases.json \
  --output results/demo/integrity.json

# Tier 2 — requires model API access:
python runners/run_synthetic.py \
  --models openai_fast \
  --prompts benchmarks/tier2/ \
  --output results/v0.2/$(date +%Y-%m-%d)/
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to add corpus records or synthetic prompts.
