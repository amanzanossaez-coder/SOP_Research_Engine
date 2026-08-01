# SOP ENGINE PROJECT STATUS

**Version:** 1.7\
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

# Execution State (as of RE-025.5)

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
  Research Validation  Exists (RE-025.1-RE-025.5), fully independent of
  Harness               run.py -- invoked manually, no wiring exists or
                        is planned yet. Deliberately offline: for each
                        historical episode it replays DecisionEngine's
                        own methodology -- ObservableUniverse(as_of=
                        episode.bottom_date) for comparables,
                        SimilarityEngine.top() for matches,
                        EvidenceEngine.build() for the forecast -- so it
                        validates the system that actually runs, not a
                        hypothetical one. Self-exclusion of the episode
                        under evaluation is by bottom_index, never by
                        object identity (ObservableUniverse.episodes()
                        returns ObservableEpisode, a type deliberately
                        distinct from Episode -- RE-023.1/ADR-004 --
                        so `is not` would never have excluded anything).
                        Unrelated to ValidationEngine above despite the
                        similar name -- see Component Status.

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

RE-025.1-RE-025.5 invoke no exception: the Research Validation
Harness consumes `ObservableUniverse`, `SimilarityEngine` and
`EvidenceEngine` exactly as published, through their existing public
interfaces. No frozen component was modified to build it.

------------------------------------------------------------------------

# Component Status

  Component                    Status
  ---------------------------- ------------------------------------
  Dataset Engine               Stable
  Snapshot Engine               Stable
  Similarity Engine             Stable (RE-021 exception — see Frozen Core Policy)
  Observable Universe           Stable in operative flow (wired through DecisionEngine, RE-023.5; AssessmentEngine pending, RE-024.3)
  Evidence Engine                v1
  Assessment Engine              v1
  Inference Engine               Planned
  Constitution                   Planned
  Protocol Engine                Planned
  Dashboard                      Planned
  Research Validation Harness    v1 — harness + MAE + directional hit-rate + rank correlation + pinned runtime dependencies (RE-025.1-RE-025.5). Offline only, not wired into run.py.

**Note — naming collision, not a duplication of function.**
`ValidationEngine` (`engine/validation_engine.py`) and the Research
Validation Harness (`engine/validation_harness.py` +
`engine/validation_metrics.py`) are two unrelated components that
happen to share a name fragment:

-   `ValidationEngine` scores the *confidence* of a single, present-day
    decision (coverage/consistency/diversity/stability), and feeds
    `AssessmentEngine.confidence()` -- itself outside the operative
    flow (see Execution State).
-   The Research Validation Harness backtests the *historical accuracy*
    of the Similarity/Evidence pipeline itself, across all past
    episodes, offline. It does not compute confidence and is not
    consumed by `AssessmentEngine` or `DecisionEngine`.

Do not conflate the two when reading the codebase or this document.

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

## RE-025.1 — Research Validation Harness

`engine/validation_harness.py` introduces `ValidationHarness`. For
each historical episode it builds the forecast the system would have
produced by replaying, exactly, the same methodology `DecisionEngine`
uses for the present: `ObservableUniverse(dataset,
as_of=episode.bottom_date)` supplies temporally-safe comparables,
`SimilarityEngine.top()` selects matches, `EvidenceEngine.build()`
yields the forecast (`median_return`). Framed as "Research
Validation", not "statistical validation" — the sample is small and
episodes are not independent; see RE-025.2's disclaimer.

Two design constraints are load-bearing, not stylistic:

**Point-in-time, not global leave-one-out.** Comparables for episode
X are restricted to episodes observable as of X's own `bottom_date`.
Comparing X against all other 22 episodes regardless of chronology
would validate a hypothetical system that already knows 2020 while
evaluating 1962 — a different, easier system than the one that
actually runs. `ObservableUniverse` also masks each comparable's own
`future_return_Xy` per RE-023.3, so no comparable can leak a future
outcome that would not yet have been known either.

**Self-exclusion by `bottom_index`, not object identity.**
`ObservableUniverse.episodes()` returns `ObservableEpisode`, a type
deliberately distinct from `Episode` and never substitutable for it
(RE-023.1/ADR-004). Because of that, the episode under evaluation is
never the same object as its projection inside the universe —
`s.episode is not target_episode` would silently exclude nothing.
`bottom_index` is the one field that survives the `Episode ->
ObservableEpisode` projection unchanged and is unique per episode; it
is used as the exclusion key instead.

`sample_size()` (episodes with a real, realized `future_return_Xy`)
and `evaluated_count()` (episodes that additionally produced a
forecast) are computed methods, not asserted constants — the gap
between them is itself diagnostic. Verified against the live Shiller
dataset: 23 episodes total, `sample_size` = 21 (2022.10 and 2025.04
have no realized 5y return yet), `evaluated_count` = 19 (1877.06 and
1880.05 additionally had 0 and 1 comparable respectively in their own
instant, and produced no forecast).

