# SOP ENGINE PROJECT STATUS

**Version:** 1.22\
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

# Documentation History Policy (RE-DOC-002)

The changelog preserves project history. It should record what was
known, claimed or shipped at the time of each version, not silently
rewrite past entries to match later knowledge.

When a later iteration supersedes a prior metric, interpretation or
claim, the correction should be documented forward in the new version
that discovered or authorized the change. Prior changelog entries may
only be edited when they contain a dangerous factual error that would
mislead current use of the system if left unqualified.

This policy follows from RE-025.5: earlier documentation had reported
MAE=7.05%, and the pinned runtime later established MAE=7.03% as the
canonical value. The correct governance pattern is to preserve the
fact that the value changed and explain why, not make the historical
path appear cleaner than it was.

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

# Execution State (as of RE-028.2)

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
  AssessmentEngine     Exists, compiles. Not called by run.py. As of
                        RE-024.3 it does use ObservableUniverse(as_of=
                        snapshot.date), so the older temporal-safety
                        concern is resolved. It still rebuilds the
                        Snapshot -> ObservableUniverse ->
                        SimilarityEngine.top() -> EvidenceEngine flow
                        locally instead of delegating to
                        build_research_result(), so the remaining issue
                        is source-of-truth duplication, not temporal
                        leakage. Also uses ValidationEngine for
                        confidence (coverage/consistency/diversity/
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
  ResearchEngine       Exists and executes a verified research pipeline
                        facade (RE-027.2-RE-027.5). It is not called by
                        run.py yet. Produces ResearchResult by delegating
                        to the shared build_research_result() pipeline,
                        the same source of truth consumed by
                        DecisionEngine.
  Research Validation  Exists (RE-025.1-RE-026.1.2), fully independent of
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

## Matches the diagram's named objects: ResearchEngine aligned

The architecture above names `ResearchEngine` producing a
`ResearchResult`. RE-027.1 verified that the prior object was stale and
dangerous to patch in isolation. RE-027.2-RE-027.4 rebuild and verify
that named object. RE-027.5 then removes the remaining duplication by
extracting the shared research pipeline into one source of truth:

    build_research_result(dataset)
        │
    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

Both `ResearchEngine` and `DecisionEngine` consume
`build_research_result()`. This resolves the RE-027.1 design risk: the
same research pipeline no longer exists as two independent
implementations that could drift apart.

Verified result from `tests/verify_research_engine.py` after RE-027.5:

-   `RESEARCH ENGINE : STABLE`
-   `snapshot_date: 2026.07`
-   `matches: 10`
-   `horizon_years: 5`
-   `median_return: 0.11386676352177`
-   `worst_return: -0.01091948933253`
-   `best_return: 0.13767334934864`
-   `return_count: 9`
-   `positive_count: 8`
-   `negative_count: 1`
-   `zero_count: 0`
-   `non_positive_probability: 0.11111111111111`
-   `return_spread: 0.14859283868117`

Remaining execution-state gap: `run.py` still calls `DecisionEngine`
directly. This no longer creates a duplicated research pipeline:
`DecisionEngine` and `ResearchEngine` share the same underlying
`build_research_result()` source of truth. Wiring the CLI entry point
through `ResearchEngine` remains a later integration choice, not an
unresolved defect in the RE-027 rebuild.

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

RE-025.1-RE-028.2 invoke no exception: the Research Validation
Harness consumes `ObservableUniverse`, `SimilarityEngine` and
`EvidenceEngine` exactly as published, through their existing public
interfaces. RE-027.1 is documentation-only audit work, and
RE-027.2-RE-027.5 rebuild `ResearchResult` / `ResearchEngine`, add
smoke tests, and extract the shared research pipeline around the same
published Snapshot, Observable Universe, Similarity and Evidence
surfaces. No frozen component was modified to build Research
Validation, to verify its canonical metrics, or to close the
`ResearchEngine` gap. RE-028.1 is documentation-only scope work for a
future Evidence Engine v2. RE-028.2 implements that Evidence v2 as an
additive Evidence-layer change, not a frozen Core modification.

------------------------------------------------------------------------

# Component Status

  Component                    Status
  ---------------------------- ------------------------------------
  Dataset Engine               Stable
  Snapshot Engine               Stable
  Similarity Engine             Stable (RE-021 exception — see Frozen Core Policy)
  Observable Universe           Stable in operative flow (wired through DecisionEngine, RE-023.5; AssessmentEngine wired in RE-024.3)
  Evidence Engine                v2 — additive descriptive sample-shape
                                  fields added in RE-028.2. Existing
                                  v1 fields and semantics preserved.
  Research Engine                v1 — rebuilt facade over the shared verified research pipeline (RE-027.2-RE-027.5). Produces ResearchResult. Smoke-tested. Not called by run.py yet.
  Assessment Engine              v1
  Inference Engine               Planned
  Constitution                   Planned
  Protocol Engine                Planned
  Dashboard                      Planned
  Research Validation Harness    v1 — harness + MAE + directional hit-rate + rank correlation + pinned runtime dependencies + effective-N caveat + overlapping outcome window diagnostic + repeated forecast diagnostic + synthesis + functional smoke test (RE-025.1-RE-026.1.2). Offline only, not wired into run.py.

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

RE-DOC-003 later corrected this historical description: RE-024.3 did
connect `AssessmentEngine` to `ObservableUniverse`. The current
remaining issue is that `AssessmentEngine` still duplicates the
research pipeline locally instead of delegating to the shared
`build_research_result()` source of truth introduced in RE-027.5.

## RE-023.6 — Responsibility correction in SimilarityEngine.top()

No behaviour change. The `peak_date < cutoff` filter cannot be split
into a "leakage" clause and a "RE-004 independence" clause — it is
one expression serving RE-004 alone, whose leakage-blocking effect is
an imprecise (peak_date, not bottom_date) side effect, kept
deliberately for callers that bypass ObservableUniverse. Comment
corrected to attribute temporal safety exclusively to
ObservableUniverse. RE-DOC-003 later verified that `AssessmentEngine`
no longer belongs to that bypassing-caller category after RE-024.3.

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
observations exist. Effective N is addressed conceptually in
RE-025.6, but not converted into a numeric correction yet.

## RE-025.6 — Effective sample size caveat

Research Validation now explicitly separates operational count from
independent evidence. The live validation set contains 19 evaluable
records, but `n=19` is only a count of records that produced both a
forecast and a realized 5-year return. It is not, by itself, a claim
that 19 statistically independent observations exist.

The first source of dependence is mechanical and outcome-side:
overlap between realized 5-year return windows. If two evaluated
episodes share part of their future 5-year window, part of their
`actual` return is literally measured over the same market interval.
That makes the two validation records less independent than two
non-overlapping observations, even if the forecast procedure is
otherwise point-in-time safe.

This 5-year-window overlap criterion is necessary, but not sufficient.
RE-025.4 exposed a second, forecast-side dependence channel: repeated
forecasts. The 19 evaluable records contain only 7 unique forecast
values. For example, 1998.09 and 2009.03 do not overlap in their
future 5-year realized-return windows, but both received the exact
same forecast value: 0.113866763522. That can happen when
`SimilarityEngine.top()` produces match sets whose median return is
effectively the same, and it means rows that look independent on the
outcome side can still share forecast structure.

RE-025.6 therefore does not publish a numeric effective N. It records
the methodological boundary: current Research Validation metrics are
exploratory diagnostics over 19 evaluable records, with known
dependence through at least two channels:

-   overlapping realized 5-year return windows;
-   repeated forecasts / potentially overlapping comparable sets.

Future work may quantify these channels separately. Until then,
MAE, directional hit-rate and rank correlation must not be described
as if they were computed over 19 independent observations.

## RE-025.7 — Core verification coverage for validation metrics

`tests/verify_core.py` now includes `engine/validation_metrics.py`
in its structural Engine checks.

This is not a functional test of MAE, directional hit-rate, rank
correlation or dependency diagnostics. `verify_core.py` only checks
that expected project paths exist. The purpose of RE-025.7 is narrower:
once `validation_metrics.py` became a real Research Validation module,
the core verification suite should at least recognize its existence.

Verified result: `python3 tests/verify_core.py` passes 6/6 checks and
reports `CORE STATUS : STABLE`.

## RE-025.8 — Overlapping outcome window diagnostic

`engine/validation_metrics.py` adds
`overlapping_outcome_windows(records)`: a diagnostic that returns
pairs of evaluable validation records whose realized 5-year outcome
windows overlap. It is a dependency diagnostic, not a new accuracy
metric.

The function deliberately returns pairs, not just a count, to preserve
explainability. It filters with `record.evaluable`, matching the
canonical Research Validation criterion used by MAE, directional
hit-rate and rank correlation. It does not change `ValidationHarness`
and does not alter any existing metric.

Window overlap is defined as:

    start_a < end_b and start_b < end_a

where:

    start = episode.bottom_date
    end = episode.bottom_date + horizon_years

The dataset stores dates as `YYYY.MM`, where `.01` through `.12`
represent months, not year fractions. For this diagnostic, comparing
dates and adding an integer 5-year horizon are valid operations:
`1932.06 + 5 == 1937.06`. Direct subtraction of these floats is not
valid for duration or ratio calculations: `1933.01 - 1932.12` would
produce `0.89`, not one month. RE-025.8 therefore publishes no overlap
duration and no overlap ratio.

Measured against the live dataset: 23 episodes, sample_size=21,
evaluated_count=19, overlap_pairs=10. The overlapping pairs are:

-   1903.10 / 1907.11
-   1957.12 / 1960.10
-   1957.12 / 1962.06
-   1960.10 / 1962.06
-   1962.06 / 1966.10
-   1966.10 / 1970.06
-   1970.06 / 1974.12
-   1987.12 / 1990.10
-   1998.09 / 2003.02
-   2018.12 / 2020.03

This strengthens the RE-025.6 conclusion: `n=19` is an operative
count, not an independent sample-size claim. RE-025.8 still does not
publish a numeric effective N. It only makes one known dependence
channel directly observable.

## RE-025.9 — Repeated forecast group diagnostic

`engine/validation_metrics.py` adds
`repeated_forecast_groups(records)`: a diagnostic that groups
evaluable validation records sharing the exact same forecast value.
It returns only groups with more than one record.

This is a forecast-side dependency diagnostic, not a new accuracy
metric and not a proof that the underlying comparable sets are
identical. `ValidationRecord` stores `comparable_count`, but not the
actual matched episodes selected by `SimilarityEngine.top()`. RE-025.9
therefore makes repeated forecasts observable without claiming to
measure comparable-set overlap directly.

Measured against the live dataset: 23 episodes, sample_size=21,
evaluated_count=19, unique_forecasts=7,
repeated_forecast_groups=4, records_in_repeated_groups=16.

The repeated forecast groups are:

-   0.090162141571: 1982.07 / 1987.12 / 2018.12 (3 records)
-   0.113866763522: 1990.10 / 1998.09 / 2009.03 / 2020.03 (4 records)
-   0.127427505966: 1921.08 / 1932.06 / 1970.06 / 1974.12 (4 records)
-   0.158567951617: 1903.10 / 1907.11 / 1957.12 / 1960.10 / 1962.06 (5 records)

This materially strengthens the RE-025.6 caveat. Of 19 evaluable
records, 16 fall into repeated forecast groups. Only 3 records have a
forecast value that is unique within the evaluated sample. This does
not invalidate MAE, directional hit-rate or rank correlation, but it
does mean those diagnostics must not be read as if each row carried a
fully independent forecast signal.

## RE-025.10 — Research Validation synthesis

RE-025.1 through RE-025.9 establish Research Validation as a coherent
offline diagnostic layer for the Similarity/Evidence pipeline. It is
point-in-time, uses the same public interfaces as the operative
DecisionEngine flow, computes canonical exploratory metrics, pins the
runtime that makes those metrics reproducible, and documents the main
known dependence channels in the evaluated sample.

The current canonical validation surface is:

-   sample_size = 21;
-   evaluated_count = 19;
-   MAE = 0.07025011023213769 (7.03%) under pinned runtime;
-   directional_hit_rate = 0.9473684210526315 (94.74%);
-   rank_correlation = -0.22902466816870654;
-   overlap_pairs = 10 realized 5-year window overlaps;
-   repeated_forecast_groups = 4;
-   records_in_repeated_forecast_groups = 16/19.

The interpretation is intentionally bounded. These numbers are useful
evidence about how the current Research Engine behaves, but they are
not strong statistical validation. The high directional hit-rate is
not very discriminating because 0/19 forecasts were negative. Rank
correlation is more informative than hit-rate but remains exploratory.
MAE is outlier-sensitive at this sample size. Most importantly, `n=19`
is an operative count, not an independent sample-size claim.

RE-025.8 and RE-025.9 make the independence caveat concrete:

-   outcome-side dependence is observable through 10 overlapping
    realized 5-year windows;
-   forecast-side dependence is observable because 16/19 evaluable
    records share a forecast value with at least one other record.

No numeric effective N is published. That is deliberate. The system now
knows enough to avoid overstating its evidence, but not enough to
compress the dependence structure into a defensible single adjusted
sample-size number. Future work may quantify effective N, comparable
set overlap, or other dependence structures, but RE-025 closes the
current block as exploratory validation with explicit limitations.

## RE-026.1 — Research Validation metrics functional smoke test

`tests/verify_validation_metrics.py` adds a functional smoke test for
the canonical Research Validation surface established by RE-025. It is
not a replacement for the offline harness; it is a regression guard
around the values that the harness and metrics now publish.

The test verifies:

-   episodes = 23;
-   sample_size = 21;
-   evaluated_count = 19;
-   MAE = 0.07025011023213769;
-   directional_hit_rate = 0.9473684210526315;
-   rank_correlation = -0.22902466816870654;
-   overlap_pairs = 10;
-   repeated_forecast_groups = 4.

RE-026.1.1 made the test executable directly from `tests/` by adding
the repository root to `sys.path` before importing `engine.*` modules.

RE-026.1.2 added a runtime gate before metric assertions. The test now
reads `requirements.txt`, compares the pinned package versions against
the active Python environment, and refuses to verify canonical metrics
outside the pinned runtime. This is deliberate: RE-025.5 showed that
different pandas/numpy versions can change validation outputs. A
runtime mismatch must therefore fail as an environment problem, not as
an ambiguous metric regression.

Verified result:

-   `RUNTIME : PINNED`
-   `RESEARCH VALIDATION METRICS : STABLE`

## RE-027.1 — ResearchEngine audit and rebuild decision

RE-027.1 audits `engine/research_engine.py` against the operative flow
that has actually been verified through `DecisionEngine` and Research
Validation.

The current `ResearchEngine` is not a partially working engine. It is
a stale architectural placeholder whose constructor and runtime logic
no longer match the rest of the repository:

-   `SnapshotEngine()` is instantiated without `dataset`;
-   `ExplanationEngine()` is instantiated without `matches`;
-   `AssessmentEngine()` is instantiated without `dataset`;
-   `SnapshotEngine.build(dataset)` is called even though no such
    method exists;
-   `SimilarityEngine` is built directly from `dataset`, bypassing
    `ObservableUniverse`;
-   `SimilarityEngine.compare(snapshot)` is used instead of
    `SimilarityEngine.top(snapshot, n=10)`;
-   evidence would therefore be built from all compared episodes, not
    only from the selected nearest matches, if the constructor errors
    were patched in isolation;
-   `ExplanationEngine` remains broken if called;
-   the method returns a plain dictionary instead of a `ResearchResult`.

The dangerous failure mode is not only that the current object crashes.
If its constructor errors were fixed without correcting the pipeline
contract, it could run while producing evidence from the wrong sample.
That would be worse than an explicit exception, because the system
would appear operational while silently mixing irrelevant historical
episodes into the evidence layer.

Design decision: the rebuilt `ResearchEngine` must be a thin facade
over the pipeline already verified through `DecisionEngine`:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

It must not become a second independent implementation of the same
pipeline. A duplicated pipeline would create another place where
architecture and execution can drift apart.

Completed rebuild sequence:

1.  RE-027.2 — redefine `models/research_result.py` so it represents
    the real Research output.
2.  RE-027.3 — rebuild `engine/research_engine.py` around the verified
    operative pipeline.
3.  RE-027.4 — add a functional smoke test for the rebuilt
    `ResearchEngine`.

## RE-027.2 — ResearchResult aligned with operative Research output

RE-027.2 updates `models/research_result.py` so `ResearchResult`
represents the objective Research output now produced by the verified
pipeline.

`ResearchResult` contains:

-   `snapshot`;
-   selected `matches`;
-   resulting `evidence`.

It deliberately does not contain recommendations, portfolio decisions,
assessment confidence or explanations. Those belong to downstream
decision / explanation responsibilities, not to the objective Research
result.

This keeps `ResearchResult` aligned with the Evidence Layer that has
already been validated through RE-025.x and RE-026.x.

## RE-027.3 — ResearchEngine rebuilt as operative pipeline facade

RE-027.3 rebuilds `engine/research_engine.py` as a thin facade over the
same operative research flow already verified through `DecisionEngine`:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

The rebuilt engine removes the stale constructor state that previously
instantiated engines with invalid arguments. It also removes the
dangerous `SimilarityEngine.compare()` path, which would have built
evidence from all compared episodes rather than the selected nearest
matches.

Design boundary: `ResearchEngine` is a Research facade only. It does
not call `ExplanationEngine`, `AssessmentEngine` or
`ProbabilityEngine`.

RE-027.3 did not yet eliminate all architecture risk: it still
contained its own copy of the same orchestration later consumed by
`DecisionEngine`. RE-027.5 supersedes that implementation detail by
extracting the shared pipeline into `engine/research_pipeline.py`.

## RE-027.4 — ResearchEngine functional smoke test

RE-027.4 adds `tests/verify_research_engine.py`.

The test verifies that the rebuilt `ResearchEngine` executes the
expected research pipeline and returns a stable `ResearchResult`
surface.

Verified result:

-   `RESEARCH ENGINE : STABLE`
-   `snapshot_date: 2026.07`
-   `matches: 10`
-   `horizon_years: 5`
-   `median_return: 0.11386676352177`
-   `worst_return: -0.01091948933253`
-   `best_return: 0.13767334934864`

This verified that `ResearchEngine` worked, but did not by itself close
the single-source-of-truth concern raised in RE-027.1. RE-027.5 closes
that remaining gap.

## RE-027.5 — Shared Research pipeline source of truth

RE-027.5 adds `engine/research_pipeline.py` with
`build_research_result()`.

This function is now the single source of truth for the objective
Research pipeline:

    SnapshotEngine
        │
    ObservableUniverse
        │
    SimilarityEngine.top()
        │
    EvidenceEngine
        │
    ResearchResult

Both `DecisionEngine` and `ResearchEngine` delegate to this shared
function. This resolves the contradiction identified after RE-027.4:
`ResearchEngine` was described as a facade, but the code still
reimplemented the same orchestration in a second location.

After RE-027.5, future changes to the objective Research pipeline have
one implementation point, not two.

Verified:

-   `engine/research_pipeline.py`, `engine/research_engine.py` and
    `engine/decision_engine.py` compile.
-   `tests/verify_research_engine.py` remains stable.
-   `tests/verify_validation_metrics.py` remains stable.
-   `DecisionEngine` keeps the existing public evidence surface while
    consuming the shared Research pipeline internally.

## RE-DOC-003 — AssessmentEngine status correction

RE-DOC-003 corrects the project status document after verifying
`engine/assessment_engine.py` directly.

Earlier status text continued to say that `AssessmentEngine` built
`SimilarityEngine` directly from `dataset.episodes` and was never
connected to `ObservableUniverse`. That was no longer true: RE-024.3
already changed `AssessmentEngine` to build:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)

