#!/usr/bin/env python3
"""
SOP Research Engine
Research Validation Metrics Verification

Functional smoke test for the exploratory Research Validation metrics.
It verifies the canonical values established by RE-025 under the pinned
runtime in requirements.txt.
"""

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
from typing import Optional
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.drawdown_engine import run_drawdown_engine
from engine.validation_harness import ValidationHarness
from engine.validation_metrics import (
    directional_hit_rate,
    mean_absolute_error,
    overlapping_outcome_windows,
    rank_correlation,
    repeated_forecast_groups,
)


EXPECTED_EPISODES = 23
EXPECTED_SAMPLE_SIZE = 21
EXPECTED_EVALUATED_COUNT = 19

EXPECTED_MAE = 0.06928793787076225
EXPECTED_DIRECTIONAL_HIT_RATE = 0.9473684210526315
EXPECTED_RANK_CORRELATION = -0.26505171850684983

EXPECTED_OVERLAP_PAIRS = [
    (1903.10, 1907.11),
    (1957.12, 1960.10),
    (1957.12, 1962.06),
    (1960.10, 1962.06),
    (1962.06, 1966.10),
    (1966.10, 1970.06),
    (1970.06, 1974.12),
    (1987.12, 1990.10),
    (1998.09, 2003.02),
    (2018.12, 2020.03),
]

EXPECTED_REPEATED_FORECAST_GROUPS = [
    (0.090162141571, [1982.07, 2018.12]),
    (0.113866763522, [1987.12, 1990.10, 1998.09, 2009.03, 2020.03]),
    (0.127427505966, [1921.08, 1932.06, 1970.06]),
    (0.13285085305, [1966.10, 1974.12]),
    (0.158567951617, [1903.10, 1907.11, 1957.12, 1960.10, 1962.06]),
]


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

        print("Cannot verify canonical metrics outside pinned runtime.")
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


def bottom_date(record) -> float:
    return round(record.episode.bottom_date, 2)


def main() -> None:
    verify_runtime()

    dataset = run_drawdown_engine()
    harness = ValidationHarness(dataset)
    records = harness.run()

    episodes = len(dataset.episodes)
    sample_size = harness.sample_size(records)
    evaluated_count = harness.evaluated_count(records)
    mae = mean_absolute_error(records)
    hit_rate = directional_hit_rate(records)
    rho = rank_correlation(records)

    overlap_pairs = [
        (bottom_date(left), bottom_date(right))
        for left, right in overlapping_outcome_windows(records)
    ]

    repeated_groups = []

    for group in repeated_forecast_groups(records):
        forecast = round(group[0].forecast, 12)
        bottoms = [bottom_date(record) for record in group]
        repeated_groups.append((forecast, bottoms))

    regressions = [
        check_equal("episodes", episodes, EXPECTED_EPISODES),
        check_equal("sample_size", sample_size, EXPECTED_SAMPLE_SIZE),
        check_equal("evaluated_count", evaluated_count, EXPECTED_EVALUATED_COUNT),
        check_close("mae", mae, EXPECTED_MAE),
        check_close(
            "directional_hit_rate",
            hit_rate,
            EXPECTED_DIRECTIONAL_HIT_RATE,
        ),
        check_close("rank_correlation", rho, EXPECTED_RANK_CORRELATION),
        check_equal("overlap_pairs", overlap_pairs, EXPECTED_OVERLAP_PAIRS),
        check_equal(
            "repeated_forecast_groups",
            repeated_groups,
            EXPECTED_REPEATED_FORECAST_GROUPS,
        ),
    ]

    regressions = [
        regression
        for regression in regressions
        if regression is not None
    ]

    if regressions:
        print("RESEARCH VALIDATION METRICS : REGRESSION DETECTED")

        for regression in regressions:
            print(regression)

        raise SystemExit(1)

    print("RESEARCH VALIDATION METRICS : STABLE")
    print(f"episodes: {episodes}")
    print(f"sample_size: {sample_size}")
    print(f"evaluated_count: {evaluated_count}")
    print(f"mae: {mae:.14f}")
    print(f"directional_hit_rate: {hit_rate:.14f}")
    print(f"rank_correlation: {rho:.14f}")
    print(f"overlap_pairs: {len(overlap_pairs)}")
    print(f"repeated_forecast_groups: {len(repeated_groups)}")


if __name__ == "__main__":
    main()
