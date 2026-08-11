#!/usr/bin/env python3
"""
SOP Research Engine
Dry Powder Ledger State Verification

RE-041.4 -- synthetic checks on compute_ledger_episode_state() (pure
logic, no I/O), plus a real-pipeline check on
build_local_dry_powder_ledger_state() against the actual
data/raw/dry_powder_ledger.xlsx and today's live market state.

RE-041.5 -- synthetic checks on to_dry_powder_protocol_inputs(), the
final assembly step.

RE-041.7 -- synthetic checks on drawdown_pp_since_last_deployment now
being computed when a Shiller series is supplied, including the sign
convention (a partial market recovery since the last tranche must
clamp to 0.0 points of "additional" drawdown, never a negative
number).
"""

from datetime import date
from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.dry_powder_ledger_state import (
    LedgerEpisodeState,
    build_local_dry_powder_ledger_state,
    compute_ledger_episode_state,
    to_dry_powder_protocol_inputs,
)
from engine.dry_powder_protocol import AUTHORIZED, DryPowderProtocol
from engine.gate_combination import CONSERVE, DEPLOY_AGGRESSIVELY, DEPLOY_PARTIALLY
from engine.live_episode import CurrentEpisode
from loaders.dry_powder_ledger_loader import (
    EPISODE_START_LABEL,
    INITIAL_DRY_POWDER_LABEL,
)


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def assert_close(label: str, actual: float, expected: float, tol: float = 1e-6) -> None:

    if abs(actual - expected) > tol:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


SAMPLE_EPISODE = CurrentEpisode(
    peak_date=2026.03,
    peak_price=200.0,
    as_of_date=2026.07,
    as_of_price=170.0,
    as_of_drawdown=-0.15,
    bottom_so_far_date=2026.06,
    bottom_so_far_price=160.0,
    bottom_so_far_drawdown=-0.20,
    duration_months=4,
)


