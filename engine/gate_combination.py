from dataclasses import dataclass, field


CONSERVE = "Conserve"
PREPARE = "Prepare"
DEPLOY_PARTIALLY = "Deploy Partially"
DEPLOY_AGGRESSIVELY = "Deploy Aggressively"
BLOCKED = "Blocked"


POSTURE_ORDER = {
    CONSERVE: 0,
    PREPARE: 1,
    DEPLOY_PARTIALLY: 2,
    DEPLOY_AGGRESSIVELY: 3,
}


@dataclass
class GateCombinationInput:
    """
    Discrete gate output consumed by the combination layer.

    This structure deliberately carries posture ceilings and explanations,
    not scores or raw validation metrics.
    """

    gate_name: str
    internal_state: str
    posture_ceiling: str
    blocked: bool = False
    explanations: list[str] = field(default_factory=list)


@dataclass
class GateCombinationResult:
    """
    Combined Capital Posture ceiling with traceable limiting causes.
    """

    posture_ceiling: str
    explanations: list[str]


def _validate_posture(posture: str) -> None:

    if posture not in POSTURE_ORDER:
        raise ValueError(f"unknown posture ceiling: {posture}")


def _format_explanations(gate: GateCombinationInput) -> list[str]:

    if gate.explanations:
        details = gate.explanations
    else:
        details = [gate.internal_state]

    formatted = []

    for detail in details:

        if detail.startswith(f"{gate.gate_name}:"):
            formatted.append(detail)
        else:
            formatted.append(f"{gate.gate_name}: {detail}")

    return formatted


def combine_gate_outputs(
    gates: list[GateCombinationInput],
) -> GateCombinationResult:
    """
    Combine discrete gate ceilings into one Capital Posture ceiling.

    RE-034.3 is isolated structure only. It is not wired into run.py,
    DecisionEngine, AssessmentEngine or ValidationEngine.
    """

    if not gates:
        return GateCombinationResult(
            posture_ceiling=CONSERVE,
            explanations=["gate combination: no gate outputs available"],
        )

    blocked_gates = [gate for gate in gates if gate.blocked]

    if blocked_gates:
        explanations = []

        for gate in blocked_gates:
            explanations.extend(_format_explanations(gate))

        return GateCombinationResult(
            posture_ceiling=BLOCKED,
            explanations=explanations,
        )

    for gate in gates:
        _validate_posture(gate.posture_ceiling)

    limiting_order = min(
        POSTURE_ORDER[gate.posture_ceiling]
        for gate in gates
    )
    limiting_gates = [
        gate
        for gate in gates
        if POSTURE_ORDER[gate.posture_ceiling] == limiting_order
    ]

    explanations = []

    for gate in limiting_gates:
        explanations.extend(_format_explanations(gate))

    posture = limiting_gates[0].posture_ceiling

    return GateCombinationResult(
        posture_ceiling=posture,
        explanations=explanations,
    )
