from engine.evidence_quality_gate import (
    CONSERVATIVE as EVIDENCE_QUALITY_CONSERVATIVE,
    NOT_MEASURABLE as EVIDENCE_QUALITY_NOT_MEASURABLE,
    EvidenceQualityGateResult,
)
from engine.gate_combination import (
    CONSERVE,
    DEPLOY_AGGRESSIVELY,
    PREPARE,
    GateCombinationInput,
    GateCombinationResult,
    combine_gate_outputs,
)
from engine.regime_comparability_gate import (
    COMPARABLE,
    NOT_COMPARABLE,
    NOT_MEASURABLE as REGIME_COMPARABILITY_NOT_MEASURABLE,
    RegimeComparabilityGateResult,
)
from engine.personal_capacity_facts_gate import (
    ADEQUATE as PERSONAL_CAPACITY_FACTS_ADEQUATE,
    CONSTRAINED as PERSONAL_CAPACITY_FACTS_CONSTRAINED,
    NOT_MEASURABLE as PERSONAL_CAPACITY_FACTS_NOT_MEASURABLE,
    PersonalCapacityFactsGateResult,
)


# RE-037.1 -- tablas ya documentadas (RE-034.1, RE-034.5), traducidas
# aqui a codigo por primera vez. No se decide ningun mapeo nuevo en
# este archivo: cada entrada debe poder señalarse a la seccion del
# status doc que la autorizo.
EVIDENCE_QUALITY_POSTURE_CEILING = {
    EVIDENCE_QUALITY_NOT_MEASURABLE: PREPARE,
    EVIDENCE_QUALITY_CONSERVATIVE: CONSERVE,
}

REGIME_COMPARABILITY_POSTURE_CEILING = {
    REGIME_COMPARABILITY_NOT_MEASURABLE: CONSERVE,
    NOT_COMPARABLE: CONSERVE,
    COMPARABLE: DEPLOY_AGGRESSIVELY,
}

# RE-040.1 -- table for the newly-coded half of Personal Capacity
# (RE-032.5's facts gate only; the attested-judgement/Human Approval
# channel from RE-032.4 has no code and is not represented here).
#
# `adequate -> Deploy Aggressively` does NOT mean "authorizes an
# aggressive deployment" -- it means this gate imposes no restriction
# of its own, same reading already established for Regime
# Comparability's `comparable -> Deploy Aggressively` (RE-034.5). The
# actual ceiling, if any, comes from whichever gate is genuinely
# restrictive; min() in combine_gate_outputs() enforces that.
PERSONAL_CAPACITY_FACTS_POSTURE_CEILING = {
    PERSONAL_CAPACITY_FACTS_NOT_MEASURABLE: CONSERVE,
    PERSONAL_CAPACITY_FACTS_CONSTRAINED: CONSERVE,
    PERSONAL_CAPACITY_FACTS_ADEQUATE: DEPLOY_AGGRESSIVELY,
}


def evidence_quality_to_gate_input(
    result: EvidenceQualityGateResult,
) -> GateCombinationInput:
    """
    RE-037.1 -- traduce un EvidenceQualityGateResult ya calculado a
    GateCombinationInput, segun la tabla de RE-034.1. No reevalua ni
    reimplementa la logica del gate -- solo decide el posture_ceiling
    que le corresponde a un estado ya producido por
    EvidenceQualityGate.evaluate().

    blocked=False siempre: EvidenceQualityGate no tiene hoy ningun
    mecanismo de veto -- inventarlo aqui seria una decision de
    gobernanza nueva, fuera de alcance de esta iteracion.
    """

    posture_ceiling = EVIDENCE_QUALITY_POSTURE_CEILING.get(result.state)

    if posture_ceiling is None:
        raise ValueError(
            f"Evidence Quality state {result.state!r} has no documented "
            "posture-ceiling mapping (RE-034.1)"
        )

    return GateCombinationInput(
        gate_name="Evidence Quality",
        internal_state=result.state,
        posture_ceiling=posture_ceiling,
        blocked=False,
        explanations=list(result.explanations),
    )


