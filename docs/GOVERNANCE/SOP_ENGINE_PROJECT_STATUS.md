# SOP ENGINE PROJECT STATUS

**Version:** 1.64\
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

# Execution State (as of RE-032.2)

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
  Personal Capacity     Classified in RE-032.2 as a mixed control --
  Boundary              Armando's explicit decision, not inferred. Still
                        no code. Not called by run.py, DecisionEngine,
                        AssessmentEngine or any gate. Verifiable-facts
                        channel (liquidity, debt service, concentration,
                        etc.) is the future computable-gate half --
                        participates in gate combination via min(), same
                        ceiling-only pattern as Evidence Quality and
                        Regime Comparability. Attested-judgement channel
                        (drawdown tolerance, psychological capacity,
                        etc.) is the Human Approval half -- never enters
                        gate-combination math, never an automatic
                        ceiling. RE-032.1's two-channel separation is
                        preserved by construction, not merged into one
                        score.
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
                        RE-PRED.3 defines the provisional target-freeze
                        boundary while leaving source-column semantics
                        not fully verified. RE-PRED.4 verifies that
                        Shiller `Price.1` is Real Total Return Price.
                        RE-PRED.5 defines ordered acceptance criteria
                        for any future definitive target freeze.
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
                        5-year CAGR from `Price.1`, used as both
                        Evidence forecast surface and Research
                        Validation actual. RE-PRED.3 treats that target
                        as the provisional freeze candidate, but does
                        not verify whether `Price.1` is real / nominal
                        or price / total-return. RE-PRED.4 verifies
                        `Price.1` as Real Total Return Price from the
                        source workbook header. RE-PRED.5 records that
                        source-column semantics are verified, but
                        bottom-detection semantics are not yet audited.
                        RE-PRED.6 audits bottom detection and episode
                        boundaries, and records two verified findings:
                        price-basis asymmetry and date-arithmetic
                        duration bug. RE-BUG.1 promotes the duration
                        bug to near-term code-fix priority and defines
                        acceptance criteria. RE-BUG.2 fixes calendar-
                        month duration arithmetic. RE-BUG.3 documents
                        the downstream impact and canonical post-fix
                        metrics. RE-DATA.1 records future Shiller data
                        update automation as a validated-data pipeline,
                        not a blind download. RE-PRED.7 defines the
                        absolute-vs-excess-return boundary: absolute
                        return is the existing descriptive Evidence
                        surface, unchanged; excess return over a
                        primary naive baseline is the future predictive-
                        validity surface, to be implemented in the
                        Research Validation Harness, not in Evidence.
                        RE-PRED.8 defines acceptance criteria for that
                        primary baseline: a point-in-time expanding
                        median of `future_return_5y`, reusing
                        `ObservableUniverse` and bottom_index
                        self-exclusion, evaluated over the same
                        evaluable records already used by the model.
                        It also corrects RE-PRED.7's rank-correlation
                        claim forward: because this baseline varies per
                        episode, it does have rank variation, and its
                        rank correlation is a real, computable
                        comparison against the model's. RE-PRED.9
                        implements that baseline in code:
                        `engine/baseline_harness.py` and
                        `tests/verify_baseline_harness.py`. RE-PRED.10
                        records the canonical baseline values, confirmed
                        under the pinned runtime, and the resulting
                        finding: the model does not beat the primary
                        baseline on any of the three canonical metrics --
                        it ties on directional hit-rate and loses on MAE
                        and rank correlation. Predictive validity is not
                        demonstrated relative to this baseline. RE-PRED.11
                        implements two secondary baselines (zero,
                        mean-reversion) to isolate whether that finding
                        is an artifact of the primary baseline choice --
                        results pending pinned-runtime confirmation.
                        RE-PRED.12 records, as an explicit open question,
                        that no baseline comparison on this evaluated
                        sample addresses whether any excess value is
                        distinguishable from sampling noise given N=19
                        dependent records. RE-PRED.13 records the
                        canonical secondary-baseline values, confirmed
                        under the pinned runtime, and the resulting
                        full-picture finding: the model is not uniformly
                        dominated -- it clearly beats zero and
                        mean-reversion on MAE, ties both on hit-rate, but
                        loses to mean-reversion on rank correlation by a
                        full sign flip. The RE-PRED.10.1 deferral trigger
                        was evaluated explicitly and did not activate.
                        RE-PRED.14 tests the signal-dilution hypothesis
                        registered in RE-PRED.13 by isolating each active
                        SimilarityEngine dimension and does not find
                        support for it: every dimension in isolation
                        remains negative on rank correlation, none close
                        to mean-reversion's positive value. A revised,
                        still-unauthorized hypothesis is registered:
                        nearest-neighbor selection may not preserve
                        monotonic rank order the way a direct function of
                        the query's own value does, regardless of which
                        single dimension drives the selection. RE-PRED.15
                        closes the RE-PRED.12 method gap:
                        `engine/dependence_bootstrap.py` implements a
                        cluster bootstrap over independence clusters built
                        from the union of the RE-025.8 overlapping-outcome-
                        window and RE-025.9 repeated-forecast-group
                        diagnostics, producing dependence-aware confidence
                        intervals for the model, the primary and mean-
                        reversion baselines, and their paired excess --
                        structurally verified outside the pinned runtime
                        only. RE-PRED.16 records the canonical results,
                        confirmed under the pinned runtime: 3 independence
                        clusters (sizes 10, 8, 1), not the 4 seen in the
                        unpinned structural smoke test -- hand-verified
                        against the already-canonical RE-025.8/RE-025.9
                        tables, confirming the pinned result and not the
                        sandbox one. The excess vs. primary baseline on
                        rank correlation is not distinguishable from
                        sampling noise (90% interval [-0.06068, 0.02514],
                        straddles zero); the excess vs. mean-reversion on
                        rank correlation is robust and does not straddle
                        zero (90% interval [-0.94270, -0.34208]) -- the
                        RE-PRED.13 full sign-flip finding survives
                        dependence-aware resampling, the primary-baseline
                        loss does not.

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
                                  operative authority. RE-035.1 closes
                                  both remaining stub inputs:
                                  independence_dispersion_measured is no
                                  longer hardcoded False -- it is computed
                                  from real pairwise outcome-window overlap
                                  across the current match set (same
                                  definition as RE-025.8, applied to a live
                                  query instead of the offline validation
                                  harness). predictive_validation_status
                                  gains a recognized "not demonstrated"
                                  value with a sharper explanation, per the
                                  RE-PRED.10.1 decision not to add a new
                                  top-level gate state. Still not wired
                                  into any operative flow. Still no
                                  thresholds and no capital posture
                                  mapping -- RE-034.1's provisional mapping
                                  remains documentation-only.
  Regime Comparability Gate      Boundary documented in RE-031.1.
                                  RE-036.1 adds the first isolated
                                  implementation:
                                  `engine/regime_comparability_gate.py`.
                                  Three dimensions active (cape,
                                  inflation, interest_rate) -- already
                                  populated in `Context` per episode and
                                  unused by `SimilarityEngine`'s score, so
                                  no new data ingestion was needed.
                                  Strict [min, max] coverage check against
                                  the current match set only (local, not
                                  global), no percentile or margin --
                                  deliberate choice to defer that question
                                  until an actual outlier problem is
                                  observed. Volatility / liquidity /
                                  policy / market-structure dimensions
                                  remain explicitly not measurable -- no
                                  data source exists for them. Still not
                                  wired into run.py, DecisionEngine,
                                  EvidenceQualityGate or
                                  gate_combination. RE-034.1's posture
                                  mapping has no entry yet for this gate's
                                  real states -- that remains a separate,
                                  future governance decision, not a
                                  consequence of this code existing.
                                  Correction to RE-036.1 (RE-DOC-002):
                                  that iteration claimed `inflation`/
                                  `interest_rate` were "already populated
                                  in Context per episode" -- false, both
                                  were hardcoded `None` for every episode
                                  and for today's snapshot's
                                  `interest_rate`. RE-037.1's real
                                  audit dry-run exposed this (both
                                  dimensions read `not measurable`).
                                  RE-038.1 wires both for real, and
                                  additionally corrects `inflation` from
                                  a raw CPI index level (near-monotonic
                                  over a century, would make coverage
                                  fail almost tautologically) to a
                                  trailing 12-month rate
                                  (`InflationRate1Y`).
  Personal Capacity Boundary     Classification boundary documented in
                                  RE-032.1. RE-032.2 resolves the primary
                                  classification question: mixed control,
                                  Armando's explicit decision. Still no
                                  code, no thresholds, no capital posture
                                  mapping implemented -- classification is
                                  not implementation. Verifiable facts ->
                                  future computable gate, combined via
                                  min() like Evidence Quality/Regime
                                  Comparability. Attested judgement ->
                                  Human Approval prerequisite, outside
                                  gate-combination math entirely. This
                                  also answers one of RE-032.1's open
                                  questions directly: Personal Capacity
                                  participates in gate combination AND
                                  sits inside Human Approval -- split by
                                  channel, not either/or.
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
                                  RE-034.5 extends RE-034.1's provisional
                                  ceiling-mapping table with Regime
                                  Comparability's three real states from
                                  RE-036.1: `not comparable` -> `Conserve`;
                                  `comparable` -> `Deploy Aggressively`
                                  (the top of the ordered scale, so this
                                  gate can never itself be the binding
                                  constraint when satisfied -- the actual
                                  ceiling comes from Evidence Quality or
                                  Personal Capacity). Documentation-only;
                                  no code implements this mapping yet.
                                  RE-037.1 implements that mapping in code
                                  for the first time:
                                  `engine/posture_mapper.py` translates
                                  `EvidenceQualityGateResult` and
                                  `RegimeComparabilityGateResult` into
                                  `GateCombinationInput` per RE-034.1/
                                  RE-034.5's tables, and
                                  `evaluate_capital_posture()` combines
                                  the two real gates that exist today via
                                  `combine_gate_outputs()`, unmodified.
                                  Personal Capacity explicitly excluded --
                                  not classified (RE-032.1), no gate
                                  exists -- so this combined posture is
                                  provably optimistic relative to a full
                                  combination, and that gap is stated in
                                  the module, not hidden. Still not wired
                                  into run.py or DecisionEngine; this is
                                  an isolated, read-only composition layer
                                  for audit/dry-run, not the future
                                  Capital Posture Engine. RE-038.1 wires
                                  the previously-stubbed inflation/
                                  interest_rate data this layer depends
                                  on, confirmed under pinned runtime:
                                  cape_covered=False,
                                  inflation_covered=True,
                                  interest_rate_covered=True, state
                                  `not comparable`. RE-039.1 extracts
                                  this same audit dry-run into a
                                  standalone root-level script,
                                  `audit_posture.py`, mirroring run.py's
                                  precedent -- no logic change, just a
                                  way to run the check without the full
                                  test suite.
  Predictive Validity Boundary   Opened in RE-PRED.1. Documentation
                                  only. No code. No new calculations.
                                  No predictive-validity claim. Defines
                                  the future validation contract: target
                                  audit, model freeze, baselines,
                                  holdout policy, uncertainty treatment
                                  and live tracking. RE-PRED.2 audits
                                  the current implemented target.
                                  RE-PRED.3 defines the target-freeze
                                  decision boundary and provisional
                                  freeze candidate. RE-PRED.4 verifies
                                  `Price.1` source-column semantics.
                                  RE-PRED.5 defines target-freeze
                                  acceptance criteria. RE-PRED.6 audits
                                  bottom detection / episode boundaries
                                  and records a verified duration
                                  arithmetic bug affecting Evidence
                                  recovery statistics. RE-BUG.1 defines
                                  acceptance criteria for the future fix.
                                  RE-BUG.2 fixes the bug in code.
                                  RE-BUG.3 records the post-fix canonical
                                  metrics and match set. RE-PRED.7 defines
                                  the absolute-vs-excess-return boundary:
                                  absolute return remains the existing
                                  Evidence descriptive surface; excess
                                  return over a primary naive baseline
                                  becomes the future predictive-validity
                                  surface, computed in the Research
                                  Validation Harness. No baseline value is
                                  computed yet. RE-PRED.8 defines
                                  acceptance criteria for that primary
                                  baseline as a point-in-time expanding
                                  median of `future_return_5y`, reusing
                                  `ObservableUniverse` and bottom_index
                                  self-exclusion, evaluated over the same
                                  evaluable records already used by the
                                  model. It corrects RE-PRED.7 forward:
                                  because this baseline varies per
                                  episode, its rank correlation is a real,
                                  computable comparison, not an undefined
                                  quantity. Still no code and no computed
                                  value. RE-PRED.9 implements the
                                  baseline in code
                                  (`engine/baseline_harness.py`,
                                  `tests/verify_baseline_harness.py`),
                                  reusing `ObservableUniverse` and the
                                  existing MAE / hit-rate / rank
                                  correlation functions unmodified.
                                  Structurally verified (record
                                  alignment, the no-missing-forecast
                                  invariant) outside the pinned runtime
                                  only. RE-PRED.10 records the canonical
                                  baseline values, confirmed under
                                  `RUNTIME : PINNED`: baseline MAE
                                  0.06740858559979 vs model MAE
                                  0.06928793787076 (baseline wins);
                                  baseline hit-rate 0.94736842105263,
                                  identical to the model (tie); baseline
                                  rank correlation -0.23171864780822 vs
                                  model -0.26505171850685 (baseline
                                  wins). The model does not beat the
                                  primary baseline on any of the three
                                  canonical metrics. Predictive validity
                                  is not demonstrated relative to this
                                  baseline. A proposal to formalize a
                                  `NOT_DEMONSTRATED` gate state was
                                  raised and deliberately deferred: it
                                  would rest on one baseline over a
                                  non-independent N=19 sample, and today
                                  it would not change the resulting
                                  posture ceiling (still `Conserve`,
                                  `Prepare` allowed) versus the existing
                                  `not measurable` state. RE-PRED.11
                                  implements two secondary baselines
                                  (zero, mean-reversion) to test whether
                                  the finding is an artifact of the
                                  primary baseline choice, structurally
                                  verified outside the pinned runtime
                                  only. RE-PRED.12 records that
                                  baseline-choice robustness and
                                  sampling-noise robustness are different
                                  questions -- secondary baselines answer
                                  the first, not the second. The
                                  gate-state decision is deferred until
                                  the full three-baseline picture is
                                  confirmed under the pinned runtime.
                                  RE-PRED.13 records that picture,
                                  confirmed: model MAE 0.06929 beats zero
                                  0.12749 and mean-reversion 0.18159
                                  clearly; hit-rate ties all three at
                                  0.94737; rank correlation is where the
                                  model loses -- primary baseline
                                  -0.23172 and mean-reversion +0.26316
                                  both beat the model's -0.26505, the
                                  mean-reversion case a full sign flip.
                                  The RE-PRED.10.1 trigger ("loses to the
                                  full set on a majority of metrics") is
                                  evaluated explicitly and does not
                                  activate -- the model wins MAE against
                                  two of three baselines. `NOT_DEMONSTRATED`
                                  remains deferred. A working hypothesis
                                  is registered, not authorized as fact:
                                  drawdown depth alone may order future
                                  returns better than SimilarityEngine's
                                  multidimensional conditioning, possibly
                                  through signal dilution across
                                  dimensions -- flagged for future
                                  investigation, no SimilarityEngine
                                  change made or authorized. RE-PRED.14
                                  tests that hypothesis, confirmed under
                                  the pinned runtime: no single active
                                  dimension (drawdown -0.19692, duration
                                  -0.24916, speed -0.20327, cape -0.21701,
                                  pre_crash_return_3y -0.26353,
                                  volatility -0.23414) reproduces
                                  mean-reversion's +0.26316 rank
                                  correlation. Signal dilution is not
                                  supported as the explanation. A revised
                                  hypothesis is registered, not
                                  authorized: the gap may be structural
                                  (nearest-neighbor selection vs. a
                                  direct monotonic function), not a
                                  weighting problem. RE-PRED.15
                                  implements a dependence-aware cluster
                                  bootstrap (engine/dependence_bootstrap.py)
                                  answering RE-PRED.12: independence
                                  clusters from the union of RE-025.8 and
                                  RE-025.9, resampled at cluster level,
                                  producing percentile confidence
                                  intervals for the model, both baselines
                                  and their paired excess. RE-PRED.16
                                  records the canonical results, confirmed
                                  under the pinned runtime: 3 independence
                                  clusters, sizes 10/8/1 (not the 4 seen in
                                  the unpinned smoke test -- hand-verified
                                  against RE-025.8/RE-025.9's own canonical
                                  tables, confirming the pinned count).
                                  MAE excess vs. primary baseline is small
                                  but robust (90% CI [-0.00356, -0.00045],
                                  model loses, does not straddle zero); MAE
                                  excess vs. mean-reversion is large and
                                  robust (90% CI [0.08355, 0.14025], model
                                  wins). Hit-rate excess is exactly zero at
                                  every percentile against both baselines
                                  -- the tie holds under resampling, not
                                  just at the point estimate. Rank
                                  correlation excess vs. primary baseline
                                  straddles zero (90% CI [-0.06068,
                                  0.02514]) -- RE-PRED.13's "model loses to
                                  primary on rank correlation" finding is
                                  not distinguishable from sampling noise
                                  given this dependence structure. Rank
                                  correlation excess vs. mean-reversion
                                  does not straddle zero (90% CI [-0.94270,
                                  -0.34208]) -- the full sign-flip finding
                                  is robust, not an artifact of N=19's
                                  dependence.
  Data Update Automation         Planned. RE-DATA.1 records future
                                  Shiller source refresh policy:
                                  downloadable source may be automated
                                  later, but only through validation,
                                  backup, tests and explicit logging.
                                  No downloader exists. Current updates
                                  remain manual.
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

## RE-PRED.3 — Target freeze decision boundary

RE-PRED.3 defines the decision boundary for freezing the predictive
target.

It does not freeze the model.

It does not create a holdout.

It is documentation-only.

No code changed.

Decision:

The currently implemented target remains the provisional freeze
candidate:

    future_return_5y

Defined operationally as:

    annualized 5-year CAGR from drawdown bottom,
    calculated from Shiller `Price.1`,
    using the first available observation at or after bottom_date + 5.

Reason:

The target is already implemented and consumed consistently by:

-   `EvidenceEngine`;
-   the shared Research pipeline;
-   `AssessmentEngine`;
-   Research Validation.

Changing the target before model freeze would create a new divergence
risk between code, validation and documentation.

The correct next step is therefore not to redesign the target silently,
but to treat the implemented target as the provisional candidate while
documenting what remains unresolved.

Not yet verified:

RE-PRED.3 does not claim that `Price.1` is definitively:

-   real rather than nominal;
-   total-return rather than price-only.

RE-PRED.2 established that the code uses `Price.1`.

It did not formally verify the semantic meaning of that column.

The phrase "real total-return" must therefore not be used as a settled
property of the frozen target until the Shiller source-column semantics
are verified.

Required future verification:

Before definitive target freeze, the project must verify the meaning of
`Price.1` by inspecting the official Shiller dataset structure or
another authoritative source for the spreadsheet columns.

The verification must decide whether `Price.1` should be formally
documented as:

-   real price index;
-   real total-return index;
-   nominal price index;
-   nominal total-return index;
-   or another source-specific construct.

Until then, the provisional target should be described as:

    annualized 5-year CAGR from `Price.1`

not as:

    annualized real total-return CAGR

CAGR vs cumulative return:

The provisional target remains annualized CAGR, not cumulative
five-year return.

This preserves consistency with the current code and validation metrics.

However, this choice changes how existing error metrics must be read.

MAE reinterpretation:

The canonical MAE reported by Research Validation is an error over
annualized CAGR.

It is not an error over cumulative five-year return.

Therefore:

    MAE ~= 7.03%

means approximately 7.03 percentage points of annualized-rate error, not
7.03 percentage points of total five-year outcome error.

Over a five-year compounding window, an annualized error can imply a
larger cumulative-outcome difference.

Any future governance discussion must preserve that distinction.

Absolute vs excess return:

RE-PRED.3 does not decide whether predictive validation should ultimately
evaluate absolute return or excess return versus a baseline.

That decision belongs with baseline design.

Until baselines are defined, the provisional target remains the absolute
implemented target:

    future_return_5y

Bottom-date anchor:

The provisional start anchor remains:

    bottom_date

This is consistent with the current Research Validation harness, which
asks what the system would have forecast at the drawdown bottom.

RE-PRED.3 does not authorize changing the anchor to peak date, recovery
date, signal date or action date.

Maturity vs missingness:

The code currently represents unavailable future outcomes as `None`.

That remains correct.

Future live tracking should distinguish:

-   not yet matured;
-   structurally missing data;
-   unavailable because of source failure.

RE-PRED.3 does not implement that distinction.

Freeze status:

The target is not definitively frozen.

It is designated as the provisional freeze candidate.

Definitive target freeze requires at minimum:

-   verification of `Price.1` semantics;
-   explicit decision on annualized vs cumulative return;
-   explicit decision on absolute vs excess return;
-   explicit decision on bottom-date anchor;
-   explicit missing-outcome taxonomy for live tracking;
-   numbered documentation recording the freeze.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No model frozen.
-   No holdout created.
-   No baseline introduced.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.4 — Source column semantics verification

RE-PRED.4 verifies the semantic meaning of the Shiller source column
used by the current predictive target.

It is documentation-only.

No code changed.

Verified source:

The verification was performed against the real project file:

    data/raw/shiller.xlsx

using the workbook header rows that `shiller_loader.py` skips with:

    header=7

The inspected header area was:

    rows 4-8

No merged cells were present in that header area, so each header label
belongs to its exact column.

Verified column mapping:

Column H is loaded by pandas as:

    Price

Its stacked header labels are:

    row 7: Real
    row 8: Price

Therefore column H is:

    Real Price

Column J is loaded by pandas as:

    Price.1

because the visible row-8 label `Price` is duplicated and pandas
deduplicates the second occurrence.

Its stacked header labels are:

    row 5: Real
    row 6: Total
    row 7: Return
    row 8: Price

Therefore column J / `Price.1` is:

    Real Total Return Price

Result:

The inference recorded in RE-PRED.2 is now verified.

`Price.1` is the Shiller Real Total Return Price column.

Current predictive target semantics:

The currently implemented target:

    future_return_5y

is therefore:

    annualized real total-return CAGR
    from drawdown bottom
    over the five-year horizon
    using Shiller Real Total Return Price

This confirms:

-   real rather than nominal;
-   total return rather than price-only;
-   annualized CAGR rather than cumulative return.

What remains provisional:

RE-PRED.4 verifies source-column semantics.

It does not definitively freeze the predictive target.

It does not decide whether SOP governance should ultimately prefer:

-   absolute return or excess return;
-   annualized CAGR or cumulative return;
-   bottom-date anchor or another action anchor.

Those decisions still require numbered future iterations.

Documentation correction:

Future references may describe the current implemented target as:

    annualized real total-return CAGR from drawdown bottom

They should still distinguish:

-   current implemented target;
-   provisional freeze candidate;
-   definitive frozen target.

MAE interpretation:

The RE-PRED.3 MAE reinterpretation remains valid.

The canonical MAE is error over annualized real total-return CAGR, not
cumulative five-year real total return.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No metric changed.
-   No validation result changed.
-   No baseline introduced.
-   No holdout introduced.
-   No live-tracking log introduced.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.5 — Target freeze acceptance criteria

RE-PRED.5 defines acceptance criteria for any future definitive target
freeze.

It does not freeze the target.

It does not freeze the model.

It is documentation-only.

No code changed.

Purpose:

The project must not freeze a predictive target just because the current
implementation already exists.

It may use the implemented target as the provisional freeze candidate,
but definitive freeze requires an ordered set of decisions and
verifications.

Ordered dependency structure:

The target-freeze criteria are not a flat checklist.

They have dependencies.

Future work must respect this order.

1.  Target mechanics and semantics.

    The project must first verify what the target means mechanically and
    economically.

    Already verified:

    -   `future_return_5y` uses `Price.1`;
    -   `Price.1` is Shiller Real Total Return Price;
    -   the return is annualized CAGR;
    -   the horizon is five years;
    -   missing mature outcomes remain `None`, never 0.0.

    Not yet audited:

    -   how `bottom_date` is selected;
    -   how drawdown episodes are detected;
    -   how episode start, bottom and recovery are delimited;
    -   whether the bottom-detection algorithm is the correct target
        anchor for predictive governance.

    Therefore "target semantically verified" is not fully complete yet.
    Source-column semantics are verified; bottom-detection semantics are
    not.

2.  Target unit and horizon decision.

    The project must decide whether the definitive target remains:

        annualized real total-return CAGR over five years

    or whether governance requires a different unit or horizon.

    This must be decided before baselines are designed.

3.  Absolute vs excess-return decision.

    The project must decide whether predictive validation evaluates:

    -   absolute realized return; or
    -   excess return over a baseline.

    This decision must come before baseline design.

    A baseline used only for comparison is not the same as a baseline
    subtracted from the target.

4.  Baseline design.

    Baselines may only be defined after the absolute-vs-excess decision.

    If the target remains absolute return, baselines are comparators.

    If the target becomes excess return, a baseline becomes part of the
    target construction.

    RE-PRED.5 therefore prohibits closing baseline design before the
    absolute-vs-excess target decision is explicit.

5.  Missingness taxonomy.

    The target freeze must distinguish at least:

    -   not yet matured;
    -   structurally missing data;
    -   unavailable because of source failure.

    Current code uses `None`, which remains correct as a representation
    of unavailable outcome. Future live tracking needs a richer
    explanation layer so that different `None` causes do not collapse
    into one state.

6.  Model freeze reference.

    RE-PRED.5 does not redefine the model freeze checklist.

    The authoritative freeze checklist is the one defined in RE-PRED.1.

    Future target-freeze work must reference that checklist rather than
    duplicating it.

    This avoids two competing sources of truth for what "frozen model"
    means.

7.  Target unfreeze criteria.

    A frozen target must not be reopened because early validation
    results are disappointing.

    Reopening a target after observing results would convert future
    validation into exploratory analysis unless the reason was
    pre-authorized.

    Acceptable future unfreeze reasons may include:

    -   discovered source-data error;
    -   verified source-column mapping error;
    -   discovered target-construction bug;
    -   authoritative change in the source dataset structure;
    -   documented governance decision that the target no longer matches
        the SOP objective.

    Unacceptable unfreeze reasons include:

    -   poor validation performance;
    -   desire to improve MAE after seeing results;
    -   desire to improve hit-rate after seeing results;
    -   desire to improve rank correlation after seeing results;
    -   market pressure or urgency.

Acceptance criteria for definitive target freeze:

A future target-freeze PR or documentation iteration is acceptable only
if it:

-   states the target field;
-   states the target formula;
-   states the source column and verified source-column semantics;
-   states the start anchor;
-   states the end anchor;
-   states the horizon;
-   states annualized vs cumulative unit;
-   states absolute vs excess-return choice;
-   states missingness taxonomy;
-   references the RE-PRED.1 model-freeze checklist;
-   states target unfreeze criteria;
-   explicitly confirms that no validation results were used to tune the
    target after freeze evaluation began.

Current status:

The implemented target remains the provisional freeze candidate.

It is not definitively frozen.

The main blocker is no longer `Price.1` semantics.

The remaining blockers are:

-   bottom-detection / episode-boundary audit;
-   absolute vs excess-return decision;
-   baseline design after that decision;
-   missingness taxonomy;
-   formal freeze / unfreeze governance.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No model frozen.
-   No baseline introduced.
-   No holdout created.
-   No live-tracking log introduced.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.6 — Bottom detection / episode boundary audit

RE-PRED.6 audits how the current code selects `bottom_date` and defines
drawdown episodes.

It is documentation-only.

No code changed.

Audited code:

    engine/drawdown_engine.py

Audited functions:

-   `calculate_running_peak()`;
-   `calculate_drawdown()`;
-   `detect_drawdowns()`;
-   `filter_episodes()`;
-   `enrich_recovery()`;
-   `_future_return()`.

Current definitions:

Peak:

`RunningPeak = P.cummax()`.

The peak is the cumulative historical maximum of nominal price `P` up to
the current row.

`detect_drawdowns()` updates the active peak whenever:

    Drawdown == 0

Drawdown:

`calculate_drawdown()` computes:

    (P - RunningPeak) / RunningPeak

Therefore drawdown severity is measured against nominal price `P`, not
against `Price.1`.

Episode start:

An episode starts when the system is outside a drawdown episode and:

    Drawdown <= MIN_DRAWDOWN

with:

    MIN_DRAWDOWN = -0.10

At that moment, the code stores the prior full-recovery peak as
`peak_before` and initializes the bottom as the current row.

Bottom:

While an episode is active, the bottom is updated whenever:

    row["Drawdown"] < bottom["Drawdown"]

The bottom is therefore the most negative drawdown observed inside the
active episode.

Recovery:

Recovery is detected when:

    Drawdown == 0

The episode is appended only in that recovery branch.

This means recovered drawdowns are included, but an unrecovered drawdown
still active at the end of the dataset is structurally excluded.

Duration:

`duration_months` is currently calculated as:

    int(round((bottom_date - peak_date) * 12))

Recovery months:

`recovery_months` is currently calculated as:

    int(round((recovery_date - bottom_date) * 12))

Target anchor:

`_future_return()` starts the predictive target window from:

    bottom_date

not from:

-   the -10% trigger date;
-   the peak date;
-   recovery date;
-   action date;
-   human approval date.

Confirmed limits:

-   The drawdown threshold is hardcoded at -10%.
-   Episode detection uses nominal price `P`.
-   Future return uses `Price.1`.
-   The model learns only from drawdowns that later recovered.
-   The target starts at the final bottom, not at the first trigger.

Verified finding 1 — price-basis asymmetry:

Episode detection and target measurement use different price bases.

Drawdown detection uses:

    P

which is nominal price.

Target returns use:

    Price.1

which RE-PRED.4 verified as Real Total Return Price.

Therefore:

-   what counts as a drawdown episode is measured on nominal price;
-   what the model later predicts is measured on real total return.

This is a real methodological asymmetry.

RE-PRED.6 does not decide whether it is wrong.

It records that definitive target freeze must explicitly accept,
reject or redesign this asymmetry.

Verified finding 2 — unrecovered drawdowns are structurally excluded:

`drawdowns.append(...)` exists only inside the recovery branch of
`detect_drawdowns()`.

Therefore an active drawdown that has not returned to `Drawdown == 0` by
the end of the dataset never becomes an `Episode`.

It is never available to:

-   `ObservableUniverse`;
-   `SimilarityEngine`;
-   `EvidenceEngine`;
-   Research Validation.

The current dataset run contains 23 episodes and all have
`recovery_date`.

So this property does not currently create a missing active episode in
the produced episode list.

But it is structural: the model's historical universe consists only of
crises that eventually recovered.

Verified finding 3 — duration arithmetic bug:

The current code subtracts dates encoded as floats in `YYYY.MM` format.

That arithmetic is not calendar-month arithmetic.

This affects:

-   `duration_months`;
-   `recovery_months`.

A data check against the current dataset found discrepancies in all 23
episodes when compared with true calendar-month arithmetic.

Example:

    peak:   1929.09
    bottom: 1932.06

Current code:

    36 months

Calendar-month calculation:

    33 months

The observed recovery-month discrepancy reaches up to 7 months.

Severity:

This is a verified bug, not merely a methodological question.

It affects fields currently produced by the system:

-   `Episode.duration_months`;
-   `Episode.recovery_months`;
-   `Evidence.average_recovery_months`;
-   `Evidence.median_recovery_months`.

It affects Similarity directly because `duration_months` participates in
duration scoring and also in speed scoring through `abs(drawdown) /
duration_months`.

RE-PRED.6 does not fix the bug.

It records it as a required follow-up before definitive target freeze or
any governance reliance on recovery-duration evidence.

Implications for target freeze:

RE-PRED.6 completes part of the bottom-anchor audit, but it does not
clear the target for definitive freeze.

Remaining blockers include:

-   deciding whether nominal-price drawdown detection is acceptable for a
    real-total-return target;
-   deciding whether unrecovered drawdowns should remain structurally
    excluded;
-   fixing or formally accepting the date-arithmetic bug;
-   re-verifying any affected canonical metrics after the bug decision.

Boundary:

-   No code changed.
-   No bug fixed.
-   No target definitively frozen.
-   No model frozen.
-   No baseline introduced.
-   No holdout created.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-BUG.1 — Calendar-month duration bug acceptance criteria

RE-BUG.1 defines acceptance criteria for fixing the date-arithmetic bug
identified in RE-PRED.6.

It is documentation-only.

No code changed.

Bug classification:

This is a verified implementation bug.

It is not a methodology question.

The current code calculates calendar durations by subtracting floats in
`YYYY.MM` format:

    int(round((bottom_date - peak_date) * 12))
    int(round((recovery_date - bottom_date) * 12))

That is not calendar-month arithmetic.

Affected fields:

-   `Episode.duration_months`;
-   `Episode.recovery_months`;
-   `Evidence.average_recovery_months`;
-   `Evidence.median_recovery_months`.

Directly affected behavior:

-   Similarity duration scoring, because `episode.duration_months` is
    compared directly against `snapshot.duration_months`;
-   Similarity speed scoring, because `snapshot_speed` is calculated as
    `abs(drawdown) / duration_months`.

This means the bug is not limited to recovery-statistic fields.

Correcting duration arithmetic may change the actual match set selected
by `SimilarityEngine.top()`.

Priority:

This bug must be near the head of the code-fix queue.

Reason:

It already affects public Research / Evidence outputs.

Any future consumer of Evidence recovery statistics could read those
fields without knowing they are wrong.

Required fix behavior:

The future fix must calculate month distance from `YYYY.MM` encoded
dates by converting year and month components explicitly.

For two dates:

    start = YYYY.MM
    end   = YYYY.MM

the correct month distance must be:

    (end_year - start_year) * 12 + (end_month - start_month)

The fix must not use direct float subtraction.

Required examples:

The future test must include at least:

    1929.09 -> 1932.06 = 33 months

This case currently returns 36 months.

The test should also include a same-year cross-month case and a
multi-year case whose month component decreases.

Required regression scope:

The future verification must prove:

-   all 23 current drawdown episodes have calendar-correct
    `duration_months`;
-   all recovered episodes have calendar-correct `recovery_months`;
-   no duration uses float date subtraction;
-   `Evidence.average_recovery_months` and
    `Evidence.median_recovery_months` are recalculated from corrected
    `recovery_months`;
-   the fix does not change `future_return_5y`;
-   the fix does not change source-column semantics;
-   the fix does not change episode threshold logic;
-   the fix does not change the nominal-price vs real-total-return
    asymmetry documented in RE-PRED.6.
-   the fix compares today's selected match identifiers before and after
    the correction.

Expected downstream impact:

Because `duration_months` participates in two active Similarity
dimensions, correcting it may change:

-   selected matches;
-   Evidence return statistics;
-   Evidence Quality local inputs;
-   Research Validation metrics.

Such changes are acceptable if caused by corrected duration arithmetic.

They must be reported explicitly in the future fix iteration.

They must not be hidden as unrelated regression noise.

If selected matches do not change, that fact must be reported explicitly
as well.

The future fix must not assume that canonical numbers survive unchanged:

-   `Evidence.return_count`;
-   `Evidence.median_return`;
-   `Evidence.worst_return`;
-   `Evidence.best_return`;
-   Research Validation MAE;
-   directional hit rate;
-   rank correlation.

Required tests:

The future code change should add or update a focused verification test.

Minimum assertions:

-   date-to-month conversion helper returns correct values;
-   1929.09 to 1932.06 returns 33;
-   every produced episode has corrected `duration_months`;
-   every recovered episode has corrected `recovery_months`;
-   public Evidence recovery statistics are based on corrected values;
-   today's top-match identifiers are compared before and after the fix;
-   `verify_research_engine.py` passes after the fix;
-   `verify_assessment_engine.py` passes after the fix;
-   `verify_validation_metrics.py` is rerun after the fix, with expected
    values updated only if changed matches or corrected arithmetic explain
    the difference;
-   the existing Research pipeline still runs.

Rejected shortcuts:

-   Do not patch only the 1929 case.
-   Do not round float differences differently.
-   Do not keep using `YYYY.MM` float subtraction.
-   Do not silently update canonical validation numbers without
    explaining whether changed Similarity matches caused the change.
-   Do not assume Similarity is unaffected without comparing match
    identifiers.
-   Do not combine this bug fix with target-freeze, baseline, holdout or
    gate-threshold work.

Boundary:

-   No code changed in RE-BUG.1.
-   No bug fixed yet.
-   No target changed.
-   No episode-detection redesign authorized.
-   No price-basis asymmetry decision made.
-   No unrecovered-drawdown decision made.
-   No validation metrics recalculated.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-BUG.3 — Calendar-month duration fix impact record

RE-BUG.3 documents the impact of the RE-BUG.2 code fix.

It is documentation-only.

No code changed.

Fix status:

RE-BUG.2 fixed the verified calendar-month duration bug by adding
centralized date arithmetic and replacing direct `YYYY.MM` float
subtraction in `engine/drawdown_engine.py`.

The fix introduced:

-   `engine/date_utils.py`;
-   corrected `duration_months` calculation;
-   corrected `recovery_months` calculation;
-   `tests/verify_duration_arithmetic.py`;
-   updated canonical Research, Assessment and Research Validation
    verification expectations.

Verification status:

The post-fix pinned-runtime verification passes:

-   `tests/verify_duration_arithmetic.py`;
-   `tests/verify_research_engine.py`;
-   `tests/verify_assessment_engine.py`;
-   `tests/verify_validation_metrics.py`.

Forward-looking documentation rule:

The pre-fix canonical values remain part of project history.

They must not be silently rewritten.

From RE-BUG.2 onward, the post-fix values below are the official
current canonical values.

Current snapshot match set:

The current `SimilarityEngine.top()` match identifiers, expressed as
`bottom_date`, are:

    [
        2018.12,
        1998.09,
        1966.10,
        2020.03,
        1960.10,
        1990.10,
        2022.10,
        1962.06,
        1880.05,
        1903.10,
    ]

Current Evidence / Research canonical values:

-   `Evidence.median_return`: `0.10192496249726091`;
-   `Evidence.worst_return`: `-0.01091948933252962`;
-   `Evidence.best_return`: `0.13767334934864284`;
-   `Evidence.return_count`: `9`;
-   `Evidence.positive_count`: `8`;
-   `Evidence.negative_count`: `1`;
-   `Evidence.zero_count`: `0`;
-   `Evidence.non_positive_probability`: `0.1111111111111111`;
-   `Evidence.return_spread`: `0.14859283868117246`.

Current Assessment canonical values:

-   `expected_return_5y`: `0.10192496249726091`;
-   `upside_potential`: `0.13285520801656237`;
-   `downside_risk`: `-0.01091948933252962`;
-   `drawdown_zone`: `NORMAL`;
-   `matches`: `10`.

Current Research Validation canonical values:

-   `episodes`: `23`;
-   `sample_size`: `21`;
-   `evaluated_count`: `19`;
-   `mae`: `0.06928793787076225`;
-   `directional_hit_rate`: `0.9473684210526315`;
-   `rank_correlation`: `-0.26505171850684983`;
-   `overlap_pairs`: `10`;
-   `repeated_forecast_groups`: `5`.

Impact interpretation:

The fix corrected an objectively wrong duration calculation.

The change affected active Similarity scoring through both direct
duration scoring and speed scoring.

Therefore changes in selected matches, Evidence statistics and Research
Validation metrics are expected consequences of the corrected arithmetic,
not unrelated regressions.

Methodological interpretation:

The predictive-validity conclusion does not improve because of this fix.

The updated validation surface remains conservative:

-   rank correlation remains negative;
-   directional hit-rate remains non-discriminant;
-   the effective sample-size caveat remains unresolved;
-   Evidence Quality remains unable to justify capital deployment on
    predictive-validity grounds.

Boundary:

-   No target changed.
-   No target freeze authorized.
-   No baseline decision made.
-   No holdout policy changed.
-   No episode-detection redesign authorized.
-   No price-basis asymmetry decision made.
-   No unrecovered-drawdown decision made.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-DATA.1 — Shiller source update automation note

RE-DATA.1 records a future data-update capability.

It is documentation-only.

No code changed.

Current state:

The Shiller dataset is updated manually.

The local source file remains:

    data/raw/shiller.xlsx

Future capability:

A later iteration may add a controlled updater, for example:

    python3 tools/update_shiller_data.py

The updater may download the Shiller source workbook from the official
Shiller data site.

Boundary:

This must not be implemented as a blind download-and-overwrite step.

Any future automated update must:

-   download the source file to a temporary location first;
-   preserve or back up the previous local workbook;
-   verify the expected workbook structure;
-   verify that `Price.1` still maps to Real Total Return Price;
-   verify required columns before replacing local data;
-   verify that the latest observation is not older than the current
    local source;
-   run the loader / drawdown / research verification tests after the
    update;
-   log the source URL, update date, prior latest observation and new
    latest observation;
-   fail closed if validation does not pass.

Timing:

This is not a near-term priority.

It should be revisited after the RE-PRED target / baseline work is
closed, because changing data sources while target semantics are still
open would make validation harder to interpret.

Rejected shortcut:

Do not silently replace `data/raw/shiller.xlsx` from the network without
structural validation and test reruns.

------------------------------------------------------------------------

## RE-PRED.7 — Absolute vs Excess Return Boundary

RE-PRED.7 defines whether predictive validity should be evaluated
against absolute 5-year return, excess return over a naive baseline, or
both, in separate channels.

It is documentation-only.

No code changed.

Two channels, not one:

-   Absolute return channel: what happened after the drawdown bottom.
    This is the existing Evidence descriptive surface
    (`Evidence.median_return`, `future_return_5y`). No new field, no
    renamed field. Its purpose is descriptive evidence, not a
    predictive-validity claim by itself.
-   Excess return channel: whether the model's forecast adds value over
    a naive rule that requires no similarity matching. This is the
    future predictive-validity surface. It does not exist yet.

Motivation:

RE-025.3 already found that a rule that always predicts "positive"
produces almost the same directional hit rate as the current model,
because 0/19 forecasts were negative in the evaluated sample. A model
can score well on an absolute-return metric while adding no
discriminating value over a rule that ignores current conditions
entirely. Absolute-return metrics alone cannot distinguish those two
cases. Excess return can.

Primary baseline:

The primary baseline for excess return is the unconditional historical
mean/median `future_return_5y` across the full episode set, evaluated
point-in-time (same `ObservableUniverse` discipline as RE-025.1) so it
does not itself leak future information. This baseline answers the
sharpest question available today: does conditioning the forecast on
the current snapshot via `SimilarityEngine` add anything beyond "stocks
have historically gone up over 5 years"?

Secondary baselines, already named in RE-PRED.1, remain diagnostic, not
headline: constant full-universe forecast, zero/no-change, simple
mean-reversion. This is a mandatory-comparison requirement, not a
beat-all-four requirement.

Per-metric mechanics are not uniform:

-   MAE and directional hit-rate require an actual baseline forecast
    series to compute excess against. Excess MAE is baseline MAE minus
    model MAE (positive means the model beats the baseline). Excess
    hit-rate is defined analogously.
-   Rank correlation does not need a baseline forecast series. A
    constant-forecast baseline has no rank variation, so its rank
    correlation is undefined / zero by construction. The existing rank
    correlation value already tests whether the model's forecast
    ordering carries information beyond none. No new "excess"
    transformation is needed for this metric; this boundary states that
    explicitly so it is not built twice.

Placement:

Excess return is a Research Validation Harness concept, not an Evidence
concept. Evidence describes a live snapshot's matched sample and has no
"actual" to compare against; excess return is only computable in
backtest, across historical episodes with realized outcomes. This
iteration keeps that boundary explicit so no future implementation adds
baseline or excess-return logic into `models/evidence.py` or
`engine/evidence_engine.py`.

Expected outcome, stated in advance:

Given RE-025.3 (a trivial rule already matches the model's hit rate) and
RE-BUG.3 (rank correlation moved further negative after the duration
fix, not less negative), the most likely outcome once excess return is
actually computed (a future iteration) is that the primary baseline
matches or beats the model on at least one canonical metric. That
outcome, if it occurs, must be recorded plainly as a finding, not
softened or treated as an implementation problem to fix.

Rejected shortcuts:

-   Do not treat absolute-return metrics (current MAE, hit-rate, rank
    correlation) as if they already constitute predictive-validity
    evidence.
-   Do not compute excess return using a single blended baseline that
    mixes the four candidate baselines into one number.
-   Do not add baseline or excess-return fields to `Evidence` or
    `models/evidence.py`.
-   Do not apply the same excess-return transformation to rank
    correlation as to MAE / hit-rate.
-   Do not compute any baseline value in this iteration.

Boundary:

-   No code changed in RE-PRED.7.
-   No baseline value computed.
-   No excess-return metric implemented.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.
-   No Evidence field added.

------------------------------------------------------------------------

## RE-PRED.8 — Primary baseline acceptance criteria

RE-PRED.8 defines acceptance criteria for computing the primary
excess-return baseline defined in RE-PRED.7. It also corrects
RE-PRED.7's rank-correlation claim forward.

It is documentation-only.

No code changed.

Correction to RE-PRED.7:

RE-PRED.7 stated that rank correlation "does not need a baseline
forecast series" because "a constant-forecast baseline has no rank
variation." That claim implicitly assumed a single global baseline
number computed once over the full 23-episode dataset. That design
would violate the point-in-time discipline established in RE-025.1 — it
would inform a 1907 episode's baseline with data from 2020, which did
not yet exist in 1907. The primary baseline, as specified below, is not
a single constant: it is a point-in-time expanding statistic that varies
per episode. It therefore does have rank variation, and its rank
correlation against realized outcomes is a real, computable comparison
against the model's rank correlation, not an undefined quantity. This
correction is recorded here rather than silently rewriting RE-PRED.7,
per RE-DOC-002.

Baseline definition:

For each evaluable episode `X`, with `bottom_date = t`:

    baseline_forecast(X) = median(future_return_5y) over
    ObservableUniverse(dataset, as_of=t).episodes(),
    excluding X by bottom_index

This reuses the exact same temporal-safety machinery already verified
for the model's own forecast in RE-025.1 (`ObservableUniverse`,
self-exclusion by `bottom_index`) — no new mechanism is introduced. The
only difference from the model's forecast is that the baseline is
unconditional: it does not pass through `SimilarityEngine.top()`, so it
does not condition on the current snapshot's similarity to `X`.

Statistic choice:

Median, not mean, is the primary baseline statistic. It matches the
model's own canonical statistic (`Evidence.median_return`), keeping the
comparison apples-to-apples. Mean may be recorded as a secondary
diagnostic, never as the headline comparator.

Sample alignment:

The baseline is evaluated over exactly the same evaluable record set
already established by `ValidationHarness` (today: 19 records). No
separate inclusion or exclusion criteria are invented for the baseline.
Using a different sample for baseline vs. model would bias the
comparison.

Metrics:

Three head-to-head comparisons against the model's existing canonical
metrics, side by side, not blended:

-   Baseline MAE vs model MAE (`0.06928793787076225`).
-   Baseline directional hit-rate vs model directional hit-rate
    (`0.9473684210526315`).
-   Baseline rank correlation vs model rank correlation
    (`-0.26505171850684983`).

Excess is reported as baseline MAE minus model MAE for MAE (lower is
better, so a positive excess means the model wins), and as model minus
baseline for hit-rate and rank correlation (higher is better, so a
positive excess means the model wins).

Deferred to a later iteration:

-   Secondary baselines (constant full-universe forecast, zero /
    no-change, simple mean-reversion) are not defined here. If the
    constant full-universe forecast is used later, it must be labeled
    explicitly as not point-in-time-safe and used as a diagnostic only,
    never as a headline comparator.
-   Actual baseline computation and values belong to the next code
    iteration, not to RE-PRED.8.

Rejected shortcuts:

-   Do not use a single global constant baseline computed once over all
    23 episodes.
-   Do not invent a separate evaluable-record definition for the
    baseline.
-   Do not use mean as the primary baseline statistic.
-   Do not blend MAE, hit-rate and rank correlation excess into one
    score.
-   Do not compute any baseline value in this iteration.

Boundary:

-   No code changed in RE-PRED.8.
-   No baseline value computed.
-   No excess-return metric implemented.
-   No secondary baseline defined.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.9 — Primary baseline implementation

RE-PRED.9 implements the primary baseline defined in RE-PRED.8 in code.

New files:

-   `engine/baseline_harness.py` — `baseline_forecast()`, computing the
    point-in-time expanding median of `future_return_{years}y` by
    reusing `ObservableUniverse` and bottom_index self-exclusion, the
    same temporal-safety machinery already verified for the model's own
    forecast in RE-025.1; `BaselineHarness`, producing baseline
    `ValidationRecord`s aligned 1:1 with the model's, inheriting
    `evaluable` and `actual` directly rather than deciding its own
    inclusion criteria; `missing_baseline_forecast_count()`, an explicit
    diagnostic for the invariant below; `excess_summary()`, the
    head-to-head comparison required by RE-PRED.8, reusing
    `mean_absolute_error()`, `directional_hit_rate()` and
    `rank_correlation()` from `engine/validation_metrics.py`
    unmodified.
-   `tests/verify_baseline_harness.py` — functional smoke test.

No existing file was modified except `tests/verify_core.py`, which adds
`engine/baseline_harness.py` to its structural Engines list, following
the RE-025.7 precedent.

No Frozen Core component was touched. `ObservableUniverse`,
`SimilarityEngine`, `EvidenceEngine` and the existing metric functions
are consumed through their public interfaces exactly as published, the
same pattern already used to justify RE-025.1-RE-026.1.2 under the
Frozen Core Policy.

Invariant proven by construction, not merely observed:

If a model `ValidationRecord` is evaluable, its baseline counterpart
can never have `forecast=None`. The model's `SimilarityEngine.top()`
matches are drawn from `_comparable_episodes(dataset, episode)` — the
exact same unconditional pool this baseline uses without narrowing by
similarity. If at least one of the model's matches had a non-`None`
`future_return_{years}y` (a necessary condition for the model to be
evaluable), that same value is present in the baseline's pool. The
verification test checks this invariant explicitly via
`missing_baseline_forecast_count()` rather than assuming it holds.

Sample alignment, verified structurally:

-   `episodes = 23`, `sample_size = 21`, `evaluated_count = 19` — the
    existing canonical values, unchanged.
-   Baseline record count equals model record count.
-   Baseline evaluable count equals model evaluable count.
-   `missing_baseline_forecast_count = 0`.

Verification status:

`tests/verify_baseline_harness.py` was run outside the pinned runtime
only, to confirm the code executes without error and the structural
invariants above hold. It was not run under `requirements.txt`.

No baseline value is canonical yet. `mean_absolute_error()`,
`directional_hit_rate()` and `rank_correlation()` applied to the
baseline records produce real numbers in that non-pinned run, but
RE-025.5 already established that different pandas/numpy versions can
change these exact computations. Treating a non-pinned result as
canonical here would repeat, on new code, the same category of mistake
RE-BUG.2 spent an entire iteration correcting. The next iteration
(RE-PRED.10) records the canonical baseline values once
`tests/verify_baseline_harness.py` has been run and confirmed under the
pinned runtime.

Rejected shortcuts:

-   Do not treat a non-pinned execution result as canonical.
-   Do not hardcode `EXPECTED_*` baseline constants before pinned-runtime
    confirmation.
-   Do not modify `engine/validation_metrics.py` to special-case the
    baseline; reuse it unmodified.
-   Do not let the baseline invent its own evaluable set.

Boundary:

-   No Frozen Core component modified.
-   No existing file modified except `tests/verify_core.py` (structural
    list only).
-   No canonical baseline value established.
-   No secondary baseline implemented.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.10 — Canonical baseline values and predictive-validity finding

RE-PRED.10 records the canonical primary baseline values, confirmed by
running `tests/verify_baseline_harness.py` under `RUNTIME : PINNED`
(`requirements.txt`), and the finding that follows from them.

It is documentation-only.

No code changed.

Structural verification, confirmed under the pinned runtime:

-   `episodes = 23`, `sample_size = 21`, `evaluated_count = 19`,
    `baseline_evaluated_count = 19`.
-   `missing_baseline_forecast_count = 0` — the invariant proven by
    construction in RE-PRED.9 (a baseline forecast can never be `None`
    when the corresponding model record is evaluable) holds empirically
    on the live dataset, not only in principle.

Canonical baseline values:

    model_mae:                 0.06928793787076
    baseline_mae:               0.06740858559979
    excess_mae:                -0.00187935227097

    model_hit_rate:             0.94736842105263
    baseline_hit_rate:          0.94736842105263
    excess_hit_rate:            0.00000000000000

    model_rank_correlation:    -0.26505171850685
    baseline_rank_correlation: -0.23171864780822
    excess_rank_correlation:   -0.03333307069863

Values are recorded to the fourteen decimal places produced by
`tests/verify_baseline_harness.py`'s own print formatting. This is the
precision actually captured from the pinned-runtime execution; it is
not re-derived to a higher precision.

Reading excess: for MAE, `excess_mae = baseline MAE - model MAE`,
positive meaning the model wins. For hit-rate and rank correlation,
`excess = model metric - baseline metric`, positive meaning the model
wins (RE-PRED.8/RE-PRED.9 convention).

Finding, stated plainly, as committed to in advance in RE-PRED.7 and
RE-PRED.8:

The model does not beat the primary baseline on any of the three
canonical metrics.

-   MAE: the baseline wins. Baseline error is 0.06741, model error is
    0.06929 — the baseline is closer to realized outcomes on average.
-   Directional hit-rate: exact tie. Both are 0.94737. This adds no new
    information beyond what RE-025.3 already established — a
    conditionless prediction of "positive" was already known to match
    the model's directional performance.
-   Rank correlation: the baseline wins. Baseline correlation is
    -0.23172, model correlation is -0.26505 — the model's ordering of
    forecast strength is further from informative than the baseline's,
    though both remain weakly negative.

Interpretation:

Conditioning the forecast on the current snapshot's similarity to
historical episodes, via `SimilarityEngine`, does not currently produce
a forecast that is more accurate, more discriminating, or better
ordered than simply taking the unconditional historical median of
comparable episodes observable at each point in time. On this canonical
19-record evaluated sample, predictive validity is not demonstrated
relative to this baseline.

This finding does not by itself prove `SimilarityEngine` conditioning
has no value under any circumstance — the evaluated sample remains
small, non-independent (RE-025.6, RE-025.8, RE-025.9), and only one
primary baseline has been tested. It does mean the burden of proof
established in RE-PRED.1 has not been met: this is not a case where
predictive validity is assumed to be a matter of time or more code. The
governing principle recorded at the start of the Predictive Validity
Boundary applies directly here: predictive validity must first be shown
to exist before any threshold or gate-relaxation design proceeds as if
it did.

Connection to Evidence Quality Gate:

This sharpens, but does not by itself change, the existing
`EvidenceQualityGate` state. RE-029.6 already recorded that the gate
starts conservative because current Research Validation does not yet
show reliable discriminatory power. This finding replaces that
qualitative judgment with a direct, head-to-head quantitative result:
not merely "hit-rate is non-discriminating and rank correlation is
weakly negative," but "the model loses to a naive baseline on two of
three canonical metrics and ties on the third." No gate threshold or
posture ceiling is changed by this iteration — RE-029.7's calibration
boundary still requires an explicit, pre-registered governance decision
before any gate state changes, and this finding argues for continued
conservatism, not relaxation.

Rejected shortcuts:

-   Do not soften this finding or reframe it as an implementation
    problem to fix.
-   Do not treat the exact directional hit-rate tie as if it were
    informative on its own, independent of RE-025.3's existing finding.
-   Do not use this finding to automatically change any gate threshold
    or capital posture ceiling.
-   Do not treat this single primary-baseline result as a final verdict
    on predictive validity; secondary baselines and a larger or
    differently-sampled evaluation remain open.

Boundary:

-   No code changed in RE-PRED.10.
-   No gate threshold changed.
-   No capital posture ceiling changed.
-   No target freeze changed.
-   No secondary baseline computed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.10.1 — Deferred: `NOT_DEMONSTRATED` gate state proposal

A proposal was raised, immediately after RE-PRED.10, to formalize a
third `EvidenceQualityGate` output state, `NOT_DEMONSTRATED`, distinct
from `NOT_MEASURABLE` and `CONSERVATIVE`, taking precedence over local
input completeness (a globally disproven method cannot be rescued by a
well-measured local sample).

The proposal is deferred, not rejected, for three reasons:

-   It would rest on a single baseline comparison over a non-independent
    N=19 sample (RE-025.6, RE-025.8, RE-025.9) -- the same category of
    overreaction-to-one-data-point the project's robustness axiom exists
    to prevent.
-   `EvidenceQualityGate.evaluate()`'s current code already forces
    `NOT_MEASURABLE` today regardless of global state, because
    `independence_dispersion_measured` is hardcoded `False`
    (RE-030.1/RE-030.2). A new state would today produce the identical
    posture-ceiling consequence (`Conserve`, `Prepare` allowed) as the
    existing `not measurable` state -- no operative behavior depends on
    making the distinction yet.
-   Adding a new state touches the taxonomy `GateCombination` (RE-034)
    already consumes, before there is a concrete behavioral reason for
    treating it differently from `NOT_MEASURABLE`.

Explicit trigger for revisiting: once RE-PRED.11's secondary baselines
are confirmed under the pinned runtime, if the model loses to the full
set (primary, zero, mean-reversion) on a majority of canonical metrics,
the case for a formal `NOT_DEMONSTRATED` state becomes materially
stronger and should be reopened. If the model beats one or more
secondary baselines while only losing to the primary, the finding is
more nuanced and likely does not warrant a new top-level state --
sharper `explanations` text within the existing two-state model may be
sufficient instead.

Boundary:

-   No code changed.
-   No new gate state added.
-   No posture ceiling changed.
-   This is not a rejection of the underlying finding from RE-PRED.10 --
    only of formalizing it into gate architecture before a fuller
    evidentiary basis exists.

------------------------------------------------------------------------

## RE-PRED.11 — Secondary baselines implementation

RE-PRED.11 implements two secondary baselines in
`engine/baseline_harness.py`, to isolate whether the RE-PRED.10 finding
is an artifact of the primary baseline choice.

It extends an already-isolated, non-Frozen-Core file (RE-PRED.9). No
existing function in that file is modified. No other file changes.

New functions:

-   `zero_forecast(episode)` -- returns `0.0` unconditionally. No
    parameters, no dependency on `ObservableUniverse` or any comparable.
    By construction, `directional_hit_rate()` excludes `forecast == 0`
    records and `rank_correlation()` returns `None` when all forecasts
    are identical -- this baseline can only produce a signal in MAE.
    This is expected, not a defect.
-   `mean_reversion_forecast(episode)` -- returns `-episode.drawdown`.
    Coefficient 1, zero parameters fitted against history. Uses only
    `episode.drawdown`, an Event field already known at the episode's
    own bottom -- no comparable episodes, no calibration. Deliberately
    the simplest defensible definition of "reversion," not the only
    possible one: a history-calibrated version was rejected to avoid
    introducing a new overfitting risk inside what must remain a naive
    baseline.
-   `build_baseline_records(model_records, forecast_fn)` -- generic
    constructor for baselines that do not need `ObservableUniverse`.
    Same RE-PRED.8 rule as `BaselineHarness`: `evaluable` and `actual`
    are inherited directly from the model's own records, never decided
    separately for the baseline.

`tests/verify_secondary_baselines.py` re-asserts the existing canonical
model and primary-baseline values (RE-BUG.3, RE-PRED.10) as a regression
guard, asserts the expected `None` degeneracy of zero's hit-rate and
rank correlation, and prints the full three-way comparison table (model
/ primary baseline / zero / mean-reversion). It does not hardcode
canonical zero/mean-reversion values -- those require pinned-runtime
confirmation, the same discipline RE-PRED.9 established and RE-BUG.2
motivated.

Boundary:

-   No Frozen Core component modified.
-   No existing function modified.
-   No canonical secondary-baseline value established.
-   No gate state changed.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.12 — Open question: sampling-noise robustness

RE-PRED.12 records an explicit open question that RE-PRED.11's
secondary baselines do not, and cannot, resolve.

It is documentation-only. No code changed.

Two distinct notions of robustness:

-   Baseline-choice robustness: is the RE-PRED.10 finding specific to
    the point-in-time expanding median, or does it hold against other
    naive baselines too? RE-PRED.11 answers this.
-   Sampling-noise robustness: are the excess differences observed
    (e.g. -0.00187935227097 excess MAE, -0.03333307069863 excess rank
    correlation from RE-PRED.10) distinguishable from chance, given that
    all evaluations share the same 19 evaluable records, already
    documented as non-independent through two channels (RE-025.6):
    overlapping realized 5-year outcome windows (RE-025.8) and repeated
    forecasts (RE-025.9)? RE-PRED.11 does not answer this -- every
    additional baseline is still scored against the same dependent
    19-record sample.

This is not a new discovery. It follows directly from RE-025.6, which
already declined to publish a numeric effective N. It is recorded here,
specifically, so that a favorable or unfavorable secondary-baseline
result is not mistaken for statistical confirmation either way.

What this explicitly does not authorize:

-   An i.i.d. bootstrap over the 19 records -- prohibited by RE-PRED.1's
    uncertainty requirement, which requires dependence-aware resampling,
    not naive resampling that ignores the known overlap and repeated-
    forecast structure.
-   Treating N=19 as if it were 19 independent observations for any
    significance statement.

This gap is not resolved by this iteration. It remains open, tracked
here, for future dependence-aware uncertainty work -- scope and method
not yet defined.

Boundary:

-   No code changed.
-   No statistical test implemented.
-   No effective-N value published.
-   No gate state changed.

------------------------------------------------------------------------

## RE-PRED.13 — Canonical secondary baseline values and full-picture finding

RE-PRED.13 records the canonical secondary-baseline values, confirmed
by running `tests/verify_secondary_baselines.py` under
`RUNTIME : PINNED`, and the full-picture finding that follows.

It is documentation-only. No code changed.

Structural verification, confirmed under the pinned runtime:

-   `episodes = 23`, `evaluated_count = 19` — unchanged.
-   `zero_hit_rate` and `zero_rank_correlation` are `None`, exactly as
    expected by construction (RE-PRED.11): `directional_hit_rate()`
    excludes `forecast == 0`, and `rank_correlation()` returns `None`
    when all forecasts are identical.
-   `missing_reversion_forecast_count = 0` — no evaluable model record
    produced a missing mean-reversion forecast.

Canonical secondary-baseline values:

    zero_mae:                       0.12749337012113
    reversion_mae:                  0.18158697149305
    excess_mae_vs_zero:             0.05820543225037
    excess_mae_vs_reversion:        0.11229903362229

    zero_hit_rate:                  None
    reversion_hit_rate:             0.94736842105263
    excess_hit_rate_vs_reversion:   0.00000000000000

    zero_rank_correlation:          None
    reversion_rank_correlation:     0.26315789473684
    excess_rank_correlation_vs_reversion: -0.52820961324369

Full comparison table (model, primary baseline from RE-PRED.10, zero,
mean-reversion):

    Metric              Model      Primary    Zero       Reversion
    MAE                 0.06929    0.06741*   0.12749    0.18159
    Directional hit-rate 0.94737   0.94737    None       0.94737
    Rank correlation    -0.26505   -0.23172*  None       0.26316*

    * beats the model on that metric

Finding, stated plainly:

The model is not uniformly dominated. It clearly beats zero and
mean-reversion on MAE — 0.06929 versus 0.12749 and 0.18159
respectively, a wide margin either way. It ties all measurable
baselines on directional hit-rate. Where it loses is rank correlation:
the primary baseline beats it by a moderate margin, and mean-reversion
beats it by a full sign flip — mean-reversion's rank correlation is
positive (0.26316), the model's is negative (-0.26505).

RE-PRED.10.1 trigger, evaluated explicitly:

RE-PRED.10.1 pre-registered a trigger for reopening the
`NOT_DEMONSTRATED` gate-state proposal: "if the model loses to the full
set (primary, zero, mean-reversion) on a majority of canonical
metrics." That condition does not hold — the model wins MAE against two
of the three baselines. The proposal remains deferred. Per
RE-PRED.10.1's own alternative, sharper `explanations` text within the
existing `NOT_MEASURABLE`/`CONSERVATIVE` states remains the appropriate
tool if this distinction needs to be made visible, not a new top-level
state.

Working hypothesis, registered but not authorized as fact:

Mean-reversion's positive rank correlation against the model's negative
one is a striking, specific result: drawdown depth alone, with no
comparables and no calibration, orders realized 5-year outcomes better
than `SimilarityEngine`'s multidimensional conditioning does on this
sample. One candidate explanation is signal dilution — blending
drawdown depth with duration, speed, CAPE, pre-crash return and
volatility (`SIMILARITY_WEIGHTS`, `core/constants.py`) may be
weighting away the single dimension carrying the strongest ordering
information, in favor of episodes that resemble the current snapshot
contextually without capturing the magnitude of the reversion. This is
recorded as a working hypothesis for future investigation, not a
diagnosis. No `SimilarityEngine` change is made or authorized by this
iteration — that component remains Frozen Core, and RE-021 already
establishes the evidentiary bar for touching it.

Mandatory caveat (per RE-PRED.12):

Both the +0.26316 and -0.26505 rank correlations above are computed
over the same 19 evaluable records already documented as
non-independent (RE-025.6, RE-025.8, RE-025.9). Neither figure is
established as distinguishable from sampling noise. This finding
sharpens the picture of what the model does on this sample; it does not
resolve, and must not be read as resolving, RE-PRED.12's open question.

Rejected shortcuts:

-   Do not read this as vindicating the model — it still loses to the
    primary baseline and to mean-reversion on rank correlation.
-   Do not read this as confirming `NOT_DEMONSTRATED` — the
    pre-registered trigger explicitly did not activate.
-   Do not treat the signal-dilution hypothesis as established; it is
    unauthorized speculation about mechanism, clearly labeled as such.
-   Do not treat +0.26316 or -0.26505 as stable, final values immune to
    sampling noise.

Boundary:

-   No code changed in RE-PRED.13.
-   No gate state changed.
-   No capital posture ceiling changed.
-   No `SimilarityEngine` change made or authorized.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.14 — Similarity dimension diagnostic: signal-dilution hypothesis not supported

RE-PRED.14 adds an exploratory, read-only diagnostic to test the
signal-dilution hypothesis registered in RE-PRED.13, and records the
result confirmed under the pinned runtime.

New files:

-   `engine/dimension_diagnostic.py` -- `dimension_forecast()` isolates
    one active `SimilarityEngine` dimension at a time by re-sorting the
    already-computed per-dimension scores that
    `SimilarityEngine.compare()` returns, instead of the blended score
    `top()` uses. Applies the same `peak_date` recency cutoff as
    `top()`. Excludes `recovery` deliberately -- RE-021 already removed
    it from the combined score as a data-leakage fix, and this
    diagnostic has no business reopening that. `dimension_records()`
    produces `ValidationRecord`s aligned with the model's, inheriting
    `evaluable`/`actual` per the same RE-PRED.8 rule, with `evaluable`
    additionally requiring a non-`None` forecast -- unlike RE-PRED.9's
    primary baseline, a single-dimension top-10 is not guaranteed to
    contain a resolved outcome by construction, so this must be checked,
    not assumed.
-   `tests/diagnostic_similarity_dimensions.py` -- not a `verify_*.py`
    regression gate. Makes no canonical claim, asserts no expected
    values, prints a comparison table. Still enforces the pinned-runtime
    gate (RE-025.5) before printing anything, because the reproducibility
    rule applies regardless of whether the script is exploratory.

No Frozen Core component modified. `SimilarityEngine.compare()` is
consumed exactly as published, the same justification pattern already
used for RE-025.1 and RE-PRED.9.

A real bug was found and fixed during construction, not in
`SimilarityEngine`: sorting by `pre_crash_return_3y_score` raised
`TypeError` because that score is `None` for episodes without three
years of prior price history. Fixed by excluding `None`-scored
comparables from that dimension's ranking, mirroring exactly how
`SimilarityEngine._weighted_score()` already excludes `None` from the
blended score -- absence of a dimension's signal is not treated as
maximal dissimilarity.

Results, confirmed under `RUNTIME : PINNED`:

    Dimension                  Evaluated   MAE      Hit-rate   Rank corr.
    model (blended, RE-BUG.3)  19          0.06929  0.94737    -0.26505
    drawdown_score              19          0.06765  0.94737    -0.19692
    duration_score               19          0.07079  0.94737    -0.24916
    speed_score                  19          0.07049  0.94737    -0.20327
    cape_score                   19          0.06899  0.94737    -0.21701
    pre_crash_return_3y_score    19          0.06592  0.94737    -0.26353
    volatility_score              19          0.06740  0.94737    -0.23414
    mean-reversion (RE-PRED.13, ref.)        0.18159  0.94737     0.26316

All six dimensions returned `evaluated = 19`, matching the model -- in
this run, isolating a single dimension did not reduce the evaluable set,
though the module docstring records that this is not guaranteed in
general.

Finding, stated plainly:

The signal-dilution hypothesis, as registered in RE-PRED.13, is not
supported. If blending were diluting a real positive signal present in
one dimension, isolating that dimension should have recovered something
closer to mean-reversion's positive rank correlation. It did not: every
dimension in isolation remains negative, ranging from -0.19692
(drawdown, the closest to positive) to -0.26353 (pre_crash_return_3y,
effectively matching the blended model). No single active
`SimilarityEngine` dimension is the hidden source of mean-reversion's
advantage.

Revised working hypothesis, registered but not authorized as fact:

The gap may not be a weighting problem at all. Mean-reversion is a
direct, monotonic function of the query episode's own drawdown depth --
by construction, a larger drawdown always produces a larger forecast,
preserving rank order exactly. `SimilarityEngine`, even sorted by a
single dimension, still selects a top-10 nearest-neighbor set and
forecasts the median outcome of whichever historical episodes happen to
rank closest -- a mechanism that does not preserve the query's own rank
order the same way, regardless of which dimension drives the selection.
If this is correct, the gap is not fixable by reweighting dimensions; it
would require reconsidering whether nearest-neighbor selection is the
right conditioning mechanism at all -- a materially larger question,
explicitly out of scope for this iteration.

Caveat (per RE-PRED.12, with extra force):

Every column above is computed over an even smaller, still-dependent
slice of the same 23-episode dataset -- isolating a dimension does not
add independent observations. This is hypothesis generation, not
hypothesis confirmation. The revised hypothesis above is speculation
about mechanism, clearly labeled, not a finding.

Rejected shortcuts:

-   Do not treat this as confirming or ruling out any mechanism with
    statistical confidence.
-   Do not treat the revised hypothesis as established; it is
    unauthorized speculation, one plausible explanation among others.
-   Do not use this diagnostic's results to modify `SimilarityEngine`,
    `SIMILARITY_WEIGHTS`, or any Frozen Core component.
-   Do not treat per-dimension `evaluated = 19` as guaranteed in future
    runs or future datasets.

Boundary:

-   No Frozen Core component modified.
-   No `SimilarityEngine` change made or authorized.
-   No gate state changed.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.15 — Dependence-aware cluster bootstrap

RE-PRED.15 closes the method gap opened in RE-PRED.12: whether the
excess differences observed against the primary baseline (RE-PRED.10)
and mean-reversion (RE-PRED.13) are distinguishable from sampling
noise, given that all 19 evaluable records are already documented as
non-independent through two channels (RE-025.6): overlapping realized
5-year outcome windows (RE-025.8) and repeated forecasts (RE-025.9).

New file: `engine/dependence_bootstrap.py`.

Method, agreed with Armando before implementation:

-   `independence_clusters(records)` partitions evaluable records into
    clusters via connected components over the union of two edge
    sources: pairs returned by `overlapping_outcome_windows()`
    (RE-025.8) and groups returned by `repeated_forecast_groups()`
    (RE-025.9). No new dependence criterion is introduced -- both edge
    sources are the same diagnostics already validated in RE-025.6/8/9,
    connected here for the first time. Clusters are returned as
    positions, not objects, so the same partition applies unchanged to
    any parallel `ValidationRecord` list sharing the same order --
    model, primary baseline (RE-PRED.9) or secondary baseline
    (RE-PRED.11) -- an invariant those modules already guarantee.
-   `cluster_bootstrap_ci()` resamples whole clusters with replacement,
    never individual records, preserving intra-cluster dependence
    instead of destroying it. This is the dependence-aware resampling
    RE-PRED.1 requires; an i.i.d. bootstrap over the 19 records remains
    explicitly prohibited (RE-PRED.12).
-   `cluster_bootstrap_paired_excess()` applies the identical cluster
    draw, in the same replica, to both model and baseline records
    before computing the excess -- not two independent bootstraps
    subtracted afterward. This preserves the paired variance structure
    that RE-PRED.10/11's excess figures already rely on (model and
    baseline are always evaluated on the same episodes, row for row).
