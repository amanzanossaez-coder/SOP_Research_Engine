"""
SOP Research Engine
RE-DASH.1 -- Static SOP/Shiller Audit Dashboard

Generates a single static HTML file (outputs/dashboard.html) that
makes the current state of the Research Engine and the SOP gates/
protocols visible, without changing anything about how they work.

Read-only, single command, no server:

    python3 generate_dashboard.py

Scope, confirmed with Armando 2026-08-15 (RE-DASH.1 spec, closed
after two rounds of correction):

-   Reuses the exact same pipeline audit_posture.py already exercises
    end-to-end (drawdown dataset -> ResearchEngine -> Evidence
    Quality / Regime Comparability / Personal Capacity Facts gates ->
    evaluate_capital_posture() -> Human Approval -> Dry Powder
    Protocol). This module computes nothing new -- it only collects
    the same results into a structure a template can render, instead
    of printing them.
-   Gates are ONLY Evidence Quality, Regime Comparability and Personal
    Capacity Facts -- the three that combine via min() in
    engine/gate_combination.py. Human Approval and Dry Powder Protocol
    are rendered as a separate "Prerrequisitos y protocolos" block:
    grouping Human Approval under "Gates" would contradict
    CONSTITUTION.md v2.0 Section 5 (Kernel), written the same day --
    Human Approval is never a scored gate and never enters that
    min() combination (RE-032.4 rule 1).
-   Personal Capacity Facts, Human Approval and Dry Powder Protocol
    are shown per patrimonio (AMS / AML), never fused into one
    combined state -- RE-043.1, "nunca fusionado". The header shows a
    single "Techo de mercado" figure, but that is Evidence Quality +
    Regime Comparability only -- both are market-wide signals,
    computed once, by explicit design (RE-043.1's own comment). It is
    not a fused per-patrimonio posture; Personal Capacity is what
    makes the real posture per-patrimonio, and that only appears
    inside each patrimonio's own block.
-   Historical evidence is a compact summary only: sample size,
    horizon, median/worst/best return, and the fixed
    `NOT_DEMONSTRATED` governance state. No top-10 matches table in
    v1 -- explicitly retired from this iteration's acceptance
    criteria (it was in the original DASH-001 draft; Armando removed
    it once "primero decisión, luego causa, luego datos mínimos"
    became the organizing rule for the whole dashboard, 2026-08-15).
    Supporting/weak similarity dimensions and contradicting
    precedents are Research Engine output that exists
    (engine/explanation_engine.py) but were not asked for in this
    block either -- left out on purpose, not an oversight, following
    the same rule: nothing goes on screen that doesn't answer one of
    the confirmed questions.
-   Alerts are synthesized, not hand-written: a fixed list of checks
    against this run's actual results, capped at 5, each one only
    appears if the condition it describes is actually true this run.
    Never a recommendation ("comprar ahora") -- only what changed or
    what is missing.
-   Read-only. No button executes, approves or modifies anything. Not
    wired into run.py, DecisionEngine, posture_mapper.py beyond the
    same audit-only call audit_posture.py already makes.
-   Fail-closed throughout: a missing file produces "not available"
    text in the relevant block, never an invented number or a
    favorable default.
"""

import html
from datetime import datetime
from pathlib import Path

from engine.date_utils import year_month
from engine.drawdown_engine import run_drawdown_engine
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
from engine.human_approval import HumanApprovalGate
from engine.human_approval_state import build_local_human_approval_inputs
from engine.live_episode import run_live_episode_detector
from engine.personal_capacity_facts_gate import (
    PersonalCapacityFactsGate,
    build_local_personal_capacity_facts_inputs,
)
from engine.posture_mapper import evaluate_capital_posture
from engine.regime_comparability_gate import (
    RegimeComparabilityGate,
    build_local_regime_comparability_inputs,
)
from engine.research_engine import ResearchEngine


OUTPUT_PATH = Path("outputs/dashboard.html")

# RE-DASH.1 -- posture ceilings mapped to a discrete, muted color
# class. Never used alone: every colored value on the page is always
# paired with its explanatory text, per the visual design Armando
# fixed 2026-08-14 ("siempre explicación textual junto al numero").
POSTURE_COLOR = {
    "Conserve": "warn",
    "Prepare": "warn",
    "Deploy Partially": "ok",
    "Deploy Aggressively": "ok",
    "Blocked": "bad",
}

GATE_STATE_COLOR = {
    "conservative": "ok",
    "comparable": "ok",
    "adequate": "ok",
    "not measurable": "warn",
    "not comparable": "bad",
    "constrained": "bad",
}

