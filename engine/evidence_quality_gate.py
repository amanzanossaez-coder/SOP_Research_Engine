from dataclasses import dataclass
from typing import Optional


NOT_MEASURABLE = "not measurable"
CONSERVATIVE = "conservative"


@dataclass
class LocalEvidenceQualityInputs:
    """
    Local evidence quality for the current snapshot match set only.

    These fields describe today's selected evidence sample. They do not
    claim that the Research Engine has predictive skill globally.
    """

    coverage: Optional[float] = None
    consistency: Optional[float] = None
    diversity: Optional[float] = None
    independence_dispersion_measured: bool = False


@dataclass
class GlobalModelValidationState:
    """
    Global model-validation state, separate from local snapshot quality.

    This answers whether the model has demonstrated predictive
    discrimination under a pre-registered validation protocol.
    """

    predictive_validation_status: Optional[str] = None


@dataclass
class EvidenceQualityGateResult:
    """
    Discrete gate result with explicit explanations.

    Absence of measurement is represented as NOT_MEASURABLE, never as a
    numeric default. This follows the RE-024.1 Evidence rule: absence of
    evidence is not 0.0.
    """

    state: str
    explanations: list[str]


class EvidenceQualityGate:
    """
    RE-030.1 -- isolated Evidence Quality Gate structure.

    This class is deliberately not wired into run.py, DecisionEngine,
    AssessmentEngine or ValidationEngine. It does not consume
    AssessmentEngine.confidence().score and does not define thresholds.
    """

    def evaluate(
        self,
        local: LocalEvidenceQualityInputs,
        global_state: GlobalModelValidationState,
    ) -> EvidenceQualityGateResult:

        explanations = []

        if local.coverage is None:
            explanations.append("local coverage unavailable")

        if local.consistency is None:
            explanations.append("local consistency unavailable")

        if local.diversity is None:
            explanations.append("local diversity unavailable")

        if not local.independence_dispersion_measured:
            explanations.append("independence / dispersion not measured")

        if global_state.predictive_validation_status is None:
            explanations.append("predictive validation status unavailable")
        elif global_state.predictive_validation_status != "validated":
            explanations.append("global model-validation state not validated")

        if explanations:
            return EvidenceQualityGateResult(
                state=NOT_MEASURABLE,
                explanations=explanations,
            )

        return EvidenceQualityGateResult(
            state=CONSERVATIVE,
            explanations=[
                "no less-restrictive Evidence Quality state is authorized"
            ],
        )