-   One fixed cluster partition, built once from the model's own
    records, is reused for every bootstrap in this iteration --
    standalone and paired. Outcome-window overlap (RE-025.8) is
    episode/horizon-based and therefore identical for the model and
    both baselines; repeated-forecast grouping (RE-025.9) is
    model-specific by construction (it reflects `SimilarityEngine.top()`
    match-set structure, which neither baseline shares), and using the
    model's partition uniformly is what makes "paired" resampling
    well-defined across all three series.
-   Seed and replicate count are fixed constants, not free script
    parameters: `BOOTSTRAP_SEED=42`, `BOOTSTRAP_REPLICATES=5000`.
    Percentile interval fixed at (5, 95) -- a 90% interval, an explicit
    design choice, not the only possible one.
-   A bootstrap replica where a metric function returns `None` (e.g.
    `rank_correlation()` degenerating when a resample happens to
    produce identical forecasts) is excluded from that metric's
    percentile, not treated as `0.0` -- the same absence-of-evidence
    rule used throughout this module. `valid_replicates` is reported
    explicitly alongside every interval.

New test file: `tests/diagnostic_dependence_bootstrap.py` -- not a
`verify_*.py` regression gate. Asserts no expected values. Still
enforces the pinned-runtime gate (RE-025.5) before printing anything.
Reports, for MAE / hit-rate / rank correlation: the model's own
interval, the primary and mean-reversion baselines' intervals, and the
paired excess interval against each. Zero baseline is explicitly out
of scope for this iteration -- RE-PRED.13 already found it loses to
the model on MAE by a wide, unambiguous margin; only primary and
mean-reversion were flagged as open by RE-PRED.12.