Produces `ValidationRecord(episode, horizon_years, forecast, actual,
comparable_count, evaluable)` only. No aggregate statistic — that is
RE-025.2.

Naming risk, flagged deliberately: unrelated to the pre-existing
`engine/validation_engine.py` (`ValidationEngine`). See the note under
Component Status.

## RE-025.2 — MAE (canonical Research Validation metric)

`engine/validation_metrics.py` adds `mean_absolute_error()`: the mean
of `|forecast - actual|` over the `evaluable` records produced by
RE-025.1, in the same annualized-CAGR units as
`EvidenceEngine.median_return` — no unit conversion, no new
assumption. `None` if no record is evaluable, following the same
Research-Engine-wide rule as `Evidence` (RE-024.1): absence of
evidence is `None`, never `0.0`. Ships together with
`EXPLORATORY_DISCLAIMER`, a literal string callers must surface
alongside the number — this harness produces exploratory evidence
over a small, non-independent sample, not statistical validation in
the strict sense.

Measured against the live dataset: MAE = 7.03% over the 19 evaluated
episodes. Read with caution before treating it as a stable figure —
it is a mean over 19 points, and a single one (1932.06, bottom of the
Great Depression) contributes 18.91 points of error on its own, more
than double any other episode's. Hit-rate (RE-025.3) and rank
correlation (RE-025.4) are the intended check on whether 7.03% is
representative or driven by that outlier.

**Deviation resolved.** The first shipped version of
`mean_absolute_error()` filtered records with two explicit `is None`
checks on `forecast` and `actual`, instead of reading
`record.evaluable` — the flag RE-025.1 already computes for exactly
this purpose. The two criteria agreed on the live dataset, so no
measured result was ever wrong, but the function held its own,
duplicate notion of "is this record usable" and could have silently
diverged from `ValidationHarness` if `evaluable`'s definition ever
changed (e.g., a minimum `comparable_count`). Fixed: the loop now
reads `if not record.evaluable: continue`. Re-verified against the
live dataset after the fix — sample_size=21, evaluated_count=19,
MAE=7.03%, unchanged.

## RE-025.3 — Directional Hit Rate

`engine/validation_metrics.py` adds `directional_hit_rate()`: the
share of evaluable validation records where forecast and realized
return have the same sign. It uses `ValidationRecord.evaluable`,
like `mean_absolute_error()`, and excludes zero-valued forecast or
actual returns because zero does not express a direction.

Measured against the live dataset: directional hit-rate = 94.74%
(18/19). Supporting counts: 19 directional records, 19 positive
forecasts, 0 negative forecasts, 18 positive actuals, 1 negative
actual, 18 hits, 1 miss. MAE was rechecked in the same run and
remained unchanged at 7.03%.

Interpretation is deliberately constrained. This high hit-rate is
not evidence, by itself, that `SimilarityEngine` has meaningful
directional skill. In this sample, `EvidenceEngine.median_return`
never produced a negative forecast: 0/19 forecasts were negative.
The metric therefore mostly reflects the fact that 18/19 realized
5-year returns in the evaluated sample were positive. A naive rule
that always predicted "positive" would have produced almost the same
directional result. RE-025.3 is useful as a diagnostic check, not as
a strong validation claim.

This finding increases the importance of RE-025.4: rank correlation
is expected to be more informative here because it evaluates ordering
of forecast strength against realized outcomes, not just sign.

## RE-025.4 — Rank Correlation

`engine/validation_metrics.py` adds `rank_correlation()`: Spearman
rank correlation between forecast and realized return over evaluable
validation records. Unlike `directional_hit_rate()`, zero values are
not excluded: a zero is a valid value to rank, not an absence of
direction.

Ranks use average-rank tie handling. This is not cosmetic in the live
dataset: the 19 evaluable records contain only 7 unique forecast
values, because `EvidenceEngine.median_return()` can repeat when the
effective match set produces the same median. Average ranks avoid
letting input order decide ties silently.

Measured against the live dataset: rank_count=19,
unique_forecasts=7, unique_actuals=19, Spearman rank correlation =
-0.2290. MAE remained 7.03% and directional hit-rate remained
94.74% in the same verification run.

Interpretation remains exploratory. The negative value is a weak
negative rank relationship in this small, non-independent sample: in
this validation slice, higher forecast ranks did not correspond to
higher realized-return ranks. It should not be read as a formal
statistical rejection of the method, but it is materially more
informative than RE-025.3 because it tests ordering rather than
merely sign.

## RE-025.5 — Runtime reproducibility

`requirements.txt` is now a real dependency file, not an empty
directory. It pins the runtime libraries that materially affect
Research Validation calculations:

-   pandas==3.0.5
-   numpy==2.5.1
-   openpyxl==3.1.5

