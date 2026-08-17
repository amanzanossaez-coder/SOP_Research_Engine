"""
SOP Research Engine
Kernel assembly layer -- read-only

Read-only kernel assembly layer.

This is not the full SOP Kernel described in CONSTITUTION.md.
It only centralizes the currently implemented K4/governance fragments:
Evidence Quality, Regime Comparability, Personal Capacity Facts,
Human Approval state and Dry Powder state.

It does not implement K1/K2/K3/K5/K6.
It does not execute decisions.
It is not wired to run.py or DecisionEngine.

RE-KERNEL.1 -- Armando, on unifying the Kernel: "extraer lo que ya
existe a un modulo" (not designing K1/K2/K3/K5/K6, which have zero
spec today -- CONSTITUTION.md Section 5 lists them as prose, not
code). This module is a pure extraction of the orchestration logic
that already lived inline inside audit_posture.py (RE-039.1 through
RE-C) -- zero new decision logic, zero behavior change. Verified by
diffing audit_posture.py's stdout before and after this refactor:
byte-identical (see governance doc for the exact diff command run).

Return-value contract (Armando's review, RE-KERNEL.1): the second
element of build_kernel_results()'s return tuple is None for exactly
one reason -- data/raw/personal_capacity_facts.xlsx cannot be found,
meaning no per-patrimonio audit can be built at all. Every other
missing-data case (no Human Approval attestation for a given
patrimonio, no Dry Powder ledger, no active episode) is NOT
represented by collapsing the whole result to None -- it surfaces as
a populated KernelPatrimonioResult with the affected field set to
None, exactly as audit_posture.py already printed it before this
refactor (fail-closed per field, not fail-closed for the whole
audit).

Deviation from the literal design text Armando approved, flagged
explicitly rather than silently applied: the original proposal had
build_kernel_results() return a single bare `None` for the whole
tuple when the facts file is missing. That would have been wrong --
audit_posture.py's current behavior in that exact branch still prints
Evidence Quality and Regime Comparability (they never depended on
personal_capacity_facts.xlsx) plus a combined posture computed from
just those two. A bare None would have thrown away information the
script currently reports and broken the "identical output"
acceptance criterion Armando set. So only the per-patrimonio half can
be None; KernelMarketResult is always returned.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from engine.dry_powder_ledger_state import (
    LedgerEpisodeState,
    build_local_dry_powder_ledger_state,
    to_dry_powder_protocol_inputs,
)
from engine.dry_powder_protocol import DryPowderProtocol, DryPowderProtocolResult
from engine.evidence_quality_gate import (
    EvidenceQualityGate,
    EvidenceQualityGateResult,
    GlobalModelValidationState,
    PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    build_local_evidence_quality_inputs,
)
from engine.gate_combination import GateCombinationResult
from engine.human_approval import HumanApprovalGate, HumanApprovalResult
from engine.human_approval_state import build_local_human_approval_inputs
from engine.personal_capacity_facts_gate import (
    PersonalCapacityFactsGate,
    PersonalCapacityFactsGateResult,
    build_local_personal_capacity_facts_inputs,
)
from engine.posture_mapper import evaluate_capital_posture
from engine.regime_comparability_gate import (
    RegimeComparabilityGate,
    RegimeComparabilityGateResult,
    build_local_regime_comparability_inputs,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine


@dataclass
class KernelMarketResult:
    """
    Shared across all patrimonios -- computed once, same market
    signals for everyone. Mirrors audit_posture.py's eq_result/
    regime_result, unchanged. Never depends on
    personal_capacity_facts.xlsx.

    combined_posture_without_personal_capacity mirrors the original
    script's fallback `evaluate_capital_posture(eq_result,
    regime_result)` call (no third, per-patrimonio argument) -- only
    ever printed by audit_posture.py in the branch where
    personal_capacity_facts.xlsx is missing (see build_kernel_results()
    docstring). Computed unconditionally here, not only inside that
    branch, so this dataclass alone -- without re-deriving any gate
    logic in the wrapper -- can reproduce either branch's output.
    """

    evidence_quality_result: EvidenceQualityGateResult
    regime_comparability_result: RegimeComparabilityGateResult
    combined_posture_without_personal_capacity: GateCombinationResult


@dataclass
class KernelPatrimonioResult:
    """
    One per patrimonio (one sheet in personal_capacity_facts.xlsx).
    Optional fields are None exactly when audit_posture.py printed a
    "not found" / "not evaluated" message for that piece -- never
    inferred, never defaulted to a favorable value. The reason for a
    None is always recoverable from the sibling field already on this
    object (e.g. dry_powder_ledger_state.explanations when
    dry_powder_result is None but dry_powder_ledger_state is not) --
    no separate "reason" field, to avoid a second copy of the same
    fact that could drift from the first.
    """

    patrimonio_name: str
    personal_capacity_result: PersonalCapacityFactsGateResult
    combined_posture: GateCombinationResult
    human_approval_result: Optional[HumanApprovalResult]
    dry_powder_ledger_state: Optional[LedgerEpisodeState]
    dry_powder_result: Optional[DryPowderProtocolResult]


def build_kernel_results() -> Tuple[
    KernelMarketResult, Optional[Dict[str, KernelPatrimonioResult]]
]:
    """
    RE-KERNEL.1 -- pure extraction of audit_posture.py's orchestration
    (RE-039.1 through RE-C), zero logic change. See module docstring
    for the exact None contract and the one deliberate deviation from
    the literal originally-approved signature.
    """

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

    market = KernelMarketResult(
        evidence_quality_result=eq_result,
        regime_comparability_result=regime_result,
        combined_posture_without_personal_capacity=evaluate_capital_posture(
            eq_result, regime_result
        ),
    )

    personal_capacity_inputs = build_local_personal_capacity_facts_inputs()

    if personal_capacity_inputs is None:
        return market, None

    pc_gate = PersonalCapacityFactsGate()

    ledger_states = build_local_dry_powder_ledger_state()
    human_approval_inputs = build_local_human_approval_inputs()
    human_approval_gate = HumanApprovalGate()

    by_patrimonio: Dict[str, KernelPatrimonioResult] = {}

    for patrimonio_name, pc_local in personal_capacity_inputs.items():

        pc_result = pc_gate.evaluate(pc_local)
        combined = evaluate_capital_posture(eq_result, regime_result, pc_result)

        ha_inputs = (
            human_approval_inputs.get(patrimonio_name)
            if human_approval_inputs
            else None
        )
        # RE-C -- default fail-closed, same as before: absence of a
        # Human Approval result never becomes an assumed
        # authorization.
        ha_result = (
            human_approval_gate.evaluate(ha_inputs) if ha_inputs is not None else None
        )

        ledger_state = ledger_states.get(patrimonio_name) if ledger_states else None

        dp_result = None
        if ledger_state is not None:
            human_approval_above_ceiling = (
                ha_result.authorizes_dry_powder_ceiling_90
                if ha_result is not None
                else False
            )
            dp_inputs = to_dry_powder_protocol_inputs(
                ledger_state,
                combined.posture_ceiling,
                human_approval_above_ceiling=human_approval_above_ceiling,
            )
            if dp_inputs is not None:
                dp_result = DryPowderProtocol().evaluate(dp_inputs)

        by_patrimonio[patrimonio_name] = KernelPatrimonioResult(
            patrimonio_name=patrimonio_name,
            personal_capacity_result=pc_result,
            combined_posture=combined,
            human_approval_result=ha_result,
            dry_powder_ledger_state=ledger_state,
            dry_powder_result=dp_result,
        )

    return market, by_patrimonio
