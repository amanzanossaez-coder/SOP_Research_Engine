#!/usr/bin/env python3
"""
SOP Research Engine
Secondary Baselines Verification

Functional smoke test for RE-PRED.11 -- the two secondary baselines
(zero, mean-reversion) that isolate whether the RE-PRED.10 finding is
an artifact of the primary baseline choice.

Same discipline as tests/verify_baseline_harness.py (RE-PRED.9): this
test does NOT hardcode canonical secondary-baseline values yet. Those
require confirmation under the pinned runtime. It re-asserts the
already-established canonical model and primary-baseline values
(RE-BUG.3, RE-PRED.10) as a regression guard, and prints the full
three-way comparison table (model / primary baseline / zero /
mean-reversion) for that confirmation to happen against.

Zero is expected to produce None for directional_hit_rate and
rank_correlation by construction (see baseline_harness.zero_forecast
docstring) -- this is asserted explicitly, not treated as a failure.
"""

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
from typing import Optional
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.baseline_harness import (
    BaselineHarness,
    build_baseline_records,
    excess_summary,
    mean_reversion_forecast,
    missing_baseline_forecast_count,
    zero_forecast,
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

# Ya establecidos y verificados en el entorno pinneado (RE-BUG.3 /
# RE-PRED.10). Se reafirman aqui como guarda de regresion.
EXPECTED_MODEL_MAE = 0.06928793787076225
EXPECTED_MODEL_DIRECTIONAL_HIT_RATE = 0.9473684210526315
EXPECTED_MODEL_RANK_CORRELATION = -0.26505171850684983

EXPECTED_PRIMARY_BASELINE_MAE = 0.06740858559979
EXPECTED_PRIMARY_BASELINE_HIT_RATE = 0.94736842105263
EXPECTED_PRIMARY_BASELINE_RANK_CORRELATION = -0.23171864780822


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


def check_close(label: str, actual: float, expected: float, tol=1e-11) -> Optional[str]:
    if abs(actual - expected) > tol:
        return f"{label}: expected {expected}, got {actual}"

    return None


def check_equal(label: str, actual, expected) -> Optional[str]:
    if actual != expected:
        return f"{label}: expected {expected}, got {actual}"

    return None


def check_none(label: str, actual) -> Optional[str]:
    if actual is not None:
        return f"{label}: expected None, got {actual}"

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

    primary_harness = BaselineHarness(dataset)
    primary_records = primary_harness.run(model_records)

    zero_records = build_baseline_records(model_records, zero_forecast)
    reversion_records = build_baseline_records(
        model_records,
        mean_reversion_forecast,
    )

    model_mae = mean_absolute_error(model_records)
    model_hit_rate = directional_hit_rate(model_records)
    model_rank_correlation = rank_correlation(model_records)

    primary_mae = mean_absolute_error(primary_records)
    primary_hit_rate = directional_hit_rate(primary_records)
    primary_rank_correlation = rank_correlation(primary_records)

    zero_mae = mean_absolute_error(zero_records)
    zero_hit_rate = directional_hit_rate(zero_records)
    zero_rank_correlation = rank_correlation(zero_records)

    reversion_mae = mean_absolute_error(reversion_records)
    reversion_hit_rate = directional_hit_rate(reversion_records)
    reversion_rank_correlation = rank_correlation(reversion_records)

    missing_reversion_forecast = missing_baseline_forecast_count(
        model_records,
        reversion_records,
    )

    regressions = [
        check_equal("episodes", len(dataset.episodes), EXPECTED_EPISODES),
        check_equal(
            "sample_size",
            harness.sample_size(model_records),
            EXPECTED_SAMPLE_SIZE,
        ),
        check_equal(
            "evaluated_count",
            harness.evaluated_count(model_records),
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
        check_close(
            "primary_baseline_mae",
            primary_mae,
            EXPECTED_PRIMARY_BASELINE_MAE,
            tol=1e-10,
        ),
        check_close(
            "primary_baseline_hit_rate",
            primary_hit_rate,
            EXPECTED_PRIMARY_BASELINE_HIT_RATE,
            tol=1e-10,
        ),
        check_close(
            "primary_baseline_rank_correlation",
            primary_rank_correlation,
            EXPECTED_PRIMARY_BASELINE_RANK_CORRELATION,
            tol=1e-10,
        ),
        # RE-PRED.11 -- zero degenera por construccion, no por error.
        check_none("zero_hit_rate_must_be_none", zero_hit_rate),
        check_none("zero_rank_correlation_must_be_none", zero_rank_correlation),
        check_equal(
            "missing_reversion_forecast_count",
            missing_reversion_forecast,
            0,
        ),
    ]

    regressions = [r for r in regressions if r is not None]

    if regressions:
        print("SECONDARY BASELINES : REGRESSION DETECTED")

        for regression in regressions:
            print(regression)

        raise SystemExit(1)

    zero_summary = excess_summary(model_records, zero_records)
    reversion_summary = excess_summary(model_records, reversion_records)

    print("SECONDARY BASELINES : STABLE")
    print(f"episodes: {len(dataset.episodes)}")
    print(f"evaluated_count: {harness.evaluated_count(model_records)}")
    print()
    print("--- MAE ---")
    print(f"model_mae: {fmt(model_mae)}")
    print(f"primary_baseline_mae: {fmt(primary_mae)}")
    print(f"zero_mae: {fmt(zero_mae)}")
    print(f"reversion_mae: {fmt(reversion_mae)}")
    print(f"excess_mae_vs_zero: {fmt(zero_summary['excess_mae'])}")
    print(f"excess_mae_vs_reversion: {fmt(reversion_summary['excess_mae'])}")
    print()
    print("--- Directional hit-rate ---")
    print(f"model_hit_rate: {fmt(model_hit_rate)}")
    print(f"primary_baseline_hit_rate: {fmt(primary_hit_rate)}")
    print(f"zero_hit_rate: {fmt(zero_hit_rate)} (expected None by construction)")
    print(f"reversion_hit_rate: {fmt(reversion_hit_rate)}")
    print(
        "excess_hit_rate_vs_reversion: "
        f"{fmt(reversion_summary['excess_hit_rate'])}"
    )
    print()
    print("--- Rank correlation ---")
    print(f"model_rank_correlation: {fmt(model_rank_correlation)}")
    print(f"primary_baseline_rank_correlation: {fmt(primary_rank_correlation)}")
    print(
        f"zero_rank_correlation: {fmt(zero_rank_correlation)} "
        "(expected None by construction)"
    )
    print(f"reversion_rank_correlation: {fmt(reversion_rank_correlation)}")
    print(
        "excess_rank_correlation_vs_reversion: "
        f"{fmt(reversion_summary['excess_rank_correlation'])}"
    )
    print()
    print(
        "NOTE: zero_* and reversion_* values above are NOT canonical "
        "yet. They become canonical only after being confirmed under "
        "this pinned runtime and hardcoded in a future iteration "
        "(RE-PRED.13)."
    )
    print(
        "NOTE: this table addresses baseline-choice robustness only. "
        "It does not address whether any excess value is "
        "distinguishable from sampling noise on N=19 dependent "
        "records (RE-PRED.12)."
    )


if __name__ == "__main__":
    main()
