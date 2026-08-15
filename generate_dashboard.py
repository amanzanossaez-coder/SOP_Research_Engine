"""
SOP -- Panel de Estado
RE-DASH.1.4 -- Static SOP/Shiller Audit Dashboard, "lectura rápida" pass

Generates a single static HTML file (outputs/dashboard.html) that
makes the current state of the Research Engine and the SOP gates/
protocols visible, without changing anything about how they work.

Read-only, single command, no server:

    python3 generate_dashboard.py

RE-DASH.1.4 (2026-08-15) is a full design pass agreed with Armando
BEFORE writing any code (see conversation the same day) -- explicitly
"no dispares todavía en ejecutar, vamos a centrarnos antes en dejarlo
bien perfilado". Confirmed points, all implemented here:

-   "Estado hoy": a colored dot (semáforo) next to the dominant action
    text -- color supports, text leads, never the other way round.
-   "Por qué no se actúa": one line per variable (label + short pill
    value), not prose sentences. No notes -- if the reader wants more,
    the relevant block below already has it.
-   "Estado por patrimonio": two separate compact tables (Armando's
    explicit choice, option B over one wide table) -- one for
    liquidity (cifra real + suelo + techo + estado), one for
    postura/Human Approval/Dry Powder. Keeps money and permissions
    visually separate.
-   "Datos de mercado": each figure gets a one-line historical context
    computed from real data -- z-score against the FULL Shiller series
    (1871-2026, Armando's explicit choice over a shorter window, for
    traceability), banded at |z|<0.5 "cerca de", <1.5 "por encima/por
    debajo", >=1.5 "muy por encima/por debajo" (thresholds Armando
    confirmed). Drawdown is reported as a plain fact, not a z-score --
    "en máximo histórico" or "caída del X% desde máximo" reads more
    honestly than comparing a mostly-zero series to its own mean.
-   "Evidencia histórica": reworded once more, folding "horizonte" and
    "fondo del episodio" into one plain intro sentence instead of a
    separate technical row, answering both questions Armando asked
    ("¿fondo es el punto de máximo drawdown?" -- sí; "¿qué es el
    retorno mediano?" -- el valor típico de los 5 años siguientes) in
    the sentence itself, not as an aside.
-   Title/subtitle: "SOP -- Panel de Estado" / "Lectura de mercado,
    evidencia y autorización patrimonial. Solo lectura."

One feature discussed and explicitly DROPPED, not built: "Qué haría
falta para cambiar el estado". Verified by direct execution before
deciding, not assumed: Evidence Quality Gate's ceiling is structurally
capped at `Prepare` today (`not measurable` -> `Prepare`; if it were
ever `validated` it would map to `Conserve`, an even MORE restrictive
ceiling -- RE-037.1's own design, "no less-restrictive Evidence
Quality state is authorized"). And `Prepare` authorizes exactly the
same 0% Dry Powder deployment as `Conserve`
(`DryPowderProtocol.TRANCHE_PARAMETERS` only defines tranches for
`Deploy Partially`/`Deploy Aggressively`) -- confirmed by running
`DryPowderProtocol().evaluate()` directly with `current_posture=Prepare`
before this decision, not assumed. A "path from Conserve to Prepare"
feature would therefore describe a transition with zero practical
consequence, add no information beyond what "Por qué no se actúa"
already states (just grammatically inverted), and push the dashboard's
tone from "objective mirror" toward "roadmap to action" -- exactly what
this project has resisted everywhere else (no simuladores, no
proyecciones, no falsa sensación de progreso). Armando's own closing
question ("¿de verdad necesitamos esto?") is answered here: no.

Kept unchanged from earlier iterations, still correct: never fuses
AMS/AML into one number when they disagree (RE-043.1); predictive
validity is never framed as a cause of today's `Conserve` ceiling;
real liquidity floor AND ceiling from `personal_capacity_facts.xlsx`
(RE-DASH.1.3 correction); Detalle técnico stays the only place raw
English state names and code identifiers appear; Spanish
decimal/thousands number formatting throughout the main view.
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
    REQUIRED_LABELS,
    PersonalCapacityFactsGate,
    build_local_personal_capacity_facts_inputs,
)
from engine.posture_mapper import evaluate_capital_posture
from engine.regime_comparability_gate import (
    RegimeComparabilityGate,
    build_local_regime_comparability_inputs,
)
from engine.research_engine import ResearchEngine
from loaders.personal_capacity_facts_loader import load_personal_capacity_facts_raw


OUTPUT_PATH = Path("outputs/dashboard.html")

# RE-DASH.1.3 -- real column in data/raw/personal_capacity_facts.xlsx, not
# in REQUIRED_LABELS because no gate scores it (display-only figure).
LIQUIDITY_CEILING_LABEL = "Techo de liquidez total (máximo óptimo)"

# RE-DASH.1.5 -- the workbook already computes these two gaps itself
# (formulas, not this script) -- reused as-is rather than recomputed, same
# principle as the floor/ceiling above: one audited source of truth, not a
# second calculation that could drift from it.
LIQUIDITY_GAP_FLOOR_LABEL = "Exceso/(Déficit) vs. suelo de liquidez"
LIQUIDITY_GAP_CEILING_LABEL = "Exceso/(Déficit) vs. techo de liquidez"

# RE-DASH.1.4 -- thresholds for "Datos de mercado"'s historical-context
# column, confirmed by Armando: objective z-score bands, not a judgment
# call per figure.
Z_THRESHOLD_NEAR = 0.5
Z_THRESHOLD_NOTABLE = 1.5

# RE-DASH.1.5 -- second historical reference window for Datos de mercado,
# alongside the full series -- Armando's request: "quizás de los últimos
# 50 años", both shown side by side.
RECENT_WINDOW_YEARS = 50


# ---------------------------------------------------------------------------
# Translation layer
# ---------------------------------------------------------------------------

POSTURE_ES = {
    "Conserve": "Conservar",
    "Prepare": "Preparar",
    "Deploy Partially": "Desplegar Parcialmente",
    "Deploy Aggressively": "Desplegar Agresivamente",
    "Blocked": "Bloqueado",
}

POSTURE_COLOR = {
    "Conserve": "warn",
    "Prepare": "warn",
    "Deploy Partially": "ok",
    "Deploy Aggressively": "ok",
    "Blocked": "bad",
}

ACTION_ES = {
    "Conserve": "NO ACTUAR",
    "Prepare": "PREPARARSE, SIN DESPLEGAR",
    "Deploy Partially": "DESPLIEGUE PARCIAL AUTORIZADO",
    "Deploy Aggressively": "DESPLIEGUE AGRESIVO AUTORIZADO",
    "Blocked": "BLOQUEADO",
}

GATE_STATE_ES = {
    "conservative": "Sin límite adicional",
    "not measurable": "No medible",
    "comparable": "Comparable",
    "not comparable": "No comparable",
}

# Short, label-friendly dimension names (distinct from REGIME_DIMENSION_ES
# below, which is grammatically fitted for mid-sentence use).
REGIME_DIMENSION_LABEL_ES = {
    "cape": "CAPE",
    "inflation": "Inflación",
    "interest_rate": "Tipo de interés",
}

REGIME_DIMENSION_ES = {
    "cape": "CAPE",
    "inflation": "la inflación",
    "interest_rate": "el tipo de interés",
}

# Short compact verdict, for one-line rows (Por qué no se actúa).
FACT_FIELD_SHORT_ES = {
    "liquidity_adequate": "Por debajo del suelo",
    "near_term_cash_needs_covered": "Sin cubrir",
    "fixed_obligations_manageable": "Sin cubrir",
    "debt_service_manageable": "No manejable",
    "income_concentration_acceptable": "Concentración alta",
    "portfolio_concentration_acceptable": "Concentración alta",
    "emergency_reserve_adequate": "Por debajo del mínimo",
    "time_horizon_constraints_covered": "Evento próximo sin cubrir",
    "fiscal_operational_constraints_manageable": "Restricción pendiente",
}

FACT_FIELD_LABEL_ES = {
    "liquidity_adequate": "liquidez",
    "near_term_cash_needs_covered": "necesidades de caja a corto plazo",
    "fixed_obligations_manageable": "obligaciones fijas",
    "debt_service_manageable": "servicio de deuda",
    "income_concentration_acceptable": "concentración de ingresos",
    "portfolio_concentration_acceptable": "concentración de cartera",
    "emergency_reserve_adequate": "colchón de emergencia",
    "time_horizon_constraints_covered": "horizonte / eventos de liquidez",
    "fiscal_operational_constraints_manageable": "restricciones fiscales/operativas",
}


# ---------------------------------------------------------------------------
# Formatting -- Spanish decimal/thousands convention throughout the main
# view (comma decimal, period thousands): "10,2%", "172.330,77 €".
# ---------------------------------------------------------------------------


def _es_decimal(formatted: str) -> str:
    return formatted.replace(".", ",")


def _fmt_pct(value, decimals=1):
    if value is None:
        return "No disponible"
    return _es_decimal(f"{value * 100:.{decimals}f}%")


def _fmt_rate(value, decimals=2):
    """
    `Rate GS10` is already a percentage-point figure (4.44 means 4.44%),
    confirmed by reading Snapshot.context.interest_rate directly. Never
    multiplies by 100 like `_fmt_pct` does for the fraction-typed fields
    (drawdown, inflation).
    """
    if value is None:
        return "No disponible"
    return _es_decimal(f"{value:.{decimals}f}%")


def _fmt_num(value, decimals=1):
    if value is None:
        return "No disponible"
    return _es_decimal(f"{value:.{decimals}f}")


def _fmt_shiller_date(value):
    if value is None:
        return "No disponible"
    year, month = year_month(value)
    return f"{year}-{month:02d}"


def _fmt_amount(value):
    """Full Spanish thousands+decimal convention: 172330.77 -> "172.330,77"."""
    if value is None:
        return "No disponible"
    formatted = f"{value:,.2f}"
    return formatted.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _fmt_signed_amount(value):
    """Same as _fmt_amount but prefixes a "+" for positive values, so
    exceso/deficit reads unambiguously at a glance."""
    if value is None:
        return "No disponible"
    sign = "+" if value > 0 else ""
    return f"{sign}{_fmt_amount(value)}"


def _esc(value) -> str:
    return html.escape(str(value))


# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------


def build_dashboard_data() -> dict:
    """
    Collects every result this dashboard shows, using exactly the same
    calls audit_posture.py already makes end-to-end, plus two read-only
    additions: real liquidity figures from
    load_personal_capacity_facts_raw() (RE-DASH.1.2/.3), and historical
    mean/std for CAPE/inflación/tipos over the full Shiller series
    (RE-DASH.1.4), both computed from data already loaded for the
    pipeline -- no new data source, no gate logic touched.
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
    # Deliberately NOT a per-patrimonio fusion.
    market_ceiling = evaluate_capital_posture(eq_result, regime_result)

    # RE-DASH.1.4 -- historical reference for "Datos de mercado", full
    # Shiller series (1871-2026, Armando's explicit choice). .mean()/.std()
    # skip NaN by default -- early rows with unpopulated columns are
    # excluded from the reference the same way pandas always handles this,
    # not a special case introduced here.
    market_context = {
        "cape": (dataset.data["CAPE"].mean(), dataset.data["CAPE"].std()),
        "inflation": (
            dataset.data["InflationRate1Y"].mean(),
            dataset.data["InflationRate1Y"].std(),
        ),
        "interest_rate": (
            dataset.data["Rate GS10"].mean(),
            dataset.data["Rate GS10"].std(),
        ),
    }

    # RE-DASH.1.5 -- second reference window, Armando's request: full
    # history AND a more recent 50-year slice, side by side, not one
    # replacing the other. RECENT_WINDOW_YEARS subtracted directly from the
    # latest Shiller AAAA.MM float date -- same integer-year-offset pattern
    # drawdown_engine.py already uses (e.g. peak_date - 3 for the 3-year
    # pre-crash window), not a new date-arithmetic convention.
    earliest_date = dataset.data["Date"].min()
    latest_date = dataset.data["Date"].max()
    recent_cutoff = latest_date - RECENT_WINDOW_YEARS
    recent_df = dataset.data[dataset.data["Date"] >= recent_cutoff]
    market_context_recent = {
        "cape": (recent_df["CAPE"].mean(), recent_df["CAPE"].std()),
        "inflation": (
            recent_df["InflationRate1Y"].mean(),
            recent_df["InflationRate1Y"].std(),
        ),
        "interest_rate": (
            recent_df["Rate GS10"].mean(),
            recent_df["Rate GS10"].std(),
        ),
    }

    personal_capacity_inputs = build_local_personal_capacity_facts_inputs()
    liquidity_raw = load_personal_capacity_facts_raw()
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
                ha_missing_reason = "data/raw/human_approval_attestations.xlsx not found"
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

            concepto_map = (
                liquidity_raw.get(patrimonio_name, {}) if liquidity_raw is not None else {}
            )
            liquidity_actual = concepto_map.get(REQUIRED_LABELS["liquidez_total"])
            liquidity_floor = concepto_map.get(REQUIRED_LABELS["suelo_total_liquidez"])
            liquidity_ceiling = concepto_map.get(LIQUIDITY_CEILING_LABEL)
            liquidity_gap_floor = concepto_map.get(LIQUIDITY_GAP_FLOOR_LABEL)
            liquidity_gap_ceiling = concepto_map.get(LIQUIDITY_GAP_CEILING_LABEL)

            patrimonios[patrimonio_name] = {
                "personal_capacity": pc_result,
                "combined": combined,
                "human_approval": ha_result,
                "human_approval_missing_reason": ha_missing_reason,
                "dry_powder": dp_result,
                "dry_powder_note": dp_note,
                "liquidity_actual": liquidity_actual,
                "liquidity_floor": liquidity_floor,
                "liquidity_ceiling": liquidity_ceiling,
                "liquidity_gap_floor": liquidity_gap_floor,
                "liquidity_gap_ceiling": liquidity_gap_ceiling,
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
        "market_context": market_context,
        "market_context_recent": market_context_recent,
        "recent_window_start": recent_cutoff,
        "market_full_start": earliest_date,
        "market_latest_date": latest_date,
        "personal_capacity_available": personal_capacity_inputs is not None,
        "patrimonios": patrimonios,
        "predictive_validation_status": PREDICTIVE_VALIDATION_NOT_DEMONSTRATED,
    }


