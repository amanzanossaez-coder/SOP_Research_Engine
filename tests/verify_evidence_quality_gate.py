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
    EvidenceQualityGate,
    GlobalModelValidationState,
    LocalEvidenceQualityInputs,
)


LESS_RESTRICTIVE_STATES = {
    "neutral",
    "risk on",
    "less restrictive",
}


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
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


def main() -> None:

    gate = EvidenceQualityGate()

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
    print(f"today_state: {today.state}")
    print(f"incomplete_state: {incomplete.state}")
    print(
        "measured_but_not_authorized_state: "
        f"{measured_but_not_authorized.state}"
    )


if __name__ == "__main__":
    main()
