"""
SOP Research Engine
Human Approval -- RE-032.6, first isolated code

Implements RE-032.4's attested-judgement channel + Human Approval
procedural boundary. Pure logic, no I/O, no storage -- an adapter that
reads a real attestation history (data/raw/human_approval_attestations.xlsx,
not built yet) is separate future work, same split every gate this
project has used (personal_capacity_facts_gate.py, dry_powder_protocol.py).

Not wired into gate_combination.py, posture_mapper.py, run.py or
DecisionEngine. Human Approval is explicitly NOT a scored gate and
does not participate in combine_gate_outputs()'s min() combination
(RE-032.4, rule 1) -- it is a binary procedural prerequisite for
capital action, checked separately, never blended into a posture
ceiling.

Two design corrections resolved with Armando before writing this,
recorded here because the governance doc's RE-032.4 text, read
literally, does not resolve them on its own:

1.  Rules 5 and 7, read literally, contradict each other. Rule 5:
    `under_cooling_off` blocks all capital action. Rule 7: "during
    cooling-off, the previously valid attestation remains in force."
    Resolved: cooling-off delays the EFFECTIVENESS of a
    tolerance-increasing revision: it never invalidates a prior,
    still-valid attestation. `under_cooling_off` as the reported
    top-level state -- and the only case that actually blocks -- is
    reserved for when there is no valid prior attestation to fall
    back on. When a valid predecessor exists, the reported state stays
    `valid` (governed by the predecessor), with the pending revision
    surfaced separately as `pending_increase`, not folded into the
    top-level state.

2.  A first-ever attestation is measured for "is this an increase"
    against an implicit baseline equivalent to CONSERVE (the most
    restrictive posture) -- there being no attestation yet is treated
    the same as having attested to nothing but the floor. A first
    attestation that authorizes anything above CONSERVE is therefore
    itself a tolerance increase and goes through the same cooling-off
    as any revision; a first attestation at or below CONSERVE (a tie,
    per rule 6's "including ties") takes effect immediately, same as
    any non-increasing revision.

market_crisis (RE-032.4's objective crisis signal, "Drawdown <=
MIN_DRAWDOWN, the same constant drawdown_engine.py already uses") is
deliberately NOT computed inside this module -- it is exactly what
engine/live_episode.py already computes (RE-041.2), so duplicating the
threshold check here would violate this project's own repeated
"don't duplicate logic" discipline. Instead, each Attestation carries
`market_crisis_at_registration: bool`, a fact about conditions AT THE
TIME that specific attestation was registered -- resolved by a future
adapter via engine.live_episode.drawdown_at_month(), not by this pure
function. Cooling-off length for a revision is fixed by conditions at
ITS OWN registration, not re-evaluated against today's live market
state on every check -- a crisis that starts after a revision was
already registered does not retroactively lengthen a cooling-off
period already running (a defensible reading of "when active" as "when
the revision was made," open to revisiting if it produces an
unwelcome edge case in practice).

Validity (90 days) is measured from each attestation's own
registration timestamp, never from when its cooling-off ends -- taken
literally from RE-032.4 rule 4.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from engine.gate_combination import CONSERVE, POSTURE_ORDER


MISSING = "missing"
VALID = "valid"
EXPIRED = "expired"
UNDER_COOLING_OFF = "under_cooling_off"

COOLING_OFF_BASE_DAYS = 14
COOLING_OFF_CRISIS_DAYS = 30
VALIDITY_DAYS = 90


@dataclass(frozen=True)
class Attestation:
    """
    One registered attestation event. registered_at is a real calendar
    date, not a Shiller month -- Human Approval is Armando's own
    procedural act, not a market signal.

    market_crisis_at_registration is a fact ABOUT this specific
    attestation (was the market in crisis, per RE-032.4's objective
    definition, the day this was registered) -- not a live value
    re-read on every evaluation. See module docstring.
    """

    registered_at: date
    approved_posture_ceiling: str
    personal_crisis_declared: bool = False
    market_crisis_at_registration: bool = False
    notes: str = ""


@dataclass(frozen=True)
class HumanApprovalInputs:

    attestations: tuple = ()
    as_of_date: Optional[date] = None


@dataclass
class PendingIncrease:
    """
    A tolerance-increasing revision that has been registered but has
    not yet taken effect. Not a state of its own -- surfaced alongside
    a top-level state of VALID (governed by a still-valid predecessor)
    or UNDER_COOLING_OFF (no predecessor to fall back on).
    """

    approved_posture_ceiling: str
    registered_at: date
    effective_date: date
    cooling_off_days_required: int


@dataclass
class HumanApprovalResult:

    state: str
    effective_posture_ceiling: Optional[str]
    blocked: bool
    pending_increase: Optional[PendingIncrease] = None
    explanations: list[str] = field(default_factory=list)


def _validate_posture(label: str, posture: str) -> None:

    if posture not in POSTURE_ORDER:
        raise ValueError(f"{label}: unknown posture {posture!r}")


class HumanApprovalGate:

    def evaluate(self, inputs: HumanApprovalInputs) -> HumanApprovalResult:

        if not inputs.attestations:
            return HumanApprovalResult(
                state=MISSING,
                effective_posture_ceiling=None,
                blocked=True,
                explanations=["no attestation has ever been registered"],
            )

        as_of_date = inputs.as_of_date or date.today()

        attestations = sorted(
            inputs.attestations, key=lambda a: a.registered_at
        )

        for a in attestations:
            _validate_posture("approved_posture_ceiling", a.approved_posture_ceiling)

        latest = attestations[-1]
        previous = attestations[-2] if len(attestations) >= 2 else None

        days_since_latest = (as_of_date - latest.registered_at).days

        # Rule 4 -- validity is measured from registration, always,
        # regardless of cooling-off. Checked first: an expired
        # attestation cannot govern under any circumstance, and there
        # is no fallback-to-something-older concept once the most
        # recent attestation itself has lapsed.
        if days_since_latest >= VALIDITY_DAYS:
            return HumanApprovalResult(
                state=EXPIRED,
                effective_posture_ceiling=None,
                blocked=True,
                explanations=[
                    f"latest attestation ({latest.registered_at}) is "
                    f"{days_since_latest} days old, past the "
                    f"{VALIDITY_DAYS}-day validity window"
                ],
            )

        baseline_posture = previous.approved_posture_ceiling if previous else CONSERVE

        is_increase = (
            POSTURE_ORDER[latest.approved_posture_ceiling]
            > POSTURE_ORDER[baseline_posture]
        )

        if not is_increase:
            return HumanApprovalResult(
                state=VALID,
                effective_posture_ceiling=latest.approved_posture_ceiling,
                blocked=False,
                explanations=[
                    "latest attestation does not increase tolerance "
                    f"relative to {'the prior attestation' if previous else 'the implicit Conserve baseline'} "
                    "-- applies immediately, no cooling-off"
                ],
            )

        cooling_off_days = (
            COOLING_OFF_CRISIS_DAYS
            if (latest.personal_crisis_declared or latest.market_crisis_at_registration)
            else COOLING_OFF_BASE_DAYS
        )

        if days_since_latest >= cooling_off_days:
            return HumanApprovalResult(
                state=VALID,
                effective_posture_ceiling=latest.approved_posture_ceiling,
                blocked=False,
                explanations=[
                    f"tolerance-increasing revision registered "
                    f"{days_since_latest} days ago has cleared its "
                    f"{cooling_off_days}-day cooling-off -- now fully "
                    "in effect"
                ],
            )

        effective_date = date.fromordinal(
            latest.registered_at.toordinal() + cooling_off_days
        )

        pending = PendingIncrease(
            approved_posture_ceiling=latest.approved_posture_ceiling,
            registered_at=latest.registered_at,
            effective_date=effective_date,
            cooling_off_days_required=cooling_off_days,
        )

        if previous is not None:

            days_since_previous = (as_of_date - previous.registered_at).days

            if days_since_previous < VALIDITY_DAYS:
                return HumanApprovalResult(
                    state=VALID,
                    effective_posture_ceiling=previous.approved_posture_ceiling,
                    blocked=False,
                    pending_increase=pending,
                    explanations=[
                        f"a tolerance-increasing revision to "
                        f"{latest.approved_posture_ceiling} is under "
                        f"{cooling_off_days}-day cooling-off, effective "
                        f"{effective_date} -- the prior attestation "
                        f"({previous.approved_posture_ceiling}, "
                        f"registered {previous.registered_at}) remains "
                        "in force in the meantime (rule 7)"
                    ],
                )

        return HumanApprovalResult(
            state=UNDER_COOLING_OFF,
            effective_posture_ceiling=None,
            blocked=True,
            pending_increase=pending,
            explanations=[
                f"tolerance-increasing revision to "
                f"{latest.approved_posture_ceiling} is under "
                f"{cooling_off_days}-day cooling-off, effective "
                f"{effective_date} -- no prior valid attestation exists "
                "to fall back on, so capital action is blocked until "
                "then (rule 5)"
            ],
        )
