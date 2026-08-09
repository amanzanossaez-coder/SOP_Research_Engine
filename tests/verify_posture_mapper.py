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
from engine.gate_combination import (
    BLOCKED,
    CONSERVE,
    DEPLOY_AGGRESSIVELY,
    PREPARE,
)
from engine.posture_mapper import (
    evaluate_capital_posture,
    evidence_quality_to_gate_input,
    personal_capacity_facts_to_gate_input,
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
from engine.personal_capacity_facts_gate import (
    ADEQUATE as PC_ADEQUATE,
    CONSTRAINED as PC_CONSTRAINED,
    NOT_MEASURABLE as PC_NOT_MEASURABLE,
    PersonalCapacityFactsGateResult,
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

    # -- Single-gate translation, Personal Capacity Facts, RE-040.1 --

    pc_adequate_input = personal_capacity_facts_to_gate_input(
        PersonalCapacityFactsGateResult(
            state=PC_ADEQUATE, blocked=False, explanations=["x"],
        )
    )
    assert_equal(
        "pc_adequate_ceiling", pc_adequate_input.posture_ceiling, DEPLOY_AGGRESSIVELY,
    )
    assert_equal("pc_adequate_blocked", pc_adequate_input.blocked, False)

    pc_constrained_input = personal_capacity_facts_to_gate_input(
        PersonalCapacityFactsGateResult(
            state=PC_CONSTRAINED, blocked=False, explanations=["x"],
        )
    )
    assert_equal(
        "pc_constrained_ceiling", pc_constrained_input.posture_ceiling, CONSERVE,
    )

    pc_not_measurable_input = personal_capacity_facts_to_gate_input(
        PersonalCapacityFactsGateResult(
            state=PC_NOT_MEASURABLE, blocked=False, explanations=["x"],
        )
    )
    assert_equal(
        "pc_not_measurable_ceiling", pc_not_measurable_input.posture_ceiling, CONSERVE,
    )

    pc_blocked_input = personal_capacity_facts_to_gate_input(
        PersonalCapacityFactsGateResult(
            state=PC_CONSTRAINED,
            blocked=True,
            explanations=["hard block: emergency_reserve_adequate"],
        )
    )
    assert_equal("pc_blocked_propagates", pc_blocked_input.blocked, True)
    assert_contains(
        "pc_blocked_explanation_reaches_input",
        pc_blocked_input.explanations,
        "hard block: emergency_reserve_adequate",
    )

    assert_raises(
        "unknown_personal_capacity_state_raises",
        lambda: personal_capacity_facts_to_gate_input(
            PersonalCapacityFactsGateResult(
                state="made up", blocked=False, explanations=[],
            )
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

    # -- Combined posture with Personal Capacity Facts, RE-040.1 --

    # personal_capacity_facts_result omitted (None): must behave exactly
    # as before RE-040.1 -- no ghost gate, no change to existing results.
    omitted_matches_two_gate_call = evaluate_capital_posture(
        EvidenceQualityGateResult(state=EQ_NOT_MEASURABLE, explanations=["eq unmeasured"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
    )
    assert_equal(
        "personal_capacity_omitted_ceiling",
        omitted_matches_two_gate_call.posture_ceiling,
        PREPARE,
    )

    # All three present, facts adequate: facts gate imposes no
    # restriction of its own -- weakest gate (Evidence Quality,
    # not measurable) still determines the ceiling.
    three_gates_facts_adequate = evaluate_capital_posture(
        EvidenceQualityGateResult(state=EQ_NOT_MEASURABLE, explanations=["eq unmeasured"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
        PersonalCapacityFactsGateResult(
            state=PC_ADEQUATE, blocked=False, explanations=["all nine facts adequate"],
        ),
    )
    assert_equal(
        "three_gates_facts_adequate_ceiling",
        three_gates_facts_adequate.posture_ceiling,
        PREPARE,
    )

    # Facts gate constrained: becomes the binding (weakest) gate.
    three_gates_facts_constrained = evaluate_capital_posture(
        EvidenceQualityGateResult(state=CONSERVATIVE, explanations=["eq conservative"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
        PersonalCapacityFactsGateResult(
            state=PC_CONSTRAINED,
            blocked=False,
            explanations=["debt_service_manageable: confirmed breach"],
        ),
    )
    assert_equal(
        "three_gates_facts_constrained_ceiling",
        three_gates_facts_constrained.posture_ceiling,
        CONSERVE,
    )

    # Emergency reserve breach: hard block overrides everything,
    # regardless of how favorable the other two gates are.
    reserve_breach_blocks_everything = evaluate_capital_posture(
        EvidenceQualityGateResult(state=CONSERVATIVE, explanations=["eq conservative"]),
        RegimeComparabilityGateResult(state=COMPARABLE, explanations=["regime comparable"]),
        PersonalCapacityFactsGateResult(
            state=PC_CONSTRAINED,
            blocked=True,
            explanations=["hard block: emergency_reserve_adequate"],
        ),
    )
    assert_equal(
        "reserve_breach_blocks_everything_ceiling",
        reserve_breach_blocks_everything.posture_ceiling,
        BLOCKED,
    )
    assert_contains(
        "reserve_breach_explanation_visible",
        reserve_breach_blocks_everything.explanations,
        "Personal Capacity Facts: hard block: emergency_reserve_adequate",
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
    print(" Personal Capacity Facts (RE-032.5/RE-040.1) excluded from this")
    print(" dry-run -- no real data source exists for any of its nine")
    print(" facts; attested-judgement/Human Approval (RE-032.4) excluded")
    print(" always, has no code -- see engine/posture_mapper.py docstring)")
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