Corrected interpretation:

-   The temporal-safety concern is resolved for `AssessmentEngine`.
-   `AssessmentEngine` remains outside `run.py`.
-   `AssessmentEngine` still duplicates the Research pipeline locally
    instead of consuming `build_research_result()`.
-   The remaining issue is maintainability / source-of-truth drift, not
    temporal leakage.

This correction is documentation-only. No code changed.

## RE-028.1 — Evidence Engine v2 scope audit

RE-028.1 scopes Evidence Engine v2 before code changes.

Current verified Evidence contract:

-   `EvidenceEngine.build(matches, years=5)` consumes selected
    similarity matches and returns a descriptive `Evidence` object.
-   `Evidence` stores the historical sample (`matches`,
    `episodes_count`, `horizon_years`), return statistics
    (`average_return`, `median_return`, `worst_return`,
    `best_return`, `positive_probability`), recovery statistics and
    `percentile(p)`.
-   Absence of evidence is represented by `None`, never `0.0`.
-   `percentile(p)`, `median_return`, `worst_return` and `best_return`
    share the same percentile rule through `percentile_from_sorted()`.

Current verified consumers:

-   `build_research_result()` consumes `EvidenceEngine` as the shared
    source of truth for `DecisionEngine` and `ResearchEngine`.
-   `AssessmentEngine` still consumes `EvidenceEngine` separately
    until it is migrated to `build_research_result()`.
