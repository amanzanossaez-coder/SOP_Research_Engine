"""
SOP Research Engine
Capital Posture Audit -- standalone CLI

RE-039.1 -- extrae, sin cambios de logica, el bloque de "audit dry-run"
que ya vivia dentro de tests/verify_posture_mapper.py (lineas 182-219)
a un script propio. Objetivo: poder consultar donde caen hoy los gates
sin tener que correr la suite de tests completa.

Esto NO es el Capital Posture Engine -- no existe tal componente.
Esto NO es una herramienta de decision -- es un dry-run de lectura,
no esta conectado a run.py ni a DecisionEngine, y excluye Personal
Capacity (ver engine/posture_mapper.py). El resultado es, en el mejor
caso, tan permisivo o mas que la postura real -- nunca menos.
"""

from engine.evidence_quality_gate import (
    EvidenceQualityGate,
    GlobalModelValidationState,
    PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    build_local_evidence_quality_inputs,
)
from engine.posture_mapper import evaluate_capital_posture
from engine.regime_comparability_gate import (
    RegimeComparabilityGate,
    build_local_regime_comparability_inputs,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine


def main() -> None:

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

    print("=" * 70)
    print("SOP RESEARCH ENGINE")
    print("CAPITAL POSTURE AUDIT -- read-only dry-run")
    print("=" * 70)
    print()
    print("NOT a decision. NOT wired into run.py or DecisionEngine.")
    print("Personal Capacity excluded -- see engine/posture_mapper.py")
    print("docstring. Result is, at best, no more restrictive than the")
    print("real posture -- never less.")
    print()
    print(f"predictive_validation_status used: {PREDICTIVE_VALIDATION_NOT_DEMONSTRATED}")
    print("  (reflects RE-PRED.16's confirmed finding -- not automatic)")
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
