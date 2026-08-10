"""
SOP Research Engine
Dry Powder Protocol -- first isolated code

RE-041.1 specification. Deliberately stateless and side-effect-free:
this module does not track episodes, does not read market data, and
does not decide capital posture -- it takes an already-resolved
DryPowderProtocolInputs snapshot and returns a deterministic tranche
decision. Episode tracking (when the current drawdown started, Dry
Powder at that point, cumulative deployment and elapsed time/drawdown
since the last tranche) is the caller's responsibility -- same pattern
EvidenceQualityGate and RegimeComparabilityGate already use for their
own Local*Inputs.

Not wired into posture_mapper.py, gate_combination.py, run.py or
DecisionEngine. RE-041.1 explicitly reserves that wiring for a future
iteration. No automatic execution of any deployment -- Human Approval
still governs execution even once this module exists, unchanged.

Two corrections made against the drafted implementation spec this
module was built from, both flagged to Armando before writing:

1.  The ratchet's "active ceiling posture" is computed as
    max(current_posture, highest_posture_in_episode) by POSTURE_ORDER,
    not by a two-branch literal check. The literal version left one
    real case undefined: the first evaluation after escalating to
    Deploy Aggressively, where highest_posture_in_episode (a value the
    caller may not have updated yet to reflect "now") still reads
    Deploy Partially while current_posture already reads Deploy
    Aggressively. Taking the max closes that gap and is the more
    literal reading of RE-041.1's own wording anyway ("the highest one
    reached so far in the current episode" -- "so far" includes the
    present moment).

2.  Status is represented with plain string module-level constants,
    not a Python Enum, matching EvidenceQualityGate,
    RegimeComparabilityGate and PersonalCapacityFactsGate exactly.
    posture_mapper.py-style translators key their ceiling tables off
    plain strings directly; an Enum here would need `.value` unwrapping
    at every future integration point for no offsetting benefit.

A third, smaller addition beyond the drafted spec: cadence fields are
Optional, not required. Forcing a caller to invent a sentinel value
(e.g. "9999 days") to represent "no prior tranche exists yet in this
episode" would itself be exactly the kind of magic number this
project's fail-closed discipline rejects. Both cadence fields None
means "first tranche of the episode" and bypasses the cadence check
explicitly (see evaluate()), rather than silently failing it.
"""

from dataclasses import dataclass
from typing import Optional

from engine.gate_combination import (
    BLOCKED,
    DEPLOY_AGGRESSIVELY,
    DEPLOY_PARTIALLY,
    POSTURE_ORDER,
)


# gate_combination.POSTURE_ORDER only ranks the four deployment
# postures (Conserve..Deploy Aggressively) -- it deliberately excludes
# Blocked, which has no ordinal position, only a hard stop. But
# current_posture here is fed by that same combined ceiling, so
# Blocked is a legitimate value to receive even though it can never
# rank. Validate against this wider set instead of POSTURE_ORDER
# directly.
_KNOWN_POSTURES = set(POSTURE_ORDER) | {BLOCKED}


POSTURE_NO_DEPLOYMENT = "posture no deployment"
CADENCE_NOT_MET = "cadence not met"
CEILING_REACHED = "ceiling reached"
CEILING_REACHED_APPROVED = "ceiling reached, approved beyond ceiling"
AUTHORIZED = "authorized"


# RE-041.1 -- v1 parameters. A priori, not calibrated against
# historical data (risk-management structure, not a backtest fit,
# per the specification's own boundary). Subject to revision.
TRANCHE_PARAMETERS = {
    DEPLOY_PARTIALLY: {
        "tranche_fraction": 0.12,
        "ceiling_fraction": 0.40,
        "min_days": 30,
        "min_drawdown_points": 5.0,
    },
    DEPLOY_AGGRESSIVELY: {
        "tranche_fraction": 0.22,
        "ceiling_fraction": 0.80,
        "min_days": 14,
        "min_drawdown_points": 5.0,
    },
}


@dataclass(frozen=True)
class DryPowderProtocolInputs:
    """
    Already-resolved snapshot for one evaluation. This module computes
    none of these fields itself.

    highest_posture_in_episode should be the highest capital posture
    reached at any point during the current episode, including now --
    not just "at the last tranche". evaluate() does not trust either
    this field or current_posture blindly for the ceiling lookup; see
    module docstring, correction 1.

    days_since_last_deployment / drawdown_pp_since_last_deployment:
    both None means no tranche has been deployed yet in this episode
    -- cadence is trivially satisfied for a first tranche, never
    blocked on a sentinel value. Either field alone can be None if
    genuinely unknown; the other still gates cadence normally.
    """

    current_posture: str
    initial_dry_powder: float
    remaining_dry_powder: float
    cum_deployed_in_episode: float
    days_since_last_deployment: Optional[int]
    drawdown_pp_since_last_deployment: Optional[float]
    highest_posture_in_episode: str
    human_approval_above_ceiling: bool = False


@dataclass(frozen=True)
class DryPowderProtocolResult:
    """
    authorized_amount is None only for CEILING_REACHED_APPROVED --
    Human Approval unlocks the possibility of deploying beyond the
    ceiling, but RE-041.1 explicitly forbids computing that amount by
    formula ("v1 never authorizes 100% deployment by formula alone").
    None here means "requires a manually fixed amount per the
    attestation", never "zero" -- every other non-authorizing status
    uses 0.0 explicitly. Same discipline this project already applies
    to every Optional[bool] fact: absence is never silently read as a
    number.
    """

    status: str
    authorized_amount: Optional[float]
    reason: str


def _validate_posture(label: str, posture: str) -> None:

    if posture not in _KNOWN_POSTURES:
        raise ValueError(f"{label}: unknown posture {posture!r}")


