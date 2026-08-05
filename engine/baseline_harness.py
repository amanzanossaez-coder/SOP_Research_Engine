from typing import Dict, List, Optional, Tuple

from engine.observable_universe import ObservableUniverse
from engine.validation_harness import ValidationRecord
from engine.validation_metrics import (
    directional_hit_rate,
    mean_absolute_error,
    rank_correlation,
)
from models.evidence import percentile_from_sorted


def _comparable_episodes(dataset, target_episode) -> list:
    """
    RE-PRED.9 -- mismo universo temporal que ValidationHarness usa
    para el modelo: ObservableUniverse(dataset, as_of=target_episode
    .bottom_date).episodes(), autoexcluyendo target_episode por
    bottom_index.

    Deliberadamente reimplementado aqui en vez de llamar al metodo
    privado ValidationHarness._comparable_episodes(): tres lineas de
    logica que ya son publicas via ObservableUniverse, no una
    dependencia nueva. Ambas copias deben permanecer identicas por
    construccion -- si ObservableUniverse cambia, las dos se actualizan
    igual porque las dos lo consumen de la misma forma.
    """

    universe = ObservableUniverse(
        dataset,
        as_of=target_episode.bottom_date,
    )

    return [
        e
        for e in universe.episodes()
        if e.bottom_index != target_episode.bottom_index
    ]


def baseline_forecast(
    dataset,
    episode,
    years: int = 5,
) -> Tuple[Optional[float], int]:
    """
    RE-PRED.8/RE-PRED.9 -- baseline primario.

    Mediana expansiva point-in-time de future_return_{years}y sobre
    TODOS los episodios observables en ObservableUniverse(as_of=
    episode.bottom_date), sin pasar por SimilarityEngine.top(). Es la
    version incondicional del mismo universo temporal que ya usa el
    modelo -- no condiciona por similitud con episode.

    Usa percentile_from_sorted(..., 0.50) -- la misma fuente unica de
    verdad para mediana que EvidenceEngine.median_return (RE-024.1) --
    para que la comparacion baseline vs modelo sea apples-to-apples: el
    mismo algoritmo de percentil en ambos lados, no dos criterios de
    "mediana" que podrian desalinearse en listas de tamaño par.

    Devuelve (forecast, comparable_count). forecast es None solo si
    ningun comparable tiene future_return_{years}y ya observable en ese
    instante -- ausencia de evidencia, nunca 0.0 (misma regla del resto
    del Research Engine).

    Invariante de diseño: si el modelo produjo forecast (evaluable=True
    en el ValidationRecord correspondiente), este baseline nunca puede
    devolver None. Los matches de SimilarityEngine.top() que informan
    al modelo son un subconjunto de _comparable_episodes(dataset,
    episode) -- el mismo pool que este baseline usa sin filtrar. Si al
    menos un match del modelo tenia future_return_{years}y no nulo (
    condicion necesaria para que el modelo sea evaluable), ese mismo
    valor esta tambien en el pool incondicional de este baseline.
    """

    field = f"future_return_{years}y"

    comparables = _comparable_episodes(dataset, episode)

    values = sorted(

        value

        for value in (
            getattr(comparable, field)
            for comparable in comparables
        )

        if value is not None

    )

    return percentile_from_sorted(values, 0.50), len(values)


class BaselineHarness:
    """
    RE-PRED.9 -- produce ValidationRecord de baseline alineados 1:1 con
    los ValidationRecord del modelo, para poder reutilizar
    mean_absolute_error()/directional_hit_rate()/rank_correlation() sin
    reimplementarlos.

    Decision de diseño obligatoria por RE-PRED.8: el baseline NO decide
    su propio conjunto evaluable. evaluable y actual se heredan
    directamente de cada ValidationRecord del modelo -- inventar un
    criterio de inclusion separado para el baseline sesgaria la
    comparacion.
    """

    def __init__(self, dataset):
        self.dataset = dataset

    def run(
        self,
        model_records: List[ValidationRecord],
    ) -> List[ValidationRecord]:

        baseline_records = []

        for record in model_records:

            forecast, comparable_count = baseline_forecast(
                self.dataset,
                record.episode,
                years=record.horizon_years,
            )

            baseline_records.append(
                ValidationRecord(
                    episode=record.episode,
                    horizon_years=record.horizon_years,
                    forecast=forecast,
                    actual=record.actual,
                    comparable_count=comparable_count,
                    evaluable=record.evaluable,
                )
            )

        return baseline_records


def missing_baseline_forecast_count(
    model_records: List[ValidationRecord],
    baseline_records: List[ValidationRecord],
) -> int:
    """
    RE-PRED.9 -- cuenta cuantos records evaluables por el modelo
    recibieron forecast=None en el baseline.

    Por el invariante documentado en baseline_forecast(), este numero
    debe ser 0 siempre. No se asume silenciosamente: se expone como
    diagnostico explicito para que la verificacion lo compruebe en vez
    de darlo por hecho.
    """

    count = 0

    for model_record, baseline_record in zip(
        model_records,
        baseline_records,
    ):

        if model_record.evaluable and baseline_record.forecast is None:
            count += 1

    return count


