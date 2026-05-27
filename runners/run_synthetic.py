#!/usr/bin/env python3
"""Dali Citation Integrity Benchmark runner.

Usage:
    python runners/run_synthetic.py \\
        --models claude-haiku-4-5-20251001 gpt-4o-mini \\
        --prompts synthetic/ \\
        --output results/v0.2/$(date +%Y-%m-%d)/

Each model × prompt pair produces one result object. Results are
written as versioned JSON files (one per model). A methodology.json
is written alongside recording run metadata.

The public verification pipeline is self-contained: it extracts
citation-like spans, checks reachability, and applies a local support
scoring step. Results are therefore directly comparable across runs
without any external backend dependency.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from runners.models import MODELS, call_model
from scoring.support import MAX_TOKENS, SCORER_MODEL, score_support
from scoring.verification import verify_citations

_REPO_ROOT = Path(__file__).parent.parent


def load_benchmark_env() -> dict[str, str]:
    """Load local .env overrides for benchmark runs."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None

    if load_dotenv is not None:
        local_env = _REPO_ROOT / ".env"
        if local_env.is_file():
            load_dotenv(local_env, override=False)

    return {k: v for k, v in os.environ.items() if k.endswith("_API_KEY")}


def preflight_api_keys(model_ids: list[str], sources: dict[str, str]) -> None:
    """Fail fast before burning prompts on missing API keys."""
    providers: set[str] = {MODELS[model_id]["provider"] for model_id in model_ids}
    needed: set[str] = set()
    if "anthropic" in providers:
        needed.add("ANTHROPIC_API_KEY")
    if "openai" in providers:
        needed.add("OPENAI_API_KEY")

    problems: list[str] = []
    for secret_id in sorted(needed):
        value = os.environ.get(secret_id, "")
        source = sources.get(secret_id, "missing")
        if not value or value.startswith("placeholder"):
            problems.append(f"{secret_id} missing or placeholder (source={source})")

    if problems:
        print("Benchmark blocked — live model calls need API keys in the local environment:", file=sys.stderr)
        for line in problems:
            print(f"  • {line}", file=sys.stderr)
        sys.exit(2)


def load_prompts(prompts_dir: Path) -> list[dict]:
    """Load all .jsonl files from prompts_dir recursively."""
    prompts = []
    for jsonl_file in sorted(prompts_dir.rglob("*.jsonl")):
        with open(jsonl_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    prompts.append(json.loads(line))
    return prompts


async def run_prompt(
    prompt: dict,
    model_id: str,
    *,
    upload_snapshots: bool = True,
) -> dict:
    """Run a single prompt through the full verification pipeline."""
    prompt_id = prompt["id"]
    prompt_text = prompt["prompt"]
    run_at = datetime.now(timezone.utc).isoformat()

    # 1. Call model
    try:
        llm_output = call_model(model_id, prompt_text)
    except Exception as exc:
        return {
            "prompt_id": prompt_id,
            "model_id": model_id,
            "error": f"model_call_failed: {exc}",
            "output": None,
            "citations": [],
            "citation_count": 0,
            "existence_rate": None,
            "mean_support_score": None,
            "run_at": run_at,
        }

    # 2. Extract citations + snapshot
    try:
        verified = await verify_citations(
            llm_output,
            evidence_id=f"benchmark:{prompt_id}:{model_id}",
            audit_id="benchmark",
            upload=upload_snapshots,
        )
    except Exception as exc:
        verified = []
        print(f"  ⚠️  verify_citations failed for {prompt_id}: {exc}", file=sys.stderr)

    # 3. Build citation records
    citations = []
    support_scores = []
    for vc in verified:
        snap = vc.snapshot
        support_score = None
        support_verdict = None

        # Score support if source was archived
        if snap and snap.exists_verified and snap.extracted_text:
            try:
                from scoring.support import extract_claim_for_citation
                claim = extract_claim_for_citation(vc.raw_text, llm_output)
                if claim:
                    scored = score_support(claim, snap.extracted_text)
                    support_score = scored.score
                    support_verdict = scored.verdict
                    support_scores.append(support_score)
            except Exception as exc:
                print(f"  ⚠️  scoring failed for {vc.source_ref}: {exc}", file=sys.stderr)

        citations.append({
            "citation_text": vc.raw_text,
            "source_url": vc.source_ref,
            "resolution_method": vc.resolution_method,
            "existence_verified": vc.verdict in ("verified", "redirected"),
            "existence_score": vc.existence_score,
            "http_status": snap.http_status if snap else 0,
            "content_hash": snap.content_hash if snap else None,
            "storage_path": snap.storage_path if snap else None,
            "support_score": support_score,
            "support_verdict": support_verdict,
            "verdict": vc.verdict,
            "captured_at": snap.captured_at.isoformat() if snap else run_at,
        })

    existence_rate = (
        sum(1 for c in citations if c["existence_verified"]) / len(citations)
        if citations else None
    )
    mean_support = (
        sum(support_scores) / len(support_scores)
        if support_scores else None
    )

    return {
        "prompt_id": prompt_id,
        "model_id": model_id,
        "output": llm_output,
        "citations": citations,
        "citation_count": len(citations),
        "existence_rate": round(existence_rate, 4) if existence_rate is not None else None,
        "mean_support_score": round(mean_support, 4) if mean_support is not None else None,
        "run_at": run_at,
    }


async def run_model(
    model_id: str,
    prompts: list[dict],
    output_dir: Path,
    *,
    upload_snapshots: bool = True,
) -> list[dict]:
    """Run all prompts for one model and save results."""
    print(f"\n▶  {model_id}  ({len(prompts)} prompts)")
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i:02d}/{len(prompts)}] {prompt['id']} ... ", end="", flush=True)
        try:
            result = await run_prompt(prompt, model_id, upload_snapshots=upload_snapshots)
            n_cit = result["citation_count"]
            ex = result.get("existence_rate")
            sup = result.get("mean_support_score")
            ex_str = f"{ex:.0%}" if ex is not None else "n/a"
            sup_str = f"{sup:.2f}" if sup is not None else "n/a"
            print(f"{n_cit} citations  exist={ex_str}  support={sup_str}")
        except Exception as exc:
            print(f"ERROR: {exc}")
            traceback.print_exc()
            result = {
                "prompt_id": prompt["id"],
                "model_id": model_id,
                "error": str(exc),
                "citations": [],
                "citation_count": 0,
                "existence_rate": None,
                "mean_support_score": None,
                "run_at": datetime.now(timezone.utc).isoformat(),
            }
        results.append(result)

    # Write model results file
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_model_id = model_id.replace("/", "_").replace(":", "_")
    out_path = output_dir / f"{safe_model_id}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"   → saved {out_path}")

    return results


