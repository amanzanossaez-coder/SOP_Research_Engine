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


def evaluate_capital_posture(
    evidence_quality_result: EvidenceQualityGateResult,
    regime_comparability_result: RegimeComparabilityGateResult,
) -> GateCombinationResult:
    """
    RE-037.1 -- combina los dos gates reales que existen hoy en una
    unica postura de capital, aplicando exactamente las tablas ya
    documentadas (RE-034.1, RE-034.5) sobre
    engine/gate_combination.py sin modificarlo.

    Esto NO es el "Capital Posture Engine" referenciado en otras partes
    de este documento como componente futuro y operativo. Es una capa
    de composicion aislada, pensada para auditoria/dry-run -- no decide
    nada por si sola, no se conecta a run.py ni a DecisionEngine, y no
    persiste ni ejecuta ninguna accion sobre capital real.

    Personal Capacity NO participa en esta combinacion: RE-032.1 no lo
    ha clasificado todavia (gate paralelo, prerequisito de aprobacion
    humana o control mixto) y no existe como gate ejecutable. La
    postura que devuelve esta funcion es, por construccion, optimista
    respecto a lo que devolveria una combinacion completa una vez
    Personal Capacity exista -- esta ausencia se expone explicitamente
    aqui, no se oculta ni se compensa con un placeholder inventado.
    """

    inputs = [
        evidence_quality_to_gate_input(evidence_quality_result),
        regime_comparability_to_gate_input(regime_comparability_result),
    ]

    return combine_gate_outputs(inputs)
