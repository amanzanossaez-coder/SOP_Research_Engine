from dataclasses import dataclass
from typing import Optional


NOT_MEASURABLE = "not measurable"
COMPARABLE = "comparable"
NOT_COMPARABLE = "not comparable"

# RE-036.1 -- primer corte de dimensiones. cape/inflation/interest_rate
# ya estan pobladas en Context por episodio -- no requieren ninguna
# ingesta de datos nueva.
#
# RE-036.2 -- correccion (RE-DOC-002): el comentario original decia
# que las tres NO eran consumidas por SimilarityEngine. Es falso para
# cape, que SimilarityEngine si usa en su score (junto a
# pre_crash_return_3y/pre_crash_volatility_1y) -- inflation/interest_rate
# si son enteramente ajenas a SimilarityEngine. Que cape aparezca en
# los dos sitios no es una contradiccion de diseno: SimilarityEngine la
# usa como una dimension mas dentro de una distancia ponderada para
# RANKEAR episodios; este gate comprueba, de forma independiente, si
# el valor de cape de HOY cae dentro del rango bruto de los episodios
# ya seleccionados -- una pregunta distinta, la misma separacion que el
# docstring de RegimeComparabilityGate ya exige mas abajo ("No usa
# SimilarityEngine ni evidence quality como proxy de comparabilidad").
#
# volatility/liquidity/policy/market-structure permanecen fuera de
# alcance: RE-031.1 no autoriza inferir su medicion sin una fuente de
# datos real.
REGIME_DIMENSIONS = ["cape", "inflation", "interest_rate"]


@dataclass
class LocalRegimeComparabilityInputs:
    """
    RE-036.1 -- cobertura de regimen por dimension, para la consulta
    actual (snapshot) frente al match set ya seleccionado (evidence.
    matches), no frente al universo historico completo -- alcance
    explicito de este primer corte, per RE-031.1.

    Optional[bool] por dimension, no un score: None significa no
    medible (falta el valor de hoy, o ningun match aporta valor para
    esa dimension) -- postura por defecto de RE-031.1, ausencia nunca
    se representa como favorable. True significa que el valor de hoy
    cae dentro de [minimo, maximo] de los valores de esa dimension en
    los matches. False significa que cae fuera -- señal de
    extrapolacion, no un grado intermedio.
    """

    cape_covered: Optional[bool] = None
    inflation_covered: Optional[bool] = None
    interest_rate_covered: Optional[bool] = None


@dataclass
class RegimeComparabilityGateResult:
    """
    Resultado discreto con explicaciones. Mismo principio que
    EvidenceQualityGateResult: ausencia de medicion nunca se
    representa con un valor numerico por defecto.
    """

    state: str
    explanations: list[str]


class RegimeComparabilityGate:
    """
    RE-036.1 -- primera implementacion del Regime Comparability Gate
    documentado en RE-031.1.

    Deliberadamente no conectado a run.py, DecisionEngine,
    AssessmentEngine, EvidenceQualityGate ni gate_combination. RE-034.1
    no tiene todavia una entrada para NOT_COMPARABLE en su tabla de
    mapeo a postura -- esa decision queda fuera de alcance de esta
    iteracion, es una decision de gobernanza separada, no una
    consecuencia automatica de que el codigo exista.

    No usa SimilarityEngine ni evidence quality como proxy de
    comparabilidad -- prohibicion explicita de RE-031.1. Mide cobertura
    de rango de forma independiente a la distancia vectorial de
    similitud que ya decidio que episodios son "matches".
    """

    def evaluate(
        self,
        local: LocalRegimeComparabilityInputs,
    ) -> RegimeComparabilityGateResult:

        measured = []
        not_covered = []

        for dimension in REGIME_DIMENSIONS:

            value = getattr(local, f"{dimension}_covered")

            if value is None:
                continue

            measured.append(dimension)

            if not value:
                not_covered.append(dimension)

        if not measured:
            return RegimeComparabilityGateResult(
                state=NOT_MEASURABLE,
                explanations=["no regime dimension measurable"],
            )

        if not_covered:
            return RegimeComparabilityGateResult(
                state=NOT_COMPARABLE,
                explanations=[
                    f"{dimension}: today's value outside the matched "
                    "episodes' range"
                    for dimension in not_covered
                ],
            )

        return RegimeComparabilityGateResult(
            state=COMPARABLE,
            explanations=[
                f"{dimension}: today's value within the matched "
                "episodes' range"
                for dimension in measured
            ],
        )


def _dimension_covered(
    today_value: Optional[float],
    match_values: list,
) -> Optional[bool]:
    """
    RE-036.1 -- criterio binario estricto [minimo, maximo], sin
    percentiles ni margenes: decision explicita de Armando de no
    anticiparse a un problema de outliers que todavia no se ha
    observado. Si aparece, se documenta como hallazgo en una iteracion
    futura, no se resuelve por adelantado con numeros magicos.

    bool(...) explicito en el return: los valores de Context vienen en
    la practica de un pipeline pandas/numpy por debajo, y una
    comparacion encadenada sobre floats numpy devuelve numpy.bool_, no
    bool nativo. LocalRegimeComparabilityInputs declara
    Optional[bool] -- el campo debe contener el tipo que declara, no
    un valor que solo se comporta como tal.
    """

    if today_value is None:
        return None

    values = [value for value in match_values if value is not None]

    if not values:
        return None

    return bool(min(values) <= today_value <= max(values))


def build_local_regime_comparability_inputs(
    snapshot,
    evidence,
) -> LocalRegimeComparabilityInputs:
    """
    RE-036.1 -- construye los inputs locales a partir del snapshot de
    la consulta y del Evidence ya producido para ella.

    snapshot es la unica fuente de verdad del regimen de hoy;
    evidence.matches es la unica fuente de verdad de la muestra
    historica que realmente informa la decision actual -- no el
    universo historico completo. Mismo principio que
    build_local_evidence_quality_inputs(evidence): quien llama no debe
    pasar una lista de matches separada que pudiera desalinearse de
    evidence.matches.
    """

    if snapshot.context is None:
        return LocalRegimeComparabilityInputs()

    match_contexts = [
        match.episode.context
        for match in evidence.matches
        if match.episode.context is not None
    ]

    return LocalRegimeComparabilityInputs(
        cape_covered=_dimension_covered(
            snapshot.context.cape,
            [context.cape for context in match_contexts],
        ),
        inflation_covered=_dimension_covered(
            snapshot.context.inflation,
            [context.inflation for context in match_contexts],
        ),
        interest_rate_covered=_dimension_covered(
            snapshot.context.interest_rate,
            [context.interest_rate for context in match_contexts],
        ),
    )
