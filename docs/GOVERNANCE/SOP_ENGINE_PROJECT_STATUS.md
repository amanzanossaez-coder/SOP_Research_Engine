# SOP ENGINE PROJECT STATUS

**Version:** 1.41\
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

# Execution State (as of RE-PRED.2)

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
                        RE-029.3 it consumes build_research_result(),
                        the same shared Research pipeline used by
                        DecisionEngine and ResearchEngine. RE-029.4
                        verifies its public helper outputs after that
                        refactor. The temporal-safety and research
                        source-of-truth duplication concerns are
                        resolved. Confidence remains a separate
                        ValidationEngine path
                        (coverage/consistency/diversity/stability, with
                        stability hardcoded to 1.0). RE-029.5 defines
                        any future evidence-quality link to capital
                        posture as a gate / ceiling, not a weighted
                        input, and explicitly excludes the current
                        confidence score from SOP capital gates while
                        stability remains hardcoded. RE-029.6 defines
                        the initial Evidence Quality Gate dimensions and
                        records that the gate starts conservative because
                        current Research Validation does not yet show
                        reliable discriminatory power. RE-029.7 defines
                        the calibration boundary: any relaxation from
                        conservative must be pre-registered, discrete
                        and evidence-led, never inferred from the
                        aggregate confidence score. RE-029.8 defines
                        the first future implementation scope: a
                        separate EvidenceQualityGate structure, with
                        local snapshot inputs separated from global
                        model-validation state, and not wired into
                        run.py or DecisionEngine. RE-029.9 defines the
                        acceptance criteria for that first future code
                        change. RE-030.1 adds the isolated
                        EvidenceQualityGate module and verification
                        test, still outside the operative flow. RE-030.2
                        adds a local Evidence -> LocalEvidenceQualityInputs
                        adapter, also outside the operative flow.
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
  EvidenceQualityGate  Exists as an isolated structure (RE-030.1). Not
                        called by run.py. Not called by DecisionEngine.
                        Not called by AssessmentEngine. Does not consume
                        AssessmentEngine.confidence().score. Separates
                        local snapshot inputs from global model-validation
                        state. RE-030.2 adds
                        build_local_evidence_quality_inputs(evidence),
                        using Evidence as the single source of truth for
                        the selected match set. Defaults fail-closed:
                        today's real local inputs plus non-validated
                        global state produce `not measurable`; fully
                        measured but not yet authorized inputs produce
                        `conservative`.
  Regime Comparability Gate
                        Planned / documented boundary only (RE-031.1).
                        No code exists. Not called by run.py,
                        DecisionEngine, AssessmentEngine or
                        EvidenceQualityGate. Intended to cap capital
                        posture when today's market regime is not
                        structurally comparable to the historical
                        evidence being used.
  Personal Capacity     Planned / classification boundary only
  Boundary              (RE-032.1). No code exists. Not called by run.py,
                        DecisionEngine, AssessmentEngine or any gate.
                        RE-032.1 does not assume this becomes a parallel
                        computable gate; it classifies whether Personal
                        Capacity belongs as a gate, human approval
                        requirement or mixed control.
  Capital Posture       Vocabulary documented only (RE-033.1). No code
                        exists. No posture engine exists. No gate
                        combination logic exists. RE-033.1 defines the
                        ordered posture vocabulary that future gates may
                        cap. RE-034.1 documents the combination boundary:
                        `Blocked` first, then the most restrictive
                        posture ceiling, with Evidence Quality not
                        measurable treated differently from unavailable
                        Regime Comparability / Personal Capacity.
                        RE-034.2 defines first-code acceptance criteria
                        for that future combination layer. RE-034.3
                        adds the isolated gate-combination module and
                        verification test. RE-034.4 documents that it
                        exists and passes verification, but remains
                        outside the operative flow. RE-PRED.1 opens the
                        predictive-validity boundary: no new validation
                        claim is made until target, model freeze,
                        baselines, holdout policy and live-tracking
                        protocol are defined. RE-PRED.2 audits the
                        current predictive target implemented by code.
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
  Predictive Validity  Boundary opened in RE-PRED.1. Documentation
  Boundary              only. No code. No new calculation. No validation
                        claim. Defines what future predictive validation
                        must specify before any holdout, live tracking
                        or gate relaxation can be treated as evidence.
                        RE-PRED.2 audits the current target: annualized
                        5-year real return CAGR from `Price.1`, used as
                        both Evidence forecast surface and Research
                        Validation actual.

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

RE-025.1-RE-026.1.2 invoke no exception: the Research Validation
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
RE-029.1 and RE-029.2 are documentation-only Assessment / SOP
governance scope audits. RE-029.3 refactors `AssessmentEngine` to
consume the shared Research pipeline without modifying frozen Core
components. RE-029.4 adds verification for the public Assessment helper
surface. RE-029.5, RE-029.6, RE-029.7, RE-029.8 and RE-029.9 are
documentation-only governance iterations: no frozen component changes
are invoked. RE-030.1 adds a new isolated gate module and focused test,
without modifying Frozen Core or operative wiring. RE-030.2 extends that
isolated module with a local input adapter; Frozen Core and operative
wiring remain unchanged. RE-031.1 is documentation-only scope work for
the Regime Comparability Gate. RE-032.1 is documentation-only
classification work for Personal Capacity. RE-033.1 is
documentation-only vocabulary work for Capital Posture. RE-034.1 is
documentation-only gate-combination boundary work.

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
  Assessment Engine              v1 — consumes the shared Research
                                  pipeline as of RE-029.3. Public
                                  helpers smoke-tested in RE-029.4. Not
                                  called by run.py. RE-029.6 defines
                                  Evidence Quality as a governance gate
                                  composed of objective dimensions, but
                                  no executable thresholds yet.
                                  RE-029.7 documents the calibration
                                  boundary for moving beyond the initial
                                  conservative gate state.
                                  RE-029.8 documents the future
                                  implementation scope without changing
                                  code.
                                  RE-029.9 documents acceptance criteria
                                  for the first isolated gate PR.
                                  Remaining issue is confidence
                                  calibration/boundary, not temporal
                                  leakage or Research pipeline
                                  duplication.
  Evidence Quality Gate          v0 — isolated structure added in
                                  RE-030.1. Compiles and has focused
                                  verification. RE-030.2 adds local
                                  Evidence input adapter. Not wired into run.py,
                                  DecisionEngine, AssessmentEngine or
                                  ValidationEngine. No thresholds, no
                                  capital posture mapping and no
                                  operative authority.
  Regime Comparability Gate      Boundary documented in RE-031.1. No
                                  code. No thresholds. No capital posture
                                  mapping. Not wired into any operative
                                  flow.
  Personal Capacity Boundary     Classification boundary documented in
                                  RE-032.1. No code. No thresholds. No
                                  capital posture mapping. Not yet
                                  classified as computable gate, human
                                  approval requirement or mixed control.
  Capital Posture Vocabulary     Documented in RE-033.1. No code. No
                                  posture engine. No gate combination
                                  implementation. `Blocked` is documented
                                  as an orthogonal veto.
  Gate Combination Layer         v0 — isolated structure added in
                                  RE-034.3. `engine/gate_combination.py`
                                  exists and is verified by
                                  `tests/verify_gate_combination.py`.
                                  Not wired into run.py, DecisionEngine,
                                  AssessmentEngine or ValidationEngine.
                                  No posture engine. No thresholds. No
                                  protocol rules. No operative authority.
  Predictive Validity Boundary   Opened in RE-PRED.1. Documentation
                                  only. No code. No new calculations.
                                  No predictive-validity claim. Defines
                                  the future validation contract: target
                                  audit, model freeze, baselines,
                                  holdout policy, uncertainty treatment
                                  and live tracking. RE-PRED.2 audits
                                  the current implemented target.
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

## RE-029.1 — Assessment / SOP governance scope audit

RE-029.1 opens the Assessment / SOP governance block as documentation-only
scope work.

The purpose is to define the boundary before writing rules:

-   Evidence describes objective historical observations.
-   Assessment interprets evidence quality, fragility and applicability.
-   SOP governance maps that interpretation into capital posture.
-   Human approval remains the final control for any capital deployment.

Primary objective hierarchy:

1.  Avoid irreversible error.
2.  Preserve capital in real terms.
3.  Maximize long-term return only after the first two constraints are
    respected.

This hierarchy is a governance choice, not an output of the model. If
the order changes, the rest of the SOP changes with it.

Dry powder definition:

`Dry powder` means deployable investable liquidity available within a
short operational window without principal impairment. It is not limited
to literal cash; it may include money-market instruments, T-bills or
credit lines that the owner is explicitly willing to use
countercyclically.

Protocol separation:

-   Dry Powder Protocol: idle or reserved deployable capital becomes
    invested capital. It increases net risk exposure and is governed by
    the capital posture language below.
-   Portfolio Reallocation Protocol: one risk asset is sold to buy
    another risk asset. It does not necessarily increase net risk
    exposure; it changes concentration and requires its own future
    invalidators, including liquidity and risk of the asset sold,
    correlation between the asset sold and the asset bought, and the
    cost of crystallizing the loss on the asset sold.

These are separate SOP protocols. They must not be collapsed into one
rule merely because both can occur during a drawdown.

Capital posture language:

-   Conserve.
-   Prepare.
-   Deploy partially.
-   Deploy aggressively.

`Blocked` is not a fifth intensity level. It is an orthogonal veto flag
that can override any posture when the framework itself is not reliable
enough to act.

Initial invalidation gates:

-   Evidence quality: weak or degraded historical evidence, including
    validation diagnostics, sample fragility, dispersion or insufficient
    comparable support.
-   Regime comparability: the current drawdown must have structurally
    meaningful precedent, not only numerical proximity.
-   Personal capacity: even good evidence is unusable if deployable
    liquidity, operational readiness or personal constraints make action
    inappropriate.

Human approval policy:

-   `Conserve` and `Prepare` may be logged without committing capital.
-   `Deploy partially` and `Deploy aggressively` require explicit human
    approval with timestamp before execution.
-   A `Blocked` flag always forces human review before any deployment
    action.

Boundary:

-   No code changes in RE-029.1.
-   No thresholds are defined yet.
-   No automatic capital decisions are introduced.
-   No `AssessmentEngine` rewrite is performed in this iteration.

The Engine may surface flags and descriptive evidence. It must not
decide capital deployment by itself.

## RE-029.2 — AssessmentEngine boundary audit

RE-029.2 audits `engine/assessment_engine.py` against the RE-029.1
boundary before changing code.

Verified current behaviour:

-   `AssessmentEngine` is not called by `run.py`.
-   It does use `ObservableUniverse(dataset, as_of=snapshot.date)`, so
    the older temporal-safety concern is resolved.
-   It builds evidence from `SimilarityEngine.top(..., n=10)` and
    `EvidenceEngine().build(..., years=5)`.
-   It still implements that research flow locally instead of
    delegating to the shared `build_research_result()` pipeline used by
    `DecisionEngine` and `ResearchEngine`.
-   It computes confidence through `ValidationEngine`, using
    coverage/consistency/diversity/stability, with stability currently
    hardcoded to 1.0.