# ---------------------------------------------------------------------------
# Historical context (Datos de mercado)
# ---------------------------------------------------------------------------


def context_band(value, mean, std) -> str:
    """
    Objective z-score bands against the full historical Shiller series,
    thresholds confirmed by Armando: |z|<0.5 "cerca de", <1.5 "por
    encima/debajo", >=1.5 "muy por encima/debajo". Never claims regime
    comparability -- that is Regime Comparability Gate's job, over the
    matched-episode sample, a different and narrower reference
    population. This is a wider, purely descriptive comparison.
    """

    if value is None or mean is None or std is None or std == 0:
        return "Sin referencia histórica suficiente"

    z = (value - mean) / std

    if abs(z) < Z_THRESHOLD_NEAR:
        return "Cerca de su media histórica"
    if abs(z) < Z_THRESHOLD_NOTABLE:
        return "Por encima de su media histórica" if z > 0 else "Por debajo de su media histórica"
    return "Muy por encima de su media histórica" if z > 0 else "Muy por debajo de su media histórica"


# ---------------------------------------------------------------------------
# Por qué no se actúa -- compact rows
# ---------------------------------------------------------------------------


def _regime_direction(dim: str, snapshot_ctx, match_contexts) -> str | None:
    """
    Direction of today's value relative to the matched episodes' range
    for one regime dimension. Reuses exactly the values
    RegimeComparabilityGate._dimension_covered() already compares
    (snapshot.context.<dim> vs [episode.context.<dim> for the same
    evidence.matches]) -- not a second, independently-computed source
    of truth. Returns "alto"/"bajo" only when today's value falls
    strictly outside the matched range on that side; None if not
    determinable (missing value today, or no match provides this
    dimension) -- never guessed.
    """
    today_value = getattr(snapshot_ctx, dim, None)
    values = [v for v in (getattr(ctx, dim, None) for ctx in match_contexts) if v is not None]
    if today_value is None or not values:
        return None
    if today_value > max(values):
        return "alto"
    if today_value < min(values):
        return "bajo"
    return None


