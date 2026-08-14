from dataclasses import dataclass
from datetime import date

from models.evidence import Evidence
from models.explanation import Explanation
from models.similarity import Similarity
from models.snapshot import Snapshot


@dataclass
class ResearchResult:
    """
    Complete output produced by the Research Engine.

    RE-027.2 aligns ResearchResult with the operative Research
    pipeline that is already verified through DecisionEngine:

    SnapshotEngine
    -> ObservableUniverse
    -> SimilarityEngine.top()
    -> EvidenceEngine

    It contains objective historical evidence and the selected
    historical matches that produced it.

    It does not contain recommendations or portfolio decisions.

    RE-EXP.1 -- the global explanation object RE-027.2 excluded ("until
    it is rebuilt against the current Similarity model") is back:
    ExplanationEngine was audited, found broken (read an attribute
    that never existed on the real Similarity model -- confirmed by
    running it), fixed, and extended to cover Articulo 8's
    contradicting-evidence requirement. See
    engine/explanation_engine.py and models/explanation.py for what
    changed.

    RE-044.4 -- Articulo 5 (Trazabilidad): "toda respuesta producida
    por el motor debera poder reconstruirse... datos utilizados,
    funciones ejecutadas, parametros empleados, version del motor,
    fuentes consultadas." Until this iteration ResearchResult carried
    none of this -- core/version.py already defined ENGINE_VERSION/
    ENGINE_NAME specifically for this purpose, but nothing attached
    them to an actual result.

    Added: engine_name/engine_version (read from core/version.py, not
    reinvented here), matches_count/horizon_years (the actual
    parameters build_research_result() received, not an assumed
    value), generated_at (wall-clock date the pipeline ran -- distinct
    from snapshot.date, which is the market date being analysed, not
    when the code executed).

    Deliberately left out of this iteration:

    -   "Fuentes consultadas" -- which data file fed the Dataset. This
        object only knows the Dataset it was handed, not where it
        came from; asserting "data/raw/shiller.xlsx" here would be an
        unverified claim at this point in the code (Articulo 12).
    -   "Funciones ejecutadas" as a per-instance field -- it is the
        same fixed sequence for every instance (documented above);
        a runtime field would be redundant, not informative.
    """

    snapshot: Snapshot

    matches: list[Similarity]

    evidence: Evidence

    explanation: Explanation

    engine_name: str

    engine_version: str

    matches_count: int

    horizon_years: int

    generated_at: date