-   `ValidationHarness` consumes `EvidenceEngine.median_return` as the
    canonical forecast in offline Research Validation.

RE-028 v2 must therefore be additive and backwards-compatible:

-   Existing public fields must keep their names and semantics.
-   Existing consumers must continue to work without code changes.
-   New fields should describe the evidence sample more explicitly;
    they must not encode recommendations, portfolio decisions or
    assessment/confidence.
-   `EvidenceEngine` may compute richer descriptive diagnostics, but
    interpretation of those diagnostics belongs to Assessment / SOP
    governance, not to Evidence.

Candidate v2 additions are sample-shape and explainability fields such
as return count, positive/negative counts, dispersion, downside/upside
distribution markers or explicit sample coverage. Final field selection
is deliberately deferred to RE-028.2 after this contract boundary.

Out of scope for RE-028.1:

-   no change to `models/evidence.py`;
-   no change to `engine/evidence_engine.py`;
-   no AssessmentEngine migration;
-   no SimilarityEngine v2 work;
-   no new portfolio or recommendation logic.

This is a scope gate, not an implementation iteration.

## RE-028.2 — Evidence Engine v2 descriptive sample shape

RE-028.2 implements the first Evidence Engine v2 surface as an
additive, backwards-compatible extension.

`models/evidence.py` adds descriptive sample-shape fields:

-   `return_count`
-   `positive_count`
-   `negative_count`
-   `zero_count`
-   `non_positive_probability`
-   `return_spread`

`engine/evidence_engine.py` computes those fields from the same
horizon-specific return sample already used for
`average_return`, `median_return`, `worst_return`, `best_return` and
`positive_probability`.

Compatibility rule:

-   existing Evidence fields keep their names and semantics;
-   the new fields have defaults, so older direct `Evidence(...)`
    construction remains compatible;
-   absence of evidence still uses `None` for probability/spread fields
    where a numeric value would imply observed data.

Interpretation boundary:

-   Evidence describes the historical sample;
-   Evidence does not score confidence;
-   Evidence does not recommend portfolio action;
-   Evidence does not decide whether the SOP should deploy, hold or
    block capital.

Verified result from `tests/verify_research_engine.py` after RE-028.2:

-   `RESEARCH ENGINE : STABLE`
-   `matches: 10`
-   `return_count: 9`
-   `positive_count: 8`
-   `negative_count: 1`
-   `zero_count: 0`
-   `non_positive_probability: 0.11111111111111`
-   `return_spread: 0.14859283868117`

The distinction between `episodes_count=10` and `return_count=9` is
intentional: the selected historical sample can contain matches that do
not yet have a realized return at the requested horizon. Evidence v2
makes that sample coverage visible without turning it into an
assessment score.