HA_STATE_COLOR = {
    "valid": "ok",
    "missing": "bad",
    "expired": "bad",
    "under_cooling_off": "warn",
}

DP_STATUS_COLOR = {
    "authorized": "ok",
    "cadence not met": "warn",
    "ceiling reached": "warn",
    "posture no deployment": "neutral",
}


def _fmt_pct(value, decimals=1):
    if value is None:
        return "not available"
    return f"{value * 100:.{decimals}f}%"


def _fmt_num(value, decimals=1):
    if value is None:
        return "not available"
    return f"{value:.{decimals}f}"


def _fmt_shiller_date(value):
    if value is None:
        return "not available"
    year, month = year_month(value)
    return f"{year}-{month:02d}"


def _fmt_amount(value):
    if value is None:
        return "not available"
    return f"{value:,.2f}"


def _esc(value) -> str:
    return html.escape(str(value))


def build_dashboard_data() -> dict:
    """
    Collects every result this dashboard shows, using exactly the same
    calls audit_posture.py already makes end-to-end. No new
    computation, no new gate logic -- this function only assembles a
    structure a template can render.
    """

    dataset = run_drawdown_engine()

    if dataset is None:
        return {"shiller_available": False}

    research = ResearchEngine().run(dataset)
    snapshot = research.snapshot
    evidence = research.evidence

    current_episode = run_live_episode_detector()

    eq_local = build_local_evidence_quality_inputs(evidence)
    eq_result = EvidenceQualityGate().evaluate(
        local=eq_local,
        global_state=GlobalModelValidationState(
            predictive_validation_status=PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
        ),
    )

    regime_local = build_local_regime_comparability_inputs(snapshot, evidence)
    regime_result = RegimeComparabilityGate().evaluate(regime_local)

    # Market-wide ceiling only (Evidence Quality + Regime Comparability).
    # Deliberately NOT a per-patrimonio fusion -- see module docstring.
    market_ceiling = evaluate_capital_posture(eq_result, regime_result)

    personal_capacity_inputs = build_local_personal_capacity_facts_inputs()
    human_approval_inputs = build_local_human_approval_inputs()
    ledger_states = build_local_dry_powder_ledger_state()

    patrimonios = {}

    if personal_capacity_inputs is not None:

        pc_gate = PersonalCapacityFactsGate()
        ha_gate = HumanApprovalGate()

        for patrimonio_name, pc_local in personal_capacity_inputs.items():

            pc_result = pc_gate.evaluate(pc_local)

            combined = evaluate_capital_posture(
                eq_result, regime_result, pc_result
            )

            ha_inputs = (
                human_approval_inputs.get(patrimonio_name)
                if human_approval_inputs is not None
                else None
            )

            ha_result = None
            ha_missing_reason = None

            if human_approval_inputs is None:
                ha_missing_reason = (
                    "data/raw/human_approval_attestations.xlsx not found"
                )
            elif ha_inputs is None:
                ha_missing_reason = "no attestation recorded for this patrimonio"
            else:
                ha_result = ha_gate.evaluate(ha_inputs)

            ledger_state = (
                ledger_states.get(patrimonio_name)
                if ledger_states is not None
                else None
            )

            dp_result = None
            dp_note = None

            if ledger_states is None:
                dp_note = "data/raw/dry_powder_ledger.xlsx not found"
            elif ledger_state is None:
                dp_note = "no ledger tab found for this patrimonio"
            else:
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

                if dp_inputs is None:
                    dp_note = "; ".join(ledger_state.explanations) or "not evaluated"
                else:
                    dp_result = DryPowderProtocol().evaluate(dp_inputs)

            patrimonios[patrimonio_name] = {
                "personal_capacity": pc_result,
                "combined": combined,
                "human_approval": ha_result,
                "human_approval_missing_reason": ha_missing_reason,
                "dry_powder": dp_result,
                "dry_powder_note": dp_note,
            }

    return {
        "shiller_available": True,
        "generated_at": datetime.now(),
        "snapshot": snapshot,
        "current_episode": current_episode,
        "evidence": evidence,
        "eq_result": eq_result,
        "regime_result": regime_result,
        "market_ceiling": market_ceiling,
        "personal_capacity_available": personal_capacity_inputs is not None,
        "patrimonios": patrimonios,
        "predictive_validation_status": PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    }


