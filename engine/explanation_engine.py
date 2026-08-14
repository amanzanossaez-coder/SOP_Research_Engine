from core.constants import (
    EXPLANATION_DIMENSION_SPLIT_COUNT,
    EXPLANATION_MAX_CONTRADICTING_PRECEDENTS,
)
from models.explanation import ContradictingPrecedent, Explanation


# RE-EXP.1 -- las siete dimensiones planas y reales de Similarity
# (models/similarity.py: drawdown_score, duration_score, ...).
#
# No reutiliza engine/dimension_diagnostic.py's DIMENSION_SCORE_FIELDS
# a proposito: esa lista excluye recovery_score por fuga de datos, en
# un contexto distinto -- medir si UNA dimension sola tiene poder
# predictivo contra un snapshot en vivo, donde "como se recupero" es
# informacion del futuro. Aqui no se mide poder predictivo: se explica
# un match set ya seleccionado, donde recovery_score ya participo del
# score combinado que los selecciono (core/constants.py's
# SIMILARITY_WEIGHTS incluye "recovery": 0.10) y run.py's bloque
# SIMILARITY DIAGNOSTICS ya lo trata igual que las demas. Excluirlo
# aqui seria inconsistente con como el resto del sistema ya lo usa.
DIMENSION_FIELDS = [
    ("Drawdown", "drawdown_score"),
    ("Duration", "duration_score"),
    ("Speed", "speed_score"),
    ("CAPE", "cape_score"),
    ("Trend 3Y", "pre_crash_return_3y_score"),
    ("Volatility", "volatility_score"),
    ("Recovery", "recovery_score"),
]


class ExplanationEngine:
    """
    Builds a human-readable explanation of the evidence.

    This engine never modifies the evidence.
    It only explains how it was produced.

    RE-EXP.1 -- fixed and reconnected after auditing the Research
    Engine against its own Articulo 8 (Explicabilidad). Before this
    iteration, build() read first.event.drawdown_similarity -- an
    attribute that never existed on the real SimilarityExplanation
    object (models/similarity_explanation.py). Confirmed by running it
    against real data before touching anything:
    `AttributeError: 'SimilarityExplanation' object has no attribute
    'drawdown_similarity'`. It also only ever looked at
    self.matches[0], and never distinguished evidence that supports a
    conclusion from evidence that contradicts it -- Articulo 8
    requires both. Neither bug was caught earlier because
    ResearchResult never wired this engine in (RE-027.2's deliberate
    exclusion, closed by this same iteration -- see
    engine/research_pipeline.py).

    Now takes `evidence` in addition to `matches`: needed to read
    Evidence.median_return / Evidence.horizon_years for
    contradicting-precedent detection, reusing EvidenceEngine's
    already-computed median instead of recomputing it independently
    here (single source of truth -- same reasoning as RE-044.1's
    Confidence unification). EvidenceEngine itself is untouched; this
    class only consumes its output.
    """

    def __init__(self, matches, evidence):

        self.matches = matches
        self.evidence = evidence

    def _dimension_averages(self):

        averages = []

        for label, field_name in DIMENSION_FIELDS:

            values = [
                getattr(match, field_name)
                for match in self.matches
                if getattr(match, field_name) is not None
            ]

            if values:
                averages.append((label, sum(values) / len(values)))

        averages.sort(key=lambda item: item[1], reverse=True)

        return averages

    def _contradicting_precedents(self):
        """
        Articulo 8: variables/precedentes que CONTRADICEN la
        conclusion, no solo los que la sostienen.

        Regla, tal como la fijo Armando: si Evidence.median_return es
        positivo, contradicen los matches con retorno futuro negativo;
        si es negativo, contradicen los positivos; sin evidencia de
        retorno (median_return is None) no hay nada que comparar. El
        caso median_return == 0.0 exacto (sin signo claro) es un borde
        improbable con retornos continuos reales, pero Articulo 8 pide
        un criterio explicito, no una omision -- se listan los
        precedentes mas alejados de la mediana, topados a
        EXPLANATION_MAX_CONTRADICTING_PRECEDENTS.
        """

        horizon_field = f"future_return_{self.evidence.horizon_years}y"
        median = self.evidence.median_return

        if median is None:
            return [], (
                "No hay retorno futuro medido a este horizonte -- no "
                "se puede identificar contraevidencia."
            )

        def actual_return(match):
            return getattr(match.episode, horizon_field)

        if median > 0:

            dissenting = [
                match
                for match in self.matches
                if (r := actual_return(match)) is not None and r < 0
            ]

            criterion = (
                f"Contraevidencia: precedentes con retorno negativo "
                f"frente a una mediana positiva ({median:.2%})."
            )

        elif median < 0:

            dissenting = [
                match
                for match in self.matches
                if (r := actual_return(match)) is not None and r > 0
            ]

            criterion = (
                f"Contraevidencia: precedentes con retorno positivo "
                f"frente a una mediana negativa ({median:.2%})."
            )

        else:

            with_returns = [
                match
                for match in self.matches
                if actual_return(match) is not None
            ]

            with_returns.sort(
                key=lambda match: abs(actual_return(match) - median),
                reverse=True,
            )

            dissenting = with_returns[
                :EXPLANATION_MAX_CONTRADICTING_PRECEDENTS
            ]

            criterion = (
                "Mediana sin signo claro (0%) -- criterio aplicado: "
                "precedentes mas alejados de la mediana."
            )

        precedents = [
            ContradictingPrecedent(
                episode_date=match.episode.bottom_date,
                actual_return=actual_return(match),
                similarity_score=match.score,
            )
            for match in dissenting
        ]

        if precedents:
            note = (
                f"{criterion} {len(precedents)} de {len(self.matches)} "
                f"precedentes la contradicen."
            )
        else:
            note = (
                f"{criterion} No se encontraron precedentes que la "
                f"contradigan en este set."
            )

        return precedents, note

    def build(self):

        sample_size = len(self.matches)

        top_matches = self.matches[:5]

        dimension_averages = self._dimension_averages()

        supporting = dimension_averages[
            :EXPLANATION_DIMENSION_SPLIT_COUNT
        ]
        weak = dimension_averages[
            -EXPLANATION_DIMENSION_SPLIT_COUNT:
        ]

        contradicting_precedents, contradicting_note = (
            self._contradicting_precedents()
        )

        notes = [
            f"Evidence generated from {sample_size} historical episodes.",
            contradicting_note,
        ]

        return Explanation(

            sample_size=sample_size,

            top_matches=top_matches,

            supporting_similarity_dimensions=supporting,

            weak_similarity_dimensions=weak,

            contradicting_precedents=contradicting_precedents,

            notes=notes,

        )