## RE-028.3 — Evidence percentile field gate

RE-028.3 decides not to add new named percentile fields yet.

Current verified behavior:

-   `Evidence.percentile(p)` already exposes arbitrary downside/upside
    return percentiles on demand.
-   `median_return`, `worst_return`, `best_return` and
    `percentile(p)` share the same `percentile_from_sorted()` rule.
-   Evidence v2 already describes the current sample shape through
    return_count, positive/negative/zero counts,
    non_positive_probability and return_spread.

Design decision:

-   Explicit named percentile fields such as p10/p25/p75/p90 are
    deferred until Assessment or SOP governance defines why those exact
    thresholds are needed.
-   Evidence must not make arbitrary interpretive cutoffs look
    canonical just because they were convenient to compute.
-   Until a protocol needs named thresholds, `percentile(p)` remains
    the correct descriptive interface.

Boundary:

-   Evidence can describe a distribution.
-   Evidence must not decide which percentile is "defensive",
    "aggressive", "safe" or "actionable".
-   Those labels belong to Assessment / SOP governance, not to
    EvidenceEngine.

This is documentation-only scope control. No code changed.

## RE-028.4 — Evidence Engine v2 closure gate

RE-028.4 closes the current Evidence Engine v2 block.

Verified Evidence v2 surface:

-   existing return statistics remain unchanged;
-   `return_count` makes realized sample coverage explicit;
-   positive / negative / zero counts describe the sign distribution;
-   `non_positive_probability` describes observed downside frequency;
-   `return_spread` describes observed return range;
-   `percentile(p)` remains available for arbitrary distribution
    inspection without promoting any threshold to canonical status.

Closure decision:

-   No additional Evidence fields are added in this block.
-   Evidence v2 is now descriptive enough for the next layer to consume.
-   Further interpretation belongs to Assessment / SOP governance:
    capital tranches, dry-powder deployment, invalidation flags and
    confidence language must be defined outside Evidence.

Known boundary after RE-028.4:

-   Evidence can say what happened in comparable historical episodes.
-   Evidence can expose sample coverage, sign mix, downside frequency,
    spread and arbitrary percentiles.
-   Evidence cannot say whether to deploy capital, how much to deploy,
    whether evidence is sufficient, or whether a SOP protocol should
    be activated.

This closes Evidence Engine v2 for the current architecture pass.

------------------------------------------------------------------------

# Roadmap

## Pre-Phase Gate

Closed as of RE-027.5.

`ResearchEngine` now exists as a rebuilt, smoke-tested facade over the
shared verified research pipeline. It produces `ResearchResult` from
snapshot, observable universe, selected similarity matches and
evidence. `DecisionEngine` consumes the same shared pipeline, so there
is no second independent implementation of the objective Research
flow.

Evidence Engine v2 or Similarity Engine v2 work can now proceed
without being blocked by a stale named architecture object.

## Phase 1

Evidence Engine v2 — closed for the current architecture pass
(RE-028.1-RE-028.4). Evidence now exposes a stable descriptive surface.
Interpretation moves to Assessment / SOP governance.

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

Effective sample size is documented conceptually in RE-025.6. One
outcome-side dependence channel is observable through RE-025.8, and
one forecast-side dependence channel is observable through RE-025.9.
RE-025.10 closes the current Research Validation block as exploratory
validation with explicit limitations. No numeric effective-N correction
exists yet; Research Validation metrics should keep treating `n=19` as
an operative count, not as an independent statistical sample.

RE-026.1 adds a functional smoke test for that canonical Research
Validation surface. It first verifies the pinned runtime from
`requirements.txt`, then verifies the canonical RE-025 metrics and
dependency diagnostics.

RE-027.1 audited the gap between the documented `ResearchEngine`
object and the operative pipeline already verified through
`DecisionEngine`. RE-027.2-RE-027.4 align `ResearchResult`, rebuild
`ResearchEngine` as a thin facade, and add a functional smoke test.
RE-027.5 then closes the remaining architecture risk by extracting
the shared `build_research_result()` pipeline consumed by both
`DecisionEngine` and `ResearchEngine`.

RE-DOC-003 corrects the status of `AssessmentEngine`: code inspection
confirms that RE-024.3 already connected it to `ObservableUniverse`.
The remaining `AssessmentEngine` issue is duplication of the Research
pipeline, not temporal-safety leakage.

RE-028.1 opens Evidence Engine v2 with a scope audit only. The current
Evidence contract is stable and already consumed by the shared Research
pipeline, the offline Research Validation harness and `AssessmentEngine`.
Evidence v2 must therefore be additive: richer objective description of
the evidence sample, without changing existing fields or moving
assessment/recommendation logic into Evidence.

RE-028.2 implements the first additive Evidence v2 fields:
return_count, positive_count, negative_count, zero_count,
non_positive_probability and return_spread. These fields make the
shape of the realized return sample observable while preserving the
Evidence boundary: description only, no confidence score, no portfolio
recommendation and no SOP action.

RE-028.3 closes the next Evidence v2 scope question without adding
code: named percentile fields are deferred. `Evidence.percentile(p)`
already provides the descriptive surface; fixed percentile names should
only be added after Assessment / SOP governance defines the thresholds
it actually needs.

