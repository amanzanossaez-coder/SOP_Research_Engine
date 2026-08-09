"""
SOP Research Engine
Personal Capacity -- verifiable-facts gate

RE-032.5 -- first isolated code for the computable half of Personal
Capacity's mixed control (RE-032.2). Covers only the nine
verifiable-facts categories defined in RE-032.3. The attested-judgement
channel and Human Approval procedural boundary (RE-032.4) are entirely
separate and are not represented here -- that channel is never
computed, by design.

Honest limitation, stated rather than hidden: unlike EvidenceQualityGate
and RegimeComparabilityGate, this gate has no build_local_*_inputs()
function and no real-pipeline data source. No fact in RE-032.3's list
is tracked anywhere inside this repository -- all nine live in
Armando's own accounting / SOP ledger, outside the Research Engine's
scope. Only synthetic verification is possible until that changes.

Not wired into run.py, DecisionEngine, posture_mapper.py or
gate_combination.py. That integration is explicitly future work
(RE-040.x per the roadmap agreed this session), not this iteration.
"""

from dataclasses import dataclass, field


NOT_MEASURABLE = "not measurable"
ADEQUATE = "adequate"
CONSTRAINED = "constrained"


# Field order also defines explanation/ordering in results below.
FACT_FIELDS = [
    "liquidity_adequate",
    "near_term_cash_needs_covered",
    "fixed_obligations_manageable",
    "debt_service_manageable",
    "income_concentration_acceptable",
    "portfolio_concentration_acceptable",
    "emergency_reserve_adequate",
    "time_horizon_constraints_covered",
    "fiscal_operational_constraints_manageable",
]

# Provisional decision (RE-032.5): only this field produces a hard
# `blocked` veto. Every other failed fact only degrades `state` to
# CONSTRAINED. Whether additional facts should become hard blockers,
# and on what principle, is left open for a future iteration -- not
# decided by ad hoc expansion here.
HARD_BLOCK_FIELDS = ["emergency_reserve_adequate"]


@dataclass
class LocalPersonalCapacityFactsInputs:
    """
    Pre-computed local inputs, one per RE-032.3 verifiable-facts
    category. Uniform positive polarity throughout: True = adequate /
    acceptable / covered / manageable, False = fact confirmed to
    breach, None = not measured / not provided. A missing fact is
    never treated as favorable (fail-closed, same principle as
    EvidenceQualityGate and RegimeComparabilityGate).

    This gate does not compute these booleans itself -- whatever
    process determines, e.g., whether liquidity is "adequate" against
    Armando's own thresholds happens entirely outside this repository.
    """

    liquidity_adequate: bool | None = None
    near_term_cash_needs_covered: bool | None = None
    fixed_obligations_manageable: bool | None = None
    debt_service_manageable: bool | None = None
    income_concentration_acceptable: bool | None = None
    portfolio_concentration_acceptable: bool | None = None
    emergency_reserve_adequate: bool | None = None
    time_horizon_constraints_covered: bool | None = None
    fiscal_operational_constraints_manageable: bool | None = None


@dataclass
class PersonalCapacityFactsGateResult:
    """
    `state` is this gate's own graded read of all nine facts. `blocked`
    is an orthogonal veto signal, specific to hard-block fields
    (currently only emergency_reserve_adequate) -- it does not replace
    or collapse into `state`. A blocked result can, and typically will,
    also carry state=CONSTRAINED; state is never set to the string
    "Blocked" -- that value belongs only to
    engine/gate_combination.py's BLOCKED constant, consumed by a future
    translator (RE-040.x), not produced here.
    """

    state: str
    blocked: bool
    failed_fields: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    blocking_fields: list[str] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)


class PersonalCapacityFactsGate:

    def evaluate(
        self,
        local: LocalPersonalCapacityFactsInputs,
    ) -> PersonalCapacityFactsGateResult:

        values = {
            name: getattr(local, name)
            for name in FACT_FIELDS
        }

        failed_fields = [
            name for name in FACT_FIELDS
            if values[name] is False
        ]

        missing_fields = [
            name for name in FACT_FIELDS
            if values[name] is None
        ]

        blocking_fields = [
            name for name in HARD_BLOCK_FIELDS
            if values[name] is False
        ]

        blocked = bool(blocking_fields)

        if failed_fields:
            state = CONSTRAINED
        elif missing_fields:
            state = NOT_MEASURABLE
        else:
            state = ADEQUATE

        explanations = []

        for name in failed_fields:
            explanations.append(f"{name}: confirmed breach")

        for name in missing_fields:
            explanations.append(f"{name}: not measured")

        if blocked:
            explanations.append(
                f"hard block: {', '.join(blocking_fields)}"
            )

        if not explanations:
            explanations.append("all nine facts adequate")

        return PersonalCapacityFactsGateResult(
            state=state,
            blocked=blocked,
            failed_fields=failed_fields,
            missing_fields=missing_fields,
            blocking_fields=blocking_fields,
            explanations=explanations,
        )