def regime_comparability_to_gate_input(
    result: RegimeComparabilityGateResult,
) -> GateCombinationInput:
    """
    RE-037.1 -- misma traduccion para Regime Comparability, segun la
    tabla de RE-034.5.
    """

    posture_ceiling = REGIME_COMPARABILITY_POSTURE_CEILING.get(result.state)

    if posture_ceiling is None:
        raise ValueError(
            f"Regime Comparability state {result.state!r} has no "
            "documented posture-ceiling mapping (RE-034.5)"
        )

    return GateCombinationInput(
        gate_name="Regime Comparability",
        internal_state=result.state,
        posture_ceiling=posture_ceiling,
        blocked=False,
        explanations=list(result.explanations),
    )


def personal_capacity_facts_to_gate_input(
    result: PersonalCapacityFactsGateResult,
) -> GateCombinationInput:
    """
    RE-040.1 -- traduce un PersonalCapacityFactsGateResult ya calculado
    a GateCombinationInput, segun la tabla de este mismo archivo. No
    reevalua ni reimplementa la logica del gate.

    blocked se propaga directo desde result.blocked (RE-032.5's
    emergency_reserve_adequate hard block, hoy el unico) -- no se
    reinterpreta. explanations se copia integra desde result.explanations,
    que ya incluye la razon del bloqueo cuando blocked=True (p.ej.
    "hard block: emergency_reserve_adequate") -- sin esto, un veto
    llegaria opaco a la capa de combinacion.
    """

    posture_ceiling = PERSONAL_CAPACITY_FACTS_POSTURE_CEILING.get(
        result.state
    )

    if posture_ceiling is None:
        raise ValueError(
            f"Personal Capacity Facts state {result.state!r} has no "
            "documented posture-ceiling mapping (RE-040.1)"
        )

    return GateCombinationInput(
        gate_name="Personal Capacity Facts",
        internal_state=result.state,
        posture_ceiling=posture_ceiling,
        blocked=result.blocked,
        explanations=list(result.explanations),
    )


def evaluate_capital_posture(
    evidence_quality_result: EvidenceQualityGateResult,
    regime_comparability_result: RegimeComparabilityGateResult,
    personal_capacity_facts_result: PersonalCapacityFactsGateResult | None = None,
) -> GateCombinationResult:
    """
    RE-037.1 -- combina los gates reales que existen hoy en una unica
    postura de capital, aplicando exactamente las tablas ya
    documentadas (RE-034.1, RE-034.5, RE-040.1) sobre
    engine/gate_combination.py sin modificarlo.

    Esto NO es el "Capital Posture Engine" referenciado en otras partes
    de este documento como componente futuro y operativo. Es una capa
    de composicion aislada, pensada para auditoria/dry-run -- no decide
    nada por si sola, no se conecta a run.py ni a DecisionEngine, y no
    persiste ni ejecuta ninguna accion sobre capital real.

    RE-040.1 -- personal_capacity_facts_result es OPCIONAL (default
    None). Si no se aporta, no se añade ningun input a la combinacion
    -- nunca se inventa un gate fantasma con un valor por defecto. Si
    se aporta, participa en la combinacion via min() como cualquier
    otro gate.

    Aun cuando se aporte, el resultado sigue siendo, por construccion,
    optimista: el canal de juicio atestiguado y el boundary de Human
    Approval (RE-032.4) no tienen codigo y nunca se calculan -- solo la
    mitad computable de Personal Capacity (RE-032.5) puede participar
    aqui. Esta ausencia se expone explicitamente, no se oculta ni se
    compensa con un placeholder inventado.
    """

    inputs = [
        evidence_quality_to_gate_input(evidence_quality_result),
        regime_comparability_to_gate_input(regime_comparability_result),
    ]

    if personal_capacity_facts_result is not None:
        inputs.append(
            personal_capacity_facts_to_gate_input(
                personal_capacity_facts_result
            )
        )

    return combine_gate_outputs(inputs)