RE-028.4 closes Evidence Engine v2 for the current architecture pass:
the Evidence layer now has enough objective descriptive shape for the
next layer to consume. Remaining questions are interpretive and belong
to Assessment / SOP governance, not Evidence.

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

## Version 1.22

-   Added RE-028.4: Evidence Engine v2 closure gate.
-   Declared Evidence v2 closed for the current architecture pass.
-   Confirmed that no additional Evidence fields are added now.
-   Moved remaining interpretive work to Assessment / SOP governance:
    capital tranches, dry-powder deployment, invalidation flags and
    confidence language.
-   Updated Phase 1 roadmap status: Evidence Engine v2 closed for the
    current pass.
-   No code changed.

## Version 1.21

-   Added RE-028.3: Evidence percentile field gate.
-   Confirmed that `Evidence.percentile(p)` remains the active
    descriptive interface for arbitrary distribution markers.
-   Deferred named percentile fields such as p10/p25/p75/p90 until
    Assessment / SOP governance defines their interpretation.
-   Reaffirmed the Evidence boundary: describe distributions, do not
    label them as actionable.
-   No code changed.

## Version 1.20

-   Added RE-028.2: Evidence Engine v2 descriptive sample-shape fields.
-   Extended `models/evidence.py` with additive, defaulted fields:
    return_count, positive_count, negative_count, zero_count,
    non_positive_probability and return_spread.
-   Updated `engine/evidence_engine.py` to compute those fields from
    the same horizon-specific return sample already used by the
    existing return statistics.
-   Updated `tests/verify_research_engine.py` to verify the new
    Evidence v2 surface. Live result: matches=10, return_count=9,
    positive_count=8, negative_count=1, zero_count=0,
    non_positive_probability=0.11111111111111,
    return_spread=0.14859283868117.
-   Reaffirmed the boundary: Evidence describes; Assessment / SOP
    interprets.

## Version 1.19

-   Added RE-028.1: Evidence Engine v2 scope audit before code changes.
-   Documented the current verified Evidence contract and consumers.
-   Established the RE-028 boundary: v2 must be additive and
    backwards-compatible because `EvidenceEngine` is consumed by the
    shared Research pipeline, Research Validation and `AssessmentEngine`.
-   Explicitly excluded recommendations, portfolio decisions and
    confidence/assessment logic from Evidence v2.
-   No code changed.

## Version 1.18

-   Added RE-DOC-003: corrected stale `AssessmentEngine` documentation
    after direct code inspection.
-   Replaced the outdated claim that `AssessmentEngine` was never
    connected to `ObservableUniverse`.
-   Documented that RE-024.3 already made `AssessmentEngine` consume
    `ObservableUniverse(dataset, as_of=snapshot.date)`.
-   Clarified the current issue: `AssessmentEngine` still duplicates
    the Research pipeline locally instead of delegating to
    `build_research_result()`, so the risk is source-of-truth drift, not
    temporal leakage.
-   No code changed.

## Version 1.17

-   Added RE-027.5: extracted `engine/research_pipeline.py` as the
    shared source of truth for the objective Research pipeline.
-   Updated `DecisionEngine` and `ResearchEngine` so both delegate to
    `build_research_result()` instead of maintaining parallel copies of
    Snapshot -> ObservableUniverse -> SimilarityEngine.top() ->
    EvidenceEngine orchestration.
-   Clarified that RE-027.4 verified the rebuilt `ResearchEngine`, but
    RE-027.5 is the iteration that closes the single-source-of-truth
    concern raised in RE-027.1.
-   Confirmed that `run.py` may continue calling `DecisionEngine`
    without duplicating Research pipeline logic, because `DecisionEngine`
    now consumes the same shared pipeline as `ResearchEngine`.
-   Closed the RE-027 Pre-Phase Gate as of RE-027.5.

## Version 1.16

-   Added RE-027.2: `ResearchResult` now represents the objective
    Research output -- snapshot, selected matches and evidence.
-   Added RE-027.3: rebuilt `ResearchEngine` as a thin facade over the
    verified Snapshot -> ObservableUniverse -> SimilarityEngine.top()
    -> EvidenceEngine pipeline.
-   Removed the stale `ResearchEngine` path that instantiated engines
    with invalid constructor arguments and could have used
    `SimilarityEngine.compare()` instead of selected top matches.
-   Added RE-027.4: functional smoke test for the rebuilt
    `ResearchEngine`.
-   Closed the RE-027 Pre-Phase Gate: Evidence Engine v2 and
    Similarity Engine v2 are no longer blocked by the stale named
    ResearchEngine object.
-   Documented the remaining integration boundary: `run.py` still calls
    `DecisionEngine` directly; wiring the CLI entry point through
    `ResearchEngine` remains a future choice.

## Version 1.15

-   Added RE-027.1: audit of the current `ResearchEngine` against the
    verified operative pipeline.
-   Documented that `ResearchEngine.__init__()` currently has three
    independent constructor mismatches: `SnapshotEngine`,
    `ExplanationEngine` and `AssessmentEngine`.