`tests/verify_core.py` adds `engine/dependence_bootstrap.py` to its
structural Engine checks, per the RE-025.7/RE-PRED.9 precedent.

Structural smoke test, run outside the pinned runtime -- not
canonical: 4 independence clusters over the 19 evaluable records,
sizes `[10, 7, 1, 1]`. If this holds under the pinned runtime, it
confirms directly what RE-025.6/8/9 already implied qualitatively:
`n=19` behaves, for dependence purposes, much closer to a handful of
independent observations than to 19.

The bootstrap itself uses no pandas/numpy -- pure stdlib `random` with
a fixed integer seed, which is version-stable. The same reproducibility
discipline applies regardless (RE-025.5): interval values are not
canonical until confirmed under the pinned runtime, and no source of
non-determinism is assumed absent just because the arithmetic doesn't
touch the pinned-version-sensitive libraries.

What this does not authorize:

-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.
-   No gate-state change.
-   No reinterpretation of RE-PRED.13's point-estimate finding until
    the confidence intervals are confirmed under the pinned runtime.
-   No claim, yet, about whether any excess interval does or does not
    straddle zero -- that is exactly what pinned-runtime confirmation
    will determine, recorded in a future iteration.

Boundary:

-   Two new files: `engine/dependence_bootstrap.py`,
    `tests/diagnostic_dependence_bootstrap.py`.