-   It exposes interpretive helpers such as `drawdown_zone()`,
    `expected_return_5y()`, `upside_potential()` and `downside_risk()`.

Boundary conclusion:

-   Evidence production belongs to the shared Research pipeline.
-   Evidence description belongs to `EvidenceEngine`.
-   Evidence interpretation may belong to `AssessmentEngine`.
-   Capital posture, dry-powder deployment, portfolio reallocation and
    human approval belong to SOP governance, not to `AssessmentEngine`.

Therefore `AssessmentEngine` v2 should not become a decision engine. Its
next code iteration should first remove source-of-truth duplication by
consuming `build_research_result()` or `ResearchResult`, then expose
assessment flags about evidence quality, fragility and applicability.
It must not produce portfolio actions, capital amounts or automatic
deployment instructions.

This is documentation-only scope control. No code changed.


## RE-DOC-004 — Assessment / SOP boundary follow-up notes

RE-DOC-004 records two scope notes discovered after RE-029.2.

First, `AssessmentEngine.drawdown_zone()` and SOP capital posture are
separate axes. `drawdown_zone()` currently labels market severity
(`NORMAL`, `CORRECTION`, `BEAR MARKET`, `CRISIS`). Capital posture labels
(`Conserve`, `Prepare`, `Deploy partially`, `Deploy aggressively`) govern
action intensity. Market severity may become one input into posture, but
it is not itself a deployment decision. These taxonomies must not be
merged silently just because both describe drawdown context.

Second, stepped error tolerance remains explicitly pending. The intended
governance direction is conservative by default and aggressive only when
independent signals converge. RE-029.1 deliberately defines no thresholds
and no trigger logic, so this principle is recorded here as future SOP
governance work, not as current executable behavior.

Boundary:

-   No code changes.
-   No thresholds are defined.
-   No automatic capital decisions are introduced.
-   Future posture logic must preserve the distinction between market
    severity, evidence quality, personal capacity and capital action.

## RE-029.3 — AssessmentEngine consumes shared Research pipeline

RE-029.3 refactors `engine/assessment_engine.py` so `AssessmentEngine`
consumes `build_research_result(dataset, matches_count=10,
horizon_years=5)` instead of rebuilding Snapshot -> ObservableUniverse
-> SimilarityEngine.top() -> EvidenceEngine locally.

This closes the source-of-truth duplication identified in RE-029.2.
`AssessmentEngine`, `DecisionEngine` and `ResearchEngine` now share the
same objective Research pipeline for evidence production.

Boundary:

-   No capital posture.
-   No dry-powder deployment.
-   No portfolio reallocation.
-   No automatic recommendations.

Confidence remains out of scope. `AssessmentEngine.confidence()` still
uses `ValidationEngine`, including stability hardcoded to 1.0. That
score must not feed SOP capital gates until a later
governance/calibration pass defines it.

## RE-029.4 — AssessmentEngine public helper verification

RE-029.4 verifies that the public Assessment helper surface remains
stable after RE-029.3.

Verified result:

-   `drawdown_zone`: NORMAL
-   `expected_return_5y`: 0.113866763521769
-   `upside_potential`: 0.132855208016562
-   `downside_risk`: -0.010919489332530
-   `matches`: 10

This verifies the public helper outputs, not confidence calibration and
not SOP capital posture.

------------------------------------------------------------------------

## RE-029.5 — Confidence-to-posture gate boundary

RE-029.5 defines how evidence quality may connect to SOP capital
posture before any executable rules are written.

Decision:

-   Evidence quality / confidence is a gate, not a weighted input.
-   Weak evidence caps the maximum allowed capital posture regardless
    of expected return.
-   Evidence quality must not be averaged into a composite capital score
    that can be offset by attractive return expectations or unrelated
    favorable signals.

Rationale:

-   A weighted score optimizes, but can become a black box.
-   A gate protects: if evidence quality is insufficient, the reason for
    limiting posture remains explicit and auditable.
-   This follows the primary objective hierarchy: avoid irreversible
    error before preserving capital, and preserve capital before
    maximizing return.

Gate combination:

-   Evidence quality, regime comparability and personal capacity combine
    by veto / most restrictive ceiling.
-   One failed gate cannot be compensated by other gates.
-   The final capital posture cannot exceed the lowest ceiling produced
    by any active gate.

Current confidence restriction:

-   The current `AssessmentEngine` confidence score must not be used as
    the evidence-quality gate.
-   Reason: the score still includes `stability=1.0` as a hardcoded
    placeholder, which gives a false 25% weight to a non-measured
    dimension.
-   Until stability is calibrated, any future evidence-quality gate must
    inspect individual dimensions directly (coverage, consistency,
    diversity and explicit stability status) or remain documentation-only.

Boundary:

-   No thresholds are defined.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.6 — Evidence Quality Gate dimensions

RE-029.6 defines the documentary shape of the Evidence Quality Gate.
It does not implement the gate and does not define numeric thresholds.

The purpose of the gate is to cap maximum SOP capital posture according
to the quality of the evidence base. Evidence quality remains a ceiling,
not a weighted source of conviction. It can restrict capital posture; it
cannot make posture more aggressive by itself.

Starting posture:

-   The initial Evidence Quality Gate state must be conservative.
-   The current Research Validation surface is useful engineering
    evidence, but it does not yet demonstrate predictive validity.
-   Directional hit-rate is not discriminating in the current sample:
    0/19 evaluable forecasts were negative, so the 94.74% hit-rate
    mostly reflects that 18/19 realized 5-year outcomes were positive.
-   Rank correlation is weakly negative under the pinned runtime
    (`-0.22902466816870654`), so higher forecast ranks have not yet
    corresponded to higher realized-return ranks in this validation
    slice.
-   Therefore the gate must not start at Neutral by default. Neutral or
    more permissive states must be earned later through validation, not
    assumed from engineering consistency.

Evidence Quality dimensions:

1.  Coverage.

    Measures whether enough usable comparable evidence exists for the
    research claim being made. This aligns with the existing
    `ValidationEngine` coverage concept and with Research Validation's
    distinction between `sample_size` and `evaluated_count`.

2.  Consistency.

    Measures whether the evidence points in a coherent direction across
    the selected comparable set. This aligns with the existing
    `ValidationEngine` consistency concept. Consistency is descriptive;
    it must not be converted into a capital recommendation by itself.

3.  Diversity.

    Measures whether the evidence is supported by meaningfully different
    historical precedents rather than a narrow cluster of similar cases.
    This aligns with the existing `ValidationEngine` diversity concept.

4.  Independence / dispersion.

    Measures whether the evidence sample carries independent information
    or is structurally concentrated. This dimension captures the
    Research Validation findings from RE-025.6, RE-025.8 and RE-025.9:
    `n=19` is an operative count, not an independent sample-size claim;
    10 evaluated pairs have overlapping realized 5-year outcome windows;
    and 16/19 evaluable records belong to repeated forecast groups.

5.  Predictive validation status.

    Measures whether the Research Engine has demonstrated that its
    forecasts discriminate outcomes, not merely that the pipeline is
    reproducible. Current status is conservative: MAE is informative but
    outlier-sensitive, directional hit-rate is not discriminating, and
    rank correlation is weakly negative.

Relationship with existing `ValidationEngine`:

-   Existing `ValidationEngine` dimensions may inform future Evidence
    Quality implementation, especially coverage, consistency and
    diversity.
-   The current aggregate `AssessmentEngine.confidence().score` must not
    be used as the Evidence Quality Gate.
-   Reason: the score still includes hardcoded `stability=1.0`, and it
    does not capture the Research Validation independence / dispersion
    caveat.
-   RE-029.6 therefore defines dimensions, not executable scoring.

What Evidence Quality may limit:

-   Maximum capital posture.
-   Maximum aggressiveness of Dry Powder deployment.
-   Maximum aggressiveness of Portfolio Reallocation.
-   Whether an otherwise attractive Research output may be acted on
    beyond a conservative posture.

What Evidence Quality may not do:

-   It may not create a Risk ON posture by itself.
-   It may not override Dry Powder constraints.
-   It may not override Portfolio Reallocation constraints.
-   It may not override personal-capacity constraints.
-   It may not convert attractive expected return into permission for
    aggressive capital deployment when evidence quality is weak.

Protocol separation:

-   Dry Powder Protocol and Portfolio Reallocation Protocol remain
    separate governance protocols.
-   Dry Powder governs deployable liquidity.
-   Portfolio Reallocation governs changes to existing exposure.
-   Evidence Quality governs the maximum posture allowed by the evidence
    base across both protocols.
-   Final posture still follows veto logic: the most restrictive active
    gate wins.

Boundary:

-   No thresholds are defined.
-   No enum or state machine is implemented.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.7 — Evidence Quality Gate calibration boundary

RE-029.7 defines the calibration boundary for the Evidence Quality Gate.
It does not implement the gate and does not define numeric thresholds.

Architectural meaning of conservative:

-   The gate is fail-closed, not fail-open.
-   Evidence must actively justify any posture above the conservative
    ceiling against explicit, pre-registered criteria.
-   The default is not a middle state. Uncertainty resolves toward
    restriction because opportunity cost is subordinate to irreversible
    error in the SOP objective hierarchy.
-   Gate states must be discrete. Evidence Quality must not become a
    continuous capital-allocation function derived from a score.
-   A continuous score would reintroduce the optimization pressure that
    RE-029.5 rejected when it defined evidence quality as a gate rather
    than a weighted input.

Conditions for moving from conservative toward neutral:

-   Criteria must be pre-registered before the evidence is evaluated.
-   The decision must not be made ad hoc because a current result appears
    attractive.
-   All Evidence Quality dimensions must be measured without
    placeholders, including stability.
-   Future validation must show positive discriminatory power under a
    pre-registered validation protocol. Rank correlation positive and
    distinguishable from zero is one possible form of such evidence, but
    RE-029.7 does not define it as the only future criterion.
-   Directional metrics must be compared against naive baselines. A
    hit-rate only matters if it improves on trivial rules such as always
    predicting a positive return.
-   Error metrics such as MAE must be compared against naive baselines,
    such as unconditional historical mean or median forecasts, before
    they can support a less restrictive gate.
-   Sample dependence must be measured, bounded or explicitly discounted.
    It must not be hidden behind nominal record counts.

Current evidence that does not suffice:

-   MAE of 7.03% is informative, but not yet compared against a naive
    point-in-time baseline.
-   Directional hit-rate of 94.74% is not discriminating in the current
    sample because 0/19 evaluable forecasts were negative.
-   Rank correlation is weakly negative under the pinned runtime
    (`-0.22902466816870654`).
-   `n=19` is an operative count, not an independent sample-size claim,
    because Research Validation already documents overlapping realized
    outcome windows and repeated forecast groups.

Dimension readiness:

-   Coverage is genuine but weak. It counts usable matches, but does not
    yet judge whether those matches are strong analogies.
-   Diversity is genuine but weak. It uses decade dispersion as a coarse
    proxy and does not guarantee regime independence.
-   Consistency is real but not yet governance-grade. It measures return
    dispersion among matches, but can be inflated by temporally
    concentrated or structurally dependent observations.
-   Stability is not measured. It is currently hardcoded to `1.0` and
    must be treated as unavailable, not as weak positive evidence.
