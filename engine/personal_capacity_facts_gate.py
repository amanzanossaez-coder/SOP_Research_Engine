"""
SOP Research Engine
Personal Capacity -- verifiable-facts gate

RE-032.5 -- first isolated code for the computable half of Personal
Capacity's mixed control (RE-032.2). Covers only the nine
verifiable-facts categories defined in RE-032.3. The attested-judgement
channel and Human Approval procedural boundary (RE-032.4) are entirely
separate and are not represented here -- that channel is never
computed, by design.

RE-043.1 adds the first real-pipeline adapter,
build_local_personal_capacity_facts_inputs(), reading
data/raw/personal_capacity_facts.xlsx via
loaders/personal_capacity_facts_loader.py. Unlike
build_local_evidence_quality_inputs() or
build_local_regime_comparability_inputs(), this adapter's source is an
operator-maintained spreadsheet, not an in-memory pipeline object --
the loader/gate split mirrors loaders/shiller_loader.py +
engine/drawdown_engine.py for that reason: raw file I/O stays out of
this module.

Not every field this gate consumes is a mechanically computed fact.
FIELD_INPUT_TYPES records, per field, whether it is COMPUTED from other
recorded figures, an OPERATOR_FACT entered directly because no formula
exists (e.g. debt service), or an OPERATOR_JUDGMENT -- a structured
call the operator makes visible in the same spreadsheet (e.g. income
concentration), grounded in criteria the operator can see, but not a
declared preference subject to the emotional-revision risk RE-032.4's
attested channel exists to guard against. Recording this taxonomy
exists specifically so that, months from now, an OPERATOR_JUDGMENT
boolean is never mistaken for a mechanically verified one.

RE-043.4 -- corrects a stale claim left over from this module's
original RE-032.5 header: this gate has been wired into
gate_combination.py since RE-040.1, via
engine/posture_mapper.py::personal_capacity_facts_to_gate_input() and
evaluate_capital_posture(), which translate a
PersonalCapacityFactsGateResult into a GateCombinationInput and feed it
into combine_gate_outputs()'s min() alongside Evidence Quality and
Regime Comparability. RE-043.1 then wired real data into that path.
audit_posture.py exercises this end-to-end on every run. Still not
wired into run.py or DecisionEngine -- that remains explicit future
work, not this iteration.
"""

from dataclasses import dataclass, field
from pathlib import Path

from loaders.personal_capacity_facts_loader import (
    load_personal_capacity_facts_raw,
)


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


# RE-043.1 -- taxonomy condition Armando required before green-lighting
# the real adapter: every field's provenance must be visible, or every
# boolean will look equally "objective" to a future reader. Three
# kinds, not two -- collapsing OPERATOR_JUDGMENT into the same bucket
# as RE-032.4's attested channel would drag in machinery (cooling-off,
# 90-day validity) built for a different risk (self-interested revision
# under emotional stress) that does not apply to a structured analytical
# call like income concentration.
COMPUTED = "computed"
OPERATOR_FACT = "operator_fact"
OPERATOR_JUDGMENT = "operator_judgment"

FIELD_INPUT_TYPES = {
    "liquidity_adequate": COMPUTED,
    "near_term_cash_needs_covered": COMPUTED,
    # v1 alias of near_term_cash_needs_covered, not an independent
    # check -- Armando's own clarification that "obligaciones fijas"
    # means annual expenses, the same figure already driving the
    # near-term-cash-needs test. See RE-043.1.
    "fixed_obligations_manageable": COMPUTED,
    "debt_service_manageable": OPERATOR_FACT,
    "income_concentration_acceptable": OPERATOR_JUDGMENT,
    "portfolio_concentration_acceptable": OPERATOR_JUDGMENT,
    "emergency_reserve_adequate": COMPUTED,
    "time_horizon_constraints_covered": OPERATOR_FACT,
    "fiscal_operational_constraints_manageable": OPERATOR_FACT,
}

assert set(FIELD_INPUT_TYPES) == set(FACT_FIELDS), (
    "FIELD_INPUT_TYPES must document every FACT_FIELDS entry, and only "
    "those entries -- kept in sync deliberately, not by convention."
)


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


# RE-043.1 -- exact "Concepto" text each field is read from. Any sheet
# missing a label produces None for that field (fail-closed: a missing
# label is exactly as unmeasured as a blank cell, never inferred as
# favorable). Any future patrimonio tab only needs to reuse these
# labels for the fields it wants measured -- everything else in that
# sheet (extra breakdown rows, notes, particularities) is free to
# differ, per Armando's requirement.
REQUIRED_LABELS = {
    "gasto_anual": "Gasto anual estimado",
    "ingresos_recurrentes": "Ingresos recurrentes anuales",
    "colchon": "Colchón de seguridad mínimo (intocable)",
    "suelo_total_liquidez": "Suelo de liquidez total (mínimo óptimo)",
    "liquidez_total": "Liquidez total actual",
    "deuda": "Servicio de deuda manejable",
    "concentracion_ingresos": "Valoración cualitativa (concentración de ingresos)",
    "concentracion_cartera": "Valoración cualitativa (concentración de cartera)",
    "horizonte_evento": "Próximo evento con necesidad de liquidez conocida",
    "fiscal_pendiente": "Restricciones fiscales pendientes",
}

