#!/usr/bin/env python3
"""
SOP Research Engine
Dry Powder Protocol Verification

RE-041.1 -- first isolated code for the module. Synthetic checks only:
this protocol has no real data source of its own (stateless, caller
supplies the episode snapshot), so there is no real-pipeline section
here the way personal_capacity_facts_gate's test file has one.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.dry_powder_protocol import (
    AUTHORIZED,
    CADENCE_NOT_MET,
    CEILING_FRACTION_AGGRESSIVE_EXTENDED,
    CEILING_REACHED,
    POSTURE_NO_DEPLOYMENT,
    DryPowderProtocol,
    DryPowderProtocolInputs,
)
from engine.gate_combination import (
    BLOCKED,
    CONSERVE,
    DEPLOY_AGGRESSIVELY,
    DEPLOY_PARTIALLY,
    PREPARE,
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


def main() -> None:

    protocol = DryPowderProtocol()

    # -- Restrictive postures: Conserve, Prepare, Blocked all reject --

    for posture in (CONSERVE, PREPARE, BLOCKED):

        result = protocol.evaluate(
            DryPowderProtocolInputs(
                current_posture=posture,
                initial_dry_powder=100.0,
                remaining_dry_powder=100.0,
                cum_deployed_in_episode=0.0,
                days_since_last_deployment=None,
                drawdown_pp_since_last_deployment=None,
                highest_posture_in_episode=posture,
            )
        )
        assert_equal(f"{posture}_status", result.status, POSTURE_NO_DEPLOYMENT)
        assert_equal(f"{posture}_amount", result.authorized_amount, 0.0)

    # -- First tranche of the episode: no prior deployment, cadence --
    # -- fields both None -- bypasses cadence, authorizes --

    first_tranche = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=100.0,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=None,
            drawdown_pp_since_last_deployment=None,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("first_tranche_status", first_tranche.status, AUTHORIZED)
    assert_close("first_tranche_amount", first_tranche.authorized_amount, 12.0)

    # -- Cadence not met: 10 days, 2pp drawdown in Partially (needs --
    # -- 30 days OR 5.0pp) --

    cadence_blocked = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=100.0,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=10,
            drawdown_pp_since_last_deployment=2.0,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("cadence_blocked_status", cadence_blocked.status, CADENCE_NOT_MET)
    assert_equal("cadence_blocked_amount", cadence_blocked.authorized_amount, 0.0)

    # -- Cadence met by time alone: 31 days, 1pp (< 5.0pp) --

    cadence_by_time = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=100.0,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=1.0,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("cadence_by_time_status", cadence_by_time.status, AUTHORIZED)
    assert_close("cadence_by_time_amount", cadence_by_time.authorized_amount, 12.0)

    # -- Cadence met by drawdown alone: 5 days (< 30), 5.5pp (>= 5.0) --

    cadence_by_drawdown = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=100.0,
            cum_deployed_in_episode=0.0,
            days_since_last_deployment=5,
            drawdown_pp_since_last_deployment=5.5,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("cadence_by_drawdown_status", cadence_by_drawdown.status, AUTHORIZED)
    assert_close("cadence_by_drawdown_amount", cadence_by_drawdown.authorized_amount, 12.0)

    # -- Exact trim at the ceiling: Partially, 38% already deployed of --
    # -- a 100 initial DP (40% ceiling -> 2 of headroom), remaining DP --
    # -- still 100 so the raw 12% tranche (12) gets trimmed to exactly 2 --

    trimmed = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=100.0,
            cum_deployed_in_episode=38.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("trimmed_status", trimmed.status, AUTHORIZED)
    assert_close("trimmed_amount", trimmed.authorized_amount, 2.0)

    # -- Ratchet: highest reached was Aggressively (80% ceiling), --
    # -- current posture dropped back to Partially. 50 already --
    # -- deployed of 100 initial -- under a naive (non-ratchet) 40% --
    # -- ceiling this would already be CEILING_REACHED; the ratchet --
    # -- keeps the 80% ceiling alive, so it authorizes a Partially- --
    # -- sized tranche (12% of remaining) capped by 80% headroom --

    ratchet = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=50.0,
            cum_deployed_in_episode=50.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_AGGRESSIVELY,
        )
    )
    assert_equal("ratchet_status", ratchet.status, AUTHORIZED)
    assert_close("ratchet_amount", ratchet.authorized_amount, 6.0)

    # -- Ratchet edge case (the undefined branch in the drafted spec): --
    # -- current posture just escalated to Aggressively, but the --
    # -- caller-supplied highest_posture_in_episode still reads --
    # -- Partially (has not been updated yet). Effective ceiling must --
    # -- still be Aggressively's 80%, not Partially's 40% --

    fresh_escalation = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_AGGRESSIVELY,
            initial_dry_powder=100.0,
            remaining_dry_powder=50.0,
            cum_deployed_in_episode=38.0,
            days_since_last_deployment=None,
            drawdown_pp_since_last_deployment=6.0,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
        )
    )
    assert_equal("fresh_escalation_status", fresh_escalation.status, AUTHORIZED)
    # 22% of remaining (50) = 11; headroom to 80% ceiling (80 - 38 = 42)
    # does not bind -- full 11 authorized.
    assert_close("fresh_escalation_amount", fresh_escalation.authorized_amount, 11.0)

    # -- Ceiling invaded, no Human Approval: blocked at 0.0 --

    ceiling_no_approval = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_AGGRESSIVELY,
            initial_dry_powder=100.0,
            remaining_dry_powder=20.0,
            cum_deployed_in_episode=80.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_AGGRESSIVELY,
            human_approval_above_ceiling=False,
        )
    )
    assert_equal("ceiling_no_approval_status", ceiling_no_approval.status, CEILING_REACHED)
    assert_equal("ceiling_no_approval_amount", ceiling_no_approval.authorized_amount, 0.0)

    # -- RE-C: 80% reached, WITH Human Approval's 90% extension -- the --
    # -- ceiling itself moves to 90%, so 80% is no longer a stop -- a --
    # -- normal formula tranche continues, capped by headroom to 90% --

    assert_close(
        "ceiling_fraction_extended_is_90pct",
        CEILING_FRACTION_AGGRESSIVE_EXTENDED,
        0.90,
    )

    extended_within_band = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_AGGRESSIVELY,
            initial_dry_powder=100.0,
            remaining_dry_powder=18.0,
            cum_deployed_in_episode=82.0,
            days_since_last_deployment=14,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_AGGRESSIVELY,
            human_approval_above_ceiling=True,
        )
    )
    assert_equal("extended_within_band_status", extended_within_band.status, AUTHORIZED)
    # 22% of remaining (18) = 3.96; headroom to 90% ceiling (90 - 82 = 8)
    # does not bind -- full 3.96 authorized, computed by formula.
    assert_close(
        "extended_within_band_amount", extended_within_band.authorized_amount, 3.96
    )

    # -- RE-C: same scenario but trimmed by the extended headroom --

    extended_trimmed = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_AGGRESSIVELY,
            initial_dry_powder=100.0,
            remaining_dry_powder=12.0,
            cum_deployed_in_episode=88.0,
            days_since_last_deployment=14,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_AGGRESSIVELY,
            human_approval_above_ceiling=True,
        )
    )
    assert_equal("extended_trimmed_status", extended_trimmed.status, AUTHORIZED)
    # 22% of remaining (12) = 2.64; headroom to 90% ceiling (90 - 88 = 2)
    # binds -- trimmed to 2.0.
    assert_close("extended_trimmed_amount", extended_trimmed.authorized_amount, 2.0)

    # -- RE-C: 90% itself is still a hard stop -- never 100%, no --
    # -- further exception exists past the extended ceiling --

    extended_hard_stop = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_AGGRESSIVELY,
            initial_dry_powder=100.0,
            remaining_dry_powder=10.0,
            cum_deployed_in_episode=90.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_AGGRESSIVELY,
            human_approval_above_ceiling=True,
        )
    )
    assert_equal("extended_hard_stop_status", extended_hard_stop.status, CEILING_REACHED)
    assert_equal("extended_hard_stop_amount", extended_hard_stop.authorized_amount, 0.0)

    # -- RE-C: the extension never applies to Deploy Partially's 40% --
    # -- ceiling -- flag set, but ceiling_posture isn't Aggressively --

    partially_flag_ignored = protocol.evaluate(
        DryPowderProtocolInputs(
            current_posture=DEPLOY_PARTIALLY,
            initial_dry_powder=100.0,
            remaining_dry_powder=60.0,
            cum_deployed_in_episode=40.0,
            days_since_last_deployment=31,
            drawdown_pp_since_last_deployment=0.0,
            highest_posture_in_episode=DEPLOY_PARTIALLY,
            human_approval_above_ceiling=True,
        )
    )
    assert_equal(
        "partially_flag_ignored_status", partially_flag_ignored.status, CEILING_REACHED
    )
    assert_equal(
        "partially_flag_ignored_amount", partially_flag_ignored.authorized_amount, 0.0
    )

    # -- Unknown posture: fail-closed, raises rather than guessing --

    raised = False
    try:
        protocol.evaluate(
            DryPowderProtocolInputs(
                current_posture="Not A Real Posture",
                initial_dry_powder=100.0,
                remaining_dry_powder=100.0,
                cum_deployed_in_episode=0.0,
                days_since_last_deployment=None,
                drawdown_pp_since_last_deployment=None,
                highest_posture_in_episode=DEPLOY_PARTIALLY,
            )
        )
    except ValueError:
        raised = True
    assert_equal("unknown_posture_raises", raised, True)

    print("DRY POWDER PROTOCOL : STABLE")
    print()
    print(f"first_tranche_amount: {first_tranche.authorized_amount}")
    print(f"trimmed_amount: {trimmed.authorized_amount}")
    print(f"ratchet_amount: {ratchet.authorized_amount}")
    print(f"fresh_escalation_amount: {fresh_escalation.authorized_amount}")
    print(f"extended_within_band_amount: {extended_within_band.authorized_amount}")
    print(f"extended_trimmed_amount: {extended_trimmed.authorized_amount}")


if __name__ == "__main__":
    main()