-   Independence / dispersion and predictive validation status are
    documented dimensions, but not yet implemented as local gate
    measurements.

Prohibited shortcuts:

-   `AssessmentEngine.confidence().score` must not be used as the
    Evidence Quality Gate.
-   It must not be used as a temporary proxy until something better
    exists. That path would turn a placeholder into governance logic.
-   Aggregate Research Validation metrics must not be cited as the
    quality of a specific current snapshot. They describe historical
    model behaviour, not local evidence quality for today's match set.
-   Attractive expected return must not compensate for weak evidence
    quality.
-   No emergency or urgency argument may relax the Evidence Quality Gate
    ad hoc. Relaxation requires a numbered, documented governance
    iteration.

Open governance question:

-   A future human-approval mechanism must decide whether an exception
    iteration written during the crisis that motivates it deserves the
    same authority as one written before the pressure existed.
-   Possible safeguards include a second approver, a cooling-off period
    or a rule requiring that emergency exceptions be defined before the
    triggering event.
-   RE-029.7 records this as an open governance question only. It does
    not solve the approval mechanism.

Boundary:

-   No thresholds are defined.
-   No enum or state machine is implemented.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.8 — Evidence Quality Gate implementation scope

RE-029.8 defines the allowed scope of the first future
`EvidenceQualityGate` implementation. It does not implement the gate.

The first code iteration, when authorized, should create structure only.
It must not introduce numeric thresholds, automatic capital posture
changes or operative wiring into the current execution path.

Implementation boundary:

-   Do not modify `AssessmentEngine.confidence().score`.
-   Do not use `AssessmentEngine.confidence().score` as a temporary
    proxy.
-   Do not modify `ValidationEngine` in the first gate implementation.
-   Do not wire the first `EvidenceQualityGate` implementation into
    `run.py`.
-   Do not wire it into `DecisionEngine`.
-   The first implementation should exist, compile and be testable in
    isolation before it governs anything operative.

Separate input channels:

The future gate must not receive its inputs as one flat list of
"allowed evidence." RE-029.7 already distinguishes global Research
Validation from local snapshot quality. The implementation should
preserve that distinction in its shape.

1.  Local snapshot evidence quality.

    This channel describes the current match set only.

    Initial local inputs may include:

    -   local coverage;
    -   local consistency;
    -   local diversity.

    These values are about today's selected evidence sample. They do not
    prove that the model has predictive skill globally.

2.  Global model-validation state.

    This channel describes whether the Research Engine, as a model, has
    demonstrated predictive discrimination under pre-registered
    validation criteria.

    Current global state is conservative / not validated. Existing
    Research Validation metrics are useful diagnostics, but they do not
    yet justify a neutral gate state.

    Global validation state must not be collapsed into local match-set
    quality.

Dimension clarification:

-   RE-029.6 defines five official Evidence Quality dimensions:
    coverage, consistency, diversity, independence / dispersion and
    predictive validation status.
-   `stability` is not currently an official Evidence Quality Gate
    dimension.
-   `stability` belongs to the legacy `ValidationEngine` /
    `confidence.score` path today.
-   RE-029.7 evaluates `stability` only because the hardcoded
    `stability=1.0` blocks use of `confidence.score` as a gate or proxy.
-   Independence / dispersion does not automatically absorb stability.
    Independence / dispersion concerns the structure of the evidence
    sample. Stability concerns the stability of the engine or its
    outputs across versions, conditions or runs.
-   If stability is ever added to the Evidence Quality Gate, it must be
    introduced explicitly in a later numbered iteration.

Conceptual output states:

The future gate must distinguish absence of measurement from measured
insufficiency. This follows the same design principle as Evidence:
absence of evidence is not `0.0`.

The conceptual output therefore needs at least three states:

-   not measurable;
-   conservative;
-   future less-restrictive state, name not yet finalized.

`not measurable` means the gate lacks required measurements. It is not
the same as "measured and insufficient." Both may cap posture
conservatively, but they must remain explainably different states.

Future implementation rule:

-   The first code change should model structure and explanations only.
-   It should preserve local/global input separation.
-   It should preserve discrete output states.
-   It should default to fail-closed.
-   It should remain outside the operative flow until thresholds,
    calibration and human approval are documented in later iterations.

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No enum names are finalized.
-   No capital posture rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-029.9 — Evidence Quality Gate first-code acceptance criteria

RE-029.9 defines the acceptance criteria for the first future code PR
that introduces an isolated `EvidenceQualityGate` structure. It does not
implement that PR.

The purpose is to make the next transition from documentation to code
auditable. A future PR should be accepted or rejected by reading its
diff against these criteria.

Expected files:

-   A future implementation may introduce a new isolated module, likely
    `engine/evidence_quality_gate.py`.
-   A future verification may introduce a focused test, likely
    `tests/verify_evidence_quality_gate.py`.
-   File names are not finalized by RE-029.9, but the responsibility is:
    one isolated gate module and one focused verification surface.

Required implementation properties:

-   The gate exists and compiles in isolation.
-   The gate is not wired into `run.py`.
-   The gate is not wired into `DecisionEngine`.
-   The gate does not modify `AssessmentEngine`.
-   The gate does not modify `ValidationEngine`.
-   The gate does not read or reuse
    `AssessmentEngine.confidence().score`.
-   The gate keeps local snapshot evidence quality separate from global
    model-validation state.
-   The gate exposes discrete output states, including at least
    `not measurable` and `conservative`.
-   The gate defaults to fail-closed.
-   The gate returns explanations, not only state labels.

Required test properties:

-   Tests must verify structure and behaviour, not only importability.
-   With today's available dimensions -- partial local inputs, no local
    implementation of independence / dispersion, no local implementation
    of predictive validation status and global model-validation state
    still not validated -- the gate must return `not measurable` or
    `conservative`.
-   The same test must reject any less-restrictive state under today's
    inputs.
-   Incomplete inputs or `None` values must produce `not measurable`, not
    a crash and not an assumed default score.
-   This follows the RE-024.1 Evidence rule: absence of evidence is not
    `0.0`.

Explanation requirements:

-   Explanations must identify the specific channel or dimension causing
    the cap.
-   A generic explanation such as "insufficient evidence" is not
    acceptable by itself.
-   Acceptable explanations should name causes such as:

    -   local coverage unavailable;
    -   local consistency unavailable;
    -   local diversity unavailable;
    -   global model-validation state not validated;
    -   predictive validation status unavailable;
    -   independence / dispersion not measured.

Frozen Core rejection criterion:

-   The first `EvidenceQualityGate` PR must not modify Frozen Core.
-   Any modification to Frozen Core in that PR is grounds for rejection
    unless a separate numbered iteration explicitly invokes the Frozen
    Core Policy exception before the code change.

Explicit non-goals for the first code PR:

-   No numeric thresholds.
-   No capital posture mapping.
-   No automatic recommendations.
-   No runtime wiring.
-   No changes to `DecisionEngine`.
-   No changes to `AssessmentEngine`.
-   No changes to `ValidationEngine`.
-   No replacement of `confidence.score`.
-   No use of aggregate Research Validation metrics as local snapshot
    quality.

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No enum names are finalized.
-   No capital posture rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-030.1 — Isolated Evidence Quality Gate

RE-030.1 introduces the first isolated `EvidenceQualityGate` code
structure.

This is the first implementation step after the RE-029 governance block.
It follows the acceptance criteria documented in RE-029.9.

Files added:

-   `engine/evidence_quality_gate.py`
-   `tests/verify_evidence_quality_gate.py`

Implemented structure:

-   `LocalEvidenceQualityInputs`
-   `GlobalModelValidationState`
-   `EvidenceQualityGateResult`
-   `EvidenceQualityGate`
-   `NOT_MEASURABLE`
-   `CONSERVATIVE`

Architecture:

-   Local snapshot evidence quality and global model-validation state are
    separate input channels.
-   Local inputs currently include coverage, consistency, diversity and
    whether independence / dispersion has been measured.
-   Global input currently captures predictive validation status.
-   The gate returns a discrete state plus explanations.
-   Absence of measurement is represented as `not measurable`, not as a
    numeric default.
-   The gate defaults fail-closed.

Current behaviour:

-   Today's partial inputs return `not measurable`.
-   Incomplete local inputs or missing global validation state return
    `not measurable`.
-   Fully measured inputs with predictive validation marked `validated`
    still return `conservative`, because no less-restrictive state is
    authorized yet.
-   Explanations identify specific causes, such as local coverage
    unavailable, predictive validation status unavailable, independence /
    dispersion not measured, or global model-validation state not
    validated.

Verification:

`tests/verify_evidence_quality_gate.py` verifies:

-   today's available inputs produce `not measurable` or `conservative`,
    never a less-restrictive state;
-   incomplete inputs / `None` values produce `not measurable`;
-   explanations name specific channels or dimensions;
-   fully measured but not yet authorized inputs produce `conservative`.

Verified result:

-   `EVIDENCE QUALITY GATE : STABLE`
-   `today_state: not measurable`
-   `incomplete_state: not measurable`
-   `measured_but_not_authorized_state: conservative`

Boundary:

-   No thresholds are defined.
-   No capital posture mapping is implemented.
-   No automatic recommendation is implemented.
-   No runtime wiring is implemented.
-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.
-   Frozen Core is unchanged.

------------------------------------------------------------------------

## RE-030.2 — Local Evidence Quality input adapter

RE-030.2 adds the first adapter from real Research output into local
Evidence Quality inputs.

Function added:

    build_local_evidence_quality_inputs(evidence)

Design:

-   The adapter receives only `evidence`.
-   It does not receive `matches` separately.
-   `Evidence` remains the single source of truth for the selected match
    set through `evidence.matches`.
-   This prevents source-of-truth drift between an `Evidence` object and
    a separately supplied match list.

Local dimensions:

-   `coverage` is calculated from usable evidence:

        min(evidence.return_count / 10.0, 1.0)

    It deliberately does not use `len(evidence.matches) / 10.0`.
    Today's snapshot has 10 selected matches but only 9 usable realized
    returns at the evidence horizon, so local coverage is 0.9, not 1.0.

-   `consistency` is calculated from realized returns at the same horizon
    as the `Evidence` object:

        future_return_{evidence.horizon_years}y

    This avoids the legacy `ValidationEngine` default horizon
    (`future_return_3y`) and keeps local consistency aligned with the
    returns that produced `Evidence.median_return`,
    `Evidence.worst_return` and `Evidence.best_return`.

-   `diversity` is calculated from the number of decades represented in
    `evidence.matches`, divided by the selected match count.

-   `independence_dispersion_measured` remains `False`.

Isolation clarification:

RE-030.1 was isolated in the strongest sense: the gate structure had no
dependency on other project modules.

RE-030.2 introduces a narrower form of isolation. The adapter reads the
existing `Evidence` object and its `Similarity` matches, so it is no
longer zero-dependency. It remains architecturally isolated because
nothing calls it from the operative flow:

-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.

Verified current local values:

-   `real_local_coverage: 0.90000000000000`
-   `real_local_consistency: 0.95184562290644`
-   `real_local_diversity: 0.60000000000000`
-   `real_today_state: not measurable`

