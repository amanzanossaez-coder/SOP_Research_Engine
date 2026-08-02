#!/usr/bin/env python3
"""
SOP Research Engine
Research Engine Verification

Functional smoke test for the rebuilt ResearchEngine facade.
It verifies that ResearchEngine executes the operative research
pipeline and returns a ResearchResult with the canonical current
evidence surface.
"""

from pathlib import Path
from typing import Optional
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine
from models.research_result import ResearchResult


EXPECTED_SNAPSHOT_DATE = 2026.07
EXPECTED_MATCHES = 10
EXPECTED_HORIZON_YEARS = 5
EXPECTED_MEDIAN_RETURN = 0.11386676352176894
EXPECTED_WORST_RETURN = -0.01091948933252962
EXPECTED_BEST_RETURN = 0.13767334934864284
EXPECTED_RETURN_COUNT = 9
EXPECTED_POSITIVE_COUNT = 8
EXPECTED_NEGATIVE_COUNT = 1
EXPECTED_ZERO_COUNT = 0
EXPECTED_NON_POSITIVE_PROBABILITY = 0.1111111111111111
EXPECTED_RETURN_SPREAD = 0.14859283868117246


def check_close(label: str, actual: float, expected: float) -> Optional[str]:
    if abs(actual - expected) > 1e-12:
        return f"{label}: expected {expected}, got {actual}"

    return None


def check_equal(label: str, actual, expected) -> Optional[str]:
    if actual != expected:
        return f"{label}: expected {expected}, got {actual}"

    return None


def main() -> None:
    dataset = run_drawdown_engine()
    result = ResearchEngine().run(dataset)

    regressions = [
        check_equal("result_type", isinstance(result, ResearchResult), True),
        check_close("snapshot_date", result.snapshot.date, EXPECTED_SNAPSHOT_DATE),
        check_equal("matches", len(result.matches), EXPECTED_MATCHES),
        check_equal(
            "evidence_episodes_count",
            result.evidence.episodes_count,
            EXPECTED_MATCHES,
        ),
        check_equal(
            "horizon_years",
            result.evidence.horizon_years,
            EXPECTED_HORIZON_YEARS,
        ),
        check_close(
            "median_return",
            result.evidence.median_return,
            EXPECTED_MEDIAN_RETURN,
        ),
        check_close(
            "worst_return",
            result.evidence.worst_return,
            EXPECTED_WORST_RETURN,
        ),
        check_close(
            "best_return",
            result.evidence.best_return,
            EXPECTED_BEST_RETURN,
        ),
        check_equal(
            "return_count",
            result.evidence.return_count,
            EXPECTED_RETURN_COUNT,
        ),
        check_equal(
            "positive_count",
            result.evidence.positive_count,
            EXPECTED_POSITIVE_COUNT,
        ),
        check_equal(
            "negative_count",
            result.evidence.negative_count,
            EXPECTED_NEGATIVE_COUNT,
        ),
        check_equal(
            "zero_count",
            result.evidence.zero_count,
            EXPECTED_ZERO_COUNT,
        ),
        check_close(
            "non_positive_probability",
            result.evidence.non_positive_probability,
            EXPECTED_NON_POSITIVE_PROBABILITY,
        ),
        check_close(
            "return_spread",
            result.evidence.return_spread,
            EXPECTED_RETURN_SPREAD,
        ),
    ]

    regressions = [
        regression
        for regression in regressions
        if regression is not None
    ]

    if regressions:
        print("RESEARCH ENGINE : REGRESSION DETECTED")

        for regression in regressions:
            print(regression)

        raise SystemExit(1)

    print("RESEARCH ENGINE : STABLE")
    print(f"snapshot_date: {result.snapshot.date}")
    print(f"matches: {len(result.matches)}")
    print(f"horizon_years: {result.evidence.horizon_years}")
    print(f"median_return: {result.evidence.median_return:.14f}")
    print(f"worst_return: {result.evidence.worst_return:.14f}")
    print(f"best_return: {result.evidence.best_return:.14f}")
    print(f"return_count: {result.evidence.return_count}")
    print(f"positive_count: {result.evidence.positive_count}")
    print(f"negative_count: {result.evidence.negative_count}")
    print(f"zero_count: {result.evidence.zero_count}")
    print(
        "non_positive_probability: "
        f"{result.evidence.non_positive_probability:.14f}"
    )
    print(f"return_spread: {result.evidence.return_spread:.14f}")


if __name__ == "__main__":
    main()
