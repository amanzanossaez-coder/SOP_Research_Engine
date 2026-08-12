"""
SOP Research Engine
Human Approval State -- RE-032.7

Joins RE-032.6's pure gate (engine/human_approval.py) with a real
attestation history (data/raw/human_approval_attestations.xlsx) to
produce HumanApprovalInputs per patrimonio -- the same
loader/raw-I-O-then-adapter split every other real data source in this
project uses (loaders/human_approval_loader.py stays raw, this module
interprets).

market_crisis_at_registration is resolved here, not typed by Armando:
each attestation's real calendar date is converted to Shiller's AAAA.MM
month (engine.live_episode.calendar_date_to_shiller_month(),
extracted for reuse in RE-032.7) and the market Drawdown at that month
is looked up (engine.live_episode.drawdown_at_month(), RE-041.7) and
compared against MIN_DRAWDOWN -- RE-032.4's own literal definition of
market_crisis ("Drawdown <= MIN_DRAWDOWN, the same constant
drawdown_engine.py already uses"). No new threshold logic is
introduced; this reuses the constant directly.

Fail-closed on malformed rows: a row with an unparseable date or an
unrecognized posture is skipped, not guessed, with an explanation
recorded -- the same discipline
engine.dry_powder_ledger_state.compute_ledger_episode_state() already
applies to malformed tranche rows.

RE-B (RE-032.10 iteration B) -- reads the xlsx's new column E
("autoriza_techo_90") and passes it straight into
Attestation.authorizes_dry_powder_ceiling_90, unconditionally, even for
a row whose posture isn't Deploy Aggressively. Whether that actually
does anything is engine.human_approval._ceiling_90_active()'s decision
alone (it already checks the posture) -- duplicating that check here
would be the same logic in two places for no reason. No wiring into
Dry Powder Protocol yet -- that is iteration C.
"""

from datetime import date
from typing import Optional

from engine.drawdown_engine import MIN_DRAWDOWN
from engine.gate_combination import POSTURE_ORDER
from engine.human_approval import Attestation, HumanApprovalInputs
from engine.live_episode import (
    calendar_date_to_shiller_month,
    drawdown_at_month,
    load_prepared_shiller_df,
)
from engine.manual_entry_parsing import to_calendar_date_or_none
from loaders.human_approval_loader import load_human_approval_raw


_YES_TOKENS = {"sí", "si", "yes", "true"}


def _to_bool_si_no(value) -> bool:
    """
    Generic Sí/No -> bool parser, shared by every boolean column this
    loader's rows carry (crisis_personal, autoriza_techo_90 as of RE-B)
    -- one parsing rule, not one copy per column.
    """

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    return str(value).strip().lower() in _YES_TOKENS


def _build_patrimonio_attestations(
    events, shiller_df
) -> tuple:

    attestations = []
    explanations = []

    for event in events:

        registered_at = to_calendar_date_or_none(event.get("fecha"))

        if registered_at is None:
            explanations.append(
                f"attestation row skipped, unparseable fecha: {event.get('fecha')!r}"
            )
            continue

        posture = event.get("postura")

        if posture not in POSTURE_ORDER:
            explanations.append(
                f"attestation row on {registered_at} skipped, unrecognized "
                f"postura: {posture!r}"
            )
            continue

        market_crisis_at_registration = False

        if shiller_df is not None:
            month = calendar_date_to_shiller_month(registered_at)
            drawdown_then = drawdown_at_month(shiller_df, month)
            if drawdown_then is not None:
                market_crisis_at_registration = drawdown_then <= MIN_DRAWDOWN

        attestations.append(
            Attestation(
                registered_at=registered_at,
                approved_posture_ceiling=posture,
                personal_crisis_declared=_to_bool_si_no(
                    event.get("crisis_personal")
                ),
                market_crisis_at_registration=market_crisis_at_registration,
                # RE-B -- passed through unconditionally, even if this
                # row's posture isn't Deploy Aggressively: whether it
                # actually matters is engine.human_approval's job
                # (_ceiling_90_active already gates on posture), not
                # duplicated here.
                authorizes_dry_powder_ceiling_90=_to_bool_si_no(
                    event.get("autoriza_techo_90")
                ),
                notes=str(event.get("nota") or ""),
            )
        )

    return tuple(attestations), explanations


def build_local_human_approval_inputs(
    file_path=None,
    as_of_date: Optional[date] = None,
):
    """
    I/O + adaptation: loads
    data/raw/human_approval_attestations.xlsx, loads the prepared
    Shiller series once (for market_crisis_at_registration lookups
    across every patrimonio and every attestation), and returns
    {patrimonio_name: HumanApprovalInputs}. Returns None if the
    attestation file is missing.

    Explanations for skipped rows are printed, not silently discarded
    -- same convention as loaders/personal_capacity_facts_loader.py's
    duplicate-label warning.
    """

    raw = load_human_approval_raw(file_path)

    if raw is None:
        return None

    shiller_df = load_prepared_shiller_df()

    result = {}

    for patrimonio_name, events in raw.items():

        attestations, explanations = _build_patrimonio_attestations(
            events, shiller_df
        )

        for explanation in explanations:
            print(f"⚠️  {patrimonio_name}: {explanation}")

        result[patrimonio_name] = HumanApprovalInputs(
            attestations=attestations,
            as_of_date=as_of_date,
        )

    return result