The focused verification pins the exact current values. It does not
settle thresholds, capital posture mapping or governance authority.

Boundary:

-   No thresholds are defined.
-   No capital posture mapping is implemented.
-   No automatic recommendation is implemented.
-   No runtime wiring is implemented.
-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.
-   Frozen Core is unchanged.

------------------------------------------------------------------------

## RE-031.1 — Regime Comparability Gate boundary

RE-031.1 defines the first boundary for the Regime Comparability Gate.
It is documentation-only.

Purpose:

The Regime Comparability Gate asks whether the historical evidence being
used by the Research Engine is structurally applicable to the current
market regime.

It does not ask whether the market is attractive.

It does not ask whether expected return is high.

It asks whether the current regime is comparable enough to the regimes
represented in the evidence sample for the evidence to be allowed to
support capital posture.

Architectural role:

-   Regime comparability is a gate / ceiling, not a weighted input.
-   It can cap maximum capital posture.
-   It cannot make posture more aggressive by itself.
-   It cannot compensate for weak Evidence Quality.
-   It cannot override Personal Capacity.
-   It combines with other gates by veto / most restrictive ceiling.

Relationship with Evidence Quality:

-   Evidence Quality asks whether the evidence sample is internally
    usable and whether the model has demonstrated predictive validity.
-   Regime Comparability asks whether the current regime is structurally
    represented by that evidence.
-   These questions are related but not identical.
-   A high-quality evidence sample can still be a poor guide if today's
    regime is structurally outside the sample.
-   A comparable regime does not make weak evidence strong.

Relationship with `AssessmentEngine.drawdown_zone()`:

-   `drawdown_zone()` is a market severity taxonomy.
-   It is not a regime-comparability gate.
-   It may help describe the current market state, but it does not decide
    whether today's regime is comparable to historical precedents.
-   RE-031.1 does not modify `AssessmentEngine`.

Candidate dimensions:

The first implementation is not authorized yet, but future Regime
Comparability work may need to evaluate dimensions such as:

-   valuation regime;
-   inflation regime;
-   interest-rate regime;
-   earnings / margin regime;
-   volatility regime;
-   liquidity / credit regime;
-   policy / intervention regime;
-   market-structure regime.

These are candidate dimensions only. RE-031.1 defines no thresholds and
does not decide which dimensions become executable.

Current state:

-   No Regime Comparability code exists.
-   No local regime-comparability inputs exist.
-   No global regime taxonomy exists.
-   No thresholds exist.
-   No capital posture mapping exists.
-   The gate is not measurable today.

Default stance:

-   Until measured, Regime Comparability must be treated as unavailable,
    not favorable.
-   Absence of regime comparability evidence must not be represented as a
    positive score.
-   If a future gate requires a state before measurement exists, it must
    fail closed.

Prohibited shortcuts:

-   Do not use `drawdown_zone()` as a regime-comparability proxy.
-   Do not use expected return as a regime-comparability proxy.
-   Do not use Evidence Quality as a regime-comparability proxy.
-   Do not infer comparability from the fact that `SimilarityEngine`
    found matches.
-   Do not relax the gate ad hoc because a current market opportunity
    appears attractive.

Open questions:

-   Which regime dimensions are observable with current data?
-   Which dimensions require new data sources?
-   Should regime comparability be measured locally against the selected
    match set, globally against the full historical universe, or both?
-   Can regime comparability be computed, or does it require an explicit
    human regime assessment for some dimensions?
-   How should regime comparability interact with future Personal
    Capacity classification?

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No regime taxonomy is finalized.
-   No capital posture mapping is implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-032.1 — Personal Capacity classification boundary

RE-032.1 defines the first boundary for Personal Capacity.
It is documentation-only.

Primary classification question:

    Is Personal Capacity a parallel gate,
    a human-approval requirement,
    or a mixed control?

RE-032.1 deliberately does not assume the answer.

Purpose:

Personal Capacity asks whether the person can responsibly assume risk
now.

It does not measure market opportunity.

It does not measure evidence quality.

It does not measure regime comparability.

It asks whether the person's current financial and behavioural capacity
allows any capital posture above the conservative floor.

Architectural role:

-   Personal Capacity may become a gate, a human-approval prerequisite or
    a mixed control.
-   Until classified, it must not be treated as a fully computable gate.
-   If it becomes a gate, it must act as a ceiling, not a weighted input.
-   It cannot make posture more aggressive by itself.
-   It cannot compensate for weak Evidence Quality.
-   It cannot compensate for poor Regime Comparability.
-   It must fail closed when required facts or attestations are missing.

Two input channels:

Future Personal Capacity work must not collapse all personal dimensions
into one opaque score. Inputs must remain separated into at least two
channels.

1.  Verifiable facts.

    These are objective or documentable conditions, such as:

    -   available liquidity;
    -   near-term cash needs;
    -   fixed obligations;
    -   debt service;
    -   income concentration;
    -   portfolio concentration;
    -   required emergency reserve;
    -   known time horizon constraints.

2.  Attested judgement.

    These are human declarations or judgements, not stable objective
    measurements, such as:

    -   perceived income stability;
    -   willingness to tolerate drawdown;
    -   ability to avoid forced selling;
    -   psychological capacity to hold through stress;
    -   household or life constraints not captured in financial data.

These channels may both restrict posture, but they must not be averaged
into a single score.

Drawdown tolerance risk:

Declared tolerance to drawdown is least reliable when it matters most.

A tolerance statement made in calm conditions is more useful than a
revision made during a crisis. A change in declared tolerance during a
drawdown should be treated with the same suspicion as an emergency
exception that relaxes a gate under pressure.

Future governance should therefore prefer pre-registered personal
capacity attestations over crisis-time revisions. RE-032.1 does not
define the approval mechanism, but records the risk explicitly.

Relationship with Human Approval:

-   Personal Capacity may belong partly or entirely inside Human
    Approval.
-   If so, it should be treated as an approval prerequisite rather than a
    parallel technical gate.
-   If some parts are computable and others attested, future design must
    preserve that separation.
-   Gate combination cannot be finalized until Personal Capacity is
    classified.

Prohibited shortcuts:

-   Do not convert Personal Capacity into an opaque confidence score.
-   Do not average verifiable facts with attested judgement.
-   Do not treat a missing attestation as favorable.
-   Do not treat crisis-time risk tolerance revisions as equally reliable
    as pre-registered attestations.
-   Do not allow attractive market evidence to compensate for inadequate
    Personal Capacity.

Open questions:

-   Which Personal Capacity facts can be verified from existing records?
-   Which facts require manual entry?
-   Which dimensions require explicit human attestation?
-   Should attestations expire?
-   Should crisis-time attestation changes require a cooling-off period
    or second approval?
-   Does Personal Capacity participate in gate-combination logic, or does
    it sit inside Human Approval before any capital action is allowed?

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No personal-capacity taxonomy is finalized.
-   No capital posture mapping is implemented.
-   No operative wiring is authorized.
-   Personal Capacity is not yet classified as a gate.

------------------------------------------------------------------------

## RE-033.1 — Capital Posture vocabulary and ordering

RE-033.1 formalizes the Capital Posture vocabulary and ordering.
It is documentation-only.

This iteration does not implement posture logic. It defines the ordered
posture ceiling that future gates may cap.

Ordered posture states:

From most restrictive to least restrictive:

1.  `Conserve`
2.  `Prepare`
3.  `Deploy Partially`
4.  `Deploy Aggressively`

`Blocked` is not part of this ordered scale. It is an orthogonal veto.

State definitions:

### Conserve

No new exposure.

No Dry Powder deployment.

No Portfolio Reallocation outside routine rebalances already scheduled
outside this SOP process.

`Conserve` is the fail-closed floor.

### Prepare

No new exposure.

No Dry Powder deployment.

No Portfolio Reallocation.

`Prepare` may authorize planning, identifying funding sources,
redirecting future contributions to cash or preparing Dry Powder
capacity.

It does not authorize selling existing strategic positions unless a
future Dry Powder Protocol explicitly allows it.

### Deploy Partially

Authorizes deploying a bounded fraction of available Dry Powder into the
identified opportunity.

RE-033.1 does not define that fraction.

Portfolio Reallocation remains governed by its own future protocol.
Deploying Dry Powder does not automatically authorize reallocating
existing positions.

### Deploy Aggressively

Authorizes deploying the maximum Dry Powder amount allowed by future
protocols.

It does not automatically authorize Portfolio Reallocation.

Dry Powder deployment and Portfolio Reallocation remain independent
authorizations with their own gates.

### Blocked

Orthogonal veto.

`Blocked` overrides any ordered posture state.

It must carry an explicit reason, following the explanation standard
already required from the Evidence Quality Gate.

It may be activated by any future gate or by human approval governance,
provided the reason is documented.

Rule 1 — gate state to posture ceiling:

A gate's internal state must first map to a posture ceiling for that
gate.

Current mapping:

-   `not measurable` caps at `Conserve`;
-   `conservative` caps at `Conserve`.

These two states have the same posture ceiling today but different
explanations:

-   `not measurable` means required measurement is missing;
-   `conservative` means the gate was measured but does not authorize a
    less restrictive ceiling.

This preserves the project-wide rule: absence of evidence is not `0.0`.

Rule 2 — combining posture ceilings:

Future gate combination must operate on posture ceilings, not raw
internal scores.

Among ordered posture states, the most restrictive ceiling wins.

If `Blocked` is active, `Blocked` wins over all ordered states.

Worked current-state inference:

Current known gate states:

-   Evidence Quality: `not measurable`;
-   Regime Comparability: `not measurable`;
-   Personal Capacity: not classified / unavailable;
-   `Blocked`: false unless explicitly activated.

Documentation-level inference:

    Final capital posture ceiling: Conserve

This is a documentation-level inference, not executable logic. No
Capital Posture Engine exists yet.

Open question:

Can any gate permit `Prepare` while Evidence Quality remains
`not measurable`, or is measurable Evidence Quality a prerequisite for
any posture above `Conserve`?

RE-033.1 records this question for future gate-combination work. It does
not answer it.

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No Dry Powder Protocol rules are implemented.
-   No Portfolio Reallocation Protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.1 — Gate combination boundary

RE-034.1 defines the boundary for combining gate outputs into a final
Capital Posture ceiling.

It is documentation-only.

No posture engine is implemented.

Combination inputs:

Future combination logic must not consume scores.

It should consume discrete gate outputs such as:

-   gate name;
-   gate internal state;
-   posture ceiling;
-   `Blocked` flag;
-   explanation.

The combination layer must operate on posture ceilings and veto flags,
not raw confidence or validation scores.

Combination order:

1.  If any gate or human approval control activates `Blocked`, final
    output is `Blocked`.
2.  If `Blocked` is not active, combine ordered posture ceilings by
    taking the most restrictive ceiling.

Ordered posture scale:

    Conserve < Prepare < Deploy Partially < Deploy Aggressively

Non-deployment vs deployment:

RE-034.1 separates non-deployment postures from deployment postures.

Non-deployment postures:

-   `Conserve`
-   `Prepare`

Deployment postures:

-   `Deploy Partially`
-   `Deploy Aggressively`

Evidence Quality prerequisite:

Evidence Quality not measurable blocks deployment.