def build_porque_rows(data: dict) -> dict:
    """
    One row per variable: {"label", "value", "color"}. No prose. Never
    fuses AMS/AML: if their combined postures differ, returns
    `mixed=True` with a row set per patrimonio instead of one shared
    list (RE-043.1).
    """

    episode = data["current_episode"]
    regime = data["regime_result"]

    shared_rows = [
        {
            "label": "Caída de mercado",
            "value": "Activa" if episode is not None else "No activa",
            "color": "warn" if episode is not None else "ok",
        }
    ]

    if regime.state == "not comparable":
        snapshot_ctx = data["snapshot"].context
        match_contexts = [
            match.episode.context
            for match in data["evidence"].matches
            if match.episode.context is not None
        ]
        for e in regime.explanations:
            for dim, label in REGIME_DIMENSION_LABEL_ES.items():
                if not e.startswith(f"{dim}:"):
                    continue
                direction = _regime_direction(dim, snapshot_ctx, match_contexts)
                if direction == "alto":
                    value = "Muy alto frente al histórico comparable"
                elif direction == "bajo":
                    value = "Muy bajo frente al histórico comparable"
                else:
                    # Fail-closed: direction not determinable from the
                    # real match data (missing values on either side) --
                    # do not guess "alto"/"bajo" without verifying it.
                    value = "Fuera del rango que tuvieron los episodios parecidos"
                shared_rows.append(
                    {"label": f"Régimen ({label})", "value": value, "color": "bad"}
                )
                break
    elif regime.state == "comparable":
        shared_rows.append(
            {
                "label": "Régimen",
                "value": "Dentro del rango que tuvieron los episodios parecidos",
                "color": "ok",
            }
        )
    else:
        shared_rows.append(
            {"label": "Régimen", "value": "Sin datos suficientes para comparar", "color": "warn"}
        )

    predictive_value = (
        "No demostrada"
        if data["predictive_validation_status"] == PREDICTIVE_VALIDATION_NOT_DEMONSTRATED
        else str(data["predictive_validation_status"])
    )
    shared_rows.append({"label": "Validez predictiva", "value": predictive_value, "color": "warn"})

    if not data["personal_capacity_available"]:
        shared_rows.append({"label": "Patrimonios", "value": "No disponible", "color": "neutral"})
        return {"mixed": False, "rows": shared_rows}

    postures = {name: p["combined"].posture_ceiling for name, p in data["patrimonios"].items()}

    if len(set(postures.values())) > 1:
        per_patrimonio = {}
        for name, p in data["patrimonios"].items():
            rows = list(shared_rows)
            pc = p["personal_capacity"]
            for f in pc.failed_fields:
                rows.append({
                    "label": f"{name} — {FACT_FIELD_LABEL_ES.get(f, f).capitalize()}",
                    "value": FACT_FIELD_SHORT_ES.get(f, "Limitado"),
                    "color": "bad",
                })
            per_patrimonio[name] = {"posture": postures[name], "rows": rows}
        return {"mixed": True, "per_patrimonio": per_patrimonio}

    rows = list(shared_rows)
    for name, p in data["patrimonios"].items():
        pc = p["personal_capacity"]
        for f in pc.failed_fields:
            rows.append({
                "label": f"{name} — {FACT_FIELD_LABEL_ES.get(f, f).capitalize()}",
                "value": FACT_FIELD_SHORT_ES.get(f, "Limitado"),
                "color": "bad",
            })

    posture = next(iter(set(postures.values())))
    return {"mixed": False, "posture": posture, "rows": rows}


