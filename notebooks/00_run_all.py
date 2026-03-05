#!/usr/bin/env python3
"""
run_all.py — Execute all Engineering Truthiness experiments sequentially.

Usage:
    python run_all.py                    # Run all experiments
    python run_all.py --experiments 1 3  # Run only experiments 1 and 3
    python run_all.py --dry-run          # Parse but don't execute

All outputs are saved under outputs/<experiment_name>/<run_id>/
"""

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
NOTEBOOKS = {
    1: "01_synthetic_theory_validation.ipynb",
    2: "02_text_weak_supervision.ipynb",
    3: "03_clinical_jaccard_fairness.ipynb",
    4: "04_cifar_vision_stress.ipynb",
    5: "05_trec_external_validation.ipynb",
}

DESCRIPTIONS = {
    1: "Synthetic Double-Noise Validation (Proposition 1)",
    2: "Weakly Supervised Text Classification (IMDB/Snorkel)",
    3: "Clinical Trial Matching (Jaccard Silver Labels)",
    4: "Vision Benchmark Stress Test (CIFAR-10)",
    5: "TREC 2021 External Gold Validation",
}


def resolve_repo_root() -> Path:
    """Find repo root regardless of where script is invoked from."""
    here = Path(__file__).resolve().parent
    # If we're in notebooks/, go up
    if here.name == "notebooks":
        return here.parent
    return here


def execute_notebook(nb_path: Path, repo_root: Path, dry_run: bool = False) -> dict:
    """Execute all code cells in a notebook using exec().

    Returns a dict with status, timing, and output paths.
    """
    with open(nb_path) as f:
        nb = json.load(f)

    cells = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"]).strip()
        if not src:
            continue
        # Skip Jupyter magic / pip installs — these are handled by requirements.txt
        if src.startswith("!"):
            continue
        # Skip IPython display cells (non-essential visualization)
        if "IPython.display" in src or "ipy_display" in src:
            continue
        cells.append(src)

    if dry_run:
        return {"status": "DRY_RUN", "cells": len(cells), "errors": []}

    # Build namespace with working directory set to notebooks/
    old_cwd = os.getcwd()
    os.chdir(repo_root / "notebooks")

    namespace = {"__name__": "__main__"}
    errors = []
    t0 = time.time()

    for i, src in enumerate(cells):
        try:
            exec(src, namespace)
        except Exception as e:
            errors.append({
                "cell": i,
                "error": f"{type(e).__name__}: {e}",
                "first_line": src.split("\n")[0][:80],
            })
            # Non-fatal: continue to next cell
            print(f"    [WARN] Cell {i} failed: {type(e).__name__}: {e}")

    elapsed = time.time() - t0
    os.chdir(old_cwd)

    return {
        "status": "PASS" if not errors else "PARTIAL",
        "cells_executed": len(cells) - len(errors),
        "cells_total": len(cells),
        "errors": errors,
        "elapsed_s": round(elapsed, 2),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run all Engineering Truthiness experiments."
    )
    parser.add_argument(
        "--experiments", "-e",
        nargs="+",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5],
        help="Which experiments to run (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse notebooks but don't execute code",
    )
    args = parser.parse_args()

    # Suppress interactive plots
    os.environ["MPLBACKEND"] = "Agg"

    repo_root = resolve_repo_root()
    nb_dir = repo_root / "notebooks"

    print("=" * 70)
    print("  Engineering Truthiness — Experiment Runner")
    print("=" * 70)
    print(f"  Repo root:    {repo_root}")
    print(f"  Notebooks:    {nb_dir}")
    print(f"  Experiments:  {args.experiments}")
    print(f"  Dry run:      {args.dry_run}")
    print("=" * 70)

    results = {}
    total_t0 = time.time()

    for exp_num in sorted(args.experiments):
        nb_name = NOTEBOOKS[exp_num]
        nb_path = nb_dir / nb_name
        desc = DESCRIPTIONS[exp_num]

        print(f"\n{'─' * 70}")
        print(f"  [{exp_num}/{len(args.experiments)}] {desc}")
        print(f"  File: {nb_name}")
        print(f"{'─' * 70}")

        if not nb_path.exists():
            print(f"    [ERROR] Notebook not found: {nb_path}")
            results[exp_num] = {"status": "NOT_FOUND"}
            continue

        result = execute_notebook(nb_path, repo_root, dry_run=args.dry_run)
        results[exp_num] = result

        if result["status"] == "DRY_RUN":
            print(f"    [DRY RUN] {result['cells']} code cells parsed OK")
        elif result["status"] == "PASS":
            print(f"    [PASS] {result['cells_executed']} cells in {result['elapsed_s']}s")
        else:
            print(f"    [PARTIAL] {result['cells_executed']}/{result['cells_total']} cells,"
                  f" {len(result['errors'])} errors, {result['elapsed_s']}s")

    total_elapsed = time.time() - total_t0

    # Summary
    print(f"\n{'=' * 70}")
    print("  SUMMARY")
    print(f"{'=' * 70}")
    for exp_num in sorted(results):
        r = results[exp_num]
        icon = {"PASS": "PASS", "PARTIAL": "WARN", "DRY_RUN": "SKIP", "NOT_FOUND": "FAIL"}
        status = icon.get(r["status"], "?")
        elapsed = f" ({r.get('elapsed_s', 0)}s)" if "elapsed_s" in r else ""
        print(f"  {status}  Experiment {exp_num}: {DESCRIPTIONS[exp_num]} — {r['status']}{elapsed}")

    print(f"\n  Total time: {total_elapsed:.1f}s")

    # Check outputs
    out_dir = repo_root / "outputs"
    if out_dir.exists():
        figures = list(out_dir.rglob("*.png"))
        tables = list(out_dir.rglob("*.csv"))
        manifests = list(out_dir.rglob("*.json"))
        print(f"  Outputs: {len(figures)} figures, {len(tables)} tables, {len(manifests)} manifests")
        print(f"  Location: {out_dir}/")

    print(f"{'=' * 70}")

    # Exit with error code if any experiment fully failed
    if any(r["status"] == "NOT_FOUND" for r in results.values()):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