It does not, by itself, necessarily block `Prepare`.

Reason:

`Prepare` does not commit capital. It authorizes planning and
preparation only. Deployment states commit capital based on evidence.
Therefore measurable Evidence Quality is a hard prerequisite for
`Deploy Partially` or `Deploy Aggressively`, but not necessarily for
`Prepare`.

Asymmetric unavailable-gate treatment:

This exception applies to Evidence Quality only.

Unavailable Regime Comparability caps at `Conserve`.

Unavailable Personal Capacity, while still unclassified, caps at
`Conserve` as a placeholder.

Reason:

Evidence Quality uncertainty means the system does not know how much to
trust the expected-return evidence. That blocks capital deployment but
does not necessarily block preparation.

Regime Comparability uncertainty means the system does not know whether
the current situation is structurally comparable enough to historical
precedents to justify any reaction.

Personal Capacity unavailability means the system does not know whether
the person can act responsibly at all.

Those uncertainties are more fundamental than uncertainty about the
return estimate, so they cap at `Conserve` until measured or classified.

Current gate-ceiling mapping:

-   Evidence Quality `not measurable` -> `Prepare`;
-   Evidence Quality `conservative` -> `Conserve`;
-   Regime Comparability `not measurable` -> `Conserve`;
-   Personal Capacity unavailable / unclassified -> `Conserve`;
-   Any `Blocked` flag -> `Blocked`.

This mapping is provisional and documentary. It exists to make the
current architecture auditable before implementation.

Worked current-state inference:

Current known states:

-   Evidence Quality: `not measurable` -> `Prepare`;
-   Regime Comparability: `not measurable` -> `Conserve`;
-   Personal Capacity: unavailable / unclassified -> `Conserve`;
-   `Blocked`: false unless explicitly activated.

Combination:

    min(Prepare, Conserve, Conserve) = Conserve

Documentation-level result:

    Final capital posture ceiling: Conserve

This is a documentation-level inference, not executable logic. No
Capital Posture Engine exists yet.

Personal Capacity placeholder:

Personal Capacity is included in the worked example only as an
unavailable placeholder.

RE-032.1 has not classified Personal Capacity as a parallel gate, Human
Approval prerequisite or mixed control. Future combination logic must be
revised after that classification.

Open questions:

-   Can `Prepare` ever be authorized solely by Regime Comparability while
    Evidence Quality remains `not measurable`?
-   Should Regime Comparability have its own non-deployment exception in
    future, or is `not measurable -> Conserve` permanent?
-   Does Personal Capacity belong in gate combination, or inside Human
    Approval before any capital action is considered?
-   How should explanations be composed when several gates cap posture at
    the same level?

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No Dry Powder Protocol rules are implemented.
-   No Portfolio Reallocation Protocol rules are implemented.
-   No Human Approval implementation is added.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.2 — Gate combination first-code acceptance criteria

RE-034.2 defines acceptance criteria for the first isolated
gate-combination code.

It is documentation-only.

No posture engine is implemented.

Purpose:

The first code change must make the RE-034.1 combination boundary
testable without connecting it to the operative SOP flow.

It must model structure, ordering and explanations only.

It must not implement thresholds, protocols or automatic capital action.

Required behavior:

1.  `Blocked` wins before any ordered-posture comparison.

    If any gate or human approval control marks `Blocked`, the combined
    result must be `Blocked` regardless of all posture ceilings.

2.  Without `Blocked`, the most restrictive posture ceiling wins.

    The ordered scale is:

        Conserve < Prepare < Deploy Partially < Deploy Aggressively

3.  The current real-state anchor must be pinned as a regression test.

    With today's known gate states:

    -   Evidence Quality: `not measurable` -> `Prepare`;
    -   Regime Comparability: `not measurable` -> `Conserve`;
    -   Personal Capacity: unavailable / unclassified -> `Conserve`;
    -   `Blocked`: false.

    The combined output must be exactly:

        Conserve

    This test protects the worked RE-034.1 example from becoming only
    prose.

4.  Evidence Quality must not override more restrictive gates.

    A test must verify that if Evidence Quality authorizes up to
    `Deploy Aggressively` but Regime Comparability or Personal Capacity
    caps at `Conserve`, the combined output remains `Conserve`.

    This prevents the Evidence Quality exception from being misread as
    Evidence Quality dominance.

5.  Evidence Quality `not measurable` must not be flattened back to
    `Conserve`.

    A test must verify that:

    -   Evidence Quality: `not measurable` -> `Prepare`;
    -   Regime Comparability: `Deploy Aggressively`;
    -   Personal Capacity: `Deploy Aggressively`;
    -   `Blocked`: false.

    The combined output must be:

        Prepare

    This protects the RE-034.1 distinction between preparation and
    deployment from regression.

6.  Unavailable Regime Comparability must cap at `Conserve`.

    A test must verify that unavailable or `not measurable` Regime
    Comparability caps the combined result at `Conserve`, even if other
    gates allow less restrictive posture.

7.  Unavailable Personal Capacity must cap at `Conserve` while its role
    remains unclassified.

    A test must verify the placeholder behavior documented in RE-034.1.
    Future work may revise this after Personal Capacity is classified,
    but the first code must not silently assume it is favorable.

8.  Explanations must preserve traceability.

    The combined output must identify which gate or control caused the
    final ceiling or `Blocked` result.

    A generic explanation such as "insufficient evidence" is not enough.
    The explanation must name the specific limiting gate or control, for
    example:

    -   `Regime Comparability: not measurable`;
    -   `Personal Capacity: unavailable`;
    -   `Evidence Quality: not measurable, deployment blocked`;
    -   `Human Approval: blocked`.

9.  Inputs must be discrete.

    The combination function must consume posture ceilings, `Blocked`
    flags and explanations. It must not consume raw scores,
    `confidence.score`, MAE, hit-rate, rank correlation or any other
    validation metric directly.

Required isolation:

The first code change may add an isolated combination module and a
verification test.

It must not be wired into:

-   `run.py`;
-   `DecisionEngine`;
-   `AssessmentEngine`;
-   `ValidationEngine`;
-   Frozen Core.

Automatic rejection criteria:

A future PR fails RE-034.2 if it:

-   connects combination logic to the operative flow;
-   changes Frozen Core;
-   consumes raw scores instead of discrete gate ceilings;
-   treats Evidence Quality as dominant over the other gates;
-   maps Evidence Quality `not measurable` directly to `Conserve`;
-   treats unavailable Regime Comparability as favorable;
-   treats unavailable Personal Capacity as favorable;
-   returns a final posture without naming the limiting cause;
-   implements thresholds;
-   implements Dry Powder Protocol rules;
-   implements Portfolio Reallocation Protocol rules;
-   implements Human Approval.

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.4 — Gate combination implementation status

RE-034.4 documents the status after the first isolated
gate-combination code.

It is documentation-only.

Implemented in RE-034.3:

-   `engine/gate_combination.py`;
-   `tests/verify_gate_combination.py`.

Verified command:

    python3 tests/verify_gate_combination.py

Verified output:

    GATE COMBINATION : STABLE

What now exists:

-   discrete Capital Posture constants:
    `Conserve`, `Prepare`, `Deploy Partially`,
    `Deploy Aggressively`, `Blocked`;
-   ordered posture comparison for non-blocked gates;
-   `Blocked` precedence over posture ordering;
-   discrete gate-combination input objects;
-   combined result with traceable explanations;
-   regression coverage for today's documentary state:
    Evidence Quality `not measurable`, Regime Comparability
    `not measurable`, Personal Capacity unavailable / unclassified and
    `Blocked=false` combine to `Conserve`;
-   regression coverage for the Evidence Quality asymmetry:
    Evidence Quality `not measurable` caps at `Prepare`, not `Conserve`,
    when the other gates allow less restrictive posture;
-   regression coverage proving that Evidence Quality does not override
    a more restrictive Regime Comparability or Personal Capacity cap.

What does not exist:

-   no Capital Posture Engine;
-   no automatic recommendation;
-   no thresholds;
-   no Dry Powder Protocol rules;
-   no Portfolio Reallocation Protocol rules;
-   no Human Approval implementation;
-   no adapter from live gate outputs into the combination layer;
-   no operative wiring.

Operative boundary:

`engine/gate_combination.py` exists in the repository.

It does not participate in the `run.py` execution path.

It is not called by `DecisionEngine`.

It is not called by `AssessmentEngine`.

It is not called by `ValidationEngine`.

It does not consume `confidence.score`.

It does not consume MAE, hit-rate, rank correlation or any raw
Research Validation metric.

Current posture inference:

The documented current-state inference remains:

    min(Prepare, Conserve, Conserve) = Conserve

This is still an architectural inference and test fixture.

It is not an executable SOP recommendation.

Next implementation boundary:

Future work may define adapters from actual gate outputs into
`GateCombinationInput`.

That future work must remain isolated unless a later numbered iteration
explicitly authorizes operative wiring.

Boundary:

-   Documentation updated only.
-   No code changed in RE-034.4.
-   No posture engine is implemented.
-   No thresholds are defined.
-   No protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-PRED.1 — Predictive validity boundary

RE-PRED.1 opens the predictive-validity block.

It does not demonstrate predictive capacity.

It defines what would have to be true before the SOP may claim that the
Research Engine has predictive validity.

It is documentation-only.

No code changed.

No new calculation is executed.

No new validation claim is made.

Purpose:

The Research Engine currently produces objective, reproducible and
explainable historical evidence.

Current Research Validation does not yet show reliable predictive
discrimination:

-   rank correlation is weakly negative;
-   hit-rate is not discriminating because the evaluated forecasts lack
    meaningful sign variation;
-   MAE lacks a sufficiently specified naive baseline comparison;
-   the nominal sample size is not the independent effective sample size.

RE-PRED.1 therefore separates engineering validity from predictive
validity.

Engineering validity means the pipeline is reproducible and
methodologically consistent.

Predictive validity means the forecasts demonstrate useful out-of-sample
relationship to future realized outcomes, against pre-defined baselines,
with uncertainty reported.

RE-PRED.1 only defines the boundary for that second claim.

Predictive target audit:

Before freezing a predictive target, the project must audit what the
current code actually calculates.

At minimum, the audit must establish:

-   which return field is evaluated today;
-   whether the return is nominal or real;
-   whether it is price return or total return;
-   whether the horizon is exactly five years or convention-dependent;
-   which date anchors start and end the realized-return window;
-   whether missing future returns are excluded, imputed or treated as
    unavailable;
-   whether validation evaluates absolute return, excess return, rank or
    direction.

The future target must either match the current operative calculation or
explicitly authorize a change.

It must not diverge from implementation by accident.

Predictive claims:

Predictive validity must be decomposed into separate claims.

1.  Ranking validity.

    Higher forecasts should tend to correspond to higher realized
    outcomes.

    Rank correlation is the natural diagnostic surface for this claim.

    Ranking validity may be useful even if exact magnitudes are not yet
    calibrated.

2.  Calibration validity.

    Forecast magnitudes should resemble realized magnitudes better than
    pre-defined naive magnitude estimates.

    This is a stronger claim than ranking validity.

