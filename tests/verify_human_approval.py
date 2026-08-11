#!/usr/bin/env python3
"""
SOP Research Engine
Human Approval Verification

RE-032.6 -- synthetic checks only. No real attestation data source
exists yet (that adapter is separate future work), so there is no
real-pipeline section here.
"""

from datetime import date, timedelta
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.gate_combination import CONSERVE, DEPLOY_AGGRESSIVELY, DEPLOY_PARTIALLY, PREPARE
from engine.human_approval import (
    COOLING_OFF_BASE_DAYS,
    COOLING_OFF_CRISIS_DAYS,
    EXPIRED,
    MISSING,
    UNDER_COOLING_OFF,
    VALID,
    VALIDITY_DAYS,
    Attestation,
    HumanApprovalGate,
    HumanApprovalInputs,
)


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def main() -> None:

    gate = HumanApprovalGate()

    # -- No attestation ever registered --

    missing = gate.evaluate(HumanApprovalInputs(attestations=()))
    assert_equal("missing_state", missing.state, MISSING)
    assert_equal("missing_blocked", missing.blocked, True)
    assert_equal("missing_effective", missing.effective_posture_ceiling, None)

    today = date(2026, 8, 11)

    # -- First-ever attestation, at/below the implicit Conserve --
    # -- baseline -- a tie, not an increase -- takes effect immediately --

    first_conservative = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(registered_at=today, approved_posture_ceiling=CONSERVE),
            ),
            as_of_date=today,
        )
    )
    assert_equal("first_conservative_state", first_conservative.state, VALID)
    assert_equal("first_conservative_blocked", first_conservative.blocked, False)
    assert_equal(
        "first_conservative_effective",
        first_conservative.effective_posture_ceiling,
        CONSERVE,
    )
    assert_equal("first_conservative_pending", first_conservative.pending_increase, None)

    # -- First-ever attestation authorizing something above Conserve --
    # -- IS an increase relative to the implicit baseline -> --
    # -- cooling-off. No predecessor to fall back on -> blocked. --

    first_aggressive = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(
                    registered_at=today, approved_posture_ceiling=DEPLOY_PARTIALLY
                ),
            ),
            as_of_date=today,
        )
    )
    assert_equal("first_aggressive_state", first_aggressive.state, UNDER_COOLING_OFF)
    assert_equal("first_aggressive_blocked", first_aggressive.blocked, True)
    assert_equal("first_aggressive_effective", first_aggressive.effective_posture_ceiling, None)
    assert first_aggressive.pending_increase is not None
    assert_equal(
        "first_aggressive_cooling_off_days",
        first_aggressive.pending_increase.cooling_off_days_required,
        COOLING_OFF_BASE_DAYS,
    )
    assert_equal(
        "first_aggressive_effective_date",
        first_aggressive.pending_increase.effective_date,
        today + timedelta(days=COOLING_OFF_BASE_DAYS),
    )

    # -- Same, but with market_crisis_at_registration True -- 30-day --
    # -- cooling-off instead of 14 --

    first_aggressive_crisis = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(
                    registered_at=today,
                    approved_posture_ceiling=DEPLOY_AGGRESSIVELY,
                    market_crisis_at_registration=True,
                ),
            ),
            as_of_date=today,
        )
    )
    assert_equal(
        "first_aggressive_crisis_cooling_off_days",
        first_aggressive_crisis.pending_increase.cooling_off_days_required,
        COOLING_OFF_CRISIS_DAYS,
    )

    # -- Same first-ever aggressive attestation, but enough days have --
    # -- passed to clear the 14-day cooling-off -- now fully in effect --

    first_aggressive_cleared = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(
                    registered_at=today, approved_posture_ceiling=DEPLOY_PARTIALLY
                ),
            ),
            as_of_date=today + timedelta(days=COOLING_OFF_BASE_DAYS),
        )
    )
    assert_equal("first_aggressive_cleared_state", first_aggressive_cleared.state, VALID)
    assert_equal("first_aggressive_cleared_blocked", first_aggressive_cleared.blocked, False)
    assert_equal(
        "first_aggressive_cleared_effective",
        first_aggressive_cleared.effective_posture_ceiling,
        DEPLOY_PARTIALLY,
    )

    # -- Expired: latest attestation is >= 90 days old --

    expired = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(registered_at=today, approved_posture_ceiling=CONSERVE),
            ),
            as_of_date=today + timedelta(days=VALIDITY_DAYS),
        )
    )
    assert_equal("expired_state", expired.state, EXPIRED)
    assert_equal("expired_blocked", expired.blocked, True)
    assert_equal("expired_effective", expired.effective_posture_ceiling, None)

    # -- Two attestations: PREPARE then a DECREASE back to CONSERVE -- --
    # -- applies immediately, no cooling-off, even though the first --
    # -- one might itself still be settling --

    decrease = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(registered_at=today, approved_posture_ceiling=PREPARE),
                Attestation(
                    registered_at=today + timedelta(days=1),
                    approved_posture_ceiling=CONSERVE,
                ),
            ),
            as_of_date=today + timedelta(days=1),
        )
    )
    assert_equal("decrease_state", decrease.state, VALID)
    assert_equal("decrease_blocked", decrease.blocked, False)
    assert_equal("decrease_effective", decrease.effective_posture_ceiling, CONSERVE)
    assert_equal("decrease_pending", decrease.pending_increase, None)

    # -- Two attestations: first CONSERVE (still valid), second an --
    # -- increase to DEPLOY_AGGRESSIVELY just registered today -- --
    # -- state stays VALID governed by the first, per Armando's --
    # -- resolution of the rule 5 / rule 7 contradiction, with the --
    # -- pending increase surfaced separately --

    increase_with_fallback = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(
                    registered_at=today - timedelta(days=10),
                    approved_posture_ceiling=CONSERVE,
                ),
                Attestation(
                    registered_at=today, approved_posture_ceiling=DEPLOY_AGGRESSIVELY
                ),
            ),
            as_of_date=today,
        )
    )
    assert_equal("increase_with_fallback_state", increase_with_fallback.state, VALID)
    assert_equal("increase_with_fallback_blocked", increase_with_fallback.blocked, False)
    assert_equal(
        "increase_with_fallback_effective",
        increase_with_fallback.effective_posture_ceiling,
        CONSERVE,
    )
    assert increase_with_fallback.pending_increase is not None
    assert_equal(
        "increase_with_fallback_pending_posture",
        increase_with_fallback.pending_increase.approved_posture_ceiling,
        DEPLOY_AGGRESSIVELY,
    )

    # -- Same shape, but the FIRST attestation is already expired (>= --
    # -- 90 days) by the time the second one is checked -- no valid --
    # -- fallback -> blocked, UNDER_COOLING_OFF --

    increase_without_fallback = gate.evaluate(
        HumanApprovalInputs(
            attestations=(
                Attestation(
                    registered_at=today - timedelta(days=95),
                    approved_posture_ceiling=CONSERVE,
                ),
                Attestation(
                    registered_at=today, approved_posture_ceiling=DEPLOY_AGGRESSIVELY
                ),
            ),
            as_of_date=today,
        )
    )
    assert_equal(
        "increase_without_fallback_state", increase_without_fallback.state, UNDER_COOLING_OFF
    )
    assert_equal("increase_without_fallback_blocked", increase_without_fallback.blocked, True)
    assert_equal(
        "increase_without_fallback_effective",
        increase_without_fallback.effective_posture_ceiling,
        None,
    )

    # -- Fail-closed: unknown posture string raises, never silently --
    # -- accepted --

    raised = False
    try:
        gate.evaluate(
            HumanApprovalInputs(
                attestations=(
                    Attestation(
                        registered_at=today, approved_posture_ceiling="Not A Real Posture"
                    ),
                ),
                as_of_date=today,
            )
        )
    except ValueError:
        raised = True
    assert_equal("unknown_posture_raises", raised, True)

    print("HUMAN APPROVAL : STABLE")


if __name__ == "__main__":
    main()
