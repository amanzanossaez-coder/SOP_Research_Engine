#!/usr/bin/env python3
"""
SOP Research Engine
Research Validation Metrics Verification

Functional smoke test for the exploratory Research Validation metrics.
It verifies the canonical values established by RE-025 under the pinned
runtime in requirements.txt.
"""

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

EXPECTED_MAE = 0.07025011023213769
EXPECTED_DIRECTIONAL_HIT_RATE = 0.9473684210526315
EXPECTED_RANK_CORRELATION = -0.22902466816870654

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
    (0.090162141571, [1982.07, 1987.12, 2018.12]),
    (0.113866763522, [1990.10, 1998.09, 2009.03, 2020.03]),
    (0.127427505966, [1921.08, 1932.06, 1970.06, 1974.12]),
    (0.158567951617, [1903.10, 1907.11, 1957.12, 1960.10, 1962.06]),
]


def assert_close(label: str, actual: float, expected: float) -> None:
    if abs(actual - expected) > 1e-12:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def assert_equal(label: str, actual, expected) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def bottom_date(record) -> float:
    return round(record.episode.bottom_date, 2)


def main() -> None:
    dataset = run_drawdown_engine()
    harness = ValidationHarness(dataset)
    records = harness.run()

    assert_equal("episodes", len(dataset.episodes), EXPECTED_EPISODES)
    assert_equal("sample_size", harness.sample_size(records), EXPECTED_SAMPLE_SIZE)
    assert_equal(
        "evaluated_count",
        harness.evaluated_count(records),
        EXPECTED_EVALUATED_COUNT,
    )

    assert_close("mae", mean_absolute_error(records), EXPECTED_MAE)
    assert_close(
        "directional_hit_rate",
        directional_hit_rate(records),
        EXPECTED_DIRECTIONAL_HIT_RATE,
    )
    assert_close(
        "rank_correlation",
        rank_correlation(records),
        EXPECTED_RANK_CORRELATION,
    )

    overlap_pairs = [
        (bottom_date(left), bottom_date(right))
        for left, right in overlapping_outcome_windows(records)
    ]
    assert_equal("overlap_pairs", overlap_pairs, EXPECTED_OVERLAP_PAIRS)

    repeated_groups = []

    for group in repeated_forecast_groups(records):
        forecast = round(group[0].forecast, 12)
        bottoms = [bottom_date(record) for record in group]
        repeated_groups.append((forecast, bottoms))

    assert_equal(
        "repeated_forecast_groups",
        repeated_groups,
        EXPECTED_REPEATED_FORECAST_GROUPS,
    )

    print("RESEARCH VALIDATION METRICS : STABLE")
    print(f"episodes: {len(dataset.episodes)}")
    print(f"sample_size: {harness.sample_size(records)}")
    print(f"evaluated_count: {harness.evaluated_count(records)}")
    print(f"mae: {mean_absolute_error(records):.14f}")
    print(f"directional_hit_rate: {directional_hit_rate(records):.14f}")
    print(f"rank_correlation: {rank_correlation(records):.14f}")
    print(f"overlap_pairs: {len(overlap_pairs)}")
    print(f"repeated_forecast_groups: {len(repeated_groups)}")


if __name__ == "__main__":
    main()
