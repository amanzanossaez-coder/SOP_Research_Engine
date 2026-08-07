#!/usr/bin/env python3
"""
SOP Research Engine
Evidence Quality Gate Verification

Functional smoke test for the isolated RE-030.1 gate structure.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.evidence_quality_gate import (
    CONSERVATIVE,
    NOT_MEASURABLE,
    PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    EvidenceQualityGate,
    GlobalModelValidationState,
    LocalEvidenceQualityInputs,
    build_local_evidence_quality_inputs,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine


LESS_RESTRICTIVE_STATES = {
    "neutral",
    "risk on",
    "less restrictive",
}

EXPECTED_LOCAL_COVERAGE = 0.9
EXPECTED_LOCAL_CONSISTENCY = 0.9518456229064439
EXPECTED_LOCAL_DIVERSITY = 0.6


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def assert_close(label: str, actual: float, expected: float) -> None:

    if abs(actual - expected) > 1e-12:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def assert_in(label: str, actual, expected) -> None:

    if actual not in expected:
        raise AssertionError(
            f"{label}: expected one of {expected}, got {actual}"
        )


def assert_not_in(label: str, actual, rejected) -> None:

    if actual in rejected:
        raise AssertionError(
            f"{label}: rejected state {actual}"
        )


def assert_contains(label: str, values: list[str], expected: str) -> None:

    if expected not in values:
        raise AssertionError(
            f"{label}: expected {expected!r} in {values!r}"
        )


def assert_none_contains(label: str, values: list[str], fragment: str) -> None:

    if any(fragment in value for value in values):
        raise AssertionError(
            f"{label}: expected no explanation containing {fragment!r}, "
            f"got {values!r}"
        )


def main() -> None:

    gate = EvidenceQualityGate()

    dataset = run_drawdown_engine()
    research = ResearchEngine().run(dataset)
    real_local = build_local_evidence_quality_inputs(
        research.evidence,
    )

    assert_close(
        "real_local_coverage",
        real_local.coverage,
        EXPECTED_LOCAL_COVERAGE,
    )
    assert_close(
        "real_local_consistency",
        real_local.consistency,
        EXPECTED_LOCAL_CONSISTENCY,
    )
    assert_close(
        "real_local_diversity",
        real_local.diversity,
        EXPECTED_LOCAL_DIVERSITY,
    )
    assert_equal(
        "real_local_independence_dispersion_measured",
        real_local.independence_dispersion_measured,
        True,
    )
    if (
        not isinstance(real_local.overlapping_match_pairs, int)
        or real_local.overlapping_match_pairs < 0
    ):
        raise AssertionError(
            "real_local_overlapping_match_pairs: expected a "
            f"non-negative int, got {real_local.overlapping_match_pairs!r}"
        )

    real_today = gate.evaluate(
        local=real_local,
        global_state=GlobalModelValidationState(
            predictive_validation_status="not validated",
        ),
    )

    assert_equal(
        "real_today_state",
        real_today.state,
        NOT_MEASURABLE,
    )
    assert_none_contains(
        "real_today_explanations",
        real_today.explanations,
        "independence / dispersion not measured",
    )
    assert_contains(
        "real_today_explanations",
        real_today.explanations,
        "global model-validation state not validated",
    )

    real_today_not_demonstrated = gate.evaluate(
        local=real_local,
        global_state=GlobalModelValidationState(
            predictive_validation_status=(
                PREDICTIVE_VALIDATION_NOT_DEMONSTRATED
            ),
        ),
    )

    assert_equal(
        "real_today_not_demonstrated_state",
        real_today_not_demonstrated.state,
        NOT_MEASURABLE,
    )
    assert_contains(
        "real_today_not_demonstrated_explanations",
        real_today_not_demonstrated.explanations,
        "predictive validation status: not demonstrated "
        "-- evaluated under a pre-registered protocol, "
        "required advantage not shown",
    )
    assert_none_contains(
        "real_today_not_demonstrated_explanations",
        real_today_not_demonstrated.explanations,
        "global model-validation state not validated",
    )

    today = gate.evaluate(
        local=LocalEvidenceQualityInputs(
            coverage=1.0,
            consistency=0.9,
            diversity=0.4,
            independence_dispersion_measured=False,
        ),
        global_state=GlobalModelValidationState(
            predictive_validation_status="not validated",
        ),
    )

    assert_in(
        "today_state",
        today.state,
        {NOT_MEASURABLE, CONSERVATIVE},
    )
    assert_not_in(
        "today_state_less_restrictive",
        today.state,
        LESS_RESTRICTIVE_STATES,
    )
    assert_contains(
        "today_explanations",
        today.explanations,
        "independence / dispersion not measured",
    )
    assert_contains(
        "today_explanations",
        today.explanations,
        "global model-validation state not validated",
    )

    incomplete = gate.evaluate(
        local=LocalEvidenceQualityInputs(
            coverage=None,
            consistency=None,
            diversity=None,
        ),
        global_state=GlobalModelValidationState(),
    )

    assert_equal(
        "incomplete_state",
        incomplete.state,
        NOT_MEASURABLE,
    )
    assert_contains(
        "incomplete_explanations",
        incomplete.explanations,
        "local coverage unavailable",
    )
    assert_contains(
        "incomplete_explanations",
        incomplete.explanations,
        "local consistency unavailable",
    )
    assert_contains(
        "incomplete_explanations",
        incomplete.explanations,
        "local diversity unavailable",
    )
    assert_contains(
        "incomplete_explanations",
        incomplete.explanations,
        "predictive validation status unavailable",
    )

    measured_but_not_authorized = gate.evaluate(
        local=LocalEvidenceQualityInputs(
            coverage=1.0,
            consistency=1.0,
            diversity=1.0,
            independence_dispersion_measured=True,
        ),
        global_state=GlobalModelValidationState(
            predictive_validation_status="validated",
        ),
    )

    assert_equal(
        "measured_but_not_authorized_state",
        measured_but_not_authorized.state,
        CONSERVATIVE,
    )
    assert_contains(
        "measured_but_not_authorized_explanations",
        measured_but_not_authorized.explanations,
        "no less-restrictive Evidence Quality state is authorized",
    )

    print("EVIDENCE QUALITY GATE : STABLE")
    print(f"real_local_coverage: {real_local.coverage:.14f}")
    print(f"real_local_consistency: {real_local.consistency:.14f}")
    print(f"real_local_diversity: {real_local.diversity:.14f}")
    print(
        "real_local_independence_dispersion_measured: "
        f"{real_local.independence_dispersion_measured}"
    )
    print(
        "real_local_overlapping_match_pairs: "
        f"{real_local.overlapping_match_pairs}"
        "  (NOT canonical until confirmed under RUNTIME : PINNED)"
    )
    print(f"real_today_state: {real_today.state}")
    print(
        "real_today_not_demonstrated_state: "
        f"{real_today_not_demonstrated.state}"
    )
    print(f"today_state: {today.state}")
    print(f"incomplete_state: {incomplete.state}")
    print(
        "measured_but_not_authorized_state: "
        f"{measured_but_not_authorized.state}"
    )


if __name__ == "__main__":
    main()
