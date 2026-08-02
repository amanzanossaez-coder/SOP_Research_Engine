from engine.research_pipeline import build_research_result
from models.research_result import ResearchResult


class ResearchEngine:
    """
    Orchestrates the objective Research pipeline.

    RE-027.5 makes ResearchEngine delegate to the shared Research
    pipeline, so it cannot drift from DecisionEngine.

    ResearchEngine produces evidence. It never produces portfolio
    decisions, recommendations or protocol actions.
    """

    def run(
        self,
        dataset,
        matches_count: int = 10,
        horizon_years: int = 5,
    ) -> ResearchResult:

        return build_research_result(
            dataset,
            matches_count=matches_count,
            horizon_years=horizon_years,
        )
