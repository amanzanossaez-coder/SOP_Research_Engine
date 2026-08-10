"""
SOP Research Engine
Capital Posture Audit -- standalone CLI

RE-039.1 -- extrae, sin cambios de logica, el bloque de "audit dry-run"
que ya vivia dentro de tests/verify_posture_mapper.py (lineas 182-219)
a un script propio. Objetivo: poder consultar donde caen hoy los gates
sin tener que correr la suite de tests completa.

RE-043.1 -- Evidence Quality y Regime Comparability son senales de
mercado, compartidas por todos los patrimonios; se calculan una sola
vez. Personal Capacity Facts es, por decision explicita de Armando,
independiente por patrimonio -- nunca fusionado. Por eso este script
ahora produce una postura combinada POR PATRIMONIO (una por cada
pestaña de data/raw/personal_capacity_facts.xlsx), no una unica postura
global.

RE-041.5 -- añade, por patrimonio, el dry-run de Dry Powder Protocol:
la postura combinada de arriba mas engine/dry_powder_ledger_state.py
(que ya cruza engine/live_episode.py con data/raw/dry_powder_ledger.xlsx)
se ensamblan en un DryPowderProtocolInputs real y se evaluan. Hoy no
hay ningun episodio activo (RE-041.2), asi que esto imprime
"not evaluated" para ambos patrimonios -- el valor de esta iteracion es
que la tuberia completa queda demostrada end-to-end, no que produzca
una cifra hoy.

Esto NO es el Capital Posture Engine -- no existe tal componente.
Esto NO es una herramienta de decision -- es un dry-run de lectura, no
esta conectado a run.py ni a DecisionEngine. El resultado es, en el
mejor caso, tan permisivo o mas que la postura real -- nunca menos: el
canal de juicio atestiguado y Human Approval (RE-032.4) siguen sin
codigo y nunca participan aqui -- human_approval_above_ceiling se pasa
siempre como False, nunca asumido True.
"""

from engine.dry_powder_ledger_state import (
    build_local_dry_powder_ledger_state,
    to_dry_powder_protocol_inputs,
)
from engine.dry_powder_protocol import DryPowderProtocol
from engine.evidence_quality_gate import (
    EvidenceQualityGate,
    GlobalModelValidationState,
    PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    build_local_evidence_quality_inputs,
)
from engine.personal_capacity_facts_gate import (
    PersonalCapacityFactsGate,
    build_local_personal_capacity_facts_inputs,
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

    print("=" * 70)
    print("SOP RESEARCH ENGINE")
    print("CAPITAL POSTURE AUDIT -- read-only dry-run")
    print("=" * 70)
    print()
    print("NOT a decision. NOT wired into run.py or DecisionEngine.")
    print("Attested-judgement / Human Approval channel (RE-032.4) has no")
    print("code and never participates here. Result is, at best, no more")
    print("restrictive than the real posture -- never less.")
    print()
    print(f"predictive_validation_status used: {PREDICTIVE_VALIDATION_NOT_DEMONSTRATED}")
    print("  (reflects RE-PRED.16's confirmed finding -- not automatic)")
    print()
    print(f"Evidence Quality state: {eq_result.state}")
    print(f"Evidence Quality explanations: {eq_result.explanations}")
    print()
    print(f"Regime Comparability state: {regime_result.state}")
    print(f"Regime Comparability explanations: {regime_result.explanations}")

    personal_capacity_inputs = build_local_personal_capacity_facts_inputs()

    if personal_capacity_inputs is None:
        print()
        print("Personal Capacity Facts: data/raw/personal_capacity_facts.xlsx")
        print("not found -- combined posture below excludes it, same as")
        print("before RE-043.1.")
        combined = evaluate_capital_posture(eq_result, regime_result)
        print()
        print(f"COMBINED posture ceiling: {combined.posture_ceiling}")
        print(f"COMBINED explanations: {combined.explanations}")
        return

    pc_gate = PersonalCapacityFactsGate()

    ledger_states = build_local_dry_powder_ledger_state()

    for patrimonio_name, pc_local in personal_capacity_inputs.items():

        pc_result = pc_gate.evaluate(pc_local)
        combined = evaluate_capital_posture(
            eq_result, regime_result, pc_result
        )

        print()
        print("-" * 70)
        print(f"PATRIMONIO: {patrimonio_name}")
        print("-" * 70)
        print(f"Personal Capacity Facts state: {pc_result.state}")
        print(f"Personal Capacity Facts blocked: {pc_result.blocked}")
        print(f"Personal Capacity Facts explanations: {pc_result.explanations}")
        print()
        print(f"COMBINED posture ceiling ({patrimonio_name}): {combined.posture_ceiling}")
        print(f"COMBINED explanations ({patrimonio_name}): {combined.explanations}")

        ledger_state = (
            ledger_states.get(patrimonio_name) if ledger_states else None
        )

        print()
        if ledger_state is None:
            print(
                f"Dry Powder Ledger ({patrimonio_name}): "
                "data/raw/dry_powder_ledger.xlsx not found."
            )
            continue

        print(f"Dry Powder Ledger state ({patrimonio_name}): {ledger_state}")

        dp_inputs = to_dry_powder_protocol_inputs(
            ledger_state,
            combined.posture_ceiling,
            human_approval_above_ceiling=False,
        )

        if dp_inputs is None:
            print(
                f"Dry Powder Protocol ({patrimonio_name}): not evaluated "
                f"-- {ledger_state.explanations}"
            )
            continue

        dp_result = DryPowderProtocol().evaluate(dp_inputs)

        print(f"Dry Powder Protocol status ({patrimonio_name}): {dp_result.status}")
        print(
            f"Dry Powder Protocol authorized_amount ({patrimonio_name}): "
            f"{dp_result.authorized_amount}"
        )
        print(f"Dry Powder Protocol reason ({patrimonio_name}): {dp_result.reason}")


if __name__ == "__main__":
    main()