def build_alerts(data: dict) -> list:
    """Synthesized, not hand-written, fully in Spanish. Capped at 5, most restrictive first."""

    alerts = []

    if not data.get("shiller_available"):
        return ["data/raw/shiller.xlsx no encontrado -- ningún otro bloque es calculable."]

    if data["current_episode"] is None:
        alerts.append("Sin episodio de caída activo -- Dry Powder Protocol no es evaluable hoy.")
    else:
        ep = data["current_episode"]
        alerts.append(
            f"Episodio de caída activo desde {_fmt_shiller_date(ep.peak_date)} "
            f"({ep.duration_months} meses)."
        )

    if data["eq_result"].state == "not measurable":
        alerts.append("Evidencia: validez predictiva no medible esta ejecución.")

    if data["regime_result"].state == "not comparable":
        dims = []
        for e in data["regime_result"].explanations:
            for dim, label in REGIME_DIMENSION_LABEL_ES.items():
                if e.startswith(f"{dim}:") and label not in dims:
                    dims.append(label)
        alerts.append(f"Régimen no comparable ({', '.join(dims)}).")

    if not data["personal_capacity_available"]:
        alerts.append("personal_capacity_facts.xlsx no encontrado -- posturas por patrimonio no evaluables.")
    else:
        for name, p in data["patrimonios"].items():
            pc = p["personal_capacity"]
            if pc.blocked:
                labels = [FACT_FIELD_LABEL_ES.get(f, f) for f in pc.blocking_fields]
                alerts.append(f"{name}: bloqueo duro en capacidad personal ({', '.join(labels)}).")
            elif pc.state == "constrained":
                alerts.append(f"{name}: capacidad personal limitada.")

            ha = p["human_approval"]
            if ha is None:
                alerts.append(f"{name}: Human Approval sin registrar.")
            elif ha.state in ("missing", "expired", "under_cooling_off"):
                label = {
                    "missing": "sin registrar",
                    "expired": "caducado",
                    "under_cooling_off": "en periodo de espera",
                }[ha.state]
                alerts.append(f"{name}: Human Approval {label}.")

    return alerts[:5]


