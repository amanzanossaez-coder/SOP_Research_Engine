#!/usr/bin/env python3
"""
SOP Research Engine
Baseline Harness Verification

Functional smoke test for RE-PRED.9 -- the primary excess-return
baseline defined in RE-PRED.8.

Unlike the other verify_*.py scripts in this suite, this test does NOT
assert hardcoded canonical baseline values yet. Those do not exist:
this is the first execution of engine/baseline_harness.py against the
live dataset. Canonical baseline values must be established from a run
verified under the pinned runtime (requirements.txt), exactly like
RE-025.2-RE-025.4 established the model's own canonical metrics only
after RE-025.1's harness first ran. A future iteration (RE-PRED.10)
promotes the printed values below to hardcoded EXPECTED_* regression
guards, once they have been confirmed in the pinned environment -- not
before.

What this test DOES assert:

-   the pinned runtime (requirements.txt);
-   the model's already-established canonical metrics are unchanged
    (regression guard against anything this iteration might have
    disturbed, even though no Frozen Core or existing file was
    modified);
-   structural alignment between model and baseline records (same
    length, same evaluable count);
-   the RE-PRED.9 invariant: no evaluable model record produces a
    None baseline forecast.
"""

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
from typing import Optional
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.baseline_harness import (
    BaselineHarness,
    excess_summary,
    missing_baseline_forecast_count,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.validation_harness import ValidationHarness
from engine.validation_metrics import (
    directional_hit_rate,
    mean_absolute_error,
    rank_correlation,
)


EXPECTED_EPISODES = 23
EXPECTED_SAMPLE_SIZE = 21
EXPECTED_EVALUATED_COUNT = 19

# Ya establecidos y verificados en el entorno pinneado (RE-BUG.3).
# Se reafirman aqui como guarda de regresion -- este iteration no debe
# haberlos movido, porque no toca ningun archivo del que dependan.
EXPECTED_MODEL_MAE = 0.06928793787076225
EXPECTED_MODEL_DIRECTIONAL_HIT_RATE = 0.9473684210526315
EXPECTED_MODEL_RANK_CORRELATION = -0.26505171850684983


def pinned_runtime() -> dict[str, str]:
    requirements = {}

    for line in (ROOT / "requirements.txt").read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "==" not in line:
            continue

        package, expected_version = line.split("==", 1)
        requirements[package] = expected_version

    return requirements


def verify_runtime() -> None:
    expected = pinned_runtime()
    mismatches = []

    for package, expected_version in expected.items():
        try:
            actual_version = version(package)
        except PackageNotFoundError:
            actual_version = "not installed"

        if actual_version != expected_version:
            mismatches.append(
                f"Expected {package}=={expected_version}, got {actual_version}"
            )

    if mismatches:
        print("RUNTIME : MISMATCH")

        for mismatch in mismatches:
            print(mismatch)

        print("Cannot verify baseline metrics outside pinned runtime.")
        raise SystemExit(1)

    print("RUNTIME : PINNED")


def check_close(label: str, actual: float, expected: float) -> Optional[str]:
    if abs(actual - expected) > 1e-12:
        return f"{label}: expected {expected}, got {actual}"

    return None


def check_equal(label: str, actual, expected) -> Optional[str]:
    if actual != expected:
        return f"{label}: expected {expected}, got {actual}"

    return None


def fmt(value) -> str:
    if value is None:
        return "None"

    return f"{value:.14f}"


def main() -> None:
    verify_runtime()

    dataset = run_drawdown_engine()

    harness = ValidationHarness(dataset)
    model_records = harness.run()

    baseline_harness = BaselineHarness(dataset)
    baseline_records = baseline_harness.run(model_records)

    model_evaluated_count = harness.evaluated_count(model_records)
    baseline_evaluated_count = sum(
        1 for r in baseline_records if r.evaluable
    )

    missing = missing_baseline_forecast_count(
        model_records,
        baseline_records,
    )

    model_mae = mean_absolute_error(model_records)
    model_hit_rate = directional_hit_rate(model_records)
    model_rank_correlation = rank_correlation(model_records)

    regressions = [
        check_equal("episodes", len(dataset.episodes), EXPECTED_EPISODES),
        check_equal(
            "sample_size",
            harness.sample_size(model_records),
            EXPECTED_SAMPLE_SIZE,
        ),
        check_equal(
            "evaluated_count",
            model_evaluated_count,
            EXPECTED_EVALUATED_COUNT,
        ),
        check_close("model_mae", model_mae, EXPECTED_MODEL_MAE),
        check_close(
            "model_directional_hit_rate",
            model_hit_rate,
            EXPECTED_MODEL_DIRECTIONAL_HIT_RATE,
        ),
        check_close(
            "model_rank_correlation",
            model_rank_correlation,
            EXPECTED_MODEL_RANK_CORRELATION,
        ),
        check_equal(
            "baseline_record_count",
            len(baseline_records),
            len(model_records),
        ),
        check_equal(
            "baseline_evaluated_count_matches_model",
            baseline_evaluated_count,
            model_evaluated_count,
        ),
        check_equal(
            "missing_baseline_forecast_count",
            missing,
            0,
        ),
    ]

    regressions = [r for r in regressions if r is not None]

    if regressions:
        print("BASELINE HARNESS : REGRESSION DETECTED")

        for regression in regressions:
            print(regression)

        raise SystemExit(1)

    summary = excess_summary(model_records, baseline_records)

    print("BASELINE HARNESS : STABLE")
    print(f"episodes: {len(dataset.episodes)}")
    print(f"sample_size: {harness.sample_size(model_records)}")
    print(f"evaluated_count: {model_evaluated_count}")
    print(f"baseline_evaluated_count: {baseline_evaluated_count}")
    print(f"missing_baseline_forecast_count: {missing}")
    print()
    print("--- MAE ---")
    print(f"model_mae: {fmt(summary['model_mae'])}")
    print(f"baseline_mae: {fmt(summary['baseline_mae'])}")
    print(f"excess_mae: {fmt(summary['excess_mae'])}")
    print()
    print("--- Directional hit-rate ---")
    print(f"model_hit_rate: {fmt(summary['model_hit_rate'])}")
    print(f"baseline_hit_rate: {fmt(summary['baseline_hit_rate'])}")
    print(f"excess_hit_rate: {fmt(summary['excess_hit_rate'])}")
    print()
    print("--- Rank correlation ---")
    print(
        "model_rank_correlation: "
        f"{fmt(summary['model_rank_correlation'])}"
    )
    print(
        "baseline_rank_correlation: "
        f"{fmt(summary['baseline_rank_correlation'])}"
    )
    print(
        "excess_rank_correlation: "
        f"{fmt(summary['excess_rank_correlation'])}"
    )
    print()
    print(
        "NOTE: baseline_* and excess_* values above are NOT canonical "
        "yet. They become canonical only after being confirmed under "
        "this pinned runtime and hardcoded in a future iteration "
        "(RE-PRED.10)."
    )


if __name__ == "__main__":
    main()
