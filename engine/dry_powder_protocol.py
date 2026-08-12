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

RE-C (RE-032.10 iteration C) -- wires `human_approval_above_ceiling`
for real. Closes the gap this module's own docstrings already flagged
honestly since RE-041.5/RE-032.8: the field existed, but nothing ever
set it to True.

Design point 1 of RE-032.10 (engine/human_approval.py's module
docstring) specified the shape this had to take: "dry_powder_protocol.py
will compute tranches up to this new 90% the same way it already does
up to 80% -- this module only produces the boolean that unlocks it."
Concretely: when `ceiling_posture` (the ratchet's active ceiling
posture, correction 1 above) is Deploy Aggressively AND
`human_approval_above_ceiling` is True, `ceiling_fraction` for Step 2's
ceiling computation becomes `CEILING_FRACTION_AGGRESSIVE_EXTENDED`
(90%) instead of the normal 80% -- nothing else about the tranche
formula changes. Tranches between the old 80% and the new 90% are
computed exactly like any other tranche (Step 5), capped by headroom
under the extended ceiling, same as always.

This retires `CEILING_REACHED_APPROVED` as a reachable outcome. Before
RE-C, reaching the 80% ceiling with Human Approval set produced that
status, with `authorized_amount=None` -- RE-041.1's original text
forbade computing a number by formula because there was no upper bound
on how far "beyond the ceiling" could go. RE-032.10 supplied that upper
bound (90%, explicitly never 100%), which is exactly what made
formula-driven computation safe in that band. Once the ceiling itself
extends, there is nothing left for a separate "approved beyond ceiling,
fix it manually" status to describe -- the ceiling check in Step 3 is
now always a hard stop, extended or not. The constant stays defined
(status-string schema stability for any caller already matching on it,
e.g. `audit_posture.py`'s printed output) but `evaluate()` no longer
produces it. If a future policy ever wants a further manual-override
tier beyond 90%, that is new, explicit design work -- not a
resurrection of this one, which was scoped to the 80/90 gap only.
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
# RE-C -- kept for status-string schema stability (see module
# docstring); evaluate() no longer produces this. Reaching the ceiling
# with Human Approval's 90% extension active now returns CEILING_REACHED
# like any other ceiling hit, because the extension already widened
# ceiling_fraction itself in Step 2, not this separate status.
CEILING_REACHED_APPROVED = "ceiling reached, approved beyond ceiling"
AUTHORIZED = "authorized"

# RE-032.10 / RE-C -- the extraordinary ceiling Human Approval can
# unlock for Deploy Aggressively only, replacing its normal 80%. Never
# 100% -- RE-032.10's design explicitly stops at 90%, no further
# exception exists in v1.
CEILING_FRACTION_AGGRESSIVE_EXTENDED = 0.90


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
    authorized_amount is None only for CEILING_REACHED_APPROVED, a
    status evaluate() no longer produces as of RE-C (see module
    docstring) -- kept Optional rather than tightened to float because
    the schema itself should not assume that will always be true.
    Every status evaluate() actually returns today uses 0.0 for "not
    authorized", never None -- same discipline this project already
    applies to every Optional[bool] fact: absence is never silently
    read as a number.
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

        # RE-C -- Human Approval's extension only ever applies to
        # Deploy Aggressively's own ceiling, and only replaces it
        # (never stacks with it): 90% instead of 80%, not 80% + 90%.
        ceiling_extended = (
            ceiling_posture == DEPLOY_AGGRESSIVELY
            and inputs.human_approval_above_ceiling
        )
        if ceiling_extended:
            ceiling_fraction = CEILING_FRACTION_AGGRESSIVE_EXTENDED

        ceiling_limit_amount = inputs.initial_dry_powder * ceiling_fraction

        # Step 3 -- ceiling. Always a hard stop once reached -- the
        # Human Approval extension, if any, has already been folded
        # into ceiling_fraction above (RE-C, see module docstring).
        # There is no further "approved beyond ceiling" tier past this
        # point in v1.
        if inputs.cum_deployed_in_episode >= ceiling_limit_amount:

            if ceiling_extended:
                extension_note = (
                    " -- this already includes Human Approval's "
                    "extraordinary 90% ceiling (RE-032.10); hard stop, "
                    "never 100%"
                )
            elif ceiling_posture == DEPLOY_AGGRESSIVELY:
                extension_note = (
                    " -- blocked without a fresh Human Approval "
                    "attestation authorizing the extended 90% ceiling "
                    "(RE-032.10)"
                )
            else:
                # Deploy Partially's 40% ceiling has no exception
                # mechanism at all -- nothing to point to here.
                extension_note = " -- blocked, no exception exists for this ceiling"

            return DryPowderProtocolResult(
                status=CEILING_REACHED,
                authorized_amount=0.0,
                reason=(
                    "cumulative deployed "
                    f"{inputs.cum_deployed_in_episode:.2f} has reached the "
                    f"{ceiling_fraction:.0%} cumulative ceiling "
                    f"({ceiling_limit_amount:.2f}) for {ceiling_posture}"
                    f"{extension_note}"
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