# ---------------------------------------------------------------------------
# Estado por patrimonio -- compact per-patrimonio helpers
# ---------------------------------------------------------------------------


def liquidity_status(actual, floor, ceiling) -> tuple:
    if actual is None or floor is None:
        return "Sin datos", "neutral"
    if ceiling is not None and actual > ceiling:
        return "Por encima del techo", "warn"
    if actual < floor:
        return "Por debajo del suelo", "bad"
    return "Dentro de rango", "ok"


def liquidity_gap(actual, floor, ceiling, gap_floor, gap_ceiling):
    """
    Picks the one exceso/deficit figure that matches the current status,
    reusing the pre-audited spreadsheet formulas (never recomputed here):
    - Below suelo -> gap vs. suelo (how much is missing).
    - Above techo -> gap vs. techo (how much is over).
    - Within range -> gap vs. suelo (the buffer already secured).
    """
    if actual is None or floor is None:
        return None
    if ceiling is not None and actual > ceiling:
        return gap_ceiling
    return gap_floor


def human_approval_short(ha, missing_reason) -> str:

    if ha is None:
        return "Sin registrar"

    if ha.state == "valid" and ha.pending_increase is None:
        posture = POSTURE_ES.get(ha.effective_posture_ceiling, ha.effective_posture_ceiling)
        return f"Vigente ({posture})"

    if ha.state == "valid" and ha.pending_increase is not None:
        posture = POSTURE_ES.get(ha.effective_posture_ceiling, ha.effective_posture_ceiling)
        return f"Vigente ({posture}); revisión {_esc(ha.pending_increase.effective_date)}"

    if ha.state == "under_cooling_off":
        pi = ha.pending_increase
        return f"En espera (hasta {_esc(pi.effective_date)})" if pi else "En espera"

    if ha.state == "expired":
        return "Caducado"

    if ha.state == "missing":
        return "Sin registrar"

    return ha.state


def dry_powder_short(dp, note, episode_active: bool) -> str:

    if not episode_active:
        return "No aplica (sin caída)"

    if dp is None:
        return "No evaluable"

    mapping = {
        "authorized": f"Autorizado ({_fmt_amount(dp.authorized_amount)} €)",
        "ceiling reached": "Techo alcanzado",
        "cadence not met": "Cadencia no cumplida",
        "posture no deployment": "Sin despliegue permitido",
    }
    return mapping.get(dp.status, dp.status)


def other_findings(pc) -> list:
    """Findings beyond liquidity -- liquidity has its own dedicated table."""

    findings = []
    for f in pc.failed_fields:
        if f == "liquidity_adequate":
            continue
        findings.append((FACT_FIELD_LABEL_ES.get(f, f).capitalize(), FACT_FIELD_SHORT_ES.get(f, "Limitado")))
    for f in pc.missing_fields:
        if f == "liquidity_adequate":
            continue
        findings.append((FACT_FIELD_LABEL_ES.get(f, f).capitalize(), "No medido"))
    return findings


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _card(title: str, body: str) -> str:
    return f'<section class="card"><h2>{_esc(title)}</h2>{body}</section>'


def _pill(text: str, color_class: str) -> str:
    return f'<span class="pill {color_class}">{_esc(text)}</span>'


def _dot(color_class: str) -> str:
    return f'<span class="dot {color_class}"></span>'