-   `tests/verify_core.py` updated to recognize the new engine file.
-   No Frozen Core component modified.
-   No existing metric function
    (`mean_absolute_error`/`directional_hit_rate`/`rank_correlation`)
    modified or reimplemented.
-   No gate state changed.
-   No operative wiring changed.
-   No canonical interval values published yet -- pending pinned-runtime
    confirmation, to be recorded in a future iteration.

------------------------------------------------------------------------

## RE-PRED.16 — Canonical dependence-aware bootstrap values

RE-PRED.16 records the canonical results of RE-PRED.15's bootstrap,
confirmed by running `tests/diagnostic_dependence_bootstrap.py` under
`RUNTIME : PINNED`, closing RE-PRED.12's open question.

It is documentation-only. No code changed.

Cluster structure, confirmed:

    independence_clusters: 3
    cluster_sizes (desc): [10, 8, 1]

This differs from the 4 clusters (`[10, 7, 1, 1]`) seen in RE-PRED.15's
unpinned structural smoke test. Hand-verified against the already-
canonical RE-025.8 overlap pairs and RE-025.9 repeated-forecast groups:
tracing the union of both edge sets by hand over the 19 evaluable
records produces exactly the 10-node and 8-node components reported
here, plus one untouched singleton -- confirming the pinned result, not
the sandbox one. The discrepancy is attributed to the sandbox's
unpinned environment producing slightly different underlying forecast
values, which changes `repeated_forecast_groups()`'s exact-float-
equality grouping -- not a defect in the new bootstrap code. This is
the same discipline RE-025.5 already established, now demonstrated
concretely: even code that touches no pandas/numpy directly can surface
environment-dependent results, because it consumes forecasts computed
upstream by code that does.

