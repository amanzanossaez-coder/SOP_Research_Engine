"""
SOP Research Engine
Dry Powder Ledger State -- RE-041.4

Joins RE-041.2's live market-episode detection
(engine/live_episode.py) with RE-041.3's manual ledger
(data/raw/dry_powder_ledger.xlsx) to produce the parts of
DryPowderProtocolInputs (engine/dry_powder_protocol.py) that neither
piece can supply alone.

Deliberately does NOT produce a ready-to-evaluate
DryPowderProtocolInputs. `current_posture` and
`human_approval_above_ceiling` are not this module's concern -- they
come from the combined-gate pipeline and Human Approval respectively,
neither of which this module reads or should read (single
responsibility, same discipline as every other gate/adapter this
session). A future caller merges this module's LedgerEpisodeState with
those two separately-sourced values to build the final
DryPowderProtocolInputs.

Scope of this iteration, stated plainly rather than silently
shipped partial: `drawdown_pp_since_last_deployment` is NOT computed
here. Doing so correctly requires looking up the market drawdown at
the exact historical month of the last tranche against the full
prepared Shiller series (not just the terminal CurrentEpisode
snapshot RE-041.2 exposes) -- a real feature, deferred to its own
iteration rather than bolted on here. Its absence is safe: RE-041.1's
cadence check is days OR drawdown-points, so leaving this field None
never blocks or wrongly authorizes anything -- cadence can still be
satisfied on days alone.

Two fail-closed judgment calls made explicit here rather than buried
in code:

1.  If the ledger's Section 1 episode marker is missing, or its start
    date does not match the live-detected episode's peak_date, this
    module treats initial_dry_powder as unknown -- never falls back to
    a stale figure from a different (possibly prior) episode.
2.  If no tranche has been logged yet for the current episode,
    highest_posture_in_episode defaults to CONSERVE (the lowest rank).
    Combined with dry_powder_protocol.py's own
    max(current_posture, highest_posture_in_episode) ratchet logic,
    this means the ratchet grants no unearned benefit until at least
    one tranche has actually been logged at a higher posture.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from engine.gate_combination import CONSERVE, POSTURE_ORDER
from engine.live_episode import run_live_episode_detector
from loaders.dry_powder_ledger_loader import (
    EPISODE_START_LABEL,
    INITIAL_DRY_POWDER_LABEL,
    load_dry_powder_ledger_raw,
)


_PLACEHOLDER_TOKENS = {"pendiente"}


@dataclass
class LedgerEpisodeState:

    has_active_episode: bool

    initial_dry_powder: Optional[float]
    remaining_dry_powder: Optional[float]
    cum_deployed_in_episode: float

    days_since_last_deployment: Optional[int]
    drawdown_pp_since_last_deployment: Optional[float]

    highest_posture_in_episode: str

    explanations: list[str] = field(default_factory=list)


def _to_float_or_none(value):

    if value is None:
        return None

    if isinstance(value, str) and value.strip().lower() in _PLACEHOLDER_TOKENS:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_calendar_date_or_none(value):

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):

        text = value.strip()

        if not text or text.lower() in _PLACEHOLDER_TOKENS:
            return None

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue

    return None


def _calendar_date_to_shiller_month(d: date) -> float:

    return d.year + d.month / 100


def compute_ledger_episode_state(
    current_episode,
    raw_patrimonio,
    as_of_calendar_date: Optional[date] = None,
) -> LedgerEpisodeState:
    """
    Pure logic, no I/O -- current_episode is
    engine.live_episode.CurrentEpisode or None, raw_patrimonio is one
    entry of loaders.dry_powder_ledger_loader.load_dry_powder_ledger_raw()'s
    return value. Kept separate from build_local_dry_powder_ledger_state()
    so this can be exercised directly with synthetic inputs.
    """

    if as_of_calendar_date is None:
        as_of_calendar_date = date.today()

    if current_episode is None:
        return LedgerEpisodeState(
            has_active_episode=False,
            initial_dry_powder=None,
            remaining_dry_powder=None,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=None,
            drawdown_pp_since_last_deployment=None,
            highest_posture_in_episode=CONSERVE,
            explanations=[
                "no active market episode detected -- Dry Powder "
                "Protocol inputs are not meaningful today"
            ],
        )

    episode_marker = raw_patrimonio.get("episode_marker", {})

    ledger_start = _to_float_or_none(episode_marker.get(EPISODE_START_LABEL))
    initial_dry_powder = _to_float_or_none(
        episode_marker.get(INITIAL_DRY_POWDER_LABEL)
    )

    marker_matches_live_episode = (
        ledger_start is not None
        and initial_dry_powder is not None
        and abs(ledger_start - current_episode.peak_date) < 1e-9
    )

    if not marker_matches_live_episode:

        if ledger_start is None or initial_dry_powder is None:
            reason = (
                "ledger Section 1 (episode marker) is not filled in for "
                "any episode yet"
            )
        else:
            reason = (
                f"ledger episode start ({ledger_start}) does not match "
                f"the live-detected peak ({current_episode.peak_date}) -- "
                "treating as not yet logged for the current episode "
                "rather than trusting a possibly stale figure"
            )

        return LedgerEpisodeState(
            has_active_episode=True,
            initial_dry_powder=None,
            remaining_dry_powder=None,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=None,
            drawdown_pp_since_last_deployment=None,
            highest_posture_in_episode=CONSERVE,
            explanations=[reason],
        )

    explanations = []

    episode_tranches = []

    for tranche in raw_patrimonio.get("tranches", []):

        tranche_date = _to_calendar_date_or_none(tranche.get("fecha"))

        if tranche_date is None:
            explanations.append(
                f"tranche row skipped, unparseable fecha: {tranche.get('fecha')!r}"
            )
            continue

        tranche_month = _calendar_date_to_shiller_month(tranche_date)

        if tranche_month < ledger_start:
            # belongs to a prior, already-closed episode -- the ledger
            # is append-only, this is expected, not an error.
            continue

        episode_tranches.append((tranche_date, tranche))

    cum_deployed_in_episode = 0.0
    highest_posture_in_episode = CONSERVE
    days_since_last_deployment = None

    for tranche_date, tranche in episode_tranches:

        importe = _to_float_or_none(tranche.get("importe"))

        if importe is None:
            explanations.append(
                f"tranche on {tranche_date} skipped, unparseable importe: "
                f"{tranche.get('importe')!r}"
            )
            continue

        cum_deployed_in_episode += importe

        postura = tranche.get("postura")

        if postura in POSTURE_ORDER and (
            POSTURE_ORDER[postura] > POSTURE_ORDER[highest_posture_in_episode]
        ):
            highest_posture_in_episode = postura

    if episode_tranches:
        last_tranche_date = max(d for d, _ in episode_tranches)
        days_since_last_deployment = (
            as_of_calendar_date - last_tranche_date
        ).days

    remaining_dry_powder = max(
        0.0, initial_dry_powder - cum_deployed_in_episode
    )

    explanations.append(
        "drawdown_pp_since_last_deployment not computed this iteration "
        "-- requires a month-level Shiller lookup not yet built; cadence "
        "can still be satisfied on days_since_last_deployment alone"
    )

    return LedgerEpisodeState(
        has_active_episode=True,
        initial_dry_powder=initial_dry_powder,
        remaining_dry_powder=remaining_dry_powder,
        cum_deployed_in_episode=cum_deployed_in_episode,
        days_since_last_deployment=days_since_last_deployment,
        drawdown_pp_since_last_deployment=None,
        highest_posture_in_episode=highest_posture_in_episode,
        explanations=explanations,
    )


def build_local_dry_powder_ledger_state(file_path=None):
    """
    I/O + adaptation: loads data/raw/dry_powder_ledger.xlsx, runs the
    live episode detector once, and evaluates
    compute_ledger_episode_state() per patrimonio tab. Returns None if
    the ledger file is missing (same fail-closed convention as every
    other loader in this project).
    """

    raw = load_dry_powder_ledger_raw(file_path)

    if raw is None:
        return None

    current_episode = run_live_episode_detector()

    return {
        patrimonio_name: compute_ledger_episode_state(
            current_episode, raw_patrimonio
        )
        for patrimonio_name, raw_patrimonio in raw.items()
    }
