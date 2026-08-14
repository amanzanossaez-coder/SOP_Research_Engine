"""
SOP Research Engine
Confidence -- categorical layer

RE-044.1 -- this file existed but was empty since the Research
Engine's founding constitution (Articulo 7) required a categorical
Alta/Media/Baja confidence reading, with thresholds as named global
constants, never a raw score leaked as false precision.

In its absence, two independent confidence computations had grown up
with no relationship to each other:

1. engine/validation_engine.py::ValidationEngine.confidence() builds
   models/confidence.py's `Confidence` dataclass (coverage +
   consistency + diversity + stability, averaged into `.score`).
   Consumed only by AssessmentEngine, which explicitly warned this
   score "must not be used as a capital-allocation gate until the
   placeholder is replaced or explicitly governed" -- `stability` has
   never been implemented and is hardcoded to 1.0.

2. engine/decision_engine.py::DecisionEngine.confidence() -- a second,
   unrelated computation: counted matches with similarity score >=
   0.75 and thresholded that count (>=8 Alta, >=4 Media), hardcoded
   inline. This is the one actually printed by run.py -- the one
   Armando has been seeing. DecisionEngine's own module docstring
   claims "DecisionEngine deja de contener ninguna logica estadistica
   propia" (RE-024.2), which this method directly contradicted.

RE-044.1 unifies these into one categorical reading, per Armando's
explicit decision (chose unification over keeping two parallel,
separately-documented confidence systems). `categorize()` below is
the only place this translation happens.
DecisionEngine.confidence() now delegates here instead of carrying
its own logic -- see engine/decision_engine.py (RE-044.1).

Known caveat, carried forward unchanged from AssessmentEngine's
original warning, not resolved by this iteration: `stability` is
still a placeholder pinned at 1.0. Every score computed today
includes a guaranteed +0.25 contribution that is not real
measurement. The thresholds in core/constants.py are calibrated
against the achievable range this produces ([0.25, 1.0], never
lower) -- see the comment there. This iteration does not implement
stability; it only makes the categorical reading explicit and
singular instead of duplicated and silent.
"""

from core.constants import (
    CONFIDENCE_SCORE_ALTA_THRESHOLD,
    CONFIDENCE_SCORE_MEDIA_THRESHOLD,
)


ALTA = "ALTA"
MEDIA = "MEDIA"
BAJA = "BAJA"


def categorize(score: float) -> str:
    """
    Translates a Confidence.score (0.0-1.0) into the categorical
    reading Articulo 7 requires. This is the only function in the
    codebase that should make this translation -- callers (e.g.
    engine/decision_engine.py) call this rather than reimplementing
    their own thresholds.
    """

    if score >= CONFIDENCE_SCORE_ALTA_THRESHOLD:
        return ALTA

    if score >= CONFIDENCE_SCORE_MEDIA_THRESHOLD:
        return MEDIA

    return BAJA
