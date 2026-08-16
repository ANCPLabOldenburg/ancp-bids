#!/usr/bin/env python3
"""Compare benchmark metrics against a persisted baseline.

Fails when any tracked metric is more than ``--threshold`` slower than baseline
(default 10%). Faster results pass. Missing baseline bootstraps unless
``--require-baseline`` is set.

Persistence model
-----------------
* Committed ``benchmarks/baseline.json`` is the source of truth across runs.
* CI also uploads ``benchmarks/latest.json`` as an artifact for history.
* Update the committed baseline intentionally after accepted improvements::

    uv run python tools/bench_performance.py --preset medium -o benchmarks/baseline.json

Example
-------
  uv run python tools/compare_performance.py \\
      --current benchmarks/latest.json \\
      --baseline benchmarks/baseline.json \\
      --threshold 0.10
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


TRACKED_METRICS = (
    "load_seconds",
    "validate_seconds",
    "load_validate_seconds",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def compare(
    current: dict,
    baseline: dict,
    threshold: float,
) -> Tuple[List[str], List[str]]:
    """Return (failures, notes)."""
    failures: List[str] = []
    notes: List[str] = []

    cur_preset = current.get("preset")
    base_preset = baseline.get("preset")
    if cur_preset and base_preset and cur_preset != base_preset:
        failures.append(
            f"preset mismatch: current={cur_preset!r} baseline={base_preset!r}"
        )

    cur_metrics: Dict[str, float] = current.get("metrics") or {}
    base_metrics: Dict[str, float] = baseline.get("metrics") or {}

    for key in TRACKED_METRICS:
        if key not in cur_metrics:
            failures.append(f"missing current metric: {key}")
            continue
        if key not in base_metrics:
            notes.append(f"baseline missing {key}; skipping")
            continue

        cur = float(cur_metrics[key])
        base = float(base_metrics[key])
        if base <= 0:
            failures.append(f"invalid baseline {key}={base}")
            continue

        ratio = cur / base
        delta_pct = (ratio - 1.0) * 100.0
        line = (
            f"{key}: current={cur:.4f}s baseline={base:.4f}s "
            f"delta={delta_pct:+.2f}%"
        )
        if ratio > 1.0 + threshold:
            failures.append(line + f" exceeds +{threshold * 100:.1f}% threshold")
        elif ratio < 1.0 - threshold:
            notes.append(line + " (improved)")
        else:
            notes.append(line + " (within threshold)")

    return failures, notes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.10,
        help="Max allowed slowdown fraction (default: 0.10 = 10%%)",
    )
    parser.add_argument(
        "--require-baseline",
        action="store_true",
        help="Fail if baseline file is missing (default: bootstrap baseline)",
    )
    parser.add_argument(
        "--write-baseline-on-missing",
        action="store_true",
        help="When baseline is missing, copy current metrics to baseline path",
    )
    args = parser.parse_args(argv)

    if not args.current.is_file():
        print(f"ERROR: current metrics not found: {args.current}", file=sys.stderr)
        return 2

    current = _load(args.current)

    if not args.baseline.is_file():
        msg = f"baseline not found: {args.baseline}"
        if args.require_baseline:
            print(f"ERROR: {msg}", file=sys.stderr)
            return 2
        print(f"WARNING: {msg}")
        if args.write_baseline_on_missing:
            args.baseline.parent.mkdir(parents=True, exist_ok=True)
            args.baseline.write_text(json.dumps(current, indent=2) + "\n")
            print(f"bootstrapped baseline -> {args.baseline}")
        else:
            print("skipping comparison (no baseline)")
        return 0

    baseline = _load(args.baseline)
    failures, notes = compare(current, baseline, args.threshold)

    print("Performance comparison")
    print(f"  current:  {args.current}")
    print(f"  baseline: {args.baseline}")
    print(f"  threshold: +{args.threshold * 100:.1f}%")
    for note in notes:
        print(f"  OK  {note}")
    for fail in failures:
        print(f"  FAIL {fail}")

    if failures:
        print(
            f"\nPerformance regression detected ({len(failures)} metric(s)).",
            file=sys.stderr,
        )
        return 1

    print("\nNo regressions above threshold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
