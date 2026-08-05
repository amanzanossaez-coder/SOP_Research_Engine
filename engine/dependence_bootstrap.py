import random
from typing import Callable, Dict, List, Optional, Tuple

from engine.validation_harness import ValidationRecord
from engine.validation_metrics import (
    overlapping_outcome_windows,
    repeated_forecast_groups,
)

# RE-PRED.15 -- semilla y numero de replicas fijos y documentados
# explicitamente (Art. 4, reproducibilidad). No se exponen como
# parametros libres en el script de diagnostico: cualquier cambio aqui
# es un cambio de metodo, no un ajuste de ejecucion.
BOOTSTRAP_SEED = 42
BOOTSTRAP_REPLICATES = 5000

# RE-PRED.15 -- intervalo de percentil por defecto (90%: percentiles 5
# y 95). Eleccion de diseño explicita, no la unica posible.
BOOTSTRAP_PERCENTILES = (5, 95)


def independence_clusters(
    records: List[ValidationRecord],
) -> List[List[int]]:
    """
    RE-PRED.15 -- particion de records evaluables en clusters de
    independencia, identificados por POSICION dentro de `records` (no
    por objeto ni por episode.bottom_index directamente), para poder
    aplicar exactamente el mismo particionado a cualquier lista
    paralela de ValidationRecord (baseline primario RE-PRED.9,
    baseline secundario RE-PRED.11) que comparta el mismo orden y la
    misma longitud -- invariante que BaselineHarness.run() y
    build_baseline_records() ya garantizan por construccion.

    Arista entre dos records si aparecen juntos en
    overlapping_outcome_windows() (RE-025.8, dependencia por el lado
    del outcome) o en el mismo grupo de repeated_forecast_groups()
    (RE-025.9, dependencia por el lado del forecast). No se introduce
    ningun tercer criterio de dependencia: son exactamente los dos
    canales ya diagnosticados y confirmados en RE-025.6/8/9, conectados
    aqui por primera vez en un grafo de componentes conexas.

    Un record evaluable que no comparte arista con ningun otro es su
    propio cluster de tamaño 1 -- no se descarta, participa en el
    bootstrap como un cluster independiente mas.

    Devuelve una lista de clusters, cada uno una lista de posiciones
    (indices en `records`).
    """

    evaluable_positions = [
        i for i, record in enumerate(records) if record.evaluable
    ]

    position_by_id = {
        id(records[i]): i for i in evaluable_positions
    }

    parent = {i: i for i in evaluable_positions}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[root_a] = root_b

    for left, right in overlapping_outcome_windows(records):
        union(position_by_id[id(left)], position_by_id[id(right)])

    for group in repeated_forecast_groups(records):
        first_position = position_by_id[id(group[0])]
        for record in group[1:]:
            union(first_position, position_by_id[id(record)])

    clusters: Dict[int, List[int]] = {}

    for position in evaluable_positions:
        root = find(position)
        clusters.setdefault(root, []).append(position)

    return list(clusters.values())


def _resample_positions(
    clusters: List[List[int]],
    rng: random.Random,
) -> List[int]:
    """
    RE-PRED.15 -- un remuestreo con reemplazo A NIVEL DE CLUSTER, no de
    record individual: se sortean tantos clusters como clusters
    originales existen, y se concatenan sus posiciones. Esto preserva
    la dependencia intra-cluster documentada en RE-025.8/RE-025.9 en
    vez de romperla -- es precisamente lo que RE-PRED.1 exige y lo que
    un bootstrap i.i.d. sobre records individuales no respetaria.
    """

    resampled_clusters = [
        clusters[rng.randrange(len(clusters))]
        for _ in range(len(clusters))
    ]

    return [
        position
        for cluster in resampled_clusters
        for position in cluster
    ]


def _percentile_summary(
    values: List[float],
    replicates: int,
    percentiles: Tuple[int, int],
) -> Dict[str, Optional[float]]:

    valid_replicates = len(values)

    if valid_replicates == 0:
        return {
            "replicates": replicates,
            "valid_replicates": 0,
            "low": None,
            "high": None,
        }

    values = sorted(values)

    def _at(p: int) -> float:
        index = round((p / 100) * (valid_replicates - 1))
        index = max(0, min(valid_replicates - 1, index))
        return values[index]

    return {
        "replicates": replicates,
        "valid_replicates": valid_replicates,
        "low": _at(percentiles[0]),
        "high": _at(percentiles[1]),
    }


def cluster_bootstrap_ci(
    clusters: List[List[int]],
    records: List[ValidationRecord],
    metric_fn: Callable[[List[ValidationRecord]], Optional[float]],
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
    percentiles: Tuple[int, int] = BOOTSTRAP_PERCENTILES,
) -> Dict[str, Optional[float]]:
    """
    RE-PRED.15 -- intervalo de percentil dependence-aware para una
    metrica ya existente (mean_absolute_error, directional_hit_rate o
    rank_correlation de validation_metrics.py -- ninguna se reimplementa
    aqui).

    Replicas en las que metric_fn devuelve None (p.ej. rank_correlation
    degenera si el remuestreo produce forecasts todos identicos) se
    excluyen del percentil, no se tratan como 0.0 -- misma regla de
    ausencia de evidencia que el resto del modulo. valid_replicates lo
    expone explicitamente.
    """

    rng = random.Random(seed)

    values = []

    for _ in range(replicates):

        positions = _resample_positions(clusters, rng)

        resampled_records = [records[p] for p in positions]

        value = metric_fn(resampled_records)

        if value is not None:
            values.append(value)

    return _percentile_summary(values, replicates, percentiles)


def cluster_bootstrap_paired_excess(
    clusters: List[List[int]],
    model_records: List[ValidationRecord],
    baseline_records: List[ValidationRecord],
    metric_fn: Callable[[List[ValidationRecord]], Optional[float]],
    better_is_higher: bool,
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
    percentiles: Tuple[int, int] = BOOTSTRAP_PERCENTILES,
) -> Dict[str, Optional[float]]:
    """
    RE-PRED.15 -- version pareada de cluster_bootstrap_ci: aplica EL
    MISMO sorteo de clusters, en la misma replica, tanto al modelo como
    al baseline, y calcula el excess sobre ese par -- no dos bootstraps
    independientes restados al final. RE-PRED.10/11 ya evaluan modelo y
    baseline sobre exactamente los mismos episodios fila a fila; este
    bootstrap respeta esa misma correspondencia dentro de cada replica,
    preservando la varianza pareada en vez de inflarla.

    Convencion de signo identica a excess_summary()
    (engine/baseline_harness.py): better_is_higher=False para MAE
    (positivo = gana el modelo), True para hit-rate y rank correlation.

    Una replica se descarta si metric_fn devuelve None para el modelo o
    para el baseline en esa replica -- no se imputa ningun valor.
    """

    rng = random.Random(seed)

    values = []

    for _ in range(replicates):

        positions = _resample_positions(clusters, rng)

        resampled_model = [model_records[p] for p in positions]
        resampled_baseline = [baseline_records[p] for p in positions]

        model_value = metric_fn(resampled_model)
        baseline_value = metric_fn(resampled_baseline)

        if model_value is None or baseline_value is None:
            continue

        excess = (
            (model_value - baseline_value)
            if better_is_higher
            else (baseline_value - model_value)
        )

        values.append(excess)

    return _percentile_summary(values, replicates, percentiles)