-   Documented that `ResearchEngine.run()` would use
    `SimilarityEngine.compare()` rather than `.top()`, creating a
    silent evidence-sample risk if constructor errors were patched in
    isolation.
-   Established the rebuild decision: `ResearchEngine` must become a
    thin facade over the already verified `DecisionEngine` pipeline,
    not a second independent implementation.
-   Added a Pre-Phase Gate: close the `ResearchEngine` rebuild before
    starting Evidence Engine v2 or Similarity Engine v2 work.

## Version 1.14

-   Added RE-026.1: functional smoke test for the canonical Research
    Validation metrics and diagnostics.
-   Documented RE-026.1.1: the test is executable directly from
    `tests/`.
-   Documented RE-026.1.2: the test verifies the pinned runtime before
    comparing canonical metric values, so environment mismatches fail
    as environment errors rather than ambiguous metric regressions.
-   Verified result: `RUNTIME : PINNED` and
    `RESEARCH VALIDATION METRICS : STABLE`.

## Version 1.13

-   Added RE-025.10: Research Validation synthesis.
-   Consolidated the interpretation of RE-025.6, RE-025.8 and
    RE-025.9 into one closing statement: `n=19` is an operative count,
    not an independent sample-size claim.
-   Summarized the current canonical Research Validation surface:
    sample_size=21, evaluated_count=19, MAE=7.03%, directional
    hit-rate=94.74%, rank_correlation=-0.2290, overlap_pairs=10,
    repeated_forecast_groups=4, and 16/19 records in repeated forecast
    groups.
-   Closed the current RE-025 block as exploratory validation with
    explicit limitations, without publishing a numeric effective N.

## Version 1.12

-   Added RE-025.9: repeated forecast group diagnostic.
-   Added `repeated_forecast_groups(records)` to
    `engine/validation_metrics.py`, grouping evaluable records by exact
    repeated forecast value.
-   Verified against the live dataset: 23 episodes, sample_size=21,
    evaluated_count=19, unique_forecasts=7,
    repeated_forecast_groups=4, records_in_repeated_groups=16.
-   Documented the four repeated forecast groups and clarified that
    this is a forecast-side dependency diagnostic, not proof of
    identical comparable sets.
-   Reaffirmed that no numeric effective N is published yet.

## Version 1.11

-   Added missing RE-025.7 documentation: `tests/verify_core.py` now
    includes `engine/validation_metrics.py` in the structural Engine
    checks.
-   Applied RE-DOC-002 to this document's own changelog: restored the
    historical v1.4, v1.5 and v1.6 MAE references to 7.05%, the value
    documented at the time.
-   Left RE-025.5 as the forward correction that supersedes those
    historical values with the pinned-runtime canonical MAE=7.03%.

## Version 1.10

-   Added RE-025.8: overlapping outcome window diagnostic.
-   Added `overlapping_outcome_windows(records)` to
    `engine/validation_metrics.py`, returning pairs of evaluable
    records whose realized 5-year outcome windows overlap.
-   Verified against the live dataset: 23 episodes, sample_size=21,
    evaluated_count=19, overlap_pairs=10.
-   Documented the `YYYY.MM` date constraint: comparisons and adding
    an integer 5-year horizon are valid for boolean overlap detection;
    direct subtraction is not valid for durations or ratios.
-   Reaffirmed that no numeric effective N is published yet.

## Version 1.9

-   Added RE-DOC-002: documentation history policy.
-   Established that changelog entries preserve historical project
    state; corrections should be documented forward in the version
    that discovers or authorizes them.
-   Recorded the RE-025.5 MAE correction as the motivating example:
    previous documentation reported 7.05%, while the pinned runtime
    established 7.03% as canonical.

## Version 1.8

-   Added RE-025.6: effective sample size caveat for Research
    Validation.
-   Documented that `n=19` is an operative count of evaluable records,
    not an independent sample-size claim.
-   Identified overlapping realized 5-year return windows as the
    first mechanical source of dependence.
-   Recorded a second, forecast-side dependence channel: repeated
    forecasts / potentially overlapping comparable sets. Live dataset
    currently has 19 evaluable records but only 7 unique forecast
    values; 1998.09 and 2009.03 share forecast=0.113866763522 despite
    non-overlapping future 5-year windows.
-   Kept RE-025.6 conceptual only: no numeric effective-N correction
    is published yet.

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
    rank_correlation=-0.2290, MAE unchanged at 7.05%, directional
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
-   Rechecked MAE in the same validation run: unchanged at 7.05%.
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
    exploratory-evidence disclaimer. Measured MAE=7.05%, flagged as
    outlier-sensitive at this sample size (n=19).
-   Logged, then fixed within the same version, a duplication risk in
    the shipped MAE implementation: `mean_absolute_error()` now reads
    `ValidationRecord.evaluable` instead of recomputing the same
    criterion inline. Re-verified: MAE unchanged at 7.05%.
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
