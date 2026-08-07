from dataclasses import dataclass
from statistics import pstdev
from typing import Optional


NOT_MEASURABLE = "not measurable"
CONSERVATIVE = "conservative"
EXPECTED_MATCHES = 10

# RE-035.1 -- valor reconocido de predictive_validation_status distinto
# de "validated" y de None: evidencia que SI fue evaluada bajo un
# protocolo pre-registrado (RE-PRED.1) y no demostro la ventaja
# requerida (RE-PRED.13/16), frente a "unavailable" (nunca evaluada) o
# cualquier otro string no reconocido. No introduce un tercer estado de
# salida del gate -- RE-PRED.10.1 descarto explicitamente esa opcion a
# favor de explicaciones mas nitidas dentro de NOT_MEASURABLE/
# CONSERVATIVE. Este modulo no conoce, y no debe conocer, los numeros
# concretos de ninguna iteracion RE-PRED: quien construya
# GlobalModelValidationState decide cuando este valor aplica.
PREDICTIVE_VALIDATION_NOT_DEMONSTRATED = "not_demonstrated"


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

    # RE-035.1 -- numero de pares de matches del set actual cuyas
    # ventanas de outcome se solapan (misma definicion que RE-025.8,
    # aplicada aqui al match set de una consulta en vivo, no al
    # historico de validacion). None mientras independence_dispersion_
    # measured sea False -- ausencia de medicion, no un 0 que afirmaria
    # "medido y sin solapes".
    overlapping_match_pairs: Optional[int] = None


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
        elif (
            global_state.predictive_validation_status
            == PREDICTIVE_VALIDATION_NOT_DEMONSTRATED
        ):
            explanations.append(
                "predictive validation status: not demonstrated "
                "-- evaluated under a pre-registered protocol, "
                "required advantage not shown"
            )
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


def _overlapping_match_pairs(evidence) -> int:
    """
    RE-035.1 -- cuenta pares del match set ACTUAL cuyas ventanas de
    outcome (bottom_date .. bottom_date + horizon_years) se solapan.

    Misma definicion booleana que RE-025.8's overlapping_outcome_
    windows() -- start_a < end_b and start_b < end_a -- pero
    reimplementada aqui en vez de reutilizada, porque opera sobre un
    tipo distinto: Similarity (matches de una consulta en vivo, con un
    unico evidence.horizon_years compartido), no ValidationRecord
    (registros de backtesting, cada uno con su propio horizon_years y
    su propio evaluable). Cuarta duplicacion controlada de este mismo
    criterio en el proyecto (ya usado en validation_harness,
    baseline_harness y dimension_diagnostic para bottom_index self-
    exclusion) -- mismo principio: tres lineas de logica publica, no
    una dependencia cruzada forzando un adaptador entre tipos que no
    deberian conocerse.
    """

    horizon = evidence.horizon_years

    windows = [
        (
            match.episode.bottom_date,
            match.episode.bottom_date + horizon,
        )
        for match in evidence.matches
    ]

    pairs = 0

    for i, (left_start, left_end) in enumerate(windows):
        for right_start, right_end in windows[i + 1:]:
            if left_start < right_end and right_start < left_end:
                pairs += 1

    return pairs


def build_local_evidence_quality_inputs(
    evidence,
) -> LocalEvidenceQualityInputs:
    """
    Build local Evidence Quality inputs from one Evidence object.

    Evidence is the single source of truth for the selected match set:
    callers must not pass a separate matches list that could drift from
    evidence.matches.
    """

    coverage = min(evidence.return_count / EXPECTED_MATCHES, 1.0)

    returns = []

    for match in evidence.matches:

        value = getattr(
            match.episode,
            f"future_return_{evidence.horizon_years}y",
        )

        if value is not None:
            returns.append(value)

    if len(returns) < 2:
        consistency = 0.0
    else:
        consistency = max(0.0, 1.0 - pstdev(returns))

    decades = set()

    for match in evidence.matches:

        year = int(match.episode.bottom_date)
        decades.add((year // 10) * 10)

    diversity = min(
        len(decades) / max(len(evidence.matches), 1),
        1.0,
    )

    overlapping_pairs = _overlapping_match_pairs(evidence)

    return LocalEvidenceQualityInputs(
        coverage=coverage,
        consistency=consistency,
        diversity=diversity,
        independence_dispersion_measured=True,
        overlapping_match_pairs=overlapping_pairs,
    )
