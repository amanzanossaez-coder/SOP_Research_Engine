#!/usr/bin/env python3
"""
SOP Research Engine
Similarity Dimension Diagnostic

RE-PRED.14 -- exploratory, read-only diagnostic. NOT a verify_*.py
regression gate: it makes no canonical claim and asserts no expected
values. It exists to investigate one specific question raised by
RE-PRED.13: mean-reversion (-drawdown alone) beat the model on rank
correlation by a full sign flip (+0.26316 vs -0.26505). Does isolating
SimilarityEngine's active dimensions, one at a time, show any single
dimension driving that inversion -- consistent with the "signal
dilution" hypothesis registered (not authorized) in RE-PRED.13?

Does NOT modify SimilarityEngine. Reuses SimilarityEngine.compare()
exactly as published -- it already computes every dimension's individual
score alongside the blended one; this script only re-sorts those
already-computed scores by a single dimension instead of the blend.

"recovery" is deliberately excluded -- RE-021 already removed it from
the combined score as a data-leakage fix (it is Outcome, not known
until the episode resolves). Including it here would reintroduce the
same leakage this diagnostic has no business reopening.

Per-dimension evaluable counts can differ from the model's 19 and from
each other: re-sorting by a different dimension can select a different
top-10, which can change how many of those matches already have a
realized future_return_5y. This is reported explicitly, not hidden.

Caveat (RE-PRED.12, applies with extra force here): every column below
is computed over an even smaller, still-dependent slice of the same
23-episode dataset. Nothing here is a significance test. This is
hypothesis generation, not hypothesis confirmation.
"""

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.dimension_diagnostic import (
    DIMENSION_SCORE_FIELDS,
    dimension_records,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.validation_harness import ValidationHarness
from engine.validation_metrics import (
    directional_hit_rate,
    mean_absolute_error,
    rank_correlation,
)


def pinned_runtime() -> dict[str, str]:
    requirements = {}

    for line in (ROOT / "requirements.txt").read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "==" not in line:
            continue

        package, expected_version = line.split("==", 1)
        requirements[package] = expected_version

    return requirements


def verify_runtime() -> None:
    expected = pinned_runtime()
    mismatches = []

    for package, expected_version in expected.items():
        try:
            actual_version = version(package)
        except PackageNotFoundError:
            actual_version = "not installed"

        if actual_version != expected_version:
            mismatches.append(
                f"Expected {package}=={expected_version}, got {actual_version}"
            )

    if mismatches:
        print("RUNTIME : MISMATCH")

        for mismatch in mismatches:
            print(mismatch)

        print(
            "This is an exploratory diagnostic, but the same "
            "reproducibility rule applies (RE-025.5): numbers from an "
            "unpinned environment are not to be treated as meaningful."
        )
        raise SystemExit(1)

    print("RUNTIME : PINNED")


def fmt(value) -> str:
    if value is None:
        return "None"

    return f"{value:.5f}"


def main() -> None:
    verify_runtime()

    dataset = run_drawdown_engine()

    harness = ValidationHarness(dataset)
    model_records = harness.run()

    model_evaluated = harness.evaluated_count(model_records)
    model_mae = mean_absolute_error(model_records)
    model_hit_rate = directional_hit_rate(model_records)
    model_rank_correlation = rank_correlation(model_records)

    print()
    print("SIMILARITY DIMENSION DIAGNOSTIC : EXPLORATORY")
    print(f"episodes: {len(dataset.episodes)}")
    print(f"model_evaluated_count: {model_evaluated}")
    print()
    print(
        f"{'dimension':<28}{'evaluated':>10}{'MAE':>10}"
        f"{'hit-rate':>10}{'rank_corr':>11}"
    )
    print("-" * 69)
    print(
        f"{'model (blended, RE-BUG.3)':<28}{model_evaluated:>10}"
        f"{fmt(model_mae):>10}{fmt(model_hit_rate):>10}"
        f"{fmt(model_rank_correlation):>11}"
    )

    for field in DIMENSION_SCORE_FIELDS:

        records = dimension_records(dataset, model_records, field)

        evaluated = sum(1 for r in records if r.evaluable)
        mae = mean_absolute_error(records)
        hit_rate = directional_hit_rate(records)
        rho = rank_correlation(records)

        print(
            f"{field:<28}{evaluated:>10}{fmt(mae):>10}"
            f"{fmt(hit_rate):>10}{fmt(rho):>11}"
        )

    print("-" * 69)
    print(
        f"{'mean-reversion (RE-PRED.13, ref.)':<28}{'19':>10}"
        f"{'0.18159':>10}{'0.94737':>10}{'0.26316':>11}"
    )
    print()
    print(
        "NOTE: no value above is canonical. This is an exploratory "
        "diagnostic, not a verify_*.py regression gate."
    )
    print(
        "NOTE: per-dimension evaluated counts can legitimately differ "
        "from 19 and from each other -- see module docstring."
    )
    print(
        "NOTE: RE-PRED.12's sampling-noise caveat applies with extra "
        "force here -- these are smaller, still-dependent slices of the "
        "same 23-episode dataset. Hypothesis generation, not "
        "confirmation."
    )


if __name__ == "__main__":
    main()