3.  Directional validity.

    Forecast sign should carry useful information only when the sample
    has meaningful sign variation.

    A high hit-rate with almost no negative forecasts is not, by itself,
    predictive evidence.

Future model-validation state may need to represent these claims
separately. A single `validated` / `not validated` string may be too
coarse if ranking improves before calibration.

Validation surfaces:

Future predictive validation must separate at least three surfaces.

1.  Existing historical backtest.

    This is useful for diagnostics, reproducibility and failure-mode
    discovery.

    It is not fully clean out-of-sample evidence because the Similarity
    Engine was designed while exposed to the historical dataset.

2.  Prospective holdout from the freeze date.

    A clean holdout cannot be created retroactively from data already
    used to design, inspect or iterate the model.

    Any historical holdout claim must therefore be treated cautiously.

    A genuinely clean holdout starts only after the model, dataset
    cutoff, target, metrics and baselines are frozen.

3.  Live tracking.

    Live tracking is the slowest but most honest evidence source.

    It should begin as soon as the logging protocol is defined, even if
    the later evaluation horizon takes years to mature.

Model freeze requirement:

No holdout or live-tracking result may count as clean predictive evidence
unless the evaluated model was frozen before the forecast was observed.

The freeze must include:

-   code version or commit;
-   dataset cutoff;
-   feature definitions;
-   similarity dimensions;
-   similarity weights;
-   episode-selection rules;
-   forecast horizon;
-   target definition;
-   metrics;
-   baselines;
-   missing-data rules.

Changing the model after seeing validation results makes the affected
sample exploratory again.

Without this freeze, validation risks becoming p-hacking with extra
steps.

Baseline requirement:

Predictive claims must be compared against pre-defined naive baselines.

RE-PRED.1 does not define pass/fail thresholds.

It requires future work to specify baselines before evaluation.

Candidate baselines include:

-   unconditional historical mean or median;
-   constant forecast equal to the full historical universe expected
    return;
-   zero-return or no-change forecast where appropriate to the target;
-   simple mean-reversion rule based on drawdown depth, without
    similarity matching.

The model does not become predictive merely by beating one trivial
baseline.

Future validation must explain which baseline each claim is tested
against and why that comparison is appropriate to the target.

Uncertainty requirement:

No future metric should be interpreted from its point estimate alone.

Given the known dependence documented in RE-025.6, RE-025.8 and
RE-025.9, uncertainty estimates must respect dependence between
observations.

An i.i.d. bootstrap is not sufficient by default.

Future work should consider block-aware resampling or another method
that preserves overlapping outcome windows and repeated forecast groups.

Effective sample size:

The current `n=19` is an operational count, not an independent sample
size.

RE-PRED future work should move from qualitative warning to quantitative
effective-sample-size estimation where feasible.

Until then, predictive claims must remain conservative.

Live tracking log:

Future live tracking should be append-only.

The minimum record should include:

-   timestamp;
-   model commit or version;
-   dataset cutoff;
-   snapshot inputs;
-   forecast horizon;
-   forecast summary;
-   forecast distribution or match-return distribution;
-   selected matches;
-   Evidence Quality state;
-   Regime Comparability state if available;
-   Personal Capacity state if available;
-   combined posture ceiling if available;
-   human approval state if available;
-   whether any action was taken;
-   later realized outcome when available.

The purpose is to know, years later, exactly what was forecast, by which
model, using which data, and under which governance state.

No gate relaxation in RE-PRED.1:

RE-PRED.1 does not authorize any relaxation of Evidence Quality, Regime
Comparability, Personal Capacity or Capital Posture.

It does not set numeric thresholds.

It does not change the current posture inference.

If future predictive evidence remains weak:

The project must treat permanent weak predictive evidence as a named
design branch, not as an implementation failure.

If predictive validity never becomes demonstrable, the Research Engine
may remain a descriptive and contextual evidence system rather than a
forecast-backed deployment engine.

In that scenario, any future capital deployment would need a different
transparent justification framework. It should not pretend to be backed
by predictive validation that does not exist.

RE-PRED.1 does not decide that branch.

It records it as a probable architectural question for future
constitutional governance if the evidence does not improve.

Boundary:

-   No code changed.
-   No new calculations executed.
-   No new metrics introduced.
-   No target frozen yet.
-   No model frozen yet.
-   No holdout created yet.
-   No live-tracking log implemented.
-   No predictive-validity claim made.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.2 — Predictive target audit

RE-PRED.2 audits the predictive target currently implemented by code.

It does not freeze the target.

It does not change the target.

It is documentation-only.

No code changed.

No new validation claim is made.

Audited code path:

-   `engine/drawdown_engine.py`;
-   `engine/evidence_engine.py`;
-   `engine/validation_harness.py`;
-   `engine/validation_metrics.py`;
-   `engine/research_pipeline.py`;
-   `models/evidence.py`;
-   `models/episode.py`;
-   `models/observable_episode.py`;
-   `tests/verify_validation_metrics.py`.

Current target field:

The operative five-year predictive target is:

    future_return_5y

It is stored on `Episode` and `ObservableEpisode`.

It is generated by:

    enrich_future_returns()

using:

    _future_return(df, bottom_date, years=5)

Current target formula:

`_future_return()` computes:

    (p1 / p0) ** (1 / years) - 1

Therefore the current target is an annualized CAGR, not a cumulative
multi-year return.

Return unit:

Returns are decimal annualized rates.

Example:

    0.1138667635

means approximately 11.39% annualized, not 11.39% cumulative over five
years.

Price source:

The code uses:

    Price.1

from the Shiller data frame.

`P` is used to detect drawdowns and recovery against historical price
levels.

`Price.1` is used for:

-   future returns;
-   pre-crash return;
-   rolling volatility input.

The code comment labels `_future_return()` as:

    CAGR real anualizado. No retorno acumulado.

Based on the Shiller column layout inspected in the source file,
`Price.1` appears to be the real total-return price index rather than
raw nominal price. RE-PRED.2 does not rename or re-map that column; it
records the current implementation and leaves formal source-column
aliasing for future work if needed.

Date anchors:

The start anchor is:

    bottom_date

For p0, `_future_return()` selects the first row with:

    Date >= bottom_date

For p1, it sets:

    future_date = bottom_date + years

and selects the first row with:

    Date >= future_date

The realized-return window therefore starts at the drawdown bottom and
ends at the first available Shiller observation at or after the target
horizon date.

Missing future returns:

`_future_return()` returns `None` when:

-   no future row exists at or after `bottom_date + years`;
-   no bottom row exists at or after `bottom_date`;
-   p0 is `None`;
-   p0 is zero.

There is no imputation.

There is no conversion of missing outcome to 0.0.

This is consistent with the Evidence rule that absence of evidence is
`None`, never zero.

Evidence forecast surface:

`EvidenceEngine.build(matches, years=5)` reads:

    future_return_5y

from each selected match.

It drops `None` values.

It sorts the realized return sample.

It sets:

-   `average_return`;
-   `median_return`;
-   `worst_return`;
-   `best_return`;
-   `positive_probability`;
-   Evidence v2 return-shape fields.

`median_return` is calculated through `percentile_from_sorted(returns,
0.50)`, not through `statistics.median()`.

The forecast used by current Research Validation is:

    evidence.median_return

Current validation actual:

`ValidationHarness.evaluate_episode(episode, years=5)` reads:

    actual = episode.future_return_5y

The harness then reconstructs the historical snapshot at the episode
bottom, builds comparable matches through the same
ObservableUniverse -> SimilarityEngine -> EvidenceEngine path, and
compares:

    forecast = evidence.median_return
    actual = episode.future_return_5y

Evaluability:

A validation record is evaluable only when both values exist:

    forecast is not None and actual is not None

Records with missing actual or missing forecast remain visible in the
harness but do not enter MAE, directional hit-rate or rank correlation.

Current validation surfaces:

The current metrics evaluate the same target in different ways:

-   MAE evaluates absolute error between forecast CAGR and realized CAGR;
-   directional hit-rate evaluates sign agreement, excluding zero
    forecast or zero actual;
-   rank correlation evaluates whether higher forecast CAGR ranks
    correspond to higher realized CAGR ranks.

The current validation does not evaluate:

-   excess return versus a baseline;
-   cumulative five-year return;
-   nominal return;
-   price-only return;
-   total-return attribution separately;
-   calibration by forecast quantile.

Current horizon:

The shared Research pipeline defaults to:

    horizon_years = 5

Evidence supports other stored horizons, but the current canonical
Research Validation metrics and SOP evidence surface use the five-year
horizon.

Current mature-outcome status:

The current dataset contains 23 drawdown episodes.

At the five-year horizon:

-   21 episodes have realized `future_return_5y`;
-   19 records are evaluable by the Research Validation harness;
-   2022.10 has no realized five-year return yet;
-   2025.04 has no realized five-year return yet.

Important distinction:

RE-PRED.2 audits the implemented target.

It does not decide that this target is the correct future governance
target.

Future work must explicitly decide whether the frozen predictive target
should remain:

    annualized real total-return CAGR from drawdown bottom to five years

or whether SOP governance requires a different target.

If a different target is chosen, that must be a numbered architectural
change, not a silent validation change.

Open questions:

-   Should `Price.1` be formally aliased in code or documentation as the
    real total-return price index?
-   Should governance evaluate real total return, real price return,
    nominal return, or excess return?
-   Should the target remain annualized CAGR or become cumulative return?
-   Should target windows use first observation at or after horizon date,
    nearest observation, or exact monthly alignment?
-   Should missing future outcomes remain `None` only, or should live
    tracking distinguish "not yet matured" from "missing data"?
-   Should future validation evaluate the same target for all gates, or
    should Evidence Quality, Regime Comparability and Capital Posture use
    different target surfaces?

Boundary:

-   No code changed.
-   No target frozen.
-   No metric changed.
-   No validation result changed.
-   No baseline introduced.
-   No holdout introduced.
-   No live-tracking log introduced.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

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

Assessment Engine v2 — opened with RE-029.1 scope audit; boundary
audited in RE-029.2; shared Research pipeline consumed in RE-029.3;
public helpers verified in RE-029.4; confidence-to-posture gate
boundary defined in RE-029.5; Evidence Quality Gate dimensions defined
in RE-029.6; calibration boundary documented in RE-029.7; future
implementation scope bounded in RE-029.8; first-code acceptance
criteria documented in RE-029.9.

RE-029.1 defines the first governance boundary for Assessment / SOP:
four capital-intensity postures, one orthogonal `Blocked` veto, three
initial invalidation gates, and mandatory human approval for capital
deployment. It deliberately does not define numeric thresholds or
automatic actions.

RE-029.2 audits the current `AssessmentEngine`: temporal safety is
already resolved, but it still duplicates the Research pipeline locally
and computes confidence through a separate `ValidationEngine` path.
RE-DOC-004 records two follow-up boundaries before trigger design:
`drawdown_zone()` is market severity, not capital posture; and stepped
error tolerance remains pending until SOP governance defines trigger
logic.