def render_html(data: dict) -> str:

    if not data.get("shiller_available"):
        return (
            "<html><body style='font-family:sans-serif;padding:2rem'>"
            "<h1>SOP -- Panel de Estado</h1>"
            "<p><strong>data/raw/shiller.xlsx no encontrado.</strong> "
            "Ningún bloque es calculable sin él.</p>"
            "</body></html>"
        )

    snapshot = data["snapshot"]
    evidence = data["evidence"]
    episode = data["current_episode"]
    ctx = snapshot.context

    generated_at = data["generated_at"].strftime("%Y-%m-%d %H:%M")
    data_date = _fmt_shiller_date(snapshot.date)

    porque = build_porque_rows(data)

    # ---- Estado hoy (semáforo, texto dominante) ----

    if not porque["mixed"]:
        posture = porque["posture"]
        color = POSTURE_COLOR.get(posture, "neutral")
        primary = "No hay caída de mercado activa." if episode is None else porque["rows"][1]["label"] + ": " + porque["rows"][1]["value"]

        estado_hoy_body = f"""
        <div class="headline-action">{_dot(color)}{_esc(ACTION_ES.get(posture, posture))}</div>
        <p class="headline-sub">{_esc(primary)}</p>
        """
    else:
        parts = "".join(
            f'<div>{_dot(POSTURE_COLOR.get(info["posture"], "neutral"))}<strong>{_esc(name)}</strong>: {_esc(ACTION_ES.get(info["posture"], info["posture"]))}</div>'
            for name, info in porque["per_patrimonio"].items()
        )
        estado_hoy_body = f"""
        <p class="headline-sub">AMS y AML difieren hoy -- nunca fusionados:</p>
        {parts}
        """

    estado_hoy_card = _card("Estado hoy", estado_hoy_body)

    # ---- Por qué no se actúa (una línea por variable) ----

    def _rows_table(rows):
        trs = "".join(
            f'<tr><td>{_esc(r["label"])}</td><td>{_pill(r["value"], r["color"])}</td></tr>'
            for r in rows
        )
        return f"<table>{trs}</table>"

    if not porque["mixed"]:
        porque_body = _rows_table(porque["rows"])
    else:
        blocks = ""
        for name, info in porque["per_patrimonio"].items():
            blocks += f'<h3>{_esc(name)}</h3>{_rows_table(info["rows"])}'
        porque_body = blocks

    porque_card = _card("Por qué no se actúa", porque_body)

    # ---- Estado por patrimonio: dos tablas compactas ----

    if not data["personal_capacity_available"]:
        patrimonio_body = "<p>personal_capacity_facts.xlsx no encontrado.</p>"
    else:
        liquidity_rows = ""
        operational_rows = ""
        findings_rows = ""

        for name, p in data["patrimonios"].items():

            status_text, status_color = liquidity_status(
                p["liquidity_actual"], p["liquidity_floor"], p["liquidity_ceiling"]
            )
            gap = liquidity_gap(
                p["liquidity_actual"],
                p["liquidity_floor"],
                p["liquidity_ceiling"],
                p["liquidity_gap_floor"],
                p["liquidity_gap_ceiling"],
            )
            liquidity_rows += (
                f"<tr><td>{_esc(name)}</td>"
                f"<td>{_fmt_amount(p['liquidity_actual'])} €</td>"
                f"<td>{_fmt_amount(p['liquidity_floor'])} € / {_fmt_amount(p['liquidity_ceiling'])} €</td>"
                f"<td>{_fmt_signed_amount(gap)} €</td>"
                f"<td>{_pill(status_text, status_color)}</td></tr>"
            )

            combined = p["combined"]
            operational_rows += (
                f"<tr><td>{_esc(name)}</td>"
                f"<td>{_pill(POSTURE_ES.get(combined.posture_ceiling, combined.posture_ceiling), POSTURE_COLOR.get(combined.posture_ceiling, 'neutral'))}</td>"
                f"<td>{_esc(human_approval_short(p['human_approval'], p['human_approval_missing_reason']))}</td>"
                f"<td>{_esc(dry_powder_short(p['dry_powder'], p['dry_powder_note'], episode is not None))}</td></tr>"
            )

            for label, verdict in other_findings(p["personal_capacity"]):
                findings_rows += f"<tr><td>{_esc(name)}</td><td>{_esc(label)}</td><td>{_esc(verdict)}</td></tr>"

        findings_html = ""
        if findings_rows:
            findings_html = f"""
            <p><strong>Otros hallazgos (más allá de liquidez):</strong></p>
            <table><tr><th>Patrimonio</th><th>Hecho</th><th>Estado</th></tr>{findings_rows}</table>
            """

        patrimonio_body = f"""
        <p><strong>Liquidez</strong></p>
        <table>
          <tr><th>Patrimonio</th><th>Liquidez disponible</th><th>Rango de liquidez (suelo / techo)</th><th>Exceso/Déficit</th><th>Estado</th></tr>
          {liquidity_rows}
        </table>
        <p><strong>Postura y permisos</strong></p>
        <table>
          <tr><th>Patrimonio</th><th>Postura</th><th>Human Approval</th><th>Dry Powder</th></tr>
          {operational_rows}
        </table>
        {findings_html}
        """

    patrimonio_card = _card("Estado por patrimonio", patrimonio_body)

    # ---- Datos de mercado, con contexto histórico ----

    cape_mean, cape_std = data["market_context"]["cape"]
    inflation_mean, inflation_std = data["market_context"]["inflation"]
    rate_mean, rate_std = data["market_context"]["interest_rate"]

    recent_cape_mean, recent_cape_std = data["market_context_recent"]["cape"]
    recent_inflation_mean, recent_inflation_std = data["market_context_recent"]["inflation"]
    recent_rate_mean, recent_rate_std = data["market_context_recent"]["interest_rate"]

    # RE-DASH.1.6 -- both context windows expressed as the same
    # "AAAA-AAAA" range format, computed from the real Shiller dates
    # (never hardcoded), so the two headers read as one consistent
    # pattern instead of a year-range next to a "desde AAAA-MM" string.
    full_range_label = (
        f"{year_month(data['market_full_start'])[0]}-{year_month(data['market_latest_date'])[0]}"
    )
    recent_range_label = (
        f"{year_month(data['recent_window_start'])[0]}-{year_month(data['market_latest_date'])[0]}"
    )

    cape_value = ctx.cape if ctx else None
    inflation_value = ctx.inflation if ctx else None
    rate_value = ctx.interest_rate if ctx else None

    if snapshot.drawdown is not None and snapshot.drawdown == 0.0:
        drawdown_context = "Mercado en máximo histórico"
    elif snapshot.drawdown is not None:
        drawdown_context = f"Caída del {_fmt_pct(abs(snapshot.drawdown))} desde el máximo"
    else:
        drawdown_context = "No disponible"

    market_body = f"""
    <table>
      <tr>
        <th rowspan="2">Dato</th><th rowspan="2">Valor</th>
        <th colspan="2">Contexto histórico (vs. media del periodo)</th>
      </tr>
      <tr><th>Serie completa ({full_range_label})</th><th>Últimos {RECENT_WINDOW_YEARS} años ({recent_range_label})</th></tr>
      <tr><td>Fecha de datos</td><td>{data_date}</td><td>--</td><td>--</td></tr>
      <tr><td>Caída actual desde máximo</td><td>{_fmt_pct(snapshot.drawdown)}</td><td>{drawdown_context}</td><td>--</td></tr>
      <tr><td>CAPE</td><td>{_fmt_num(cape_value, 1)}</td><td>{context_band(cape_value, cape_mean, cape_std)}</td><td>{context_band(cape_value, recent_cape_mean, recent_cape_std)}</td></tr>
      <tr><td>Inflación (interanual)</td><td>{_fmt_pct(inflation_value)}</td><td>{context_band(inflation_value, inflation_mean, inflation_std)}</td><td>{context_band(inflation_value, recent_inflation_mean, recent_inflation_std)}</td></tr>
      <tr><td>Tipo de interés (bono EEUU 10 años)</td><td>{_fmt_rate(rate_value)}</td><td>{context_band(rate_value, rate_mean, rate_std)}</td><td>{context_band(rate_value, recent_rate_mean, recent_rate_std)}</td></tr>
    </table>
    """

    market_card = _card("Datos de mercado", market_body)

    # ---- Evidencia histórica ----

    evidence_body = f"""
    <p>Qué mira este bloque: compara las condiciones actuales del mercado -- incluida
    la ausencia de caída -- con caídas históricas, a la vez en varias dimensiones
    (magnitud, duración, velocidad, valoración, tendencia previa, volatilidad), y
    selecciona las más parecidas en conjunto. Observa qué retorno tuvieron los
    {evidence.horizon_years} años siguientes al fondo -- el punto más bajo -- de
    cada una de esas caídas.</p>
    <table class="kv">
      <tr><td>Episodios históricos comparables</td><td>{evidence.return_count}</td></tr>
      <tr><td>Retorno mediano posterior</td><td>{_fmt_pct(evidence.median_return)} anualizado real</td></tr>
      <tr><td>Peor caso observado</td><td>{_fmt_pct(evidence.worst_return)} anualizado real</td></tr>
      <tr><td>Mejor caso observado</td><td>{_fmt_pct(evidence.best_return)} anualizado real</td></tr>
    </table>
    <p class="note">Esta evidencia no autoriza agresividad: la validación
    predictiva del modelo sigue sin demostrarse (ver «Por qué no se actúa»).</p>
    """

    evidence_card = _card("Evidencia histórica", evidence_body)

    # ---- Alertas ----

    alerts = build_alerts(data)
    alerts_html = "<ul>" + "".join(f"<li>{_esc(a)}</li>" for a in alerts) + "</ul>"
    alerts_card = _card("Alertas", alerts_html)

    # ---- Detalle técnico (colapsado) ----

    gates_rows = f"""
    <tr><td>Evidence Quality</td><td>{_esc(data['eq_result'].state)}</td><td>{_esc('; '.join(data['eq_result'].explanations))}</td></tr>
    <tr><td>Regime Comparability</td><td>{_esc(data['regime_result'].state)}</td><td>{_esc('; '.join(data['regime_result'].explanations))}</td></tr>
    """
    if data["personal_capacity_available"]:
        for name, p in data["patrimonios"].items():
            pc = p["personal_capacity"]
            gates_rows += f"<tr><td>Personal Capacity Facts -- {_esc(name)}</td><td>{_esc(pc.state)}</td><td>{_esc('; '.join(pc.explanations))}</td></tr>"

    technical_patrimonios = ""
    if data["personal_capacity_available"]:
        for name, p in data["patrimonios"].items():
            combined = p["combined"]
            ha = p["human_approval"]
            dp = p["dry_powder"]
            ha_raw = "n/a" if ha is None else (
                f"state={ha.state} effective={ha.effective_posture_ceiling} "
                f"blocked={ha.blocked} authorizes_90={ha.authorizes_dry_powder_ceiling_90}"
            )
            dp_raw = "n/a" if dp is None else f"status={dp.status} authorized_amount={dp.authorized_amount}"
            technical_patrimonios += f"""
            <div class="patrimonio-block">
              <h3>{_esc(name)}</h3>
              <table>
                <tr><td>Postura combinada (gate_combination.min())</td><td>{_esc(combined.posture_ceiling)}</td></tr>
                <tr><td>Explicaciones crudas</td><td>{_esc('; '.join(combined.explanations))}</td></tr>
                <tr><td>Human Approval (raw)</td><td>{_esc(ha_raw)}</td></tr>
                <tr><td>Dry Powder (raw)</td><td>{_esc(dp_raw)}</td></tr>
              </table>
            </div>
            """

    technical_body = f"""
    <p class="note">Techo de mercado (Evidence Quality + Regime Comparability, sin Personal Capacity --
    market-wide by design, RE-043.1): {_esc(data['market_ceiling'].posture_ceiling)}</p>
    <table><tr><th>Gate</th><th>Estado interno</th><th>Explicación cruda</th></tr>{gates_rows}</table>
    {technical_patrimonios}
    <table>
      <tr><td>Snapshot.price (Shiller Price.1 -- índice total return real, serie técnica, no es el nivel del S&amp;P 500 de prensa)</td><td>{_fmt_num(snapshot.price, 4)}</td></tr>
      <tr><td>Evidence.return_count</td><td>{evidence.return_count}</td></tr>
      <tr><td>predictive_validation_status</td><td>{_esc(data['predictive_validation_status'])}</td></tr>
      <tr><td>CAPE histórico (media / desv. típica)</td><td>{_fmt_num(cape_mean, 2)} / {_fmt_num(cape_std, 2)}</td></tr>
      <tr><td>Inflación histórica (media / desv. típica)</td><td>{_fmt_pct(inflation_mean, 2)} / {_fmt_pct(inflation_std, 2)}</td></tr>
      <tr><td>Tipo 10a histórico (media / desv. típica)</td><td>{_fmt_rate(rate_mean)} / {_fmt_rate(rate_std)}</td></tr>
    </table>
    """

    technical_card = f'<details class="card"><summary>Detalle técnico</summary>{technical_body}</details>'

    style = """
    <style>
      body { font-family: -apple-system, Helvetica, Arial, sans-serif; background:#f7f7f5; color:#222; margin:0; padding:2rem; }
      header { margin-bottom: 1.5rem; }
      h1 { font-size: 1.4rem; margin-bottom: 0.2rem; }
      .subtitle { color:#666; font-size:0.9rem; margin:0 0 0.6rem 0; }
      .header-grid { display:flex; gap:2rem; flex-wrap:wrap; font-size:0.9rem; color:#555; }
      .card { background:#fff; border:1px solid #ddd; border-radius:8px; padding:1rem 1.25rem; margin-bottom:1.25rem; text-align:left; }
      .card h2 { font-size:1.05rem; margin-top:0; border-bottom:1px solid #eee; padding-bottom:0.4rem; }
      details.card summary { cursor:pointer; font-weight:600; font-size:1.05rem; }
      .headline-action { font-size:1.6rem; font-weight:700; letter-spacing:0.02em; display:flex; align-items:center; }
      .headline-sub { color:#444; margin-top:0.3rem; }
      .dot { display:inline-block; width:14px; height:14px; border-radius:50%; margin-right:0.6rem; flex-shrink:0; }
      .dot.ok { background:#2f8f4e; }
      .dot.warn { background:#c98a00; }
      .dot.bad { background:#c23b3b; }
      .dot.neutral { background:#999; }
      table { border-collapse: collapse; width:100%; font-size:0.9rem; margin-bottom:0.5rem; }
      td, th { text-align:left; padding:0.35rem 0.5rem; border-bottom:1px solid #f0f0f0; vertical-align:top; }
      .kv { max-width:640px; }
      .kv td:first-child { width:55%; }
      .patrimonio-block { border-left:3px solid #ccc; padding-left:1rem; margin-bottom:1rem; }
      .pill { display:inline-block; padding:0.1rem 0.6rem; border-radius:10px; font-size:0.8rem; font-weight:600; }
      .pill.ok { background:#dcefdc; color:#2f6b2f; }
      .pill.warn { background:#fbe8c6; color:#8a5a00; }
      .pill.bad { background:#f6d9d9; color:#a12b2b; }
      .pill.neutral { background:#e6e6e6; color:#555; }
      .note { font-size:0.82rem; color:#666; margin-top:0.3rem; }
    </style>
    """

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>SOP -- Panel de Estado</title>{style}</head>
<body>
<header>
  <h1>SOP -- Panel de Estado</h1>
  <p class="subtitle">Lectura de mercado, evidencia y autorización patrimonial. Solo lectura.</p>
  <div class="header-grid">
    <div>Fecha de datos: <strong>{data_date}</strong></div>
    <div>Generado: <strong>{_esc(generated_at)}</strong></div>
  </div>
</header>
{estado_hoy_card}
{porque_card}
{patrimonio_card}
{market_card}
{evidence_card}
{alerts_card}
{technical_card}
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