def zero_forecast(episode) -> float:
    """
    RE-PRED.11 -- baseline secundario "zero": no se espera ningun
    retorno futuro.

    Sin parametros, sin dependencia de ObservableUniverse ni de ningun
    comparable historico -- es un valor fijo conocido de antemano.
    Sirve de piso: si el modelo no le gana ni a esto, no aporta
    ninguna direccion util.

    directional_hit_rate() excluye forecast==0 por diseño (un cero no
    expresa direccion) y rank_correlation() devuelve None cuando todos
    los forecasts son identicos (sin variacion de rango) -- este
    baseline solo puede dar señal en MAE. Es el comportamiento
    esperado, no un defecto de este baseline.
    """

    return 0.0


def mean_reversion_forecast(episode) -> Optional[float]:
    """
    RE-PRED.11 -- baseline secundario "mean-reversion": rebote de
    magnitud igual a la profundidad de la caida en el fondo,
    coeficiente 1, cero parametros ajustados contra el historico.

    Usa unicamente episode.drawdown -- un dato Event ya conocido en el
    propio fondo del episodio, no requiere ningun comparable historico
    ni calibracion. drawdown es negativo por convencion; el forecast es
    su signo invertido.

    Definicion elegida deliberadamente simple. No es la unica nocion
    posible de "reversion a la media" -- una version calibrada contra
    el historico introduciria un riesgo de sobreajuste nuevo dentro de
    lo que debe seguir siendo un baseline ingenuo, sin parametros
    libres (RE-PRED.11).
    """

    if episode.drawdown is None:
        return None

    return -episode.drawdown


def build_baseline_records(
    model_records: List[ValidationRecord],
    forecast_fn,
) -> List[ValidationRecord]:
    """
    RE-PRED.11 -- construye ValidationRecord de baseline a partir de
    una funcion forecast_fn(episode) -> float | None, para baselines
    que no dependen de ObservableUniverse (zero, mean-reversion).

    Mismo principio de diseño que BaselineHarness (RE-PRED.9): evaluable
    y actual se heredan directamente del ValidationRecord del modelo --
    nunca se inventa un criterio de inclusion propio para el baseline.

    comparable_count queda en 0 para estos baselines: no usan ningun
    comparable historico, a diferencia del baseline primario.
    """

    baseline_records = []

    for record in model_records:

        forecast = forecast_fn(record.episode)

        baseline_records.append(
            ValidationRecord(
                episode=record.episode,
                horizon_years=record.horizon_years,
                forecast=forecast,
                actual=record.actual,
                comparable_count=0,
                evaluable=record.evaluable,
            )
        )

    return baseline_records


def excess_summary(
    model_records: List[ValidationRecord],
    baseline_records: List[ValidationRecord],
) -> Dict[str, Optional[float]]:
    """
    RE-PRED.8/RE-PRED.9 -- comparacion cabeza a cabeza entre modelo y
    baseline, sobre las tres metricas canonicas existentes. No se
    mezclan en un solo numero (prohibido explicitamente por RE-PRED.8).

    MAE: menor es mejor. excess_mae = MAE baseline - MAE modelo
    (positivo significa que el modelo gana).

    directional_hit_rate / rank_correlation: mayor es mejor.
    excess_* = metrica modelo - metrica baseline (positivo significa
    que el modelo gana).

    Cualquier excess es None si alguno de los dos lados no es
    calculable -- ausencia de evidencia, nunca 0.0.
    """

    def _excess(better_is_higher: bool, a, b):

        if a is None or b is None:
            return None

        return (a - b) if better_is_higher else (b - a)

    model_mae = mean_absolute_error(model_records)
    baseline_mae = mean_absolute_error(baseline_records)

    model_hit_rate = directional_hit_rate(model_records)
    baseline_hit_rate = directional_hit_rate(baseline_records)

    model_rank_correlation = rank_correlation(model_records)
    baseline_rank_correlation = rank_correlation(baseline_records)

    return {

        "model_mae": model_mae,
        "baseline_mae": baseline_mae,
        "excess_mae": _excess(False, model_mae, baseline_mae),

        "model_hit_rate": model_hit_rate,
        "baseline_hit_rate": baseline_hit_rate,
        "excess_hit_rate": _excess(
            True, model_hit_rate, baseline_hit_rate,
        ),

        "model_rank_correlation": model_rank_correlation,
        "baseline_rank_correlation": baseline_rank_correlation,
        "excess_rank_correlation": _excess(
            True, model_rank_correlation, baseline_rank_correlation,
        ),

    }
