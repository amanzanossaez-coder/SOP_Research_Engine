"""
SOP Research Engine
Dry Powder Ledger State -- RE-041.4 / RE-041.5 / RE-041.7

Joins RE-041.2's live market-episode detection
(engine/live_episode.py) with RE-041.3's manual ledger
(data/raw/dry_powder_ledger.xlsx) to produce the parts of
DryPowderProtocolInputs (engine/dry_powder_protocol.py) that neither
piece can supply alone: compute_ledger_episode_state() /
build_local_dry_powder_ledger_state().

RE-041.5 adds the final assembly step, to_dry_powder_protocol_inputs():
it still never reads or computes `current_posture` or
`human_approval_above_ceiling` itself -- those come from the
combined-gate pipeline and Human Approval respectively, neither of
which this module has any business touching (single responsibility,
same discipline as every other gate/adapter this session). The
function only *accepts* those two as arguments from whichever caller
already has them (e.g. audit_posture.py's per-patrimonio
evaluate_capital_posture() result) and merges them with this module's
own LedgerEpisodeState output. This is glue, not a new source of
truth for either field.

RE-041.7 closes the gap RE-041.4 deliberately left open:
`drawdown_pp_since_last_deployment` is now computed, given a prepared
Shiller series (engine.live_episode.load_prepared_shiller_df()),
by looking up the market drawdown at the last tranche's month via
engine.live_episode.drawdown_at_month() and comparing it to today's.
The comparison is signed and clamped at zero, not an absolute
difference -- a partial market recovery since the last tranche must
never count as "additional drawdown" (see the comment at the
computation itself). Still optional: compute_ledger_episode_state()
accepts shiller_df=None (its previous behaviour) and simply leaves the
field unset with an explanation, which stays safe because RE-041.1's
cadence check is days OR drawdown-points.

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

from engine.dry_powder_protocol import DryPowderProtocolInputs
from engine.gate_combination import CONSERVE, POSTURE_ORDER
from engine.live_episode import (
    detect_current_episode,
    drawdown_at_month,
    load_prepared_shiller_df,
)
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
    shiller_df=None,
) -> LedgerEpisodeState:
    """
    Pure logic, no I/O of its own -- current_episode is
    engine.live_episode.CurrentEpisode or None, raw_patrimonio is one
    entry of loaders.dry_powder_ledger_loader.load_dry_powder_ledger_raw()'s
    return value. Kept separate from build_local_dry_powder_ledger_state()
    so this can be exercised directly with synthetic inputs.

    shiller_df (RE-041.7): the full prepared Shiller series (as
    returned by engine.live_episode.load_prepared_shiller_df()), used
    only to look up the market drawdown at the last tranche's month
    for drawdown_pp_since_last_deployment. Optional and caller-supplied
    rather than loaded internally, to keep this function testable with
    synthetic data and to avoid this module owning Shiller I/O -- when
    None, that one field is left unset (RE-041.4's original behaviour),
    which is always safe since RE-041.1's cadence check is days OR
    drawdown-points.
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
    drawdown_pp_since_last_deployment = None

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

        if shiller_df is None:
            explanations.append(
                "drawdown_pp_since_last_deployment not computed -- no "
                "Shiller series supplied; cadence can still be satisfied "
                "on days_since_last_deployment alone"
            )
        else:
            last_tranche_month = _calendar_date_to_shiller_month(
                last_tranche_date
            )
            drawdown_then = drawdown_at_month(shiller_df, last_tranche_month)

            if drawdown_then is None or current_episode.as_of_drawdown is None:
                explanations.append(
                    "drawdown_pp_since_last_deployment not computed -- "
                    "could not look up market drawdown at the last "
                    "tranche's month"
                )
            else:
                # Both Drawdown values are negative (or zero). A market
                # that has fallen FURTHER since the last tranche has
                # as_of_drawdown more negative than drawdown_then, so
                # (drawdown_then - as_of_drawdown) is positive -- "N
                # points of additional drawdown." A partial recovery
                # since the last tranche makes this negative; clamped
                # to 0.0 rather than reported as a negative number of
                # points, because a recovery is not "additional
                # drawdown" and must never satisfy this cadence leg.
                drawdown_pp_since_last_deployment = max(
                    0.0,
                    (drawdown_then - current_episode.as_of_drawdown) * 100,
                )

    remaining_dry_powder = max(
        0.0, initial_dry_powder - cum_deployed_in_episode
    )

    return LedgerEpisodeState(
        has_active_episode=True,
        initial_dry_powder=initial_dry_powder,
        remaining_dry_powder=remaining_dry_powder,
        cum_deployed_in_episode=cum_deployed_in_episode,
        days_since_last_deployment=days_since_last_deployment,
        drawdown_pp_since_last_deployment=drawdown_pp_since_last_deployment,
        highest_posture_in_episode=highest_posture_in_episode,
        explanations=explanations,
    )


def to_dry_powder_protocol_inputs(
    ledger_state: LedgerEpisodeState,
    current_posture: str,
    human_approval_above_ceiling: bool = False,
) -> Optional[DryPowderProtocolInputs]:
    """
    RE-041.5 -- assembles a DryPowderProtocolInputs from this module's
    output plus the two fields that are never this module's concern:
    current_posture (combined-gate ceiling, e.g.
    engine.posture_mapper.evaluate_capital_posture()'s result) and
    human_approval_above_ceiling (Human Approval / RE-032.4, no code
    yet -- defaults to False, never assumed True).

    Returns None when there is nothing meaningful to evaluate yet:
    no active episode, or an active episode whose ledger Section 1
    isn't resolved (initial_dry_powder/remaining_dry_powder unknown).
    dry_powder_protocol.py requires concrete floats for both, not
    Optional -- inventing a placeholder number here would be exactly
    the silent-guess failure mode this project rejects elsewhere.
    """

    if not ledger_state.has_active_episode:
        return None

    if (
        ledger_state.initial_dry_powder is None
        or ledger_state.remaining_dry_powder is None
    ):
        return None

    return DryPowderProtocolInputs(
        current_posture=current_posture,
        initial_dry_powder=ledger_state.initial_dry_powder,
        remaining_dry_powder=ledger_state.remaining_dry_powder,
        cum_deployed_in_episode=ledger_state.cum_deployed_in_episode,
        days_since_last_deployment=ledger_state.days_since_last_deployment,
        drawdown_pp_since_last_deployment=(
            ledger_state.drawdown_pp_since_last_deployment
        ),
        highest_posture_in_episode=ledger_state.highest_posture_in_episode,
        human_approval_above_ceiling=human_approval_above_ceiling,
    )


def build_local_dry_powder_ledger_state(file_path=None):
    """
    I/O + adaptation: loads data/raw/dry_powder_ledger.xlsx, loads and
    prepares the Shiller series once (RE-041.7 -- shared for both the
    live episode detection and the drawdown_pp_since_last_deployment
    lookup, so this only reads shiller.xlsx a single time per call),
    and evaluates compute_ledger_episode_state() per patrimonio tab.
    Returns None if the ledger file is missing (same fail-closed
    convention as every other loader in this project).
    """

    raw = load_dry_powder_ledger_raw(file_path)

    if raw is None:
        return None

    shiller_df = load_prepared_shiller_df()

    current_episode = (
        detect_current_episode(shiller_df) if shiller_df is not None else None
    )

    return {
        patrimonio_name: compute_ledger_episode_state(
            current_episode, raw_patrimonio, shiller_df=shiller_df
        )
        for patrimonio_name, raw_patrimonio in raw.items()
    }