def build_alerts(data: dict) -> list[str]:
    """
    Synthesized, not hand-written: each line only appears if the
    condition it names is actually true in `data` this run. Capped at
    5, most restrictive/urgent first. Never a recommendation -- only
    what needs a look.
    """

    alerts = []

    if not data.get("shiller_available"):
        return ["data/raw/shiller.xlsx not found -- no other block computed"]

    if data["current_episode"] is None:
        alerts.append(
            "Sin episodio de caída activo -- Dry Powder Protocol no es "
            "evaluable hoy."
        )
    else:
        alerts.append(
            "Episodio de caída activo desde "
            f"{_fmt_shiller_date(data['current_episode'].peak_date)} "
            f"({data['current_episode'].duration_months} meses)."
        )

    if data["eq_result"].state == "not measurable":
        alerts.append("Evidence Quality: not measurable esta ejecución.")

    if data["regime_result"].state == "not comparable":
        alerts.append(
            "Regime Comparability: not comparable -- "
            + "; ".join(data["regime_result"].explanations)
        )

    if not data["personal_capacity_available"]:
        alerts.append(
            "data/raw/personal_capacity_facts.xlsx no encontrado -- "
            "posturas por patrimonio no evaluables."
        )
    else:
        for patrimonio_name, p in data["patrimonios"].items():
            if p["personal_capacity"].blocked:
                alerts.append(
                    f"{patrimonio_name}: Personal Capacity Facts con "
                    f"bloqueo duro ({', '.join(p['personal_capacity'].blocking_fields)})."
                )
            elif p["personal_capacity"].state == "constrained":
                alerts.append(
                    f"{patrimonio_name}: Personal Capacity Facts "
                    "constrained."
                )

            ha = p["human_approval"]
            if ha is None:
                alerts.append(
                    f"{patrimonio_name}: Human Approval -- "
                    f"{p['human_approval_missing_reason']}."
                )
            elif ha.state in ("missing", "expired", "under_cooling_off"):
                alerts.append(
                    f"{patrimonio_name}: Human Approval {ha.state}."
                )

    return alerts[:5]


def _card(title: str, body: str) -> str:
    return f'<section class="card"><h2>{_esc(title)}</h2>{body}</section>'


def _pill(text: str, color_class: str) -> str:
    return f'<span class="pill {color_class}">{_esc(text)}</span>'


