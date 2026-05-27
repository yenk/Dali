# Examples

This page collects the most common ways to use Dali from the public repo.

## 1. Run the deterministic Tier 1 evaluator

Use the canonical case corpus to verify the workflow-centric benchmark locally without external services.

```bash
git clone https://github.com/yenk/Dali
cd Dali
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python runners/run_integrity.py \
  --corpus data/public/citation_failure_cases.json \
  --output results/demo/integrity.json
```

What this does:
- loads the public canonical corpus
- applies the deterministic Tier 1 rubric
- writes a reproducible JSON artifact under `results/demo/`

## 2. Check source reachability

If you want to see which sources are currently reachable, add `--check-reachability`.

```bash
python runners/run_integrity.py \
  --corpus data/public/citation_failure_cases.json \
  --output results/demo/integrity.json \
  --check-reachability
```

## 3. Run the shipped Tier 2 synthetic probes

Tier 2 uses the built-in 25-prompt synthetic set under `synthetic/`.

```bash
python runners/run_synthetic.py \
  --models <model-a> <model-b> \
  --prompts synthetic/ \
  --output results/v0.2/$(date +%Y-%m-%d)/synthetic.json
```

What this does:
- evaluates the shipped benchmark prompts
- compares outputs across models
- writes one result file per model plus a `methodology.json`

## 4. Run your own prompt set

You can point `--prompts` at any directory of JSONL prompts that follow the same schema as the shipped probes.

```bash
python runners/run_synthetic.py \
  --models <model-a> <model-b> \
  --prompts path/to/your/prompts/ \
  --output results/v0.2/$(date +%Y-%m-%d)/custom-synthetic.json
```

Use this for local experimentation or extended evaluation. If you want your prompts to become part of the benchmark standard, add them through the contribution path in [contributing.md](contributing.md).

## 5. Add a new synthetic prompt

Create a JSONL entry under `synthetic/` that matches the repo schema:

```json
{
  "id": "legal_case_009",
  "category": "legal",
  "subcategory": "case_citations",
  "prompt": "...",
  "difficulty": "known_case",
  "notes": "Optional. What this prompt is testing."
}
```

Then follow the prompt contribution rules in [contributing.md](contributing.md):
- keep the prompt neutral
- explain the failure mode it exercises
- choose the appropriate difficulty tier

## 6. Inspect a result file

The benchmark writes plain JSON, so you can inspect the output directly:

```bash
jq '.[] | {prompt_id, model_id, citation_count, existence_rate, mean_support_score}' results/v0.2/$(date +%Y-%m-%d)/*.json
```

## 7. Verify the repo

The public testing steps are documented in [benchmark/testing.md](benchmark/testing.md).