# Explicit tokens required for a "nothing known" cell to read True.
# Blank never does -- RE-043.1's fix to the earlier draft, where an
# empty cell silently meant favorable.
_NONE_KNOWN_TOKENS = {
    "horizonte_evento": {"ninguno conocido"},
    "fiscal_pendiente": {"ninguna conocida"},
}


def _to_bool_yesno(value):
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"sí", "si", "sí (fijo)", "si (fijo)", "true"}:
        return True
    if normalized in {"no", "false"}:
        return False
    return None


def _to_bool_judgment(value):
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized == "adecuado":
        return True
    if normalized in {"no adecuado", "inadecuado"}:
        return False
    return None



# "Pendiente" is this workbook's placeholder for "not filled in yet" --
# it must read as not-measured, exactly like a blank cell, never as
# confirmed content. Missing this was caught by the first real-pipeline
# run of this adapter: both new cells read "Pendiente" and were
# initially scored as "confirmed breach" instead of "not measured" --
# a bug in the honest direction (still conservative) but a dishonest
# explanation, exactly what RE-043.1's provenance requirement exists to
# prevent.
_PLACEHOLDER_TOKENS = {"pendiente"}


def _to_bool_explicit_none_token(value, none_tokens):
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized or normalized in _PLACEHOLDER_TOKENS:
        return None
    if normalized in none_tokens:
        return True
    return False


def _safe_ge(a, b):
    if a is None or b is None:
        return None
    return bool(a >= b)


def _or_optional(a, b):
    """
    Optional[bool] OR that never guesses. True if either side is
    confirmed True. False only if both sides are confirmed False.
    Anything else (an unresolved None on either side, with neither
    confirmed True) stays None -- an unknown cannot be allowed to
    collapse a real gap into a confirmed pass.
    """

    if a is True or b is True:
        return True
    if a is False and b is False:
        return False
    return None


def _build_single_patrimonio_inputs(concepto_map):

    def get(key):
        return concepto_map.get(REQUIRED_LABELS[key])

    gasto = get("gasto_anual")
    ingresos = get("ingresos_recurrentes")
    colchon = get("colchon")
    suelo_total = get("suelo_total_liquidez")
    liquidez_total = get("liquidez_total")

    liquidity_adequate = _safe_ge(liquidez_total, suelo_total)
    emergency_reserve_adequate = _safe_ge(liquidez_total, colchon)

    covered_by_income = _safe_ge(ingresos, gasto)
    covered_by_cushion = _safe_ge(liquidez_total, colchon)
    near_term_cash_needs_covered = _or_optional(
        covered_by_income, covered_by_cushion
    )

    return LocalPersonalCapacityFactsInputs(
        liquidity_adequate=liquidity_adequate,
        near_term_cash_needs_covered=near_term_cash_needs_covered,
        # RE-043.1 -- v1 alias of near_term_cash_needs_covered, not an
        # independent read. See FIELD_INPUT_TYPES's comment.
        fixed_obligations_manageable=near_term_cash_needs_covered,
        debt_service_manageable=_to_bool_yesno(get("deuda")),
        income_concentration_acceptable=_to_bool_judgment(
            get("concentracion_ingresos")
        ),
        portfolio_concentration_acceptable=_to_bool_judgment(
            get("concentracion_cartera")
        ),
        emergency_reserve_adequate=emergency_reserve_adequate,
        time_horizon_constraints_covered=_to_bool_explicit_none_token(
            get("horizonte_evento"), _NONE_KNOWN_TOKENS["horizonte_evento"]
        ),
        fiscal_operational_constraints_manageable=_to_bool_explicit_none_token(
            get("fiscal_pendiente"), _NONE_KNOWN_TOKENS["fiscal_pendiente"]
        ),
    )


def build_local_personal_capacity_facts_inputs(file_path=None):
    """
    RE-043.1 -- first real-pipeline adapter for Personal Capacity
    Facts. Reads data/raw/personal_capacity_facts.xlsx via
    loaders.personal_capacity_facts_loader (or a custom file_path, for
    tests) and returns {patrimonio_name: LocalPersonalCapacityFactsInputs},
    one independent entry per sheet -- per Armando's explicit decision
    that AMS and AML (and any future patrimonio) are evaluated as
    separate capital postures, never merged into one.

    Returns None if the workbook cannot be found, mirroring
    loaders/shiller_loader.py's own missing-file behaviour.
    """

    raw = load_personal_capacity_facts_raw(file_path)

    if raw is None:
        return None

    return {
        patrimonio_name: _build_single_patrimonio_inputs(concepto_map)
        for patrimonio_name, concepto_map in raw.items()
    }