RE-029.3 makes `AssessmentEngine` consume the shared
`build_research_result()` pipeline, closing the Research source-of-truth
duplication identified in RE-029.2. RE-029.4 verifies the public helper
outputs after that refactor. RE-029.5 defines the connection pattern
between confidence / evidence quality and capital posture: gate /
ceiling, not weighted input. Gates combine by veto / most restrictive
ceiling across evidence quality, regime comparability and personal
capacity. The current `AssessmentEngine` confidence score is explicitly
excluded from SOP capital gates while stability remains hardcoded.
RE-029.6 defines the Evidence Quality Gate dimensions: coverage,
consistency, diversity, independence / dispersion and predictive
validation status. It also records the initial conservative stance:
current Research Validation is reproducible but not yet predictive
validation, because hit-rate is not discriminating and rank correlation
is weakly negative. RE-029.7 defines the calibration boundary: the gate
is fail-closed, movement beyond conservative requires pre-registered
criteria, current validation metrics do not suffice, `confidence.score`
is prohibited even as a temporary proxy, and aggregate Research
Validation metrics must not be confused with local snapshot quality.
RE-029.8 defines the first future implementation scope: create a
separate `EvidenceQualityGate` structure only, keep local snapshot
inputs separate from global model-validation state, preserve at least
three conceptual output states (`not measurable`, conservative and a
future less-restrictive state), clarify that `stability` is not one of
the five official Evidence Quality dimensions today, and keep the gate
unwired from `run.py` and `DecisionEngine`. Remaining Assessment / SOP
work is executable thresholds, gate calibration, regime comparability,
personal capacity and capital posture mapping. RE-029.9 defines the
acceptance criteria for the first isolated gate PR: it must be testable,
fail-closed with today's incomplete inputs, explain the specific cause
of any cap, treat `None` or incomplete inputs as `not measurable`, avoid
Frozen Core, and remain unwired from the operative flow.

RE-030.1 implements that first isolated gate structure. It adds
`engine/evidence_quality_gate.py` and
`tests/verify_evidence_quality_gate.py`. The gate separates local
snapshot inputs from global model-validation state, returns discrete
states with explanations, defaults fail-closed and remains outside
`run.py`, `DecisionEngine`, `AssessmentEngine` and `ValidationEngine`.
No thresholds or capital posture mapping exist yet.

RE-030.2 adds `build_local_evidence_quality_inputs(evidence)`, the first
adapter from real Research output into local Evidence Quality inputs.
The adapter uses `Evidence` as the single source of truth for matches,
calculates coverage from usable returns (`return_count`, not selected
match count), calculates consistency at `evidence.horizon_years`, and
keeps independence / dispersion unmeasured. Current real local values:
coverage=0.9, consistency=0.9518456229064439, diversity=0.6. With
global model-validation state still not validated, the gate returns
`not measurable` for today's snapshot.

RE-031.1 opens the Regime Comparability Gate as a separate governance
boundary. It defines regime comparability as a gate / ceiling, not a
weighted input, and separates it from both Evidence Quality and
`AssessmentEngine.drawdown_zone()`. No code, thresholds, regime taxonomy
or capital posture mapping exist yet. Current Regime Comparability state
is not measurable.

RE-032.1 opens the Personal Capacity classification boundary. It does
not assume Personal Capacity is a parallel computable gate. The first
classification question is whether Personal Capacity belongs as a gate,
as a Human Approval prerequisite, or as a mixed control. The document
separates verifiable personal facts from attested judgement and records
the special unreliability of crisis-time drawdown tolerance revisions.
No code, thresholds, personal-capacity taxonomy or capital posture
mapping exist yet.

RE-033.1 formalizes Capital Posture vocabulary and ordering:
`Conserve`, `Prepare`, `Deploy Partially`, `Deploy Aggressively`, with
`Blocked` as an orthogonal veto. It separates internal gate-state mapping
from multi-gate combination. Current `not measurable` and `conservative`
gate states both cap at `Conserve`, with different explanations. Given
current known gate states, the documentation-level capital posture
ceiling is `Conserve`. No posture engine or gate-combination logic exists
yet.

RE-034.1 defines the gate-combination boundary. Combination consumes
discrete posture ceilings and `Blocked` flags, not scores. `Blocked`
wins first; otherwise the most restrictive ordered ceiling wins.
RE-034.1 separates non-deployment postures (`Conserve`, `Prepare`) from
deployment postures (`Deploy Partially`, `Deploy Aggressively`). Evidence
Quality not measurable blocks deployment but may still allow `Prepare`.
Unavailable Regime Comparability and unavailable / unclassified Personal
Capacity cap at `Conserve`. Given current states, the
documentation-level final posture ceiling remains `Conserve`.

RE-034.2 defines first-code acceptance criteria for the future isolated
gate-combination module. The required tests must pin the current real
state to `Conserve`, verify that `Blocked` wins first, verify that the
most restrictive ceiling wins, protect the Evidence Quality
`not measurable -> Prepare` exception from regression, prove that
Evidence Quality does not override more restrictive gates, and require
traceable explanations naming the limiting gate or control.

RE-034.3 adds the isolated gate-combination module and verification test.
RE-034.4 documents its status: `engine/gate_combination.py` exists,
`tests/verify_gate_combination.py` passes, and the module remains outside
the operative flow. It provides discrete posture constants, `Blocked`
precedence, most-restrictive ceiling selection, and traceable limiting
explanations. It does not implement a posture engine, thresholds,
protocol rules, Human Approval or runtime wiring.

RE-PRED.1 opens the predictive-validity boundary. It makes no new
validation claim and runs no new calculation. It defines the future
contract for any predictive claim: audit the actual target before
freezing it, freeze the model before holdout or live tracking,
separate historical backtest from prospective holdout and live tracking,
predefine baselines, report uncertainty under dependence-aware methods,
and treat permanent weak predictive evidence as a named design branch
rather than an implementation bug.

RE-PRED.2 audits the currently implemented predictive target. The
operative target is `future_return_5y`: annualized five-year CAGR from
drawdown bottom, calculated as `(p1 / p0) ** (1 / years) - 1` using
Shiller `Price.1`. Evidence forecasts use `Evidence.median_return` over
matched `future_return_5y` values, and Research Validation compares that
forecast against each episode's realized `future_return_5y`. Missing
future outcomes remain `None`, never 0.0. RE-PRED.2 does not freeze or
change the target.

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

## Version 1.41

-   Added RE-PRED.2: Predictive target audit.
-   Audited the current implemented target field: `future_return_5y`.
-   Documented that `_future_return()` computes annualized CAGR:
    `(p1 / p0) ** (1 / years) - 1`.
-   Documented that the current target uses Shiller `Price.1`.
-   Documented that the start anchor is `bottom_date` and the end anchor
    is the first available observation at or after `bottom_date + years`.
-   Documented missing-outcome behavior: future returns remain `None`
    when no mature future row exists or p0 is unavailable / zero.
-   Documented that current Evidence forecasts use
    `Evidence.median_return` over matched `future_return_5y` values.
-   Documented that current Research Validation compares
    `evidence.median_return` against each episode's realized
    `future_return_5y`.
-   Clarified that RE-PRED.2 audits the implemented target but does not
    freeze it or claim it is the final governance target.
-   No code changed.

## Version 1.40

-   Added RE-PRED.1: Predictive validity boundary.
-   Clarified that RE-PRED.1 makes no new predictive-validity claim and
    executes no new calculation.
-   Required a future predictive-target audit before freezing the target:
    return field, nominal vs real, price vs total return, horizon,
    date anchors, missing-data treatment and validation surface.
-   Separated future predictive claims into ranking validity,
    calibration validity and directional validity.
-   Separated validation surfaces into existing historical backtest,
    prospective holdout from freeze date and live tracking.
-   Documented that a retroactive clean holdout is not available by
    default because the Similarity Engine was designed while exposed to
    the historical dataset.
-   Required model freeze before any holdout or live-tracking result can
    count as clean predictive evidence.
-   Required future baseline comparisons to be pre-defined.
-   Required future uncertainty treatment to respect known dependence
    rather than assuming i.i.d. observations.
-   Defined minimum fields for a future append-only live-tracking log.
-   Recorded permanent weak predictive evidence as a named future design
    branch, not an implementation failure.
-   No code changed.

## Version 1.39

-   Added RE-034.4: Gate combination implementation status.
-   Documented that RE-034.3 added `engine/gate_combination.py` and
    `tests/verify_gate_combination.py`.
-   Recorded verified command:
    `python3 tests/verify_gate_combination.py`.
-   Recorded verified output: `GATE COMBINATION : STABLE`.
-   Updated Component Status from boundary-only to isolated
    Gate Combination Layer v0.
-   Clarified that the layer exists and passes verification but remains
    outside the operative flow.
-   Clarified that no Capital Posture Engine, thresholds, protocol rules,
    Human Approval implementation, live gate adapters or runtime wiring
    exist.
-   Preserved the current posture inference:
    `min(Prepare, Conserve, Conserve) = Conserve`.
-   No code changed in RE-034.4.

## Version 1.38

-   Added RE-034.2: Gate combination first-code acceptance criteria.
-   Required a regression test for the current real state:
    Evidence Quality `not measurable`, Regime Comparability
    `not measurable`, Personal Capacity unavailable / unclassified and
    `Blocked=false` must combine to `Conserve`.
-   Required a test proving that Evidence Quality does not override more
    restrictive gates.
-   Required a test proving that Evidence Quality `not measurable` caps
    at `Prepare`, not `Conserve`, when the other gates allow less
    restrictive posture.
-   Required unavailable Regime Comparability and unavailable Personal
    Capacity to cap at `Conserve`.
-   Required combined explanations to name the specific limiting gate or
    control.
-   Repeated first-code isolation boundaries: no `run.py`,
    `DecisionEngine`, `AssessmentEngine`, `ValidationEngine` or Frozen
    Core wiring.
-   No code changed.

## Version 1.37

-   Added RE-034.1: Gate combination boundary.
-   Defined combination inputs as discrete gate outputs: gate name,
    internal state, posture ceiling, `Blocked` flag and explanation.
-   Prohibited combination logic from consuming raw scores.
-   Defined combination order: `Blocked` wins first; otherwise the most
    restrictive ordered posture ceiling wins.
-   Separated non-deployment postures (`Conserve`, `Prepare`) from
    deployment postures (`Deploy Partially`, `Deploy Aggressively`).
-   Documented that Evidence Quality `not measurable` blocks deployment
    but does not necessarily block `Prepare`.
-   Documented the intentional asymmetry: unavailable Regime
    Comparability and unavailable / unclassified Personal Capacity cap
    at `Conserve`, while Evidence Quality `not measurable` caps at
    `Prepare`.
-   Added current-state inference:
    `min(Prepare, Conserve, Conserve) = Conserve`.
-   Clarified that Personal Capacity is included only as an unavailable
    placeholder until RE-032.1 classification is resolved.
-   No code changed.

## Version 1.36

-   Added RE-033.1: Capital Posture vocabulary and ordering.
-   Formalized ordered posture states from most restrictive to least
    restrictive: `Conserve`, `Prepare`, `Deploy Partially`,
    `Deploy Aggressively`.
-   Documented `Blocked` as an orthogonal veto outside the ordered
    posture scale.
-   Defined each posture state in terms of capital consequences.
-   Tightened `Prepare`: it may authorize planning and preparing Dry
    Powder capacity, but not selling existing strategic positions unless
    a future Dry Powder Protocol explicitly allows it.
