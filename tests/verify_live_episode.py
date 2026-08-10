#!/usr/bin/env python3
"""
SOP Research Engine
Live Episode Detector Verification

Synthetic checks build a minimal DataFrame with only Date/P and run it
through drawdown_engine.py's own calculate_running_peak/calculate_drawdown
before calling detect_current_episode() -- exercising the exact same
precondition run_live_episode_detector() relies on, not a hand-built
Drawdown column that could silently drift from the real definition.

Also includes a real-pipeline check against data/raw/shiller.xlsx.
"""

from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.drawdown_engine import calculate_drawdown, calculate_running_peak
from engine.live_episode import detect_current_episode, run_live_episode_detector


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def assert_close(label: str, actual: float, expected: float, tol: float = 1e-9) -> None:

    if abs(actual - expected) > tol:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def _prepared(dates, prices):

    df = pd.DataFrame({"Date": dates, "P": prices})

    df = calculate_running_peak(df)
    df = calculate_drawdown(df)

    return df


def main() -> None:

    # -- No episode: monotonically rising, always at the peak --

    rising = _prepared(
        [2020.01, 2020.02, 2020.03, 2020.04],
        [100, 105, 110, 115],
    )
    assert_equal("rising_no_episode", detect_current_episode(rising), None)

    # -- Shallow dip only (-9.52%), never crosses the -10% threshold --

    shallow = _prepared(
        [2020.01, 2020.02, 2020.03, 2020.04],
        [100, 105, 95, 98],
    )
    assert_equal("shallow_no_episode", detect_current_episode(shallow), None)

    # -- Active episode, still deepening, no recovery yet --

    deepening = _prepared(
        [2021.01, 2021.02, 2021.03, 2021.04],
        [200, 195, 170, 160],
    )
    result = detect_current_episode(deepening)
    assert result is not None, "deepening: expected an active episode"
    assert_close("deepening_peak_date", result.peak_date, 2021.01)
    assert_close("deepening_peak_price", result.peak_price, 200)
    assert_close("deepening_as_of_date", result.as_of_date, 2021.04)
    assert_close("deepening_as_of_drawdown", result.as_of_drawdown, -0.20)
    assert_close("deepening_bottom_so_far_price", result.bottom_so_far_price, 160)
    assert_close(
        "deepening_bottom_so_far_drawdown", result.bottom_so_far_drawdown, -0.20
    )
    assert_equal("deepening_duration_months", result.duration_months, 3)

    # -- Active episode, deepened to -30% then partially recovered to --
    # -- -10% (still not a full recovery to a new peak) -- bottom_so_far --
    # -- must stay at the deepest point (-30%), not the shallower current --
    # -- reading. -10% also exercises the MIN_DRAWDOWN boundary exactly. --

    partial_recovery = _prepared(
        [2022.01, 2022.02, 2022.03, 2022.04],
        [100, 85, 70, 90],
    )
    result = detect_current_episode(partial_recovery)
    assert result is not None, "partial_recovery: expected an active episode"
    assert_close("partial_recovery_peak_price", result.peak_price, 100)
    assert_close("partial_recovery_as_of_drawdown", result.as_of_drawdown, -0.10)
    assert_close(
        "partial_recovery_bottom_so_far_price", result.bottom_so_far_price, 70
    )
    assert_close(
        "partial_recovery_bottom_so_far_drawdown",
        result.bottom_so_far_drawdown,
        -0.30,
    )

    # -- Episode that fully recovers to a new peak: no longer "active" --
    # -- by drawdown_engine.py's own definition -- ratchet reset case --

    recovered = _prepared(
        [2023.01, 2023.02, 2023.03],
        [100, 80, 100],
    )
    assert_equal("recovered_no_active_episode", detect_current_episode(recovered), None)

    # -- Real pipeline: data/raw/shiller.xlsx as it stands today --

    real_result = run_live_episode_detector()

    # As of this iteration (2026-08-10), the latest Shiller row
    # (2026.07) sits exactly at its running peak (Drawdown 0.0) --
    # confirmed by direct read before writing this test. Not a
    # canonical claim about the future: this assertion will correctly
    # start failing the day a real >=10% drawdown begins, which is the
    # point of the module.
    assert_equal("real_result_no_active_episode_today", real_result, None)

    print("LIVE EPISODE DETECTOR : STABLE")
    print()
    print(f"real_result: {real_result}")


if __name__ == "__main__":
    main()
