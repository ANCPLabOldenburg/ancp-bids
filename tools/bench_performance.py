#!/usr/bin/env python3
"""Benchmark ancpbids load/validate on a synthetic heavy dataset.

Writes a JSON metrics file for CI regression comparison.

Example
-------
  uv run python tools/bench_performance.py --preset medium -o benchmarks/latest.json
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from pathlib import Path

from create_heavy_dataset import PRESETS, create_heavy_dataset


def _mean(values):
    return statistics.mean(values) if values else None


def _stdev(values):
    return statistics.stdev(values) if len(values) > 1 else 0.0


def run_benchmark(preset: str, repeats: int, warmup: int) -> dict:
    from ancpbids import DatasetOptions, load_dataset, validate_dataset

    cfg = PRESETS[preset]
    with tempfile.TemporaryDirectory(prefix="ancpbids_bench_") as tmp:
        root = Path(tmp) / "dataset"
        n_files, n_dirs = create_heavy_dataset(
            root,
            subjects=cfg["subjects"],
            sessions=cfg["sessions"],
            runs=cfg["runs"],
            tasks=cfg["tasks"],
            acqs=cfg["acqs"],
            derivatives=cfg["derivatives"],
        )

        opts = DatasetOptions(lazy_loading=True, ignore_pickle_file=True)

        for _ in range(warmup):
            ds = load_dataset(str(root), opts)
            validate_dataset(ds)

        load_times = []
        validate_times = []
        n_messages = None
        for _ in range(repeats):
            t0 = time.perf_counter()
            ds = load_dataset(str(root), opts)
            load_times.append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            report = validate_dataset(ds)
            validate_times.append(time.perf_counter() - t0)
            n_messages = len(report.messages)

        load_mean = _mean(load_times)
        validate_mean = _mean(validate_times)
        return {
            "schema_version": "1",
            "preset": preset,
            "repeats": repeats,
            "warmup": warmup,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "n_files": n_files,
            "n_dirs": n_dirs,
            "n_messages": n_messages,
            "metrics": {
                "load_seconds": load_mean,
                "validate_seconds": validate_mean,
                "load_validate_seconds": load_mean + validate_mean,
            },
            "samples": {
                "load_seconds": load_times,
                "validate_seconds": validate_times,
            },
            "stats": {
                "load_seconds_stdev": _stdev(load_times),
                "validate_seconds_stdev": _stdev(validate_times),
            },
        }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="medium",
        help="Dataset size profile (default: medium)",
    )
    parser.add_argument("--repeats", type=int, default=3, help="Timed repetitions")
    parser.add_argument("--warmup", type=int, default=1, help="Discarded warmup runs")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("benchmarks/latest.json"),
        help="Metrics JSON output path",
    )
    args = parser.parse_args(argv)

    result = run_benchmark(args.preset, args.repeats, args.warmup)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")

    metrics = result["metrics"]
    print(
        f"preset={result['preset']} files≈{result['n_files']} "
        f"load={metrics['load_seconds']:.3f}s "
        f"validate={metrics['validate_seconds']:.3f}s "
        f"total={metrics['load_validate_seconds']:.3f}s "
        f"-> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
