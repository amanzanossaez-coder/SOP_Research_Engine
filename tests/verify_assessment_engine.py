#!/usr/bin/env python3
"""
SOP Research Engine
Assessment Engine Verification

Functional smoke test for RE-029.3.

It verifies that AssessmentEngine can consume the shared research
pipeline without changing its public assessment helpers.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.assessment_engine import AssessmentEngine
from engine.drawdown_engine import run_drawdown_engine


EXPECTED_DRAWDOWN_ZONE = "NORMAL"
EXPECTED_EXPECTED_RETURN_5Y = 0.10192496249726091
EXPECTED_UPSIDE_POTENTIAL = 0.13285520801656237
EXPECTED_DOWNSIDE_RISK = -0.01091948933252962


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


def main() -> None:

    dataset = run_drawdown_engine()
    assessment = AssessmentEngine(dataset)

    assert_equal(
        "drawdown_zone",
        assessment.drawdown_zone(),
        EXPECTED_DRAWDOWN_ZONE,
    )

    assert_close(
        "expected_return_5y",
        float(assessment.expected_return_5y()),
        EXPECTED_EXPECTED_RETURN_5Y,
    )

    assert_close(
        "upside_potential",
        float(assessment.upside_potential()),
        EXPECTED_UPSIDE_POTENTIAL,
    )

    assert_close(
        "downside_risk",
        float(assessment.downside_risk()),
        EXPECTED_DOWNSIDE_RISK,
    )

    assert_equal(
        "matches_count",
        len(assessment.matches),
        10,
    )

    print("ASSESSMENT ENGINE : STABLE")
    print(f"drawdown_zone: {assessment.drawdown_zone()}")
    print(f"expected_return_5y: {assessment.expected_return_5y():.15f}")
    print(f"upside_potential: {assessment.upside_potential():.15f}")
    print(f"downside_risk: {assessment.downside_risk():.15f}")
    print(f"matches: {len(assessment.matches)}")


if __name__ == "__main__":
    main()