def write_methodology(
    output_dir: Path,
    model_ids: list[str],
    prompt_count: int,
    git_sha: str,
) -> None:
    """Write methodology.json alongside results."""
    methodology = {
        "benchmark_version": "v0.2",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha,
        "models": {mid: MODELS[mid] for mid in model_ids if mid in MODELS},
        "scorer": {
            "model_id": SCORER_MODEL,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.0,
            "source_char_limit": 3000,
        },
        "prompt_count": prompt_count,
        "pipeline": {
            "extraction": "public citation extraction",
            "source_fetch": "public URL fetch",
            "verifier": "scoring.verification.verify_citations",
            "scorer": "scoring.support.score_support",
        },
    }

    out_path = output_dir / "methodology.json"
    with open(out_path, "w") as f:
        json.dump(methodology, f, indent=2)
    print(f"\n📋 methodology → {out_path}")


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dali Citation Integrity Benchmark runner"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(MODELS.keys()),
        help="Model IDs to run (default: all in registry)",
    )
    parser.add_argument(
        "--prompts",
        type=Path,
        default=Path("synthetic"),
        help="Path to synthetic prompt directory (default: synthetic/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(f"results/v0.2/{datetime.now().strftime('%Y-%m-%d')}"),
        help="Output directory for results",
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Retained for compatibility; the public runner does not upload snapshots",
    )
    parser.add_argument(
        "--prompt-filter",
        help="Only run prompts whose ID contains this string",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip API key placeholder check (not recommended for live runs)",
    )
    args = parser.parse_args()

    key_sources = load_benchmark_env()

    # Validate models
    unknown = [m for m in args.models if m not in MODELS]
    if unknown:
        print(f"Unknown models: {unknown}. Available: {list(MODELS.keys())}", file=sys.stderr)
        sys.exit(1)

    prompts = load_prompts(args.prompts)
    if args.prompt_filter:
        prompts = [p for p in prompts if args.prompt_filter in p["id"]]
    if not prompts:
        print("No prompts found.", file=sys.stderr)
        sys.exit(1)

    if not args.skip_preflight:
        preflight_api_keys(args.models, key_sources)

    upload = not args.no_upload
    print(f"Dali Citation Integrity Benchmark v0.2")
    print(f"Models:  {args.models}")
    print(f"Prompts: {len(prompts)}")
    print(f"Output:  {args.output}")
    print(f"Persist: {upload and 'local results only'}")

    # Get git SHA for methodology
    try:
        import subprocess
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parent.parent
        ).decode().strip()
    except Exception:
        git_sha = "unknown"

    all_results = {}
    for model_id in args.models:
        results = await run_model(
            model_id, prompts, args.output, upload_snapshots=upload
        )
        all_results[model_id] = results

    write_methodology(args.output, args.models, len(prompts), git_sha)

    # Summary table
    print("\n── Summary ──────────────────────────────────────")
    print(f"{'Model':<35} {'Prompts':>7} {'Citations':>9} {'Exist%':>7} {'Support':>8}")
    print("─" * 70)
    for model_id, results in all_results.items():
        total_cit = sum(r["citation_count"] for r in results)
        ex_rates = [r["existence_rate"] for r in results if r.get("existence_rate") is not None]
        sup_scores = [r["mean_support_score"] for r in results if r.get("mean_support_score") is not None]
        ex_mean = sum(ex_rates) / len(ex_rates) if ex_rates else None
        sup_mean = sum(sup_scores) / len(sup_scores) if sup_scores else None
        ex_str = f"{ex_mean:.0%}" if ex_mean is not None else "—"
        sup_str = f"{sup_mean:.2f}" if sup_mean is not None else "—"
        print(f"{model_id:<35} {len(results):>7} {total_cit:>9} {ex_str:>7} {sup_str:>8}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
