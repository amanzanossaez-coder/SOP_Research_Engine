# SOP ENGINE PROJECT STATUS

**Version:** 1.3\
**Status:** Core Stable — Evidence Layer Aligned

------------------------------------------------------------------------

# Purpose

This document is the technical source of truth for the Research Engine.

The Research Engine is **not** the SOP itself.

Its sole responsibility is transforming historical market data into
objective, reproducible and explainable evidence.

The SOP (Sistema Operativo Patrimonial) is the product.

The Constitution and the governance protocols decide how that evidence
is used.

------------------------------------------------------------------------

# Source of Truth Declaration (RE-DOC-001)

This document is the single official source of truth for the status
of the Research Engine.

`docs/ROADMAP.md` and `docs/PROJECT_STATE.md` are **not** authoritative.
They predate this declaration, contain roadmap information that no
longer matches this document, and are marked pending consolidation.
They should not be updated as a substitute for this file. A future,
dedicated iteration will merge or retire them — not before the
Observable Universe block (RE-023.x) is stabilized.

------------------------------------------------------------------------

# Governance Principles

-   The Constitution is the highest authority.
-   Engines produce evidence, never portfolio decisions.
-   The architecture is modular.
-   Every module has one responsibility.
-   Explainability is preferred over sophistication.
-   Small compatible iterations are preferred over large refactorings.

------------------------------------------------------------------------

# Current Architecture

    Raw Data
        │
    Dataset Engine
        │
    Snapshot Engine
        │
    Similarity Engine
        │
    Evidence Engine
        │
    Assessment Engine
        │
    Inference Engine
        │
    Constitution
        │
    Protocols
        │
    Dashboard

------------------------------------------------------------------------

# Execution State (as of RE-024.2)

This diagram describes the intended architecture. It does not
describe what `run.py` actually executes today. Distinguishing
"exists in the repository", "participates in the executed flow", and
"matches this diagram's named objects" is deliberate -- conflating
them is exactly the kind of drift this document exists to prevent.

## Operative flow

The only path whose end-to-end methodological consistency has been
verified:

    Dataset
        │
    SnapshotEngine
        │
    ObservableUniverse
        │
    SimilarityEngine
        │
    EvidenceEngine
        │
    DecisionEngine

## Exists, but outside the operative flow

  Component           State
  ------------------- ------------------------------------------------
  AssessmentEngine     Exists, compiles. Not called by run.py. Builds its
                        own SimilarityEngine directly from
                        dataset.episodes -- never connected to
                        ObservableUniverse. Also uses ValidationEngine
                        for confidence (coverage/consistency/diversity/
                        stability, with stability hardcoded to 1.0) --
                        a second, different confidence computation than
                        DecisionEngine's.
  InferenceEngine      Exists. Its responsibility (queries over
                        episodes -- drawdowns_greater_than,
                        recovered_in_less_than) remains valid. Not part
                        of the operative flow today.
  ProbabilityEngine    Exists physically. No longer used by the
                        operative flow. Its only remaining caller is
                        AssessmentEngine, which is itself outside the
                        operative flow -- so it is, transitively,
                        unused in what actually runs.
  ExplanationEngine    Exists. References attributes that do not exist
                        on SimilarityExplanation (e.g.
                        first.event.drawdown_similarity) -- would raise
                        AttributeError if ever called. Never called
                        today.
  ResearchEngine       See below -- distinct from the others because
                        the documented architecture names it
                        explicitly.

## Matches the diagram's named objects: not yet

The architecture above names `ResearchEngine` producing a
`ResearchResult`. That object does not reflect the work done in
RE-023/RE-024: its constructor calls are inconsistent with current
signatures, it calls a `SnapshotEngine.build()` method that does not
exist, and it is not part of `run.py`.

What is aligned with the architecture today is the *conceptual* flow
executed inside `DecisionEngine` -- not the `ResearchEngine` object
the documentation names. Rebuilding `ResearchEngine` so it matches
what `DecisionEngine` already does correctly remains open work.

## Other known-broken, disconnected code

`core/dataset_builder.py` builds `Episode` with fields (`date`,
`price`, `dividend_yield`, `earnings`, `cpi`, `gs10`) that do not
exist on the current `Episode`, and calls `Dataset(episodes)` with
one positional argument where two are required. Never executed by
anything in the operative flow.

------------------------------------------------------------------------

# Core Maturity Declaration

Starting with **version 1.0**, the Core architecture is considered
**stable**.

The following components are frozen as part of the Core:

-   Dataset Engine
-   Snapshot Engine
-   Drawdown calculations
-   Similarity Engine
-   Probability calculations
-   Normalization framework
-   Core domain models

Changes to these components should only occur when:

-   a functional defect exists,
-   objective evidence demonstrates incorrect behaviour,
-   or a governance decision explicitly authorizes the modification.

The primary effort of the project now shifts away from infrastructure
and towards functional capabilities:

1.  Evidence generation.
2.  Market assessment.
3.  Evidence-based inference.
4.  Executable constitutional rules.
5.  Portfolio governance protocols.

This declaration marks the end of the infrastructure phase and the
beginning of the functional phase of the Sistema Operativo Patrimonial.

------------------------------------------------------------------------

# Frozen Core Policy

The Core should remain stable.

Infrastructure refactoring must never be performed simply because a
cleaner design is possible.

Changes require objective justification.

## Exceptions invoked

-   **RE-021.** Similarity Engine (frozen) was modified to remove
    `recovery` (an Outcome variable) from the global similarity
    score. Justification: objective evidence of a data-leakage
    defect — Outcome participating in episode selection biased the
    resulting evidence. Authorized under "a functional defect
    exists."

------------------------------------------------------------------------

# Component Status

  Component           Status
  ------------------- ------------------------------------------
  Dataset Engine      Stable
  Snapshot Engine     Stable
  Similarity Engine   Stable (RE-021 exception — see Frozen Core Policy)
  Observable Universe Stable in operative flow (wired through DecisionEngine, RE-023.5; AssessmentEngine pending, RE-024.3)
  Evidence Engine     v1
  Assessment Engine   v1
  Inference Engine    Planned
  Constitution        Planned
  Protocol Engine     Planned
  Dashboard           Planned

------------------------------------------------------------------------

# Evidence Definition

Evidence must always contain three dimensions.

## Evidence

Objective historical statistics.

Examples:

-   mean outcome
-   median outcome
-   probability
-   recovery time
-   dispersion

## Confidence

How trustworthy the evidence is.

Examples:

-   sample size
-   similarity quality
-   consistency

## Quality

Quality of the historical dataset.

Examples:

-   missing data
-   structural breaks
-   outliers
-   coverage

------------------------------------------------------------------------

# Design Decisions

## RE-001

Future performance is measured using CAGR.

## RE-002

Evidence uses `future_return_5y`.

## RE-003

Assessment separates:

-   Market Position
-   Valuation Zone
-   Volatility Regime

## RE-004

Similarity excludes recent historical episodes by default.

## RE-005

Confidence is part of the Evidence object.

No standalone Confidence Engine will exist.

## RE-021

Outcome (`recovery`) removed from the global similarity score in
`SimilarityEngine`. Recovery remains under Outcome, descriptive only
— it must never influence which episodes are selected as matches.
See Frozen Core Policy exception above.

## RE-022

`SimilarityEngine.__init__` accepts an optional `cape_metric`
parameter, so a calibration built from observable episodes only can
be injected instead of recalculating over the full canonical
Dataset. Not yet wired to any caller.

## RE-023.1 — ObservableEpisode

New, independent type (does not inherit from `Episode`) representing
an episode as it could be observed at a given instant. Deliberately
not a subtype of `Episode`, to make it impossible for a canonical
and an observable episode to be substituted for one another by
accident.

## RE-023.2 — ObservableUniverse (skeleton)

`ObservableUniverse(dataset, as_of)` introduced. `episodes()` is an
identity transformation at this stage — validates the plumbing
before any temporal rule is added. Internally stores a copy of
`dataset.data` already filtered to `as_of`, never a reference to the
full canonical Dataset, so future methods cannot forget to filter it.

## RE-023.3 — Temporal masking of Outcome

`ObservableUniverse` masks Outcome fields (`recovery_*`,
`future_return_Xy`, `probability_positive_Xy`) to `None` when they
would not yet be observable at `as_of`, evaluated per field/horizon
— not per episode. Event and Context are never masked.

## RE-023.4 — Temporal existence of episodes

`ObservableUniverse.episodes()` now excludes episodes whose
`bottom_date > as_of` entirely. Cutoff uses `bottom_date`, not
`peak_date`: Event/Context are only fixed once the bottom is
reached. This does not yet replace the `peak_date`-based filter in
`SimilarityEngine.top()` — that removal is scoped for RE-023.6,
after wiring (RE-023.5) exists.

## RE-023.5 — Wiring: DecisionEngine consumes ObservableUniverse