def render_html(data: dict) -> str:

    if not data.get("shiller_available"):
        return (
            "<html><body style='font-family:sans-serif;padding:2rem'>"
            "<h1>SOP Research Engine -- Dashboard</h1>"
            "<p><strong>data/raw/shiller.xlsx not found.</strong> "
            "No block can be computed without it.</p>"
            "</body></html>"
        )

    snapshot = data["snapshot"]
    evidence = data["evidence"]
    episode = data["current_episode"]

    generated_at = data["generated_at"].strftime("%Y-%m-%d %H:%M")
    data_date = _fmt_shiller_date(snapshot.date)

    # ---- Cabecera ----

    header = f"""
    <header>
      <h1>SOP Research Engine -- Audit Dashboard</h1>
      <div class="banner">
        Research predictive validity: <strong>{_esc(data['predictive_validation_status'])}</strong>
        -- source: RE-PRED.16, fixed governance state, not recalculated on this run.<br>
        This dashboard is evidence/audit only. It does not execute decisions.
      </div>
      <div class="header-grid">
        <div>Fecha de datos (Shiller): <strong>{data_date}</strong></div>
        <div>Fecha de generación: <strong>{_esc(generated_at)}</strong></div>
        <div>Techo de mercado (Evidence Quality + Regime Comparability, sin Personal Capacity):
          {_pill(data['market_ceiling'].posture_ceiling, POSTURE_COLOR.get(data['market_ceiling'].posture_ceiling, 'neutral'))}
        </div>
      </div>
    </header>
    """

    # ---- Bloque: Mercado Shiller ----

    ctx = snapshot.context

    if episode is None:
        episode_html = "<p>No hay episodio de caída activo.</p>"
    else:
        episode_html = f"""
        <table>
          <tr><td>Peak date</td><td>{_fmt_shiller_date(episode.peak_date)}</td></tr>
          <tr><td>Duración</td><td>{_esc(episode.duration_months)} meses</td></tr>
          <tr><td>Drawdown actual</td><td>{_fmt_pct(episode.as_of_drawdown)}</td></tr>
          <tr><td>Peor punto del episodio (hasta ahora)</td><td>{_fmt_pct(episode.bottom_so_far_drawdown)}</td></tr>
        </table>
        """

    market_body = f"""
    <table>
      <tr><td>Real Total Return Price (Shiller Price.1)</td><td>{_fmt_num(snapshot.price, 2)}</td></tr>
      <tr><td>Drawdown actual</td><td>{_fmt_pct(snapshot.drawdown)}</td></tr>
      <tr><td>CAPE</td><td>{_fmt_num(ctx.cape if ctx else None, 1)}</td></tr>
      <tr><td>Inflación (interanual)</td><td>{_fmt_pct(ctx.inflation if ctx else None)}</td></tr>
      <tr><td>Tipo de interés (GS10)</td><td>{_fmt_pct(ctx.interest_rate if ctx else None)}</td></tr>
      <tr><td>Episodio de caída activo</td><td>{"Sí" if episode is not None else "No"}</td></tr>
    </table>
    {episode_html}
    """

    market_card = _card("Mercado Shiller", market_body)

    # ---- Bloque: Gates ----

    gates_rows = f"""
    <tr>
      <td>Evidence Quality</td>
      <td>{_pill(data['eq_result'].state, GATE_STATE_COLOR.get(data['eq_result'].state, 'neutral'))}</td>
      <td>{_esc('; '.join(data['eq_result'].explanations))}</td>
    </tr>
    <tr>
      <td>Regime Comparability</td>
      <td>{_pill(data['regime_result'].state, GATE_STATE_COLOR.get(data['regime_result'].state, 'neutral'))}</td>
      <td>{_esc('; '.join(data['regime_result'].explanations))}</td>
    </tr>
    """

    if not data["personal_capacity_available"]:
        gates_rows += """
        <tr>
          <td>Personal Capacity Facts</td>
          <td colspan="2">data/raw/personal_capacity_facts.xlsx not found</td>
        </tr>
        """
    else:
        for patrimonio_name, p in data["patrimonios"].items():
            pc = p["personal_capacity"]
            gates_rows += f"""
            <tr>
              <td>Personal Capacity Facts -- {_esc(patrimonio_name)}</td>
              <td>{_pill(pc.state, GATE_STATE_COLOR.get(pc.state, 'neutral'))}</td>
              <td>detalle completo en el bloque de Patrimonios, más abajo</td>
            </tr>
            """

    gates_card = _card(
        "Gates (min() combination)",
        f"<table><tr><th>Gate</th><th>Estado</th><th>Motivo</th></tr>{gates_rows}</table>",
    )

    # ---- Bloque: Prerrequisitos y protocolos ----

    protocols_body = ""

    if not data["personal_capacity_available"]:
        protocols_body = "<p>Sin datos por patrimonio disponibles.</p>"
    else:
        for patrimonio_name, p in data["patrimonios"].items():

            ha = p["human_approval"]

            if ha is None:
                ha_html = f"<p>Human Approval: {_esc(p['human_approval_missing_reason'])}.</p>"
            else:
                pending_html = ""
                if ha.pending_increase is not None:
                    pi = ha.pending_increase
                    pending_html = (
                        f"<div class='note'>Revisión pendiente a "
                        f"{_esc(pi.approved_posture_ceiling)}, efectiva "
                        f"{_esc(pi.effective_date)} "
                        f"({pi.cooling_off_days_required} días de cooling-off).</div>"
                    )
                ha_html = f"""
                <table>
                  <tr><td>Human Approval</td>
                      <td>{_pill(ha.state, HA_STATE_COLOR.get(ha.state, 'neutral'))}</td></tr>
                  <tr><td>Postura efectiva</td><td>{_esc(ha.effective_posture_ceiling or 'not available')}</td></tr>
                  <tr><td>Autoriza techo Dry Powder 90%</td><td>{"Sí" if ha.authorizes_dry_powder_ceiling_90 else "No"}</td></tr>
                </table>
                {pending_html}
                """

            dp = p["dry_powder"]

            if dp is None:
                dp_html = f"<p>Dry Powder Protocol: {_esc(p['dry_powder_note'])}.</p>"
            else:
                dp_html = f"""
                <table>
                  <tr><td>Dry Powder Protocol</td>
                      <td>{_pill(dp.status, DP_STATUS_COLOR.get(dp.status, 'neutral'))}</td></tr>
                  <tr><td>Importe autorizado</td><td>{_fmt_amount(dp.authorized_amount)}</td></tr>
                  <tr><td>Motivo</td><td>{_esc(dp.reason)}</td></tr>
                </table>
                """

            protocols_body += f"""
            <div class="patrimonio-block">
              <h3>{_esc(patrimonio_name)}</h3>
              {ha_html}
              {dp_html}
            </div>
            """

    protocols_card = _card("Prerrequisitos y protocolos (independientes de los Gates)", protocols_body)

    # ---- Bloque: Patrimonios ----

    patrimonios_body = ""

    if not data["personal_capacity_available"]:
        patrimonios_body = "<p>data/raw/personal_capacity_facts.xlsx not found.</p>"
    else:
        for patrimonio_name, p in data["patrimonios"].items():

            pc = p["personal_capacity"]
            combined = p["combined"]

            detail_rows = ""
            for field_name in pc.failed_fields:
                detail_rows += f"<tr><td>{_esc(field_name)}</td><td>confirmed breach</td></tr>"
            for field_name in pc.missing_fields:
                detail_rows += f"<tr><td>{_esc(field_name)}</td><td>not measured</td></tr>"
            if not detail_rows:
                detail_rows = "<tr><td colspan='2'>Nueve hechos verificables, todos favorables.</td></tr>"

            patrimonios_body += f"""
            <div class="patrimonio-block">
              <h3>{_esc(patrimonio_name)}</h3>
              <div>Postura combinada (Gates, este patrimonio):
                {_pill(combined.posture_ceiling, POSTURE_COLOR.get(combined.posture_ceiling, 'neutral'))}
              </div>
              <div class="note">{_esc('; '.join(combined.explanations))}</div>
              <table><tr><th>Personal Capacity Facts -- razón</th><th>Estado</th></tr>{detail_rows}</table>
            </div>
            """

    patrimonios_card = _card("Patrimonios", patrimonios_body)

    # ---- Bloque: Evidencia histórica ----

    evidence_body = f"""
    <table>
      <tr><td>Número de matches (return_count)</td><td>{evidence.return_count}</td></tr>
      <tr><td>Horizonte</td><td>{evidence.horizon_years} años</td></tr>
      <tr><td>Retorno esperado (mediana)</td><td>{_fmt_pct(evidence.median_return)}</td></tr>
      <tr><td>Peor caso</td><td>{_fmt_pct(evidence.worst_return)}</td></tr>
      <tr><td>Mejor caso</td><td>{_fmt_pct(evidence.best_return)}</td></tr>
      <tr><td>Predictive validation status</td>
          <td>{_pill(data['predictive_validation_status'], 'warn')}
              <span class="note">source: RE-PRED.16 / fixed governance state, not recalculated on this run</span></td></tr>
    </table>
    """

    evidence_card = _card("Evidencia histórica", evidence_body)

    # ---- Bloque: Alertas ----

    alerts = build_alerts(data)
    alerts_html = "<ul>" + "".join(f"<li>{_esc(a)}</li>" for a in alerts) + "</ul>"
    alerts_card = _card("Alertas", alerts_html)

    style = """
    <style>
      body { font-family: -apple-system, Helvetica, Arial, sans-serif; background:#f7f7f5; color:#222; margin:0; padding:2rem; }
      header { margin-bottom: 1.5rem; }
      h1 { font-size: 1.4rem; margin-bottom: 0.5rem; }
      .banner { background:#fff3d6; border:1px solid #e0c26a; padding:0.75rem 1rem; border-radius:6px; font-size:0.9rem; margin-bottom:1rem; }
      .header-grid { display:flex; gap:2rem; flex-wrap:wrap; font-size:0.95rem; }
      .card { background:#fff; border:1px solid #ddd; border-radius:8px; padding:1rem 1.25rem; margin-bottom:1.25rem; }
      .card h2 { font-size:1.05rem; margin-top:0; border-bottom:1px solid #eee; padding-bottom:0.4rem; }
      table { border-collapse: collapse; width:100%; font-size:0.9rem; margin-bottom:0.5rem; }
      td, th { text-align:left; padding:0.3rem 0.5rem; border-bottom:1px solid #f0f0f0; vertical-align:top; }
      .patrimonio-block { border-left:3px solid #ccc; padding-left:1rem; margin-bottom:1rem; }
      .pill { display:inline-block; padding:0.1rem 0.6rem; border-radius:10px; font-size:0.8rem; font-weight:600; }
      .pill.ok { background:#dcefdc; color:#2f6b2f; }
      .pill.warn { background:#fbe8c6; color:#8a5a00; }
      .pill.bad { background:#f6d9d9; color:#a12b2b; }
      .pill.neutral { background:#e6e6e6; color:#555; }
      .note { font-size:0.8rem; color:#666; margin-top:0.2rem; }
      ul { margin:0; padding-left:1.2rem; }
    </style>
    """

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>SOP Research Engine -- Dashboard</title>{style}</head>
<body>
{header}
{market_card}
{gates_card}
{protocols_card}
{patrimonios_card}
{evidence_card}
{alerts_card}
</body>
</html>
"""


def main() -> None:

    data = build_dashboard_data()
    output = render_html(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output, encoding="utf-8")

    print(f"Dashboard generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