This is a methodological requirement, not project hygiene. RE-025.4
exposed that different pandas/numpy environments can produce
different validation records and therefore different aggregate
metrics. The canonical Research Validation numbers are the numbers
computed under the pinned runtime above:

-   MAE = 0.07025011023213769 (7.03%).
-   Directional hit-rate = 0.9473684210526315 (94.74%).
-   Rank correlation = -0.22902466816870654.
-   Unique forecast values among evaluable records = 7.

Earlier RE-025 documentation that reported MAE as 7.05% is superseded
by this pinned-runtime result. The difference is small in presentation
but important in principle: validation evidence is only reproducible
when the computational environment is reproducible.

This does not solve effective sample size. `n=19` remains an
operative count of evaluable records, not a claim that 19 independent
observations exist. Effective N is deferred to RE-025.6.

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

Research Validation (RE-025.x) runs alongside these phases as a
cross-cutting concern — it evaluates the accuracy of what Evidence
Engine already produces, rather than belonging to any single phase.
Not yet reflected as its own phase; revisit if the harness grows
enough to justify one.

Effective sample size remains pending. Until RE-025.6 defines it,
Research Validation metrics should keep treating `n=19` as an
operative count, not as an independent statistical sample.

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

## Version 1.7

-   Converted `requirements.txt` from an empty directory into a real
    dependency file and pinned the canonical runtime:
    pandas==3.0.5, numpy==2.5.1, openpyxl==3.1.5.
-   Added RE-025.5: runtime reproducibility for Research Validation.
-   Recorded that RE-025.4 exposed environment sensitivity: different
    pandas/numpy versions can produce different validation records and
    therefore different aggregate metrics.
-   Established the pinned-runtime canonical metrics: MAE=7.03%,
    directional hit-rate=94.74%, rank_correlation=-0.2290, and
    unique_forecasts=7.
-   Superseded previous 7.05% MAE references with the pinned-runtime
    value, 7.03%.
-   Deferred effective sample size to RE-025.6; `n=19` remains an
    operative count, not an independence claim.

## Version 1.6

-   Added `rank_correlation()` to `engine/validation_metrics.py`
    (RE-025.4): Spearman rank correlation between forecast and
    realized return over evaluable validation records.
-   Implemented average-rank tie handling because the live validation
    set has repeated forecasts: 19 evaluable records, 7 unique
    forecasts, 19 unique actuals.
-   Verified against the live dataset: rank_count=19,
    rank_correlation=-0.2290, MAE unchanged at 7.03%, directional
    hit-rate unchanged at 94.74%.
-   Documented the interpretation limit: the result is exploratory,
    weakly negative, and more informative than directional hit-rate
    for this sample, but not formal statistical validation.
-   Normalized Research Validation references to RE-025.1-RE-025.4
    now that the whole initial validation metric block is present.

## Version 1.5

-   Added `directional_hit_rate()` to `engine/validation_metrics.py`
    (RE-025.3): directional agreement between forecast and realized
    return over evaluable validation records, excluding zeros.
-   Verified against the live dataset: directional_count=19,
    forecast_positive=19, forecast_negative=0, actual_positive=18,
    actual_negative=1, hits=18, misses=1, hit-rate=94.74%.
-   Documented the key interpretation limit: because 0/19 forecasts
    were negative, the high hit-rate is not strong evidence of
    directional skill; it mostly reflects that almost all realized
    5-year returns in the evaluated sample were positive.
-   Rechecked MAE in the same validation run: unchanged at 7.03%.
-   Left RE-025.4 rank correlation as the next validation metric and
    the more informative follow-up for this sample.

## Version 1.4

-   Added `engine/validation_harness.py` (RE-025.1): Research
    Validation Harness, an offline, point-in-time backtest of the
    Similarity/Evidence pipeline against realized historical
    outcomes. Not wired into `run.py`. Verified against the live
    dataset: sample_size=21, evaluated_count=19 of 23 episodes.
-   Added `engine/validation_metrics.py` (RE-025.2): MAE as the
    canonical Research Validation metric, with a mandatory
    exploratory-evidence disclaimer. Measured MAE=7.03%, flagged as
    outlier-sensitive at this sample size (n=19).
-   Logged, then fixed within the same version, a duplication risk in
    the shipped MAE implementation: `mean_absolute_error()` now reads
    `ValidationRecord.evaluable` instead of recomputing the same
    criterion inline. Re-verified: MAE unchanged at 7.03%.
-   Clarified, in Component Status and Execution State, that the
    Research Validation Harness is unrelated to the pre-existing
    `ValidationEngine` (confidence scoring for `AssessmentEngine`)
    despite the naming collision.
-   Frozen Core Policy: recorded that RE-025.1/RE-025.2 invoke no
    exception — built entirely on existing public interfaces.

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