`DecisionEngine` builds `ObservableUniverse(dataset, as_of=snapshot.date)`
and passes `universe.episodes()` into `SimilarityEngine`, which now
accepts an episode collection directly instead of a `Dataset`. CAPE
percentile calibration is fixed as a side effect: it is computed from
whatever collection `SimilarityEngine` receives, so once that
collection is Universe-sourced, the calibration is temporally safe
without any change to the calibration logic itself.
`AssessmentEngine` was mechanically adjusted to keep working
(`SimilarityEngine(dataset.episodes)`) but was deliberately not
connected to `ObservableUniverse` — out of scope, tracked under
RE-024.3.

## RE-023.6 — Responsibility correction in SimilarityEngine.top()

No behaviour change. The `peak_date < cutoff` filter cannot be split
into a "leakage" clause and a "RE-004 independence" clause — it is
one expression serving RE-004 alone, whose leakage-blocking effect is
an imprecise (peak_date, not bottom_date) side effect, kept
deliberately for callers that bypass ObservableUniverse (today,
AssessmentEngine). Comment corrected to attribute temporal safety
exclusively to ObservableUniverse.

## RE-024.1 — Evidence generalized

`Evidence` is no longer coupled to a 5-year horizon: fields renamed
without the `_5y` suffix, `horizon_years` made explicit,
`percentile(p)` computed on demand (not precomputed), single shared
percentile algorithm (`percentile_from_sorted`, also used for
`median_return`/`worst_return`/`best_return` to avoid disagreeing
with `percentile(0.5)` on even-sized match lists). `years` and `p`
are validated (`OUTCOME_HORIZONS_YEARS`, shared with
`ObservableUniverse`; `0.0 <= p <= 1.0`). Absence of evidence returns
`None`, never `0.0` — a Research-Engine-wide design rule now, not
just this object's: a 0.0 is a statistical claim, absence of data is
not. No public behaviour change; nothing consumed the generalized
object yet.

## RE-024.2 — DecisionEngine migrated off ProbabilityEngine

`expected_return()`/`upside()`/`downside()` now come from
`EvidenceEngine` built over the exact same `matches` shown as "top
episodios similares" — not from `ProbabilityEngine`'s unconditional
aggregation over the full 23-episode Dataset. `DecisionEngine`
computes `self._matches` once in `__init__` so `Evidence.matches` and
`historical_matches()` are guaranteed to be the same collection, not
two separate calls to `SimilarityEngine.top()`. `ProbabilityEngine`
no longer imported or instantiated by `DecisionEngine`.
`DecisionEngine` contains no statistical logic of its own (verified:
no `mean`/`median`/`sorted`/`percentile` calls in the class). Result
verified against an independent, by-hand recomputation from the
displayed episodes, not just against passing tests. `run.py` diff
confirmed targeted to exactly the affected lines.

------------------------------------------------------------------------

# Roadmap

## Phase 1

Evidence Engine v2

## Phase 2

Assessment Engine v2

## Phase 3

Inference Engine

## Phase 4

Executable Constitution

## Phase 5

Protocol Engine

## Phase 6

Dashboard

------------------------------------------------------------------------

# Project Axioms

-   SOP is the product.
-   Research Engine produces evidence.
-   Evidence must be explainable.
-   Governance is above prediction.
-   Robustness is preferred over sophistication.
-   Every iteration modifies one responsibility.
-   Stability has priority over novelty.

------------------------------------------------------------------------

# Changelog

## Version 1.3

-   Added "Execution State" section: explicit three-way distinction
    between exists / participates in the operative flow / matches
    the diagram's named objects (RE-023/RE-024 closing review).
-   Logged RE-023.5, RE-023.6, RE-024.1, RE-024.2.
-   Documented ResearchEngine's continued divergence from what
    DecisionEngine actually executes.
-   Catalogued additional known-broken, disconnected code
    (ExplanationEngine, core/dataset_builder.py).

## Version 1.2

-   Declared this document the single source of truth (RE-DOC-001);
    `ROADMAP.md` and `PROJECT_STATE.md` marked non-authoritative
    pending future consolidation.
-   Logged RE-021 through RE-023.4.
-   Recorded the Frozen Core Policy exception invoked by RE-021.
-   Added Observable Universe to Component Status.

## Version 1.1

-   Core declared stable.
-   Governance clarified.
-   Research Engine formally separated from SOP.
-   Infrastructure phase closed.
-   Functional roadmap established.
