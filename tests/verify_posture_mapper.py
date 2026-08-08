#!/usr/bin/env python3
"""
SOP Research Engine
Posture Mapper Verification

Functional smoke test for the isolated RE-037.1 posture-mapping layer,
plus a read-only audit dry-run against today's real snapshot.

This is NOT a test of the Capital Posture Engine -- no such component
exists yet. It only verifies that RE-034.1's and RE-034.5's documented
mapping tables are applied correctly and that engine/gate_combination.py
is consumed exactly as published.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.evidence_quality_gate import (
    CONSERVATIVE,
    NOT_MEASURABLE as EQ_NOT_MEASURABLE,
    EvidenceQualityGate,
    EvidenceQualityGateResult,
    GlobalModelValidationState,
    PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    build_local_evidence_quality_inputs,
)
from engine.gate_combination import CONSERVE, DEPLOY_AGGRESSIVELY, PREPARE
from engine.posture_mapper import (
    evaluate_capital_posture,
    evidence_quality_to_gate_input,
    regime_comparability_to_gate_input,
)
from engine.regime_comparability_gate import (
    COMPARABLE,
    NOT_COMPARABLE,
    NOT_MEASURABLE as REGIME_NOT_MEASURABLE,
    RegimeComparabilityGate,
    RegimeComparabilityGateResult,
    build_local_regime_comparability_inputs,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine


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


def assert_raises(label: str, fn) -> None:

    try:
        fn()
    except ValueError:
        return

    raise AssertionError(f"{label}: expected ValueError, none raised")


def main() -> None:

    # -- Single-gate translation, per RE-034.1 / RE-034.5 --

    eq_input = evidence_quality_to_gate_input(
        EvidenceQualityGateResult(
            state=CONSERVATIVE,
            explanations=["no less-restrictive state authorized"],
        )
    )
    assert_equal("eq_conservative_ceiling", eq_input.posture_ceiling, CONSERVE)
    assert_equal("eq_conservative_gate_name", eq_input.gate_name, "Evidence Quality")
    assert_equal("eq_conservative_blocked", eq_input.blocked, False)

    eq_not_measurable_input = evidence_quality_to_gate_input(
        EvidenceQualityGateResult(state=EQ_NOT_MEASURABLE, explanations=["x"])
    )
    assert_equal(
        "eq_not_measurable_ceiling",
        eq_not_measurable_input.posture_ceiling,
        PREPARE,
    )

    regime_comparable_input = regime_comparability_to_gate_input(
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["x"])
    )
    assert_equal(
        "regime_comparable_ceiling",
        regime_comparable_input.posture_ceiling,
        DEPLOY_AGGRESSIVELY,
    )

    regime_not_comparable_input = regime_comparability_to_gate_input(
        RegimeComparabilityGateResult(state=NOT_COMPARABLE, explanations=["x"])
    )
    assert_equal(
        "regime_not_comparable_ceiling",
        regime_not_comparable_input.posture_ceiling,
        CONSERVE,
    )

    regime_not_measurable_input = regime_comparability_to_gate_input(
        RegimeComparabilityGateResult(state=REGIME_NOT_MEASURABLE, explanations=["x"])
    )
    assert_equal(
        "regime_not_measurable_ceiling",
        regime_not_measurable_input.posture_ceiling,
        CONSERVE,
    )

    assert_raises(
        "unknown_evidence_state_raises",
        lambda: evidence_quality_to_gate_input(
            EvidenceQualityGateResult(state="made up", explanations=[])
        ),
    )
    assert_raises(
        "unknown_regime_state_raises",
        lambda: regime_comparability_to_gate_input(
            RegimeComparabilityGateResult(state="made up", explanations=[])
        ),
    )

    # -- Combined posture, synthetic --

    both_weak = evaluate_capital_posture(
        EvidenceQualityGateResult(state=EQ_NOT_MEASURABLE, explanations=["eq unmeasured"]),
        RegimeComparabilityGateResult(state=REGIME_NOT_MEASURABLE, explanations=["regime unmeasured"]),
    )
    assert_equal("both_weak_ceiling", both_weak.posture_ceiling, CONSERVE)

    evidence_conservative_regime_comparable = evaluate_capital_posture(
        EvidenceQualityGateResult(state=CONSERVATIVE, explanations=["eq conservative"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
    )
    assert_equal(
        "evidence_conservative_regime_comparable_ceiling",
        evidence_conservative_regime_comparable.posture_ceiling,
        CONSERVE,
    )

    evidence_not_measurable_regime_comparable = evaluate_capital_posture(
        EvidenceQualityGateResult(state=EQ_NOT_MEASURABLE, explanations=["eq unmeasured"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
    )
    assert_equal(
        "evidence_not_measurable_regime_comparable_ceiling",
        evidence_not_measurable_regime_comparable.posture_ceiling,
        PREPARE,
    )
    assert_contains(
        "evidence_not_measurable_regime_comparable_explanations",
        evidence_not_measurable_regime_comparable.explanations,
        "Evidence Quality: eq unmeasured",
    )

    regime_not_comparable_caps_despite_conservative_pass = evaluate_capital_posture(
        EvidenceQualityGateResult(state=CONSERVATIVE, explanations=["eq conservative"]),
        RegimeComparabilityGateResult(state=NOT_COMPARABLE, explanations=["cape out of range"]),
    )
    assert_equal(
        "regime_not_comparable_caps",
        regime_not_comparable_caps_despite_conservative_pass.posture_ceiling,
        CONSERVE,
    )

    # -- Real pipeline, audit dry-run: structural + informative, NOT canonical --

    dataset = run_drawdown_engine()
    research = ResearchEngine().run(dataset)

    eq_local = build_local_evidence_quality_inputs(research.evidence)
    eq_result = EvidenceQualityGate().evaluate(
        local=eq_local,
        global_state=GlobalModelValidationState(
            predictive_validation_status=PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
        ),
    )

    regime_local = build_local_regime_comparability_inputs(
        research.snapshot,
        research.evidence,
    )
    regime_result = RegimeComparabilityGate().evaluate(regime_local)

    combined = evaluate_capital_posture(eq_result, regime_result)

    print("POSTURE MAPPER : STABLE")
    print()
    print("-- Audit dry-run against today's real snapshot --")
    print("(NOT canonical -- read-only, not wired into any operative flow,")
    print(" Personal Capacity excluded -- see engine/posture_mapper.py docstring)")
    print()
    print(f"predictive_validation_status used: {PREDICTIVE_VALIDATION_NOT_DEMONSTRATED}")
    print(f"  (reflects RE-PRED.16's confirmed finding -- not automatic)")
    print()
    print(f"Evidence Quality state: {eq_result.state}")
    print(f"Evidence Quality explanations: {eq_result.explanations}")
    print()
    print(f"Regime Comparability state: {regime_result.state}")
    print(f"Regime Comparability explanations: {regime_result.explanations}")
    print()
    print(f"COMBINED posture ceiling: {combined.posture_ceiling}")
    print(f"COMBINED explanations: {combined.explanations}")


if __name__ == "__main__":
    main()