Canonical bootstrap results (seed=42, replicates=5000, 90% interval):

    Metric      Series                          [low, high]              valid
    MAE         model                           [0.05796, 0.07982]       5000/5000
    MAE         primary baseline (RE-PRED.10)   [0.05440, 0.07937]       5000/5000
    MAE         mean-reversion (RE-PRED.13)     [0.14151, 0.22008]       5000/5000
    MAE         excess vs primary               [-0.00356, -0.00045]    5000/5000
    MAE         excess vs mean-reversion        [0.08355, 0.14025]       5000/5000

    hit-rate    model                           [0.88235, 1.00000]       5000/5000
    hit-rate    primary baseline                [0.88235, 1.00000]       5000/5000
    hit-rate    mean-reversion                  [0.88235, 1.00000]       5000/5000
    hit-rate    excess vs primary               [0.00000, 0.00000]       5000/5000
    hit-rate    excess vs mean-reversion        [0.00000, 0.00000]       5000/5000

    rank_corr   model                           [-0.51587, -0.12759]    4814/5000
    rank_corr   primary baseline                [-0.54100, -0.06691]    4814/5000
    rank_corr   mean-reversion                  [0.20362, 0.42683]       4814/5000
    rank_corr   excess vs primary               [-0.06068, 0.02514]     4814/5000
    rank_corr   excess vs mean-reversion        [-0.94270, -0.34208]    4814/5000

`valid_replicates` for rank correlation is 4814/5000 (96.3%) -- the
remaining replicas degenerate to `None` when a resample happens to
produce identical forecasts or actuals, excluded per the module's
absence-of-evidence rule, not imputed.

Finding, stated plainly, per metric:

MAE. The model's small loss to the primary baseline (RE-PRED.10:
excess -0.00188) is real, not noise -- the 90% interval is entirely
negative and does not straddle zero, though the margin itself is
small. The model's large win over mean-reversion (RE-PRED.13) is also
real and robust -- the interval is entirely positive, no ambiguity.

Hit-rate. The exact tie holds under resampling at every percentile
computed, against both baselines. This metric has no discriminating
power on this sample, confirmed, not just observed once.

Rank correlation -- the metric RE-PRED.13 flagged as the model's
weakest point. Two different answers for two different comparisons:

-   Vs. the primary baseline: NOT distinguishable from sampling noise.
    The 90% interval `[-0.06068, 0.02514]` straddles zero. RE-PRED.13's
    "the primary baseline beats the model on rank correlation" finding
    does not survive dependence-aware resampling -- it could be
    sampling noise given how few independent clusters actually exist.
-   Vs. mean-reversion: distinguishable from sampling noise, and
    strongly so. The 90% interval `[-0.94270, -0.34208]` is entirely
    negative, nowhere near zero. RE-PRED.13's full sign-flip finding
    (`+0.26316` vs `-0.26505`) is robust to the known dependence
    structure -- it is not an artifact of treating 19 dependent records
    as if they were independent.

This is RE-PRED.12's open question, answered concretely: baseline
choice matters for how much confidence a finding deserves. The primary-
baseline rank-correlation loss was real-looking but turns out to be
noise-fragile; the mean-reversion sign-flip was equally real-looking
and turns out to be robust. Neither could have been told apart from the
point estimates alone -- that is exactly why RE-PRED.12 refused to let
either be read as resolved until this iteration.

Rejected shortcuts:

-   Do not read the primary-baseline rank-correlation result as
    "resolved in the model's favor" -- "not distinguishable from noise"
    is not the same as "the model is fine on this metric."
-   Do not read the mean-reversion rank-correlation result as
    strengthened beyond what it already was -- RE-PRED.13's point
    estimate already showed the sign flip; this iteration confirms it
    is not a sampling artifact, nothing more.
-   Do not treat the hit-rate tie as informative about predictive
    quality -- it was already known to carry no signal in this
    comparison (RE-PRED.11/13); this iteration only confirms the tie is
    stable under resampling.
-   Do not extrapolate these intervals to a different N, dataset, or
    universe -- they are specific to the current 23-episode dataset and
    its current dependence structure.

Boundary:

-   No code changed in RE-PRED.16.
-   No `SimilarityEngine` change made or authorized.
-   No gate state changed.
-   No capital posture ceiling changed.
-   No operative wiring changed.
-   No target freeze changed.

------------------------------------------------------------------------

## RE-035.1 — Close EvidenceQualityGate's remaining stub inputs

RE-035.1 closes the two hardcoded stubs in `engine/evidence_quality_gate.py`
identified while scoping governance work: `independence_dispersion_measured`
was always `False`, and `predictive_validation_status` only special-cased
the literal string `"validated"`, collapsing every other case -- including
a formally tested-and-not-demonstrated result -- into the same generic
"not validated" explanation.

First finding, before any code: fixing these stubs does not, by itself,
change today's system-level capital posture. RE-034.1 already documents
that Regime Comparability Gate and Personal Capacity Boundary being
entirely unbuilt (0% -- boundary docs only) caps posture at `Conserve`
regardless of what Evidence Quality says. That remains the real
bottleneck; RE-035.1 is correctness work on Evidence Quality Gate, not a
fix to the visible decision output.

Changes:

-   `_overlapping_match_pairs(evidence)` -- new function. Counts pairs
    within the CURRENT match set (`evidence.matches`) whose outcome
    windows (`bottom_date` .. `bottom_date + horizon_years`) overlap.
    Same boolean definition as RE-025.8's `overlapping_outcome_windows()`,
    reimplemented rather than reused: that function takes
    `ValidationRecord` (offline backtesting, one `horizon_years` per
    record), this takes `Similarity` matches sharing one
    `evidence.horizon_years` -- different enough types that forcing a
    shared function would need a more convoluted adapter than a small
    parallel implementation. Fourth controlled duplication of this
    pattern in the project (validation_harness, baseline_harness,
    dimension_diagnostic already reimplement the analogous
    `ObservableUniverse`/`bottom_index` exclusion for the same reason).
-   `LocalEvidenceQualityInputs.overlapping_match_pairs: Optional[int]` --
    new field, so the measurement is exposed, not silently discarded
    behind a bare boolean.
-   `build_local_evidence_quality_inputs()` now sets
    `independence_dispersion_measured=True` and
    `overlapping_match_pairs=<real count>`, computed from the actual
    match set, instead of hardcoding `False`.