-   Separated gate-internal state mapping from multi-gate posture-ceiling
    combination.
-   Documented that both `not measurable` and `conservative` currently
    cap at `Conserve`, while preserving different explanations.
-   Added current-state documentation inference: Evidence Quality not
    measurable, Regime Comparability not measurable and Personal Capacity
    unavailable imply `Conserve`.
-   Recorded the open question of whether measurable Evidence Quality is
    a prerequisite for any posture above `Conserve`.
-   No code changed.

## Version 1.35

-   Added RE-032.1: Personal Capacity classification boundary.
-   Framed the primary question as whether Personal Capacity is a
    parallel gate, a Human Approval requirement or a mixed control.
-   Defined Personal Capacity as the question of whether the person can
    responsibly assume risk now, separate from market opportunity,
    Evidence Quality and Regime Comparability.
-   Required future Personal Capacity work to separate verifiable facts
    from attested judgement.
-   Listed candidate verifiable facts such as liquidity, cash needs,
    obligations, debt service, income concentration, portfolio
    concentration, emergency reserve and time horizon constraints.
-   Listed candidate attested judgements such as perceived income
    stability, drawdown tolerance, ability to avoid forced selling and
    psychological capacity to hold through stress.
-   Recorded drawdown tolerance as especially unreliable under crisis
    pressure, and stated that pre-registered attestations should carry
    more weight than crisis-time revisions.
-   Documented that gate-combination logic cannot be finalized until
    Personal Capacity is classified.
-   No code changed.

## Version 1.34

-   Added RE-031.1: Regime Comparability Gate boundary.
-   Defined regime comparability as a gate / ceiling that asks whether
    current market conditions are structurally comparable to the
    historical evidence sample.
-   Separated Regime Comparability from Evidence Quality.
-   Separated Regime Comparability from `AssessmentEngine.drawdown_zone()`,
    which remains a market severity taxonomy, not a comparability gate.
-   Listed candidate future dimensions: valuation, inflation, interest
    rates, earnings / margins, volatility, liquidity / credit, policy /
    intervention and market structure.
-   Documented current state as not measurable: no code, no inputs, no
    taxonomy, no thresholds and no capital posture mapping.
-   Prohibited shortcuts such as using drawdown zone, expected return,
    Evidence Quality or the existence of similarity matches as regime
    comparability proxies.
-   No code changed.

## Version 1.33

-   Added RE-030.2: local Evidence Quality input adapter.
-   Added `build_local_evidence_quality_inputs(evidence)` to translate
    real `Evidence` into `LocalEvidenceQualityInputs`.
-   Kept `Evidence` as the single source of truth for the selected match
    set; no separate `matches` argument is accepted.
-   Calculated local coverage from usable returns:
    `min(evidence.return_count / 10.0, 1.0)`.
-   Verified current local coverage is 0.9, because today's snapshot has
    10 selected matches but 9 usable realized returns.
-   Calculated local consistency at `evidence.horizon_years`, avoiding
    the legacy `ValidationEngine` 3-year default horizon.
-   Verified current local consistency is 0.9518456229064439 and current
    local diversity is 0.6.
-   Verified today's real local inputs plus non-validated global state
    return `not measurable`.
-   Clarified that RE-030.2 is no longer zero-dependency, because it
    reads `Evidence` and its matches, but remains isolated from the
    operative flow.
-   Confirmed no thresholds, no capital posture mapping, no automatic
    recommendation and no operative authority.
-   Frozen Core unchanged.

## Version 1.32

-   Added RE-030.1: isolated Evidence Quality Gate.
-   Added `engine/evidence_quality_gate.py` with local/global input
    separation, discrete state output and specific explanations.
-   Added `tests/verify_evidence_quality_gate.py` as focused
    verification for the isolated gate.
-   Verified today's available inputs return `not measurable` or
    `conservative`, never a less-restrictive state.
-   Verified incomplete inputs / `None` values return `not measurable`.
-   Verified fully measured but not yet authorized inputs return
    `conservative`.
-   Confirmed the gate is not wired into `run.py`, `DecisionEngine`,
    `AssessmentEngine` or `ValidationEngine`.
-   Confirmed no thresholds, no capital posture mapping, no automatic
    recommendation and no operative authority.
-   Frozen Core unchanged.

## Version 1.31

-   Added RE-029.9: Evidence Quality Gate first-code acceptance
    criteria.
-   Documented likely future implementation and verification surfaces:
    an isolated gate module and a focused gate verification test.
-   Required the first future gate PR to compile and test in isolation
    without wiring into `run.py` or `DecisionEngine`.
-   Required tests to assert that today's incomplete inputs produce
    `not measurable` or `conservative`, never a less-restrictive state.
-   Required incomplete inputs or `None` values to produce
    `not measurable`, not crashes or assumed default scores.
-   Required explanations to name the specific channel or dimension
    causing the cap.
-   Made Frozen Core modification a rejection criterion for the first
    gate PR unless a separate numbered exception is authorized first.
-   Reaffirmed non-goals: no thresholds, no capital posture mapping, no
    automatic recommendations, no runtime wiring and no use of aggregate
    Research Validation metrics as local snapshot quality.
-   No code changed.

## Version 1.30

-   Added RE-029.8: Evidence Quality Gate implementation scope.
-   Documented that the first future implementation should create
    structure only: no thresholds, no capital posture rules and no
    operative wiring.
-   Prohibited first implementation changes to
    `AssessmentEngine.confidence().score`, `ValidationEngine`, `run.py`
    and `DecisionEngine`.
-   Required separate input channels for local snapshot evidence quality
    and global model-validation state.
-   Clarified that RE-029.6 defines five official Evidence Quality
    dimensions and that `stability` is not currently one of them.
-   Distinguished independence / dispersion from stability.
-   Required at least three conceptual output states: not measurable,
    conservative and a future less-restrictive state with no finalized
    name yet.
-   Reaffirmed fail-closed behaviour and isolation from the operative
    flow until later threshold, calibration and approval iterations.
-   No code changed.

## Version 1.29

-   Added RE-029.7: Evidence Quality Gate calibration boundary.
-   Defined conservative gate posture as fail-closed, discrete and
    evidence-led.
-   Documented that movement toward neutral requires pre-registered
    criteria, fully measured dimensions, baseline comparisons and
    explicit treatment of sample dependence.
-   Recorded why current Research Validation metrics do not suffice to
    relax the conservative ceiling: MAE lacks a naive baseline,
    hit-rate is not discriminating, rank correlation is weakly negative
    and `n=19` is not an independent sample-size claim.
-   Classified current dimension readiness: coverage and diversity are
    genuine but weak, consistency is real but not yet governance-grade,
    stability is unavailable, and independence / dispersion plus
    predictive validation status are not yet local gate measurements.
-   Prohibited use of `AssessmentEngine.confidence().score` as a gate or
    temporary proxy.
-   Prohibited treating aggregate Research Validation metrics as local
    snapshot evidence quality.
-   Recorded an open governance question about whether exception
    iterations written during the crisis that motivates them require
    extra safeguards.
-   No code changed.

## Version 1.28

-   Added RE-029.6: Evidence Quality Gate dimensions.
-   Defined coverage, consistency, diversity, independence / dispersion
    and predictive validation status as the documentary dimensions of
    evidence quality.
-   Documented that the gate starts conservative because current Research
    Validation does not yet demonstrate predictive discrimination:
    directional hit-rate is not discriminating and rank correlation is
    weakly negative.
-   Reaffirmed that `AssessmentEngine.confidence().score` must not be
    used as the Evidence Quality Gate while `stability=1.0` remains
    hardcoded and sample independence / dispersion is not captured.
-   Clarified what Evidence Quality may limit: maximum capital posture,
    Dry Powder deployment aggressiveness and Portfolio Reallocation
    aggressiveness.
-   Clarified what Evidence Quality may not do: create Risk ON posture,
    override other gates or compensate weak evidence with attractive
    expected return.
-   No code changed.

## Version 1.27

-   Added RE-029.5: confidence-to-posture gate boundary.
-   Defined evidence quality / confidence as a gate and posture ceiling,
    not a weighted input.
-   Defined gate combination as veto / most restrictive ceiling across
    evidence quality, regime comparability and personal capacity.
-   Explicitly excluded current `AssessmentEngine` confidence score from
    SOP capital gates while `stability=1.0` remains hardcoded.
-   No code changed.

## Version 1.26

-   Added RE-029.3: `AssessmentEngine` now consumes the shared
    `build_research_result()` Research pipeline instead of rebuilding
    Snapshot / Observable Universe / Similarity / Evidence locally.
-   Documented that source-of-truth duplication is resolved for
    Assessment evidence production.
-   Added RE-029.4: verified `AssessmentEngine` public helper outputs
    after the refactor.
-   Recorded verified outputs: `drawdown_zone=NORMAL`,
    `expected_return_5y=0.113866763521769`,
    `upside_potential=0.132855208016562`,
    `downside_risk=-0.010919489332530`, `matches=10`.
-   Clarified that confidence remains a separate unresolved path through
    `ValidationEngine`, including hardcoded stability, and must not drive
    SOP capital gates yet.

## Version 1.25

-   Added RE-DOC-004: Assessment / SOP boundary follow-up notes.
-   Clarified that `AssessmentEngine.drawdown_zone()` is a market
    severity taxonomy, not a capital posture taxonomy.
-   Recorded stepped error tolerance as pending SOP governance work:
    conservative by default, aggressive only when independent signals
    converge.
-   Reaffirmed that no thresholds, trigger logic or automatic capital
    decisions are introduced in this documentation pass.
-   No code changed.

## Version 1.24

-   Added RE-029.2: `AssessmentEngine` boundary audit.
-   Verified that `AssessmentEngine` is not called by `run.py`.
-   Verified that the older temporal-safety issue is already resolved:
    it uses `ObservableUniverse(dataset, as_of=snapshot.date)`.
-   Documented the remaining issue: `AssessmentEngine` still duplicates
    the Research pipeline locally instead of consuming
    `build_research_result()` / `ResearchResult`.
-   Documented that `AssessmentEngine` computes confidence through a
    separate `ValidationEngine` path, including hardcoded stability.
-   Clarified the v2 boundary: Assessment may interpret evidence quality,
    fragility and applicability, but must not decide capital posture,
    deployment size, dry-powder usage or portfolio reallocation.
-   No code changed.

## Version 1.23

-   Added RE-029.1: Assessment / SOP governance scope audit.
-   Defined the primary objective hierarchy: avoid irreversible error,
    preserve real capital, then maximize long-term return.
-   Defined dry powder as deployable investable liquidity, not merely
    literal cash.
-   Separated the Dry Powder Protocol from the Portfolio Reallocation
    Protocol: increasing net exposure is not the same decision as
    rotating between risk assets.
-   Established four capital-intensity postures: Conserve, Prepare,
    Deploy partially and Deploy aggressively.
-   Established `Blocked` as an orthogonal veto flag, not a fifth
    intensity level.
-   Added three initial invalidation gates: evidence quality, regime
    comparability and personal capacity.
-   Required explicit human approval with timestamp for partial or
    aggressive deployment.
-   No code changed.

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
