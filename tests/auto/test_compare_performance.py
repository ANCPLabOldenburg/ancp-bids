"""Unit tests for tools/compare_performance.py noise-aware gating."""
import importlib.util
from pathlib import Path

import pytest

_COMPARE_PATH = Path(__file__).resolve().parents[2] / "tools" / "compare_performance.py"
_SPEC = importlib.util.spec_from_file_location("compare_performance", _COMPARE_PATH)
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MOD)
compare = _MOD.compare


def _metrics(validate: float, load: float = 0.2) -> dict:
    return {
        "preset": "medium",
        "metrics": {
            "load_seconds": load,
            "validate_seconds": validate,
            "load_validate_seconds": load + validate,
        },
    }


def test_within_relative_threshold_passes():
    failures, notes = compare(
        _metrics(14.0),
        _metrics(13.0),
        threshold=0.35,
        min_absolute_seconds=4.0,
    )
    assert failures == []
    assert any("within threshold" in note for note in notes)


def test_relative_only_overrun_not_gated():
    # +40% but only +2s absolute → treat as noise, do not fail.
    failures, notes = compare(
        _metrics(7.0),
        _metrics(5.0),
        threshold=0.35,
        min_absolute_seconds=4.0,
    )
    assert failures == []
    assert any("not gated" in note for note in notes)


def test_true_regression_fails_both_gates():
    failures, _notes = compare(
        _metrics(20.0),
        _metrics(13.0),
        threshold=0.35,
        min_absolute_seconds=4.0,
    )
    assert len(failures) == 2
    assert all("exceeds" in item for item in failures)


def test_ci_outlier_against_typical_baseline_passes():
    # Observed CI swing ~11.6–17.4s around a ~13.8s typical baseline.
    failures, _notes = compare(
        _metrics(17.4383),
        _metrics(13.7537),
        threshold=0.35,
        min_absolute_seconds=4.0,
    )
    assert failures == []
