"""
SOP Research Engine
Live Episode Detector

Answers exactly one question, purely from Shiller data, with no state
of its own: is the market currently inside a drawdown episode (by
drawdown_engine.py's own -10% definition), and if so, since when.

This is the automatable half of what Dry Powder Protocol
(engine/dry_powder_protocol.py) needs. It is NOT the other half:
initial_dry_powder, cum_deployed_in_episode and the two
since-last-tranche fields cannot be derived from market data -- only
Armando knows what his real liquidity was when an episode started and
what he has actually deployed since. Those remain a manually operated
ledger, deliberately out of scope here (see the RE-041.1 code entry in
the governance doc for that design question).

Deliberately mirrors drawdown_engine.py's own state machine
(detect_drawdowns()) rather than reusing it directly, because that
function only ever returns CLOSED episodes -- an episode still
in progress at the end of the series is silently dropped (never
appended to the returned list, since the loop only appends on a
Drawdown == 0 recovery row). This module exists specifically to
surface that unresolved tail instead of discarding it. MIN_DRAWDOWN
and the run-preparation functions (calculate_running_peak,
calculate_drawdown) are imported from drawdown_engine.py, not
redefined -- both sides must use the same episode definition, and
Frozen Core stays untouched (no changes to drawdown_engine.py).
"""

from dataclasses import dataclass
from typing import Optional

from loaders.shiller_loader import load_shiller_data
from engine.date_utils import months_between
from engine.drawdown_engine import (
    MIN_DRAWDOWN,
    calculate_drawdown,
    calculate_running_peak,
)


@dataclass
class CurrentEpisode:
    """
    An unresolved (still in progress) drawdown episode, as of the most
    recent row in the Shiller dataset. There is no bottom_date /
    bottom_price here in the sense drawdown_engine.py's Episode has --
    "the bottom so far" is only ever provisional until (if) recovery
    happens, so it is named accordingly.
    """

    peak_date: float
    peak_price: float

    as_of_date: float
    as_of_price: float
    as_of_drawdown: float

    bottom_so_far_date: float
    bottom_so_far_price: float
    bottom_so_far_drawdown: float

    duration_months: Optional[int] = None


def detect_current_episode(df) -> Optional[CurrentEpisode]:
    """
    df must already carry RunningPeak/Drawdown (calculate_running_peak,
    calculate_drawdown already applied) -- same precondition
    drawdown_engine.py's own detect_drawdowns() has.

    Returns None if the series is currently at (or above, which cannot
    happen by construction of RunningPeak) its running peak, or in a
    dip shallower than MIN_DRAWDOWN -- i.e. no episode by
    drawdown_engine.py's own definition is active right now.
    """

    peak = None
    peak_index = None

    peak_before = None

    in_drawdown = False

    bottom = None

    for i, row in df.iterrows():

        if row["Drawdown"] == 0:

            peak = row
            peak_index = i

            # A full recovery to a new high closes out any prior
            # drawdown -- matches drawdown_engine.py's own episode
            # definition (RE-041.1's ratchet reset condition).
            in_drawdown = False

        elif row["Drawdown"] <= MIN_DRAWDOWN:

            if not in_drawdown:

                peak_before = peak

                bottom = row

                in_drawdown = True

            elif row["Drawdown"] < bottom["Drawdown"]:

                bottom = row

        # else: a dip shallower than MIN_DRAWDOWN -- state carries
        # over unchanged, identical to detect_drawdowns().

    if not in_drawdown:
        return None

    as_of = df.iloc[-1]

    duration_months = months_between(
        peak_before["Date"],
        as_of["Date"],
    )

    return CurrentEpisode(
        peak_date=peak_before["Date"],
        peak_price=peak_before["P"],
        as_of_date=as_of["Date"],
        as_of_price=as_of["P"],
        as_of_drawdown=as_of["Drawdown"],
        bottom_so_far_date=bottom["Date"],
        bottom_so_far_price=bottom["P"],
        bottom_so_far_drawdown=bottom["Drawdown"],
        duration_months=duration_months,
    )


def run_live_episode_detector() -> Optional[CurrentEpisode]:
    """
    Loads Shiller data fresh and runs detect_current_episode() on it.
    No caching, no persisted state -- every call re-derives the answer
    from data/raw/shiller.xlsx as it stands today. Returns None if the
    file is missing (same fail-closed convention as every other loader
    in this project) or if no episode is currently active.
    """

    df = load_shiller_data()

    if df is None:
        return None

    df = calculate_running_peak(df)
    df = calculate_drawdown(df)

    return detect_current_episode(df)