-   `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED = "not_demonstrated"` -- new
    recognized input value for `predictive_validation_status`. Does not
    add a new gate output state -- `EvidenceQualityGate.evaluate()` still
    only returns `NOT_MEASURABLE` or `CONSERVATIVE`, per RE-PRED.10.1's
    explicit decision to sharpen explanations rather than add a third
    state. When this value is passed, `evaluate()` now appends a specific
    explanation ("evaluated under a pre-registered protocol, required
    advantage not shown") instead of the generic "not validated" one.
    The module holds no RE-PRED-specific numbers -- it is the caller's
    responsibility to decide when this value applies, keeping the gate
    structure decoupled from any one research finding.
-   `tests/verify_evidence_quality_gate.py` updated: the hardcoded
    `False` expectation is replaced with a real-value check; a new case
    exercises the `not_demonstrated` path explicitly.

Structural verification: a synthetic smoke test (three mock episodes,
one overlapping pair) confirmed `_overlapping_match_pairs()` and the new
`evaluate()` branch behave as designed before any pinned-runtime check.

Confirmed under `RUNTIME : PINNED`, real pipeline, real match set:

    independence_dispersion_measured: True
    overlapping_match_pairs: 5
    state (predictive_validation_status=PREDICTIVE_VALIDATION_NOT_DEMONSTRATED):
        not measurable
    explanations: ["predictive validation status: not demonstrated --
        evaluated under a pre-registered protocol, required advantage
        not shown"]

The "independence / dispersion not measured" explanation no longer
appears, exactly as designed -- the gate's remaining `NOT_MEASURABLE`
reason today is purely `predictive_validation_status`, not a stub.

Separate, pre-existing, unrelated finding surfaced while running the
full test suite: `tests/verify_evidence_quality_gate.py`'s existing
`EXPECTED_LOCAL_CONSISTENCY` assertion (fixed in RE-030.2) now fails --
`0.9518456229064439` expected, `0.9524468147359584` produced, a
5th-decimal drift. RE-035.1 does not touch consistency computation at
all, and Armando confirmed he did not modify the Shiller source file.
Root cause not yet investigated -- candidate explanation is an upstream
Shiller data revision (historical CPI revisions shift real returns for
all episodes, not just recent ones), not confirmed. This is logged as
an open item for a future iteration, deliberately not fixed here: RE-
DOC-002 prohibits silently rewriting a canonical value without
understanding why it changed.

What this does not authorize:

-   No gate output state added beyond `NOT_MEASURABLE`/`CONSERVATIVE`.
-   No threshold defined for `overlapping_match_pairs` -- it is exposed,
    not yet used to fail or pass anything, consistent with
    coverage/consistency/diversity today also having no threshold, only
    a presence check.
-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine` or
    `ValidationEngine`.
-   No capital posture mapping change -- RE-034.1's provisional mapping
    stands unchanged.
-   No claim that this changes today's system-level posture output.

Boundary:

-   Two files changed: `engine/evidence_quality_gate.py`,
    `tests/verify_evidence_quality_gate.py`.
-   No Frozen Core component modified.
-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.
-   No gate state changed.
-   No operative wiring changed.
-   No fix attempted for the unrelated `EXPECTED_LOCAL_CONSISTENCY`
    drift -- logged as an open item, not resolved in this iteration.

------------------------------------------------------------------------

## RE-036.1 — Regime Comparability Gate: first measurable dimensions

RE-036.1 adds the first isolated implementation of the Regime
Comparability Gate boundary defined in RE-031.1.

Motivating finding, before any code: RE-031.1 left open which regime
dimensions are observable with current data. `models/context.py`
already carries `cape`, `inflation` and `interest_rate` per episode --
computed and populated, but `SimilarityEngine`'s score only consumes
`cape`, `pre_crash_return_3y` and `pre_crash_volatility_1y`.
`inflation` and `interest_rate` sit unused. This answers RE-031.1's
open question for three of its eight candidate dimensions without any
new data ingestion: valuation, inflation and interest-rate regime are
observable today.

Design, agreed with Armando before implementation:

-   Scope: local, against the current match set only (`evidence.
    matches`), not the full historical universe. This is RE-031.1's own
    framing of the question -- is the evidence actually informing
    today's decision structurally representative of today's regime --
    not a question about the dataset as a whole.
-   Method: strict `[min, max]` coverage. For each active dimension,
    does today's snapshot value fall within the range spanned by that
    dimension's values across the current matches? Binary, not graded --
    no percentile, no margin, no distance metric. Explicit reasoning:
    a single extreme match could widen the range and make a regime look
    "covered" when it barely is (small-N sensitivity, `n≈10`). Decision:
    do not anticipate this with un-observed-yet complexity (percentiles,
    trimmed ranges) -- start with the strict, fully transparent,
    zero-magic-number version; if an outlier problem is actually
    observed later, document it as a finding and address it then, not
    now.
-   Fail-closed, per RE-031.1: `None` (not `False`) when today's value
    or the match set's values for a dimension are missing -- absence of
    measurement is never treated as coverage, and is never treated as
    non-coverage either. It is its own explicit state.
-   Does not use `SimilarityEngine`'s selection, its scores, or Evidence
    Quality as a comparability proxy -- explicit prohibitions in
    RE-031.1. Coverage is measured independently of which episodes
    were selected as "similar"; a match can be close by drawdown/
    duration/speed and still sit in a completely different valuation
    or rate regime than today.

New file: `engine/regime_comparability_gate.py`.

-   `LocalRegimeComparabilityInputs` -- `Optional[bool]` per dimension
    (`cape_covered`, `inflation_covered`, `interest_rate_covered`), not
    a score. `None` = not measurable, `True`/`False` = measured result.
-   `_dimension_covered(today_value, match_values)` -- the strict
    `[min, max]` check, `None` if either side is unavailable.
-   `RegimeComparabilityGate.evaluate()` -- returns one of three states:
    `NOT_MEASURABLE` (zero dimensions measurable), `NOT_COMPARABLE` (at
    least one measured dimension falls outside its matches' range),
    `COMPARABLE` (all measured dimensions fall inside). A fresh,
    minimal vocabulary specific to this gate -- not reused from
    `EvidenceQualityGate`'s `NOT_MEASURABLE`/`CONSERVATIVE` pair, because
    the underlying question is different: Evidence Quality asks whether
    the sample is internally sound; Regime Comparability asks whether
    the sample even spans today's conditions. `NOT_COMPARABLE` has no
    equivalent on the Evidence Quality side.
-   `build_local_regime_comparability_inputs(snapshot, evidence)` --
    `snapshot` is the sole source of truth for today's regime;
    `evidence.matches` is the sole source of truth for the historical
    sample actually in use. Same non-drifting-inputs principle as
    `build_local_evidence_quality_inputs(evidence)`.

New test file: `tests/verify_regime_comparability_gate.py`. Exercises
`_dimension_covered()` directly (inside range, below, above, on
boundary, missing today value, empty match values, all-`None` match
values) and all three gate states with synthetic inputs. Also runs the
real pipeline and asserts the builder returns well-typed output -- this
iteration makes no canonical claim about what today's real snapshot
produces, only that the gate runs correctly end to end.

`tests/verify_core.py` updated to recognize both
`engine/evidence_quality_gate.py` (missing from that list since
RE-030.1) and `engine/regime_comparability_gate.py`.

Structural verification: synthetic checks for `_dimension_covered()`
and all three gate states pass in this sandbox. A synthetic end-to-end
check (mock snapshot/matches, values placed intentionally outside
range) confirms the builder and gate compose correctly. The real
pipeline run is pending pinned-runtime confirmation.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine`,
    `EvidenceQualityGate` or `gate_combination.py`.
-   No entry added to RE-034.1's posture-ceiling mapping table for
    `NOT_COMPARABLE` or `COMPARABLE` -- deciding how this gate's states
    cap posture is a separate governance decision, not a default
    consequence of the code existing.
-   No percentile, margin or outlier-robustness logic -- explicitly
    deferred until an actual problem is observed, per Armando's
    decision above.
-   No claim about volatility, liquidity/credit, policy or
    market-structure regime -- these remain unmeasurable, no data
    source exists for them yet.
-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.

Boundary:

-   Two new files: `engine/regime_comparability_gate.py`,
    `tests/verify_regime_comparability_gate.py`.
-   `tests/verify_core.py` updated to recognize both new/missing
    engine files.
-   No Frozen Core component modified.
-   No gate state changed.
-   No operative wiring changed.
-   No capital posture mapping changed.
-   Canonical real-pipeline values not published -- pending
    pinned-runtime confirmation.

------------------------------------------------------------------------

## RE-034.5 — Regime Comparability posture-ceiling mapping

RE-034.5 extends RE-034.1's provisional gate-ceiling mapping table with
the three real states RE-036.1 introduced for the Regime Comparability
Gate. It is documentation-only. No code changed.

RE-034.1 only anticipated a binary "not measurable" state for Regime
Comparability, because no code existed yet at the time. RE-036.1 gives
the gate three real states: `NOT_MEASURABLE`, `NOT_COMPARABLE`,
`COMPARABLE`. This iteration closes that gap. Per RE-DOC-002, RE-034.1's
original table is not rewritten -- this adds to it, forward.

Design, agreed with Armando before recording:

-   Regime Comparability `not comparable` -> `Conserve`. At least as
    restrictive as `not measurable`. This is not absence of
    information -- it is confirmed evidence that today's regime sits
    outside the historical sample actually informing the decision.
    Extrapolation risk, not uncertainty.
-   Regime Comparability `comparable` -> `Deploy Aggressively`, the top
    of the ordered scale. Reasoning: RE-031.1 requires this gate to
    never make posture more aggressive by itself, only cap it. Since
    combination takes the minimum ceiling across all gates, mapping the
    passing state to the top is the only way to encode "this gate
    imposes no restriction of its own" -- it can never become the
    binding constraint when satisfied. When Regime Comparability
    passes, the real ceiling is decided entirely by Evidence Quality
    and Personal Capacity, exactly as RE-031.1 requires ("a comparable
    regime does not make weak evidence strong").

Updated mapping table (supersedes RE-034.1's for Regime Comparability
only; Evidence Quality and Personal Capacity entries unchanged):

-   Evidence Quality `not measurable` -> `Prepare`;
-   Evidence Quality `conservative` -> `Conserve`;
-   Regime Comparability `not measurable` -> `Conserve`;
-   Regime Comparability `not comparable` -> `Conserve`;
-   Regime Comparability `comparable` -> `Deploy Aggressively`;
-   Personal Capacity unavailable / unclassified -> `Conserve`;
-   Any `Blocked` flag -> `Blocked`.

RE-034.1 open question closed: "Should Regime Comparability have its
own non-deployment exception in future, or is `not measurable ->
Conserve` permanent?" Answer: `not measurable` stays at `Conserve`
permanently as the fail-closed default -- that part of the question is
resolved by definition, not by new logic. The real question was what
happens once measurement exists at all, and RE-036.1 now provides that:
`comparable` removes the cap, `not comparable` confirms it.

Remaining RE-034.1 open questions, unaffected by this iteration:

-   Can `Prepare` ever be authorized solely by Regime Comparability
    while Evidence Quality remains `not measurable`? Still open --
    this iteration does not touch Evidence Quality's own mapping.
-   Does Personal Capacity belong in gate combination, or inside Human
    Approval? Still open, RE-032.1 remains unclassified.
-   How should explanations be composed when several gates cap posture
    at the same level? Still open.

What this does not authorize:

-   No code implementing this mapping -- it exists only as a documented
    decision. No function converts
    `RegimeComparabilityGateResult.state` into a `posture_ceiling`
    string yet.
-   No wiring into `gate_combination.py`, `DecisionEngine` or `run.py`.
-   No change to Evidence Quality's or Personal Capacity's own mapping
    entries.

Boundary:

-   No code changed.
-   No posture engine implemented.
-   No operative wiring authorized.
-   Documentation-only update to RE-034.1's provisional table, per
    RE-DOC-002's forward-correction discipline.

------------------------------------------------------------------------

## RE-037.1 — Isolated posture mapper (Evidence Quality + Regime Comparability)

RE-037.1 implements, for the first time in code, the mapping tables
documented in RE-034.1 and RE-034.5 -- turning "which posture ceiling
does this gate state imply" from a documentation-level worked example
into a real, callable function, still fully isolated from any
operative flow.

New file: `engine/posture_mapper.py`.

-   `EVIDENCE_QUALITY_POSTURE_CEILING` / `REGIME_COMPARABILITY_POSTURE_
    CEILING` -- dict literals, one entry per documented mapping row.
    Every entry traces to a specific status-doc section (RE-034.1 for
    Evidence Quality, RE-034.5 for Regime Comparability); no mapping is
    invented here.
-   `evidence_quality_to_gate_input()` / `regime_comparability_to_gate_
    input()` -- translate a gate's already-computed `Result` into a
    `GateCombinationInput`. Neither re-evaluates gate logic; both raise
    `ValueError` on an unrecognized state rather than silently
    defaulting to a ceiling -- an undocumented state must fail loudly,
    not resolve to a guess.
-   `evaluate_capital_posture(evidence_quality_result,
    regime_comparability_result)` -- composes both translations and
    calls `combine_gate_outputs()` (`engine/gate_combination.py`,
    RE-034.3) exactly as published. No combination logic is
    reimplemented.

Explicit, load-bearing caveat: Personal Capacity does not participate.
RE-032.1 has not classified it (parallel gate / human-approval
prerequisite / mixed control) and no code implements it. Per RE-034.1's
own worked example, an unavailable/unclassified Personal Capacity caps
posture at `Conserve` -- omitting it here means `evaluate_capital_
posture()`'s output is provably at least as permissive as a complete
combination would be. This is stated directly in the function's
docstring, not left implicit.

New test file: `tests/verify_posture_mapper.py`.

-   Synthetic checks: each documented mapping row individually: `blocked
    =False` always (neither gate has a veto mechanism yet); unrecognized
    states raise `ValueError`; several combined scenarios confirm the
    `min()` semantics -- notably that Regime Comparability `comparable`
    (mapped to the top of the scale) never overrides a more restrictive
    Evidence Quality state, and that `not comparable` caps posture even
    when Evidence Quality alone would allow more.
-   Real-pipeline audit dry-run: builds both gates' real results against
    today's snapshot and prints the full chain -- individual states,
    explanations, and the combined ceiling. Explicitly uses
    `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` for
    `GlobalModelValidationState`, reflecting RE-PRED.16's confirmed
    finding -- a deliberate choice stated in the script, not an
    automatic default. Read-only: prints a report, does not persist or
    act on anything.

`tests/verify_core.py` updated to recognize `engine/posture_mapper.py`
and (previously missing) `engine/gate_combination.py`.

Structural verification: synthetic checks for every mapping row,
unrecognized-state errors, and four combined scenarios pass in this
sandbox. The real-pipeline dry-run could not complete in this sandbox
this iteration -- the same intermittent iCloud file-lock issue already
seen in RE-035.1/RE-036.1 (`OSError: Resource deadlock avoided`), this
time failing on a plain module import before any data access. Unrelated
to this change. Pending pinned-runtime confirmation.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine` or
    `ValidationEngine`.
-   No claim that this is the Capital Posture Engine -- that remains a
    larger, future, operative component; this is a smaller, isolated
    composition layer for audit purposes only.
-   No Personal Capacity placeholder invented to fill the gap --
    explicitly absent, explicitly stated.
-   No change to `gate_combination.py`, `evidence_quality_gate.py` or
    `regime_comparability_gate.py`.
-   No capital action of any kind -- this layer prints or returns a
    ceiling, it does not act on it.

Boundary:

-   Two new files: `engine/posture_mapper.py`,
    `tests/verify_posture_mapper.py`.
-   `tests/verify_core.py` updated to recognize both new/missing
    engine files.
-   No Frozen Core component modified.
-   No existing gate or combination module modified.
-   No gate state changed.
-   No operative wiring changed.
-   Canonical real-pipeline audit output not published -- pending
    pinned-runtime confirmation.

------------------------------------------------------------------------

## RE-038.1 — Connect inflation/interest_rate; fix inflation level vs. rate

RE-038.1 closes two data-wiring gaps surfaced by RE-037.1's real audit
dry-run, and corrects a design error made in RE-036.1.

Correction to RE-036.1 (RE-DOC-002, forward, not silently rewritten):
that iteration stated `inflation` and `interest_rate` were "already
populated in `Context` per episode" -- this was false. Both fields were
hardcoded `None` in `engine/drawdown_engine.py::filter_episodes()` for
every historical episode, and `interest_rate` was also hardcoded `None`
in `engine/snapshot_engine.py::_build_snapshot()` for today's snapshot
(`inflation` there was already wired to `row["CPI"]`). This is exactly
why RE-037.1's real dry-run showed both dimensions as `not measurable`
-- not a data-availability question, a stub, discovered only once the
posture mapper made the full chain visible end to end.

Fix, part one -- wiring:

-   `engine/drawdown_engine.py::filter_episodes()`:
    `inflation`/`interest_rate` now read from the dataframe instead of
    being hardcoded.
-   `engine/snapshot_engine.py::_build_snapshot()`: `interest_rate` now
    reads from the dataframe (`inflation` was already correct).
-   `interest_rate` uses the `Rate GS10` column (US 10-Year Treasury
    Constant Maturity Rate) -- identified from
    `SnapshotEngine.latest()`'s own leftover debug print (`POSIBLES
    COLUMNAS MACRO`), now removed since it served its purpose.
-   Both fields share CAPE's existing characteristic of not filtering
    `NaN` at the source (`loaders/shiller_loader.py` only coerces
    `Date`/`P`) -- not a new risk introduced here, an existing,
    project-wide pattern, out of scope to fix in this iteration.

Fix, part two -- a real design error, caught before it mattered:
wiring `inflation` to raw `CPI` (the fix originally planned) would have
been wrong. `CPI` is an index level, near-monotonically increasing over
a century of history. Comparing today's level against any historical
episode's level would make Regime Comparability's `[min, max]` coverage
check fail almost tautologically -- not because today's inflation
regime is genuinely unprecedented, but because the index is chronologically
later, which it always will be. This was caught by inspecting the real
dry-run's numbers (a raw CPI level around 336) before publishing it as
a finding, not by design review alone.

-   New function `engine/drawdown_engine.py::calculate_inflation_rate()`
    -- adds `InflationRate1Y = CPI.pct_change(12)` to the dataframe,
    same `.rolling()`/`.pct_change()` pattern already used by
    `calculate_volatility()`. Called from `run_drawdown_engine()`
    immediately after `calculate_volatility()`.
-   Both `Context.inflation` sites (episodes and snapshot) now read
    `InflationRate1Y`, not `CPI`.

Structural verification, real pipeline, this sandbox -- NOT canonical:

    Before fix:  inflation_covered=None, interest_rate_covered=None
    After fix:   cape_covered=False, inflation_covered=True,
                 interest_rate_covered=True
    Regime Comparability state: not comparable
    Regime Comparability explanations: ["cape: today's value outside
        the matched episodes' range"]

Only CAPE remains out of range. This is a materially cleaner result
than before the fix -- the earlier `not comparable` verdict from
RE-037.1's dry-run was contaminated by two dimensions being
unmeasurable, not genuinely uncovered; today's result isolates the
actual signal.

A `FutureWarning` from pandas appeared during this sandbox run
(`Downcasting object dtype arrays on .fillna/.ffill/.bfill is
deprecated`), triggered inside `pct_change()` handling leading `NaN`
values in `CPI`. Not an error, not addressed in this iteration --
flagged so it is not mistaken for something new if it appears under
the pinned runtime too.

What this does not authorize:

-   No change to `SimilarityEngine`, `SIMILARITY_WEIGHTS`, or any
    Frozen Core component -- neither `inflation` nor `interest_rate`
    is consumed there.
-   No NaN-filtering fix for CAPE or any other Context field -- flagged
    as a known, pre-existing, project-wide characteristic, not resolved
    here.
-   No change to RE-036.1's `[min, max]` coverage method itself.
-   No claim about the `EXPECTED_LOCAL_CONSISTENCY` drift (RE-030.2) --
    unrelated, still open, deliberately left alone per the earlier
    decision not to touch data provenance questions without a
    confirmed root cause.

Boundary:

-   Two files changed: `engine/drawdown_engine.py`,
    `engine/snapshot_engine.py`.
-   No new files.
-   No Frozen Core component modified.
-   No gate, gate-combination or posture-mapper module modified.
-   No gate state-mapping table changed.
-   No operative wiring changed.
-   Confirmed under Armando's pinned runtime, exact match to sandbox:
    `cape_covered=False, inflation_covered=True,
    interest_rate_covered=True`, state `not comparable`, combined
    posture ceiling `Conserve`. As with all real-pipeline dry-run
    output in this document, this is a read against today's snapshot,
    not a frozen historical metric -- it will change as the date
    changes, and is never treated as a canonical claim in the
    RE-DOC-002 sense.

------------------------------------------------------------------------

## RE-039.1 — Standalone posture audit CLI

RE-039.1 extracts the real-pipeline audit dry-run that already lived
inside `tests/verify_posture_mapper.py` (its final section, added in
RE-037.1) into a dedicated, standalone entry-point script,
`audit_posture.py`, at repository root.

No logic changes. Same imports, same gate construction, same
`evaluate_capital_posture()` call, same disclaimers reproduced
verbatim (NOT a decision, not wired into `run.py` or `DecisionEngine`,
Personal Capacity excluded, result provably no more restrictive than
the real posture). The only difference from the version embedded in
the test file is the absence of assertions and a dedicated
`if __name__ == "__main__"` entry point, so it can be run on its own
(`python3 audit_posture.py`) without running the full verification
suite.

Placement follows the existing precedent set by `run.py`: a root-level
script that is not itself part of "Core" and is therefore not listed
in `tests/verify_core.py`'s checks, consistent with `run.py` also not
being listed there.

What this does not authorize:

-   No new gate, no new dimension, no change to any mapping table.
-   No wiring into `run.py` or `DecisionEngine`.
-   No change to `tests/verify_posture_mapper.py` -- the dry-run logic
    there is left in place, not removed, so the test suite's coverage
    of the real pipeline is unaffected.

Boundary:

-   One new file: `audit_posture.py`.
-   No files modified.
-   No Frozen Core component touched.
-   No gate, gate-combination or posture-mapper module modified.

------------------------------------------------------------------------

## RE-032.2 — Personal Capacity classified as a mixed control

RE-032.2 resolves RE-032.1's primary classification question:

    Is Personal Capacity a parallel gate,
    a human-approval requirement,
    or a mixed control?

Answer: mixed control. This is Armando's explicit decision, not an
inference drawn from the surrounding design -- recorded here as a
governance decision, the same way every prior consequential choice in
this document has been (RE-036.1's dimension proposal, RE-034.5's
posture-ceiling table, RE-037.1's implementation approach all required
the same explicit sign-off before being written).

Reasoning offered at decision time, for the record: RE-032.1 already
mandated that Personal Capacity's two input channels -- verifiable
facts and attested judgement -- must not be averaged into a single
score. That requirement is, structurally, already a mixed-control
design; classifying it as a pure gate or pure Human-Approval
requirement would have meant walking back a constraint RE-032.1 had
already set. A pure gate would force self-reported, crisis-sensitive
inputs like drawdown tolerance through the same automatic min()
combination as objective evidence -- exactly the "opaque confidence
score" RE-032.1 prohibits, and exactly the input most unreliable when
it matters most (RE-032.1's own drawdown-tolerance-risk paragraph). A
pure Human-Approval requirement would discard computability for the
half of Personal Capacity that is genuinely objective and verifiable
(liquidity, debt service, concentration) for no structural reason.

Resolved split:

-   Verifiable-facts channel (available liquidity, near-term cash
    needs, fixed obligations, debt service, income concentration,
    portfolio concentration, required emergency reserve, known time
    horizon constraints): becomes a future computable gate. When
    implemented, it participates in gate combination via `min()`,
    exactly like Evidence Quality and Regime Comparability -- ceiling
    only, cannot make posture more aggressive, fails closed on missing
    data.
-   Attested-judgement channel (perceived income stability,
    willingness to tolerate drawdown, ability to avoid forced selling,
    psychological capacity to hold through stress, household/life
    constraints): becomes a Human Approval prerequisite. It never
    enters `gate_combination.py`'s math, never produces an automatic
    posture ceiling, and is never computed by an engine -- consistent
    with the Constitution's principle that engines produce evidence,
    never portfolio decisions.

This directly answers one of RE-032.1's own open questions: "Does
Personal Capacity participate in gate-combination logic, or does it
sit inside Human Approval before any capital action is allowed?" --
both, split by channel, not either/or.

What this does not authorize:

-   No code. This is a classification decision, not an implementation.
-   No new gate, no new file, no schema for which specific facts or
    attestations are collected.
-   No Human Approval workflow defined -- its existence is now
    required by this classification, but its mechanics (who approves,
    how, how often, expiry, cooling-off periods after crisis-time
    revisions) remain fully open, per RE-032.1's own open-questions
    list.
-   No change to `posture_mapper.py`, `gate_combination.py`, or any
    existing gate's mapping table.
-   Does not resolve which specific facts are verifiable from existing
    records versus requiring manual entry -- still open.

Boundary:

-   No files changed except this document.
-   No code, no thresholds, no taxonomy.
-   Personal Capacity remains entirely outside the operative flow and
    outside the existing posture-mapper audit tooling
    (`audit_posture.py`, `tests/verify_posture_mapper.py`) -- both
    continue to state its exclusion explicitly, unchanged by this
    classification.

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

RE-PRED.3 defines the target-freeze decision boundary. The implemented
target remains the provisional freeze candidate, but not the definitive
frozen target. The existing MAE must be read as error over annualized
CAGR, not cumulative five-year return. Definitive target freeze requires
a future numbered decision.

RE-PRED.4 verifies source-column semantics directly against
`data/raw/shiller.xlsx`. Column H / `Price` is Real Price. Column J /
`Price.1` is Real Total Return Price, with stacked header labels
`Real` / `Total` / `Return` / `Price`. Therefore the current implemented
target is annualized real total-return CAGR from drawdown bottom over
the five-year horizon. This verifies the column semantics, but still
does not definitively freeze the target.

RE-PRED.5 defines target-freeze acceptance criteria. It orders the
remaining work by dependency: target mechanics and semantics first,
unit/horizon and absolute-vs-excess decision before baselines, then
missingness taxonomy, model-freeze reference and target unfreeze
criteria. It records that `Price.1` semantics are verified, but
bottom-detection and episode-boundary semantics are not yet audited.
The implemented target remains provisional, not definitively frozen.

RE-PRED.6 audits bottom detection and episode boundaries. It documents
that drawdown episodes are detected on nominal price `P`, while
future returns are measured on Real Total Return Price `Price.1`.
It also records that unrecovered drawdowns are structurally excluded
because episodes are appended only on recovery. Finally, it records a
verified date-arithmetic bug: `duration_months` and `recovery_months`
are calculated by subtracting `YYYY.MM` floats rather than calendar
months, affecting public Evidence recovery statistics and active
Similarity scoring. No code is changed in RE-PRED.6.

RE-BUG.1 promotes the date-arithmetic duration bug to near-term code-fix
priority. It defines acceptance criteria for a future fix: use explicit
calendar-month arithmetic, verify examples such as 1929.09 -> 1932.06 =
33 months, update public Evidence recovery statistics from corrected
values, compare selected match identifiers before and after the fix,
rerun Research / Assessment / Validation verifications, report any
downstream Similarity / Research Validation changes, and avoid mixing
the bug fix with target-freeze or governance work.

RE-BUG.2 fixes the calendar-month duration bug in code. It introduces
centralized `months_between()` arithmetic, updates drawdown duration and
recovery duration calculations, adds a duration-specific verification
test and updates canonical Research / Assessment / Research Validation
expectations.

RE-BUG.3 documents the post-fix impact. The current canonical evidence
surface now uses `Evidence.median_return = 0.10192496249726091`.
Research Validation now reports `mae = 0.06928793787076225`,
`directional_hit_rate = 0.9473684210526315` and
`rank_correlation = -0.26505171850684983`. These values supersede the
pre-fix values going forward without rewriting the historical record.

RE-DATA.1 records future Shiller data update automation as planned, not
implemented. Any future updater must validate workbook structure,
confirm `Price.1` semantics, back up the prior local source, rerun tests
and log the update before replacing `data/raw/shiller.xlsx`. Manual
updates remain the current process.

RE-PRED.7 defines the absolute-vs-excess-return boundary. Absolute
return stays the existing Evidence descriptive surface; it is not
redefined or renamed. Excess return over a primary naive baseline
(unconditional historical mean/median `future_return_5y`, evaluated
point-in-time) becomes the future predictive-validity surface, to be
computed in the Research Validation Harness, not in Evidence. MAE and
directional hit-rate require an explicit baseline forecast series to
compute excess against; rank correlation already tests ordering against
no signal and needs no separate excess transformation. No baseline value
is computed and no excess-return metric is implemented in this
iteration.

RE-PRED.8 defines acceptance criteria for the primary baseline and
corrects RE-PRED.7's rank-correlation claim forward: that claim assumed
a single global constant baseline, which would not be point-in-time
safe. The primary baseline is instead a point-in-time expanding median
of `future_return_5y`, computed by reusing `ObservableUniverse` and
bottom_index self-exclusion — the same temporal-safety machinery already
verified for the model's own forecast in RE-025.1 — evaluated over the
model's own evaluable record set. Because this baseline varies per
episode, its rank correlation is a real, computable comparison against
the model's, not an undefined quantity. Mean, and the remaining
secondary baselines, remain deferred. No baseline value is computed and
no code changes in this iteration.

RE-PRED.9 implements the primary baseline in code:
`engine/baseline_harness.py` and `tests/verify_baseline_harness.py`.
It reuses `ObservableUniverse`, bottom_index self-exclusion and the
existing MAE / hit-rate / rank correlation functions unmodified — no
Frozen Core component is touched, and no existing file changes except
`tests/verify_core.py`'s structural list. The invariant that a baseline
forecast can never be `None` when the model's own record is evaluable
is proven by construction (the model's matches are a subset of the
baseline's unconditional comparable pool) and checked explicitly by the
test, not assumed. The test has only been run outside the pinned
runtime, to confirm the code executes and the structural invariants
hold. No baseline value is canonical yet; RE-PRED.10 will record the
canonical baseline metrics once confirmed under `requirements.txt`.

RE-PRED.10 records those canonical values, confirmed under
`RUNTIME : PINNED`, and the finding that follows: the model does not
beat the primary baseline on any of the three canonical metrics — it
ties on directional hit-rate (0.94737 both) and loses on MAE
(baseline 0.06741 vs model 0.06929) and rank correlation (baseline
-0.23172 vs model -0.26505). Predictive validity, as defined by
RE-PRED.1's burden of proof, is not demonstrated relative to this
baseline. This sharpens the existing conservative `EvidenceQualityGate`
state with a direct quantitative result but does not itself change any
gate threshold or capital posture ceiling — that remains a separate,
explicit governance decision under RE-029.7.

A proposal to formalize `NOT_DEMONSTRATED` as a third
`EvidenceQualityGate` output state was raised immediately after
RE-PRED.10 and deferred in RE-PRED.10.1: it would rest on one baseline
over a non-independent N=19 sample, and today it would not change the
resulting posture ceiling versus the existing `not measurable` state.
RE-PRED.11 implements two secondary baselines (`zero_forecast`,
`mean_reversion_forecast = -drawdown`) in `engine/baseline_harness.py`
to test whether RE-PRED.10's finding survives a change of baseline,
structurally verified outside the pinned runtime only. RE-PRED.12
records, as an explicit open question, that baseline-choice robustness
(what RE-PRED.11 tests) and sampling-noise robustness (whether any
excess value is distinguishable from chance given N=19 dependent
records) are different questions — this iteration answers only the
first. The gate-state decision is deferred until the full three-baseline
picture is confirmed under the pinned runtime.

RE-PRED.13 records that confirmed picture. The model beats zero and
mean-reversion clearly on MAE (0.06929 vs 0.12749 and 0.18159), ties all
measurable baselines on directional hit-rate, and loses on rank
correlation to both the primary baseline and mean-reversion — the
mean-reversion case a full sign flip (+0.26316 vs the model's -0.26505).
RE-PRED.10.1's trigger ("loses to the full set on a majority of
metrics") was evaluated explicitly and does not activate, so
`NOT_DEMONSTRATED` remains deferred. A working hypothesis is registered,
not authorized as fact: drawdown depth alone may order outcomes better
than `SimilarityEngine`'s multidimensional conditioning, possibly
through signal dilution across `SIMILARITY_WEIGHTS` — flagged for
future investigation only, no Frozen Core change made or authorized.
Both new correlation values remain subject to RE-PRED.12's unresolved
sampling-noise caveat on the same N=19 dependent sample.

RE-PRED.14 adds an exploratory, read-only diagnostic
(`engine/dimension_diagnostic.py`,
`tests/diagnostic_similarity_dimensions.py`) testing the signal-dilution
hypothesis registered in RE-PRED.13 by isolating each active
`SimilarityEngine` dimension. Confirmed under the pinned runtime, no
dimension in isolation reproduces mean-reversion's positive rank
correlation -- all six remain negative, from -0.19692 (drawdown) to
-0.26353 (pre_crash_return_3y). Signal dilution is not supported as the
explanation. A revised hypothesis is registered, not authorized:
nearest-neighbor selection may not preserve monotonic rank order the
way a direct function of the query's own value does. No `SimilarityEngine`
change is made or authorized. RE-PRED.12's sampling-noise caveat applies
with extra force to this smaller, still-dependent slicing.

RE-PRED.15 closes RE-PRED.12's method gap directly.
`engine/dependence_bootstrap.py` builds independence clusters from the
union of RE-025.8's overlapping-outcome-window pairs and RE-025.9's
repeated-forecast groups, then runs a cluster bootstrap (whole clusters
resampled with replacement, never individual records) to produce
dependence-aware confidence intervals for the model, both baselines, and
their paired excess. Seed and replicate count are fixed constants
(`seed=42`, `replicates=5000`), a 90% percentile interval. Structurally
verified outside the pinned runtime only: 4 independence clusters over
the 19 evaluable records, sizes `[10, 7, 1, 1]` -- not a canonical value.
Whether the excess intervals against the primary and mean-reversion
baselines straddle zero is exactly the open question this answers, once
confirmed under the pinned runtime and recorded in a future iteration.

RE-PRED.16 records that confirmation. Canonical clusters: 3, sizes
`[10, 8, 1]` -- hand-verified against RE-025.8/RE-025.9's own canonical
tables. MAE excess vs. primary baseline is small but robust (90% CI
`[-0.00356, -0.00045]`, does not straddle zero); MAE excess vs.
mean-reversion is large and robust (`[0.08355, 0.14025]`). Hit-rate
excess is exactly zero at every percentile against both baselines --
the tie is stable under resampling. Rank correlation gives two
different answers: the excess vs. primary baseline straddles zero
(`[-0.06068, 0.02514]`) -- not distinguishable from sampling noise --
while the excess vs. mean-reversion does not (`[-0.94270, -0.34208]`)
-- RE-PRED.13's full sign-flip finding is robust to the known
dependence structure, not an artifact of it.

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

## Version 1.64

-   Added RE-032.2: Personal Capacity classified as a mixed control --
    Armando's explicit decision, resolving RE-032.1's primary
    classification question.
-   Verifiable-facts channel (liquidity, debt service, concentration,
    etc.) -> future computable gate, combined via `min()` like Evidence
    Quality and Regime Comparability.
-   Attested-judgement channel (drawdown tolerance, psychological
    capacity, etc.) -> Human Approval prerequisite, never enters
    gate-combination math, never an automatic ceiling.
-   Answers directly one of RE-032.1's open questions: Personal
    Capacity participates in gate combination AND sits inside Human
    Approval -- split by channel, not either/or.
-   Documentation-only. No code, no new gate, no schema for which
    specific facts/attestations are collected, no Human Approval
    workflow mechanics defined -- all remain open for future
    iterations.
-   Starts Path A from the prior session's roadmap review.

## Version 1.63

-   Added RE-039.1: standalone `audit_posture.py` at repository root,
    extracting the real-pipeline audit dry-run already present in
    `tests/verify_posture_mapper.py` into its own entry point. No
    logic change -- same gates, same disclaimers, no assertions, can
    be run on its own without the full verification suite.
-   Placement mirrors `run.py`'s existing precedent: not listed in
    `tests/verify_core.py` (root-level entry scripts aren't "Core").
-   RE-038.1's real-pipeline values confirmed under Armando's pinned
    runtime, exact match to sandbox: `cape_covered=False,
    inflation_covered=True, interest_rate_covered=True`, state
    `not comparable`, combined posture ceiling `Conserve`.
-   Closes items B and C from the "seguimos, dime que tocaria hacer"
    path review (B: data-wiring hygiene, C: standalone posture audit
    tool). Path A (Personal Capacity classification) remains open,
    next only if there is time/energy in a future session.

## Version 1.62

-   Added RE-038.1: connected `inflation`/`interest_rate`, previously
    hardcoded `None` everywhere; corrected `inflation` from raw CPI
    level to a trailing 12-month rate.
-   Corrected forward (RE-DOC-002) a false claim in RE-036.1: these
    fields were never actually populated, despite that iteration's
    text saying so -- surfaced by RE-037.1's real audit dry-run.
-   `engine/drawdown_engine.py`: new `calculate_inflation_rate()`
    (`InflationRate1Y = CPI.pct_change(12)`), same pattern as
    `calculate_volatility()`. `filter_episodes()` now wires both
    fields from the dataframe instead of hardcoding `None`.
-   `engine/snapshot_engine.py`: `interest_rate` now wired to
    `Rate GS10`. Removed the leftover `POSIBLES COLUMNAS MACRO` debug
    print that appeared in every test run -- it had served its
    purpose (identifying the column).
-   Sandbox structural check (NOT canonical): before,
    `inflation_covered`/`interest_rate_covered` were both `None`; after,
    both measurable (`True`), leaving only `cape` as the real driver of
    `not comparable` -- a materially cleaner result.
-   No `SimilarityEngine` change -- neither field is consumed there.
-   Left the `EXPECTED_LOCAL_CONSISTENCY` drift (RE-030.2) and the
    CAPE/context NaN-filtering pattern explicitly untouched -- both
    out of scope for this iteration.

## Version 1.61

-   Added RE-037.1: first code implementation of RE-034.1/RE-034.5's
    posture-ceiling mapping tables.
-   Added `engine/posture_mapper.py`
    (`evidence_quality_to_gate_input()`, `regime_comparability_to_
    gate_input()`, `evaluate_capital_posture()`). Unrecognized gate
    states raise `ValueError` rather than silently defaulting.
-   Explicitly excludes Personal Capacity (RE-032.1 unclassified, no
    gate exists) -- stated in the module, not hidden; output is
    provably at least as permissive as a full combination would be.
-   Added `tests/verify_posture_mapper.py`: synthetic checks for every
    mapping row and combined scenario, plus a read-only audit dry-run
    against today's real snapshot using
    `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` (RE-PRED.16).
-   `tests/verify_core.py` updated to recognize
    `engine/posture_mapper.py` and (previously missing)
    `engine/gate_combination.py`.
-   Not wired into `run.py`, `DecisionEngine` or any operative flow --
    this is an isolated composition layer for audit purposes, not the
    Capital Posture Engine.
-   Real-pipeline dry-run not completed in sandbox this iteration
    (transient iCloud file-lock error, unrelated to the change);
    pending pinned-runtime confirmation.

## Version 1.60

-   Added RE-034.5: extended RE-034.1's provisional gate-ceiling mapping
    table with Regime Comparability's three real states from RE-036.1.
-   `not comparable` -> `Conserve` (confirmed extrapolation risk, at
    least as restrictive as `not measurable`).
-   `comparable` -> `Deploy Aggressively` (top of the ordered scale --
    the only way to encode "this gate imposes no restriction of its
    own" under min()-based combination; the real ceiling stays decided
    by Evidence Quality and Personal Capacity).
-   Closed RE-034.1's open question about a future non-deployment
    exception for Regime Comparability -- resolved by definition for
    `not measurable`, and by this new mapping for the other two states.
-   Documentation-only. No code changed. No wiring into
    `gate_combination.py` authorized.

## Version 1.59

-   Added RE-036.1: first implementation of the Regime Comparability
    Gate boundary from RE-031.1.
-   Added `engine/regime_comparability_gate.py`
    (`LocalRegimeComparabilityInputs`, `RegimeComparabilityGate`,
    `_dimension_covered()`, `build_local_regime_comparability_inputs()`).
-   Three active dimensions: `cape`, `inflation`, `interest_rate` --
    already populated in `Context` per episode, unused by
    `SimilarityEngine`'s score, no new data ingestion required.
-   Method: strict `[min, max]` coverage of today's snapshot value
    against the current match set's range for each dimension. No
    percentile or margin -- deliberately deferred until an actual
    small-N outlier problem is observed, not anticipated with
    unneeded complexity.
-   Fail-closed per RE-031.1: missing values produce `None`
    (not measurable), never treated as coverage or non-coverage.
-   Three gate states, specific to this gate, not reused from
    `EvidenceQualityGate`: `NOT_MEASURABLE`, `NOT_COMPARABLE`,
    `COMPARABLE`.
-   Added `tests/verify_regime_comparability_gate.py`.
-   `tests/verify_core.py` updated to recognize
    `engine/regime_comparability_gate.py` and (previously missing)
    `engine/evidence_quality_gate.py`.
-   Not wired into any operative flow. No entry added to RE-034.1's
    posture mapping table -- that remains a separate governance
    decision.
-   Structural verification only in this sandbox; real-pipeline
    values pending pinned-runtime confirmation.

## Version 1.58

-   Added RE-035.1: closed both hardcoded stubs in
    `engine/evidence_quality_gate.py`.
-   `independence_dispersion_measured` is now computed for real
    (pairwise outcome-window overlap across the current match set, same
    definition as RE-025.8) instead of hardcoded `False`. New field
    `overlapping_match_pairs` exposes the count.
-   Added `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` as a recognized
    `predictive_validation_status` value, producing a sharper
    explanation -- no new gate output state added, per RE-PRED.10.1.
-   Updated `tests/verify_evidence_quality_gate.py` accordingly; added a
    case exercising the `not_demonstrated` path.
-   Noted explicitly: this does not change today's system-level capital
    posture -- RE-034.1's mapping still caps at `Conserve` because
    Regime Comparability and Personal Capacity are entirely unbuilt.
-   Confirmed under `RUNTIME : PINNED`: `independence_dispersion_measured
    = True`, `overlapping_match_pairs = 5` on the real match set; the
    `not_demonstrated` explanation path fires correctly.
-   Logged a separate, pre-existing, unrelated finding: the existing
    `EXPECTED_LOCAL_CONSISTENCY` canonical value (RE-030.2) no longer
    matches the live pipeline (`0.9518456229064439` expected,
    `0.9524468147359584` produced). RE-035.1 does not touch consistency
    computation. Root cause not investigated; not fixed in this
    iteration, per RE-DOC-002.

## Version 1.57

-   Added RE-PRED.16: canonical dependence-aware bootstrap values,
    confirmed under `RUNTIME : PINNED`, closing RE-PRED.12.
-   Recorded canonical cluster structure: 3 independence clusters,
    sizes `[10, 8, 1]` -- not the 4 (`[10, 7, 1, 1]`) seen in
    RE-PRED.15's unpinned structural smoke test. Hand-verified against
    RE-025.8/RE-025.9's own canonical tables; discrepancy attributed to
    the unpinned sandbox producing slightly different forecast values,
    which changes `repeated_forecast_groups()`'s exact-float-equality
    grouping -- not a defect in the bootstrap code.
-   Recorded canonical 90% bootstrap intervals for MAE, hit-rate and
    rank correlation, for the model, both baselines, and their paired
    excess (seed=42, replicates=5000).
-   Found that MAE excess vs. both baselines is robust (does not
    straddle zero in either direction); hit-rate excess is exactly zero
    at every percentile against both baselines.
-   Found that rank-correlation excess vs. the primary baseline
    straddles zero -- RE-PRED.13's "model loses to primary on rank
    correlation" finding is not distinguishable from sampling noise.
-   Found that rank-correlation excess vs. mean-reversion does not
    straddle zero -- RE-PRED.13's full sign-flip finding is robust to
    the known N=19 dependence structure, not an artifact of it.
-   No code changed in RE-PRED.16. No gate state changed.

## Version 1.56

-   Added RE-PRED.15: Dependence-aware cluster bootstrap, closing the
    RE-PRED.12 method gap.
-   Added `engine/dependence_bootstrap.py`
    (`independence_clusters()`, `cluster_bootstrap_ci()`,
    `cluster_bootstrap_paired_excess()`) and
    `tests/diagnostic_dependence_bootstrap.py`, an exploratory,
    non-canonical, non-regression-gated script that still enforces the
    pinned-runtime check (RE-025.5).
-   Clusters built via connected components over the union of
    `overlapping_outcome_windows()` (RE-025.8) and
    `repeated_forecast_groups()` (RE-025.9) -- no new dependence
    criterion introduced, both edge sources already validated.
-   Bootstrap resamples whole clusters with replacement, never
    individual records, per RE-PRED.1's dependence-aware resampling
    requirement; i.i.d. resampling over the 19 records remains
    prohibited.
-   Paired excess resampling applies the identical cluster draw to
    model and baseline in the same replica, preserving paired variance
    structure.
-   Fixed, documented constants: `BOOTSTRAP_SEED=42`,
    `BOOTSTRAP_REPLICATES=5000`, 90% percentile interval.
-   `tests/verify_core.py` updated to recognize
    `engine/dependence_bootstrap.py`, per the RE-025.7/RE-PRED.9
    precedent.
-   Structural smoke test outside the pinned runtime, not canonical: 4
    independence clusters over the 19 evaluable records, sizes
    `[10, 7, 1, 1]`.
-   No Frozen Core component modified. No canonical interval values
    published yet -- pending pinned-runtime confirmation, to be
    recorded in a future iteration.

## Version 1.55

-   Added RE-PRED.14: Similarity dimension diagnostic.
-   Added `engine/dimension_diagnostic.py`
    (`dimension_forecast()`, `dimension_records()`,
    `DIMENSION_SCORE_FIELDS`) and
    `tests/diagnostic_similarity_dimensions.py`, an exploratory,
    non-canonical, non-regression-gated script that still enforces the
    pinned-runtime check (RE-025.5).
-   Reused `SimilarityEngine.compare()` unmodified; no Frozen Core
    component changed.
-   Excluded `recovery` from the diagnostic deliberately, per RE-021's
    existing data-leakage fix.
-   Found and fixed a bug in the new diagnostic script itself (not in
    `SimilarityEngine`): sorting by `pre_crash_return_3y_score` failed on
    `None` values; fixed by excluding `None`-scored comparables from
    that dimension's ranking, mirroring
    `SimilarityEngine._weighted_score()`'s existing `None`-exclusion
    rule.
-   Recorded canonical diagnostic results confirmed under
    `RUNTIME : PINNED`: no single active dimension reproduces
    mean-reversion's `+0.26316` rank correlation; all six remain
    negative, from `drawdown_score = -0.19692` to
    `pre_crash_return_3y_score = -0.26353`.
-   Concluded that the signal-dilution hypothesis registered in
    RE-PRED.13 is not supported.
-   Registered a revised hypothesis, explicitly not authorized as fact:
    the gap may be structural (nearest-neighbor selection vs. a direct
    monotonic function of the query's own value), not a dimension-
    weighting problem.
-   Reiterated RE-PRED.12's sampling-noise caveat with extra force for
    this smaller, still-dependent slicing.
-   No `SimilarityEngine` change made or authorized.

## Version 1.54

-   Added RE-PRED.13: Canonical secondary baseline values and
    full-picture finding.
-   Recorded canonical values confirmed under `RUNTIME : PINNED`:
    `zero_mae = 0.12749337012113`, `reversion_mae = 0.18158697149305`,
    `reversion_hit_rate = 0.94736842105263`,
    `reversion_rank_correlation = 0.26315789473684`.
-   Confirmed `zero_hit_rate`/`zero_rank_correlation = None` and
    `missing_reversion_forecast_count = 0`, exactly as expected by
    construction.
-   Recorded the full-picture finding: the model beats zero and
    mean-reversion clearly on MAE, ties all measurable baselines on
    directional hit-rate, and loses on rank correlation to both the
    primary baseline and mean-reversion — the mean-reversion case a
    full sign flip.
-   Evaluated the RE-PRED.10.1 deferral trigger explicitly: does not
    activate. `NOT_DEMONSTRATED` remains a deferred proposal.
-   Registered a working hypothesis, explicitly not authorized as fact:
    possible signal dilution in `SimilarityEngine`'s multidimensional
    weighting versus drawdown depth alone. No Frozen Core change made
    or authorized.
-   Reiterated that both new correlation values remain subject to
    RE-PRED.12's unresolved sampling-noise caveat.
-   No code changed.

## Version 1.53

-   Added RE-PRED.10.1: recorded and deferred a proposal to formalize
    `NOT_DEMONSTRATED` as a third `EvidenceQualityGate` output state.
    Deferral reasons: rests on one baseline over a non-independent N=19
    sample; no operative posture-ceiling consequence today versus the
    existing `not measurable` state; touches `GateCombination` taxonomy
    before a concrete behavioral reason exists. Recorded an explicit
    trigger for revisiting once secondary baselines are confirmed.
-   Added RE-PRED.11: implemented `zero_forecast()` and
    `mean_reversion_forecast()` (`-drawdown`, zero fitted parameters) in
    `engine/baseline_harness.py`, plus generic
    `build_baseline_records(model_records, forecast_fn)`. No existing
    function modified. Added `tests/verify_secondary_baselines.py`,
    re-asserting existing canonical values as a regression guard and
    printing the full three-way comparison table. No canonical
    secondary-baseline value established yet.
-   Added RE-PRED.12: recorded, as an explicit open question,
    that baseline-choice robustness (addressed by RE-PRED.11) and
    sampling-noise robustness (whether excess values are distinguishable
    from chance given N=19 dependent records) are different questions.
    The second remains unresolved and unauthorized for naive i.i.d.
    resampling, per RE-PRED.1.
-   No code changed in RE-PRED.10.1 or RE-PRED.12.

## Version 1.52

-   Added RE-PRED.10: Canonical baseline values and predictive-validity
    finding.
-   Recorded canonical baseline values confirmed under `RUNTIME : PINNED`:
    `baseline_mae = 0.06740858559979`,
    `baseline_hit_rate = 0.94736842105263`,
    `baseline_rank_correlation = -0.23171864780822`.
-   Recorded canonical excess values: `excess_mae = -0.00187935227097`,
    `excess_hit_rate = 0.00000000000000`,
    `excess_rank_correlation = -0.03333307069863`.
-   Confirmed `missing_baseline_forecast_count = 0` empirically under the
    pinned runtime, not only by construction.
-   Recorded the finding plainly, as committed to in advance in
    RE-PRED.7/RE-PRED.8: the model does not beat the primary baseline on
    any of the three canonical metrics — it ties on directional
    hit-rate and loses on MAE and rank correlation.
-   Stated that predictive validity, under RE-PRED.1's burden of proof,
    is not demonstrated relative to this baseline.
-   Connected this finding to the existing conservative
    `EvidenceQualityGate` state (RE-029.6/RE-029.7) as sharpening, not
    changing it — no gate threshold or capital posture ceiling is
    altered by this iteration.
-   No code changed.

## Version 1.51

-   Added RE-PRED.9: Primary baseline implementation.
-   Added `engine/baseline_harness.py`: `baseline_forecast()`,
    `BaselineHarness`, `missing_baseline_forecast_count()`,
    `excess_summary()`.
-   Added `tests/verify_baseline_harness.py`: functional smoke test,
    deliberately without hardcoded canonical baseline values.
-   Added `engine/baseline_harness.py` to `tests/verify_core.py`'s
    structural Engines list.
-   No Frozen Core component modified. No existing file modified except
    `tests/verify_core.py`'s structural list.
-   Reused `ObservableUniverse`, bottom_index self-exclusion and the
    existing MAE / hit-rate / rank correlation functions unmodified —
    no duplicated metric logic.
-   Proved by construction, and checked explicitly in the test, that a
    baseline forecast can never be `None` when the corresponding model
    record is evaluable.
-   Verified structurally (record alignment, evaluable-count alignment,
    the no-missing-forecast invariant) outside the pinned runtime only.
-   Explicitly did not hardcode canonical baseline metrics: RE-025.5
    already established that non-pinned runs can differ from the pinned
    canonical values, and treating a non-pinned result as canonical here
    would repeat the mistake RE-BUG.2 corrected. Canonical baseline
    values are deferred to RE-PRED.10, pending pinned-runtime
    confirmation.

## Version 1.50

-   Added RE-PRED.8: Primary baseline acceptance criteria.
-   Corrected RE-PRED.7's rank-correlation claim forward: the primary
    baseline is not a single global constant, so it does have rank
    variation and its rank correlation is a real, computable comparison
    against the model's — not an undefined quantity.
-   Defined the primary baseline as a point-in-time expanding median of
    `future_return_5y`, reusing `ObservableUniverse` and bottom_index
    self-exclusion — the same temporal-safety machinery already verified
    for the model's own forecast in RE-025.1.
-   Required the baseline to be evaluated over the exact same evaluable
    record set already used by `ValidationHarness` (19 records), not a
    separately invented sample.
-   Fixed median, not mean, as the primary baseline statistic, to keep
    the comparison against `Evidence.median_return` apples-to-apples.
-   Deferred secondary baselines (constant full-universe forecast, zero
    / no-change, mean-reversion) to a later iteration; required the
    constant full-universe forecast, if used later, to be labeled
    explicitly as not point-in-time-safe.
-   No code changed. No baseline value computed. No excess-return metric
    implemented.

## Version 1.49

-   Added RE-PRED.7: Absolute vs Excess Return Boundary.
-   Separated absolute return (existing Evidence descriptive surface,
    unchanged) from excess return over a naive baseline (future
    predictive-validity surface, not yet implemented).
-   Selected the unconditional historical mean/median `future_return_5y`
    as the primary baseline, evaluated point-in-time.
-   Kept constant full-universe forecast, zero/no-change and simple
    mean-reversion as secondary diagnostic baselines, per the RE-PRED.1
    mandatory-comparison requirement.
-   Defined per-metric excess mechanics: MAE and directional hit-rate
    need an explicit baseline forecast series; rank correlation already
    tests ordering against no signal and needs no separate excess
    transformation.
-   Established that excess return belongs to the Research Validation
    Harness, not to `Evidence` or `models/evidence.py`.
-   Recorded, in advance, that the most likely outcome once excess
    return is computed is that the primary baseline matches or beats the
    model on at least one canonical metric, given RE-025.3 and RE-BUG.3.
-   No code changed. No baseline value computed. No excess-return metric
    implemented.

## Version 1.48

-   Added RE-DATA.1: Shiller source update automation note.
-   Recorded that Shiller data updates remain manual today.
-   Recorded future automation as a validated data-update pipeline, not
    a blind network overwrite.
-   Required any future updater to validate workbook structure and
    `Price.1` semantics before replacing local data.
-   Required backup, test reruns and explicit update logging for any
    future automated refresh.
-   Deferred implementation until after RE-PRED target / baseline work
    is closed.
-   No code changed.

## Version 1.47

-   Added RE-BUG.3: Calendar-month duration fix impact record.
-   Documented that RE-BUG.2 fixed the verified calendar-month duration
    arithmetic bug in code.
-   Recorded that the fix affects active Similarity scoring through both
    duration and speed.
-   Recorded the current post-fix match set:
    `[2018.12, 1998.09, 1966.10, 2020.03, 1960.10, 1990.10, 2022.10,
    1962.06, 1880.05, 1903.10]`.
-   Established the post-fix canonical `Evidence.median_return` as
    `0.10192496249726091`.
-   Established the post-fix canonical Research Validation metrics:
    `mae = 0.06928793787076225`,
    `directional_hit_rate = 0.9473684210526315` and
    `rank_correlation = -0.26505171850684983`.
-   Recorded that pre-fix canonical values remain historical and are
    superseded forward, not silently rewritten.
-   Reaffirmed that the predictive-validity conclusion remains
    conservative after the fix.
-   No code changed in RE-BUG.3.

## Version 1.46

-   Added RE-BUG.1: Calendar-month duration bug acceptance criteria.
-   Classified the `duration_months` / `recovery_months` issue as a
    verified implementation bug, not a methodology question.
-   Marked the bug as near-term code-fix priority because it already
    affects public Evidence recovery statistics and active Similarity
    scoring.
-   Required future fix to use explicit calendar-month arithmetic rather
    than `YYYY.MM` float subtraction.
-   Required regression coverage for `1929.09 -> 1932.06 = 33 months`.
-   Required verification that all current episode durations and recovery
    durations are calendar-correct after the fix.
-   Required public Evidence recovery statistics to be recalculated from
    corrected values.
-   Required selected match identifiers to be compared before and after
    the future fix.
-   Required rerunning `verify_research_engine.py`,
    `verify_assessment_engine.py` and `verify_validation_metrics.py`
    after the future fix.
-   Required explicit reporting of any downstream Similarity or Research
    Validation metric changes caused by corrected duration arithmetic.
-   Prohibited mixing the bug fix with target-freeze, baseline, holdout
    or gate-threshold work.
-   No code changed.

## Version 1.45

-   Added RE-PRED.6: Bottom detection / episode boundary audit.
-   Documented current peak, drawdown, episode start, bottom, recovery,
    duration and target-anchor definitions from `engine/drawdown_engine.py`.
-   Confirmed that drawdown detection uses nominal price `P`.
-   Confirmed that target returns use `Price.1`, verified in RE-PRED.4
    as Real Total Return Price.
-   Recorded the price-basis asymmetry between nominal-price episode
    detection and real-total-return target measurement.
-   Recorded that unrecovered drawdowns are structurally excluded because
    episodes are appended only when `Drawdown == 0` recovery occurs.
-   Recorded that the current dataset has 23 episodes and all have
    recovery dates, so the structural exclusion does not currently create
    a missing active episode in the produced episode list.
-   Recorded a verified date-arithmetic bug: `duration_months` and
    `recovery_months` subtract `YYYY.MM` floats instead of calendar
    months.
-   Documented that the duration bug affects public Evidence recovery
    statistics and may affect Similarity.
-   No code changed.

## Version 1.44

-   Added RE-PRED.5: Target freeze acceptance criteria.
-   Ordered target-freeze criteria by dependency instead of presenting a
    flat checklist.
-   Clarified that source-column semantics are verified, but
    bottom-detection and episode-boundary semantics are not yet audited.
-   Required unit / horizon and absolute-vs-excess decisions before
    baseline design.
-   Prohibited closing baseline design before the absolute-vs-excess
    target decision is explicit.
-   Required a future missingness taxonomy distinguishing not-yet-
    matured outcomes, structurally missing data and source failure.
-   Referenced the RE-PRED.1 model-freeze checklist instead of
    duplicating it.
-   Added target unfreeze criteria and prohibited reopening the target
    because validation results are disappointing.
-   Preserved current `future_return_5y` as provisional freeze candidate
    only, not definitive frozen target.
-   No code changed.

## Version 1.43

-   Added RE-PRED.4: Source column semantics verification.
-   Verified directly against `data/raw/shiller.xlsx` that pandas
    `Price.1` corresponds to Shiller column J.
-   Recorded that rows 4-8 of the workbook header were inspected and no
    merged cells were present in that header area.
-   Verified column H / `Price` as Real Price from stacked labels
    `Real` / `Price`.
-   Verified column J / `Price.1` as Real Total Return Price from
    stacked labels `Real` / `Total` / `Return` / `Price`.
-   Promoted the previous RE-PRED.2 inference about `Price.1` to a
    verified fact.
-   Clarified that current `future_return_5y` is annualized real
    total-return CAGR from drawdown bottom over the five-year horizon.
-   Preserved the distinction between implemented target, provisional
    freeze candidate and definitive frozen target.
-   No code changed.

## Version 1.42

-   Added RE-PRED.3: Target freeze decision boundary.
-   Designated the current implemented target, `future_return_5y`, as
    the provisional freeze candidate.
-   Clarified that the target is not definitively frozen.
-   Clarified that `Price.1` source-column semantics are not yet
    verified and must not be described as real total-return until
    confirmed from an authoritative source.
-   Required future verification of whether `Price.1` represents real
    price, real total return, nominal price, nominal total return or
    another source-specific construct.
-   Preserved annualized CAGR as the provisional target form.
-   Added MAE reinterpretation: the canonical MAE is error over
    annualized CAGR, not cumulative five-year return.
-   Deferred absolute vs excess-return choice to future baseline design.
-   Preserved `bottom_date` as the provisional start anchor.
-   Recorded that live tracking should eventually distinguish not-yet-
    matured outcomes from structurally missing data and source failure.
-   No code changed.

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
