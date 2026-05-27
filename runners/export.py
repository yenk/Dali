#!/usr/bin/env python3
"""Export and summarize benchmark results.

Usage:
    python runners/export.py results/v0.2/2026-05-25/ --format table
    python runners/export.py results/v0.2/2026-05-25/ --format csv
    python runners/export.py results/v0.2/2026-05-25/ --format json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_results(results_dir: Path) -> dict[str, list[dict]]:
    """Load all model result files from a results directory."""
    results = {}
    for path in sorted(results_dir.glob("*.json")):
        if path.name == "methodology.json":
            continue
        model_id = path.stem.replace("_", "-", 2)  # rough reverse of safe_model_id
        with open(path) as f:
            results[path.stem] = json.load(f)
    return results


def per_prompt_rows(model_results: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for model_file, results in model_results.items():
        for r in results:
            rows.append({
                "model": r.get("model_id", model_file),
                "prompt_id": r["prompt_id"],
                "citation_count": r["citation_count"],
                "existence_rate": r.get("existence_rate"),
                "mean_support_score": r.get("mean_support_score"),
                "error": r.get("error", ""),
            })
    return rows


def print_table(rows: list[dict]) -> None:
    print(f"\n{'Model':<35} {'Prompt':<30} {'Citations':>9} {'Exist%':>7} {'Support':>8}")
    print("─" * 95)
    for r in rows:
        ex = f"{r['existence_rate']:.0%}" if r["existence_rate"] is not None else "—"
        sup = f"{r['mean_support_score']:.2f}" if r["mean_support_score"] is not None else "—"
        err = f"  ERR: {r['error'][:30]}" if r["error"] else ""
        print(f"{r['model']:<35} {r['prompt_id']:<30} {r['citation_count']:>9} {ex:>7} {sup:>8}{err}")


def print_summary(model_results: dict[str, list[dict]]) -> None:
    print(f"\n── Aggregate Summary ─────────────────────────────────────────")
    print(f"{'Model':<35} {'Prompts':>7} {'Citations':>9} {'Exist%':>7} {'Support':>8}")
    print("─" * 70)
    for model_file, results in model_results.items():
        model_id = results[0].get("model_id", model_file) if results else model_file
        total_cit = sum(r["citation_count"] for r in results)
        ex_rates = [r["existence_rate"] for r in results if r.get("existence_rate") is not None]
        sup_scores = [r["mean_support_score"] for r in results if r.get("mean_support_score") is not None]
        ex_mean = sum(ex_rates) / len(ex_rates) if ex_rates else None
        sup_mean = sum(sup_scores) / len(sup_scores) if sup_scores else None
        ex_str = f"{ex_mean:.0%}" if ex_mean is not None else "—"
        sup_str = f"{sup_mean:.2f}" if sup_mean is not None else "—"
        print(f"{model_id:<35} {len(results):>7} {total_cit:>9} {ex_str:>7} {sup_str:>8}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export benchmark results")
    parser.add_argument("results_dir", type=Path, help="Results directory to export")
    parser.add_argument(
        "--format", choices=["table", "csv", "json"], default="table"
    )
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"Directory not found: {args.results_dir}", file=sys.stderr)
        sys.exit(1)

    model_results = load_results(args.results_dir)
    if not model_results:
        print("No result files found.", file=sys.stderr)
        sys.exit(1)

    rows = per_prompt_rows(model_results)

    if args.format == "table":
        if not args.summary_only:
            print_table(rows)
        print_summary(model_results)

    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    elif args.format == "json":
        json.dump(rows, sys.stdout, indent=2, default=str)
        print()


if __name__ == "__main__":
    main()
