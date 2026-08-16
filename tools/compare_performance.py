#!/usr/bin/env python3
"""Compare benchmark metrics against a persisted baseline.

Fails when a *gated* metric is slower than baseline by **both**:

* more than ``--threshold`` relatively (default 35% for CI runner noise), and
* more than ``--min-absolute-seconds`` in wall time (default 4s)

``load_seconds`` is reported only: short loads are too noisy on shared CI
runners to gate on. Faster gated results pass.

GitHub-hosted runners commonly swing validate by ~30% for the same workload
(observed ~11.6–17.4s on the medium preset), so a tight 10% gate false-fails.

Persistence model
-----------------
* Committed ``benchmarks/baseline.json`` is the gated baseline (source of truth).
* Update it intentionally after accepted improvements or costlier validation::

    uv run python tools/bench_performance.py --preset medium -o benchmarks/baseline.json

* CI may still download the previous Performance artifact for an informational
  comparison in the job summary; gating always uses the committed file.

Example
-------
  uv run python tools/compare_performance.py \\
      --current benchmarks/latest.json \\
      --baseline benchmarks/baseline.json \\
      --threshold 0.35 \\
      --min-absolute-seconds 4
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Fail the job when these regress above threshold.
GATED_METRICS = (
    "validate_seconds",
    "load_validate_seconds",
)

# Always printed for visibility; never fails the comparison.
INFO_METRICS = (
    "load_seconds",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def compare(
    current: dict,
    baseline: dict,
    threshold: float,
    min_absolute_seconds: float = 0.0,
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

    def _line(key: str, cur: float, base: float, delta_pct: float, delta_abs: float) -> str:
        return (
            f"{key}: current={cur:.4f}s baseline={base:.4f}s "
            f"delta={delta_pct:+.2f}% ({delta_abs:+.2f}s)"
        )

    for key in INFO_METRICS + GATED_METRICS:
        if key not in cur_metrics:
            if key in GATED_METRICS:
                failures.append(f"missing current metric: {key}")
            else:
                notes.append(f"missing current metric: {key}")
            continue
        if key not in base_metrics:
            notes.append(f"baseline missing {key}; skipping")
            continue

        cur = float(cur_metrics[key])
        base = float(base_metrics[key])
        if base <= 0:
            if key in GATED_METRICS:
                failures.append(f"invalid baseline {key}={base}")
            else:
                notes.append(f"invalid baseline {key}={base}")
            continue

        ratio = cur / base
        delta_pct = (ratio - 1.0) * 100.0
        delta_abs = cur - base
        line = _line(key, cur, base, delta_pct, delta_abs)

        if key in INFO_METRICS:
            notes.append(line + " (info only; not gated)")
            continue

        relative_fail = ratio > 1.0 + threshold
        absolute_fail = delta_abs > min_absolute_seconds
        if relative_fail and absolute_fail:
            failures.append(
                line
                + f" exceeds +{threshold * 100:.1f}% and +{min_absolute_seconds:.1f}s"
            )
        elif relative_fail and not absolute_fail:
            notes.append(
                line
                + f" (relative >+{threshold * 100:.1f}% but abs <={min_absolute_seconds:.1f}s; not gated)"
            )
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
        default=0.35,
        help="Max allowed relative slowdown (default: 0.35 = 35%%)",
    )
    parser.add_argument(
        "--min-absolute-seconds",
        type=float,
        default=4.0,
        help=(
            "Also require this many extra seconds before failing "
            "(default: 4.0; use 0 to disable)"
        ),
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
    failures, notes = compare(
        current,
        baseline,
        args.threshold,
        min_absolute_seconds=args.min_absolute_seconds,
    )

    print("Performance comparison")
    print(f"  current:  {args.current}")
    print(f"  baseline: {args.baseline}")
    print(
        f"  threshold: +{args.threshold * 100:.1f}% "
        f"and +{args.min_absolute_seconds:.1f}s absolute"
    )
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
