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

RE-032.8 -- añade, por patrimonio, el dry-run de Human Approval
(engine/human_approval_state.py contra
data/raw/human_approval_attestations.xlsx). Impreso como bloque
SEPARADO, nunca mezclado con "COMBINED posture ceiling": RE-032.4
rule 1 es explicito -- Human Approval no es un gate puntuado y nunca
participa en evaluate_capital_posture()'s min() combination. Los dos
son prerrequisitos independientes: la postura combinada dice hasta
donde permiten los datos; Human Approval dice, por separado, si hay
consentimiento humano vigente para actuar en absoluto. Que "hay una
atestacion valida" y "esa atestacion autoriza superar el techo del
80%" son cosas distintas fue, desde RE-032.8, la razon explicita para
NO mapear una a la otra sin una regla propia -- human_approval_above_
ceiling se quedo hardcodeado en False hasta que esa regla existiera.

RE-C (RE-032.10 iteracion C) -- esa regla ya existe:
HumanApprovalResult.authorizes_dry_powder_ceiling_90, calculado por
HumanApprovalGate.evaluate() (nunca por este script). human_approval_
above_ceiling ya no esta hardcodeado -- se lee directamente de ese
campo cuando hay una atestacion registrada para el patrimonio, False
si no la hay (mismo fail-closed de siempre, nunca se asume autorizacion
por ausencia de dato). Ver engine/dry_powder_protocol.py (RE-C) para
como se usa ese booleano una vez dentro.

RE-KERNEL.1 -- este script deja de ser "el sitio donde vive la
logica" y pasa a ser solo una vista. Toda la orquestacion que vivia
aqui (RE-039.1 a RE-C) se extrajo tal cual, sin cambiar una sola
decision, a engine/kernel.py::build_kernel_results() -- ese modulo es
ahora la unica fuente de esta logica, importable desde cualquier otro
sitio (dashboard, Reporting futuro) sin duplicarla ni hacer scraping
de este stdout. Este archivo solo llama a esa funcion e imprime.
Verificado: salida de `python3 audit_posture.py` idéntica carácter a
carácter antes y después de este refactor (ver
docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md, RE-KERNEL.1).

Esto NO es el Capital Posture Engine -- no existe tal componente.
Esto NO es una herramienta de decision -- es un dry-run de lectura, no
esta conectado a run.py ni a DecisionEngine. El resultado es, en el
mejor caso, tan permisivo o mas que la postura real -- nunca menos.
"""

from engine.evidence_quality_gate import PREDICTIVE_VALIDATION_NOT_DEMONSTRATED
from engine.kernel import build_kernel_results


def main() -> None:

    market, by_patrimonio = build_kernel_results()

    print("=" * 70)
    print("SOP RESEARCH ENGINE")
    print("CAPITAL POSTURE AUDIT -- read-only dry-run")
    print("=" * 70)
    print()
    print("NOT a decision. NOT wired into run.py or DecisionEngine.")
    print("Human Approval (RE-032.4) is printed separately below, per")
    print("patrimonio -- it is not a scored gate and never blends into")
    print("COMBINED posture ceiling. Result is, at best, no more")
    print("restrictive than the real posture -- never less.")
    print()
    print(f"predictive_validation_status used: {PREDICTIVE_VALIDATION_NOT_DEMONSTRATED}")
    print("  (reflects RE-PRED.16's confirmed finding -- not automatic)")
    print()
    print(f"Evidence Quality state: {market.evidence_quality_result.state}")
    print(f"Evidence Quality explanations: {market.evidence_quality_result.explanations}")
    print()
    print(f"Regime Comparability state: {market.regime_comparability_result.state}")
    print(f"Regime Comparability explanations: {market.regime_comparability_result.explanations}")

    if by_patrimonio is None:
        print()
        print("Personal Capacity Facts: data/raw/personal_capacity_facts.xlsx")
        print("not found -- combined posture below excludes it, same as")
        print("before RE-043.1.")
        combined = market.combined_posture_without_personal_capacity
        print()
        print(f"COMBINED posture ceiling: {combined.posture_ceiling}")
        print(f"COMBINED explanations: {combined.explanations}")
        return

    for patrimonio_name, patrimonio in by_patrimonio.items():

        pc_result = patrimonio.personal_capacity_result
        combined = patrimonio.combined_posture

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

        print()
        ha_result = patrimonio.human_approval_result
        if ha_result is None:
            print(
                f"Human Approval ({patrimonio_name}): "
                "data/raw/human_approval_attestations.xlsx not found."
            )
        else:
            print(f"Human Approval state ({patrimonio_name}): {ha_result.state}")
            print(f"Human Approval blocked ({patrimonio_name}): {ha_result.blocked}")
            print(
                f"Human Approval effective_posture_ceiling ({patrimonio_name}): "
                f"{ha_result.effective_posture_ceiling}"
            )
            if ha_result.pending_increase is not None:
                print(
                    f"Human Approval pending_increase ({patrimonio_name}): "
                    f"{ha_result.pending_increase}"
                )
            print(
                f"Human Approval authorizes_dry_powder_ceiling_90 "
                f"({patrimonio_name}): {ha_result.authorizes_dry_powder_ceiling_90}"
            )
            print(f"Human Approval explanations ({patrimonio_name}): {ha_result.explanations}")
            print()
            print(
                f"NOTE ({patrimonio_name}): COMBINED posture ceiling above and "
                "Human Approval here are independent prerequisites -- capital "
                "action requires BOTH the combined ceiling to permit it AND "
                "Human Approval to be valid, per RE-032.4 rule 5. Neither is "
                "computed from the other."
            )

        ledger_state = patrimonio.dry_powder_ledger_state

        print()
        if ledger_state is None:
            print(
                f"Dry Powder Ledger ({patrimonio_name}): "
                "data/raw/dry_powder_ledger.xlsx not found."
            )
            continue

        print(f"Dry Powder Ledger state ({patrimonio_name}): {ledger_state}")

        dp_result = patrimonio.dry_powder_result

        if dp_result is None:
            print(
                f"Dry Powder Protocol ({patrimonio_name}): not evaluated "
                f"-- {ledger_state.explanations}"
            )
            continue

        print(f"Dry Powder Protocol status ({patrimonio_name}): {dp_result.status}")
        print(
            f"Dry Powder Protocol authorized_amount ({patrimonio_name}): "
            f"{dp_result.authorized_amount}"
        )
        print(f"Dry Powder Protocol reason ({patrimonio_name}): {dp_result.reason}")


if __name__ == "__main__":
    main()