def _posture_order(posture: str) -> int:
    """
    Blocked has no ordinal rank in POSTURE_ORDER -- treat it as lower
    than every real deployment posture so it can never win the
    ratchet's max() comparison in step 2. current_posture itself can
    never reach that comparison as Blocked (step 1 returns early for
    any posture outside TRANCHE_PARAMETERS), so this only matters for
    highest_posture_in_episode.
    """

    return POSTURE_ORDER.get(posture, -1)


class DryPowderProtocol:

    def evaluate(
        self,
        inputs: DryPowderProtocolInputs,
    ) -> DryPowderProtocolResult:

        _validate_posture("current_posture", inputs.current_posture)
        _validate_posture(
            "highest_posture_in_episode",
            inputs.highest_posture_in_episode,
        )

        if inputs.initial_dry_powder < 0 or inputs.remaining_dry_powder < 0:
            raise ValueError(
                "initial_dry_powder and remaining_dry_powder must be >= 0"
            )

        # Step 1 -- posture gate. Conserve/Prepare/Blocked all fall
        # here, per RE-033.1's 0%-deployment fix -- unchanged by this
        # protocol.
        params = TRANCHE_PARAMETERS.get(inputs.current_posture)

        if params is None:
            return DryPowderProtocolResult(
                status=POSTURE_NO_DEPLOYMENT,
                authorized_amount=0.0,
                reason=(
                    f"posture {inputs.current_posture!r} authorizes 0% "
                    "deployment (RE-033.1)"
                ),
            )

        # Step 2 -- ratchet: active ceiling posture is whichever of
        # current / highest-so-far is more permissive (module
        # docstring, correction 1).
        if (
            _posture_order(inputs.current_posture)
            > _posture_order(inputs.highest_posture_in_episode)
        ):
            ceiling_posture = inputs.current_posture
        else:
            ceiling_posture = inputs.highest_posture_in_episode

        ceiling_params = TRANCHE_PARAMETERS.get(ceiling_posture, params)
        ceiling_fraction = ceiling_params["ceiling_fraction"]
        ceiling_limit_amount = inputs.initial_dry_powder * ceiling_fraction

        # Step 3 -- ceiling / Human Approval.
        if inputs.cum_deployed_in_episode >= ceiling_limit_amount:

            if (
                ceiling_posture == DEPLOY_AGGRESSIVELY
                and inputs.human_approval_above_ceiling
            ):
                return DryPowderProtocolResult(
                    status=CEILING_REACHED_APPROVED,
                    authorized_amount=None,
                    reason=(
                        "cumulative deployed "
                        f"{inputs.cum_deployed_in_episode:.2f} has reached "
                        f"the {ceiling_fraction:.0%} ceiling "
                        f"({ceiling_limit_amount:.2f}) for {ceiling_posture} "
                        "-- Human Approval authorizes going beyond it, but "
                        "the amount is not computed by formula (RE-041.1) "
                        "-- fix it manually per the attestation"
                    ),
                )

            return DryPowderProtocolResult(
                status=CEILING_REACHED,
                authorized_amount=0.0,
                reason=(
                    "cumulative deployed "
                    f"{inputs.cum_deployed_in_episode:.2f} has reached the "
                    f"{ceiling_fraction:.0%} cumulative ceiling "
                    f"({ceiling_limit_amount:.2f}) for {ceiling_posture} -- "
                    "blocked without a fresh Human Approval attestation"
                ),
            )

        # Step 4 -- dual cadence (OR), evaluated against the CURRENT
        # posture's parameters, not the ratchet ceiling posture: the
        # everyday control follows where we are today, only the
        # backstop ceiling remembers the episode's high point.
        no_prior_tranche = (
            inputs.days_since_last_deployment is None
            and inputs.drawdown_pp_since_last_deployment is None
        )

        days_ok = (
            inputs.days_since_last_deployment is not None
            and inputs.days_since_last_deployment >= params["min_days"]
        )
        drawdown_ok = (
            inputs.drawdown_pp_since_last_deployment is not None
            and inputs.drawdown_pp_since_last_deployment
            >= params["min_drawdown_points"]
        )

        if not (no_prior_tranche or days_ok or drawdown_ok):
            return DryPowderProtocolResult(
                status=CADENCE_NOT_MET,
                authorized_amount=0.0,
                reason=(
                    f"neither {params['min_days']} days since the last "
                    f"tranche nor {params['min_drawdown_points']} "
                    "additional points of drawdown have elapsed"
                ),
            )

        # Step 5 -- tranche on remainder, capped at remaining ceiling
        # headroom.
        raw_amount = inputs.remaining_dry_powder * params["tranche_fraction"]
        remaining_headroom = max(
            0.0, ceiling_limit_amount - inputs.cum_deployed_in_episode
        )
        authorized_amount = min(raw_amount, remaining_headroom)

        if authorized_amount <= 0.0:
            return DryPowderProtocolResult(
                status=CEILING_REACHED,
                authorized_amount=0.0,
                reason=(
                    "remaining headroom under the ceiling is exhausted "
                    "before applying the tranche fraction"
                ),
            )

        trimmed_note = ""
        if authorized_amount < raw_amount:
            trimmed_note = (
                f", trimmed to {authorized_amount:.2f} by remaining "
                f"headroom under the {ceiling_posture} ceiling"
            )

        return DryPowderProtocolResult(
            status=AUTHORIZED,
            authorized_amount=authorized_amount,
            reason=(
                f"{inputs.current_posture}: "
                f"{params['tranche_fraction']:.0%} of remaining Dry "
                f"Powder ({inputs.remaining_dry_powder:.2f}) = "
                f"{raw_amount:.2f}{trimmed_note}"
            ),
        )
