#!/usr/bin/env python3
"""
SOP Research Engine
Gate Combination Verification

Functional smoke test for the isolated RE-034.3 gate-combination layer.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.gate_combination import (
    BLOCKED,
    CONSERVE,
    DEPLOY_AGGRESSIVELY,
    DEPLOY_PARTIALLY,
    PREPARE,
    GateCombinationInput,
    combine_gate_outputs,
)


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def assert_contains(label: str, values: list[str], expected: str) -> None:

    if expected not in values:
        raise AssertionError(
            f"{label}: expected {expected!r} in {values!r}"
        )


def main() -> None:

    blocked = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="validated",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                explanations=["validated"],
            ),
            GateCombinationInput(
                gate_name="Human Approval",
                internal_state="blocked",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                blocked=True,
                explanations=["blocked"],
            ),
        ]
    )

    assert_equal(
        "blocked_wins",
        blocked.posture_ceiling,
        BLOCKED,
    )
    assert_contains(
        "blocked_explanations",
        blocked.explanations,
        "Human Approval: blocked",
    )

    most_restrictive = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="validated",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="measured",
                posture_ceiling=PREPARE,
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="available",
                posture_ceiling=DEPLOY_PARTIALLY,
            ),
        ]
    )

    assert_equal(
        "most_restrictive_ceiling",
        most_restrictive.posture_ceiling,
        PREPARE,
    )
    assert_contains(
        "most_restrictive_explanations",
        most_restrictive.explanations,
        "Regime Comparability: measured",
    )

    real_today = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="not measurable",
                posture_ceiling=PREPARE,
                explanations=["not measurable, deployment blocked"],
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="not measurable",
                posture_ceiling=CONSERVE,
                explanations=["not measurable"],
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="unavailable",
                posture_ceiling=CONSERVE,
                explanations=["unavailable"],
            ),
        ]
    )

    assert_equal(
        "real_today_ceiling",
        real_today.posture_ceiling,
        CONSERVE,
    )
    assert_contains(
        "real_today_regime_explanation",
        real_today.explanations,
        "Regime Comparability: not measurable",
    )
    assert_contains(
        "real_today_personal_explanation",
        real_today.explanations,
        "Personal Capacity: unavailable",
    )

    evidence_does_not_override = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="validated",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                explanations=["validated"],
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="not measurable",
                posture_ceiling=CONSERVE,
                explanations=["not measurable"],
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="available",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                explanations=["available"],
            ),
        ]
    )

    assert_equal(
        "evidence_does_not_override_ceiling",
        evidence_does_not_override.posture_ceiling,
        CONSERVE,
    )
    assert_contains(
        "evidence_does_not_override_explanations",
        evidence_does_not_override.explanations,
        "Regime Comparability: not measurable",
    )

    evidence_not_measurable_allows_prepare = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="not measurable",
                posture_ceiling=PREPARE,
                explanations=["not measurable, deployment blocked"],
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="measured",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                explanations=["measured"],
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="available",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
                explanations=["available"],
            ),
        ]
    )

    assert_equal(
        "evidence_not_measurable_allows_prepare_ceiling",
        evidence_not_measurable_allows_prepare.posture_ceiling,
        PREPARE,
    )
    assert_contains(
        "evidence_not_measurable_allows_prepare_explanations",
        evidence_not_measurable_allows_prepare.explanations,
        "Evidence Quality: not measurable, deployment blocked",
    )

    unavailable_regime_caps_conserve = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="validated",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="not measurable",
                posture_ceiling=CONSERVE,
                explanations=["not measurable"],
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="available",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
            ),
        ]
    )

    assert_equal(
        "unavailable_regime_caps_conserve",
        unavailable_regime_caps_conserve.posture_ceiling,
        CONSERVE,
    )

    unavailable_personal_caps_conserve = combine_gate_outputs(
        [
            GateCombinationInput(
                gate_name="Evidence Quality",
                internal_state="validated",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
            ),
            GateCombinationInput(
                gate_name="Regime Comparability",
                internal_state="measured",
                posture_ceiling=DEPLOY_AGGRESSIVELY,
            ),
            GateCombinationInput(
                gate_name="Personal Capacity",
                internal_state="unavailable",
                posture_ceiling=CONSERVE,
                explanations=["unavailable"],
            ),
        ]
    )

    assert_equal(
        "unavailable_personal_caps_conserve",
        unavailable_personal_caps_conserve.posture_ceiling,
        CONSERVE,
    )
    assert_contains(
        "unavailable_personal_explanations",
        unavailable_personal_caps_conserve.explanations,
        "Personal Capacity: unavailable",
    )

    empty = combine_gate_outputs([])

    assert_equal(
        "empty_defaults_conserve",
        empty.posture_ceiling,
        CONSERVE,
    )
    assert_contains(
        "empty_explanations",
        empty.explanations,
        "gate combination: no gate outputs available",
    )

    print("GATE COMBINATION : STABLE")
    print(f"blocked_wins: {blocked.posture_ceiling}")
    print(f"most_restrictive_ceiling: {most_restrictive.posture_ceiling}")
    print(f"real_today_ceiling: {real_today.posture_ceiling}")
    print(
        "evidence_not_measurable_allows_prepare: "
        f"{evidence_not_measurable_allows_prepare.posture_ceiling}"
    )
    print(
        "evidence_does_not_override: "
        f"{evidence_does_not_override.posture_ceiling}"
    )


if __name__ == "__main__":
    main()
