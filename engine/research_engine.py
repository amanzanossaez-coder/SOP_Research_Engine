from core.dataset_builder import DatasetBuilder
from engine.snapshot_engine import SnapshotEngine
from engine.similarity_engine import SimilarityEngine
from engine.evidence_engine import EvidenceEngine
from engine.assessment_engine import AssessmentEngine


class ResearchEngine:
    """
    Orquestador del Research Engine.

    Coordina la ejecución del pipeline completo respetando
    los contratos definidos por el SOP.
    """

    def __init__(self):

        self.dataset_builder = DatasetBuilder()
        self.snapshot_engine = SnapshotEngine()
        self.evidence_engine = EvidenceEngine()
        self.assessment_engine = AssessmentEngine()

    def run(self, dataframe):

        # Contrato 1
        dataset = self.dataset_builder.build(dataframe)

        # Contrato 2
        snapshot = self.snapshot_engine.build(dataframe)

        # Contrato 3
        similarity_engine = SimilarityEngine(dataset)
        similarities = similarity_engine.compare(snapshot)

        # De momento el resto del pipeline permanece igual.
        # En próximas iteraciones sustituiremos esta parte
        # por los nuevos contratos.

        return similarities