def main() -> None:

    # -- No active episode: everything trivially empty --

    no_episode = compute_ledger_episode_state(None, {"episode_marker": {}, "tranches": []})
    assert_equal("no_episode_active", no_episode.has_active_episode, False)
    assert_equal("no_episode_initial_dp", no_episode.initial_dry_powder, None)
    assert_equal("no_episode_cum_deployed", no_episode.cum_deployed_in_episode, 0.0)
    assert_equal("no_episode_highest_posture", no_episode.highest_posture_in_episode, CONSERVE)

    # -- Active episode, ledger Section 1 still "Pendiente" --

    pending_marker = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: "Pendiente",
                INITIAL_DRY_POWDER_LABEL: "Pendiente",
            },
            "tranches": [],
        },
    )
    assert_equal("pending_marker_active", pending_marker.has_active_episode, True)
    assert_equal("pending_marker_initial_dp", pending_marker.initial_dry_powder, None)
    assert_equal("pending_marker_remaining_dp", pending_marker.remaining_dry_powder, None)

    # -- Active episode, ledger marker present but from a DIFFERENT --
    # -- (mismatched) episode start -- must not trust it --

    mismatched_marker = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2020.01,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [],
        },
    )
    assert_equal("mismatched_marker_active", mismatched_marker.has_active_episode, True)
    assert_equal("mismatched_marker_initial_dp", mismatched_marker.initial_dry_powder, None)

    # -- Active episode, marker matches, no tranches logged yet --

    matched_no_tranches = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2026.03,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [],
        },
    )
    assert_equal("matched_no_tranches_active", matched_no_tranches.has_active_episode, True)
    assert_close("matched_no_tranches_initial_dp", matched_no_tranches.initial_dry_powder, 100000.0)
    assert_close("matched_no_tranches_remaining_dp", matched_no_tranches.remaining_dry_powder, 100000.0)
    assert_equal("matched_no_tranches_cum_deployed", matched_no_tranches.cum_deployed_in_episode, 0.0)
    assert_equal(
        "matched_no_tranches_highest_posture",
        matched_no_tranches.highest_posture_in_episode,
        CONSERVE,
    )
    assert_equal(
        "matched_no_tranches_days_since_last",
        matched_no_tranches.days_since_last_deployment,
        None,
    )

    # -- Active episode, marker matches, real tranches: one from a --
    # -- PRIOR episode (before ledger_start, must be excluded), two --
    # -- within the current episode at Partially then Aggressively --
    # -- (highest must be Aggressively), plus one unparseable row --

    with_tranches_as_of = date(2026, 8, 10)

    with_tranches = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2026.03,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [
                {
                    "fecha": "2025-11-10",
                    "importe": 5000.0,
                    "postura": DEPLOY_AGGRESSIVELY,
                    "nota": "episodio anterior, no debe contar",
                },
                {
                    "fecha": "2026-04-02",
                    "importe": 12000.0,
                    "postura": DEPLOY_PARTIALLY,
                    "nota": "primer tramo del episodio actual",
                },
                {
                    "fecha": "2026-06-15",
                    "importe": 22000.0,
                    "postura": DEPLOY_AGGRESSIVELY,
                    "nota": "segundo tramo, escalada",
                },
                {
                    "fecha": "no es una fecha",
                    "importe": 999.0,
                    "postura": DEPLOY_PARTIALLY,
                    "nota": "fila corrupta, debe omitirse sin romper nada",
                },
            ],
        },
        as_of_calendar_date=with_tranches_as_of,
    )
    assert_equal("with_tranches_active", with_tranches.has_active_episode, True)
    assert_close("with_tranches_cum_deployed", with_tranches.cum_deployed_in_episode, 34000.0)
    assert_close("with_tranches_remaining_dp", with_tranches.remaining_dry_powder, 66000.0)
    assert_equal(
        "with_tranches_highest_posture",
        with_tranches.highest_posture_in_episode,
        DEPLOY_AGGRESSIVELY,
    )
    assert_equal(
        "with_tranches_days_since_last",
        with_tranches.days_since_last_deployment,
        (with_tranches_as_of - date(2026, 6, 15)).days,
    )
    assert_equal(
        "with_tranches_drawdown_pp_no_shiller_df",
        with_tranches.drawdown_pp_since_last_deployment,
        None,
    )

    as_of = date(2026, 8, 10)
    with_tranches_fixed_date = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2026.03,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [
                {"fecha": "2026-06-15", "importe": 22000.0, "postura": DEPLOY_AGGRESSIVELY, "nota": ""},
            ],
        },
        as_of_calendar_date=as_of,
    )
    assert_equal(
        "with_tranches_fixed_date_days_since_last",
        with_tranches_fixed_date.days_since_last_deployment,
        (as_of - date(2026, 6, 15)).days,
    )

    # -- drawdown_pp_since_last_deployment, WITH a supplied Shiller --
    # -- series. Last tranche on 2026-06-15 (-> Shiller month 2026.06). --

    # Case A: market fell FURTHER since the last tranche (-5% then,
    # -15% now per SAMPLE_EPISODE.as_of_drawdown) -> 10.0 points.
    deepening_df = pd.DataFrame(
        {"Date": [2026.01, 2026.06, 2026.07], "Drawdown": [0.0, -0.05, -0.15]}
    )
    with_shiller_deepening = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2026.03,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [
                {"fecha": "2026-06-15", "importe": 22000.0, "postura": DEPLOY_AGGRESSIVELY, "nota": ""},
            ],
        },
        shiller_df=deepening_df,
    )
    assert_close(
        "drawdown_pp_deepening",
        with_shiller_deepening.drawdown_pp_since_last_deployment,
        10.0,
    )

    # Case B: market PARTIALLY RECOVERED since the last tranche (-25%
    # then, -15% now) -- must clamp to 0.0, never a negative number of
    # "additional" points.
    recovering_df = pd.DataFrame(
        {"Date": [2026.01, 2026.06, 2026.07], "Drawdown": [0.0, -0.25, -0.15]}
    )
    with_shiller_recovering = compute_ledger_episode_state(
        SAMPLE_EPISODE,
        {
            "episode_marker": {
                EPISODE_START_LABEL: 2026.03,
                INITIAL_DRY_POWDER_LABEL: 100000.0,
            },
            "tranches": [
                {"fecha": "2026-06-15", "importe": 22000.0, "postura": DEPLOY_AGGRESSIVELY, "nota": ""},
            ],
        },
        shiller_df=recovering_df,
    )
    assert_close(
        "drawdown_pp_recovering_clamped_to_zero",
        with_shiller_recovering.drawdown_pp_since_last_deployment,
        0.0,
    )

    # -- Assembly: no active episode -> nothing to evaluate --

    assert_equal(
        "assembly_no_episode",
        to_dry_powder_protocol_inputs(no_episode, DEPLOY_PARTIALLY),
        None,
    )

    # -- Assembly: active episode but ledger unresolved -> nothing to --
    # -- evaluate, never a guessed number --

    assert_equal(
        "assembly_pending_marker",
        to_dry_powder_protocol_inputs(pending_marker, DEPLOY_PARTIALLY),
        None,
    )

    # -- Assembly: fully resolved ledger state -> real --
    # -- DryPowderProtocolInputs, correctly mapped, default --
    # -- human_approval_above_ceiling=False, and it actually evaluates --

    assembled = to_dry_powder_protocol_inputs(with_tranches, DEPLOY_PARTIALLY)
    assert assembled is not None, "assembly: expected a resolved DryPowderProtocolInputs"
    assert_equal("assembled_current_posture", assembled.current_posture, DEPLOY_PARTIALLY)
    assert_close("assembled_initial_dp", assembled.initial_dry_powder, 100000.0)
    assert_close("assembled_remaining_dp", assembled.remaining_dry_powder, 66000.0)
    assert_close("assembled_cum_deployed", assembled.cum_deployed_in_episode, 34000.0)
    assert_equal(
        "assembled_highest_posture", assembled.highest_posture_in_episode, DEPLOY_AGGRESSIVELY
    )
    assert_equal("assembled_human_approval_default", assembled.human_approval_above_ceiling, False)

    evaluated = DryPowderProtocol().evaluate(assembled)
    assert_equal("assembled_evaluates_authorized", evaluated.status, AUTHORIZED)

    # -- Assembly: human_approval_above_ceiling passes through --

    assembled_approved = to_dry_powder_protocol_inputs(
        with_tranches, DEPLOY_AGGRESSIVELY, human_approval_above_ceiling=True
    )
    assert_equal(
        "assembled_human_approval_passthrough",
        assembled_approved.human_approval_above_ceiling,
        True,
    )

    # -- Real pipeline: today's actual ledger + live market state. As --
    # -- of RE-041.2, the market has no active episode -- both --
    # -- patrimonios should report has_active_episode=False. --

    real_state = build_local_dry_powder_ledger_state()

    assert real_state is not None, "real ledger file should load"
    assert_equal("real_state_patrimonios", set(real_state.keys()), {"AMS", "AML"})

    for name, state in real_state.items():
        assert_equal(f"real_{name}_no_active_episode_today", state.has_active_episode, False)

    print("DRY POWDER LEDGER STATE : STABLE")
    print()
    for name, state in real_state.items():
        print(f"{name}: {state}")


if __name__ == "__main__":
    main()
