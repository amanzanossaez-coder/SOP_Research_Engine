#!/usr/bin/env python3
"""
SOP Research Engine
Dependence-Aware Bootstrap Diagnostic

RE-PRED.15 -- closes the method gap opened in RE-PRED.12: are the
excess differences observed against the primary baseline (RE-PRED.10)
and against mean-reversion (RE-PRED.13) distinguishable from sampling
noise, given that all 19 evaluable records share known dependence
through two channels (RE-025.6): overlapping realized 5-year outcome
windows (RE-025.8) and repeated forecasts (RE-025.9)?

Method: cluster bootstrap. Records are partitioned into independence
clusters via connected components over the union of both already-
diagnosed dependence channels (engine/dependence_bootstrap.py,
independence_clusters()). Resampling draws whole clusters with
replacement -- never individual records -- so intra-cluster dependence
is preserved, not destroyed. This is the dependence-aware resampling
RE-PRED.1 requires; an i.i.d. bootstrap over the 19 records remains
explicitly prohibited (RE-PRED.12).

Seed and replicate count are fixed constants
(engine/dependence_bootstrap.py: BOOTSTRAP_SEED=42,
BOOTSTRAP_REPLICATES=5000), not free parameters of this script.

This is an exploratory diagnostic, not a verify_*.py regression gate:
it asserts no expected values. The bootstrap itself uses no pandas/
numpy -- pure stdlib `random` with a fixed integer seed, which is
version-stable -- but the same reproducibility discipline applies
regardless (RE-025.5): numbers are not canonical until confirmed under
the pinned runtime.
"""

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.baseline_harness import BaselineHarness, build_baseline_records, mean_reversion_forecast
from engine.dependence_bootstrap import (
    BOOTSTRAP_PERCENTILES,
    BOOTSTRAP_REPLICATES,
    BOOTSTRAP_SEED,
    cluster_bootstrap_ci,
    cluster_bootstrap_paired_excess,
    independence_clusters,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.validation_harness import ValidationHarness
from engine.validation_metrics import (
    EXPLORATORY_DISCLAIMER,
    directional_hit_rate,
    mean_absolute_error,
    rank_correlation,
)

METRICS = [
    ("MAE", mean_absolute_error, False),
    ("hit-rate", directional_hit_rate, True),
    ("rank_corr", rank_correlation, True),
]


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


def print_ci(label: str, ci: dict) -> None:
    print(
        f"{label:<32}[{fmt(ci['low'])}, {fmt(ci['high'])}]"
        f"  (valid {ci['valid_replicates']}/{ci['replicates']})"
    )


def main() -> None:
    verify_runtime()

    dataset = run_drawdown_engine()

    harness = ValidationHarness(dataset)
    model_records = harness.run()

    primary_records = BaselineHarness(dataset).run(model_records)
    reversion_records = build_baseline_records(
        model_records, mean_reversion_forecast,
    )

    clusters = independence_clusters(model_records)
    cluster_sizes = sorted(
        (len(cluster) for cluster in clusters), reverse=True,
    )

    print()
    print("DEPENDENCE-AWARE BOOTSTRAP : EXPLORATORY")
    print(f"episodes: {len(dataset.episodes)}")
    print(f"evaluated_count: {harness.evaluated_count(model_records)}")
    print(f"independence_clusters: {len(clusters)}")
    print(f"cluster_sizes (desc): {cluster_sizes}")
    print(f"seed={BOOTSTRAP_SEED} replicates={BOOTSTRAP_REPLICATES} "
          f"percentiles={BOOTSTRAP_PERCENTILES}")
    print()

    for label, metric_fn, better_is_higher in METRICS:

        print(f"-- {label} --")

        print_ci(
            "model",
            cluster_bootstrap_ci(clusters, model_records, metric_fn),
        )
        print_ci(
            "primary baseline (RE-PRED.10)",
            cluster_bootstrap_ci(clusters, primary_records, metric_fn),
        )
        print_ci(
            "mean-reversion (RE-PRED.13)",
            cluster_bootstrap_ci(clusters, reversion_records, metric_fn),
        )
        print_ci(
            "excess vs primary",
            cluster_bootstrap_paired_excess(
                clusters, model_records, primary_records,
                metric_fn, better_is_higher,
            ),
        )
        print_ci(
            "excess vs mean-reversion",
            cluster_bootstrap_paired_excess(
                clusters, model_records, reversion_records,
                metric_fn, better_is_higher,
            ),
        )
        print()

    print(EXPLORATORY_DISCLAIMER)
    print(
        "NOTE: excess CIs use the same sign convention as "
        "excess_summary() -- positive means the model wins."
    )
    print(
        "NOTE: if an excess CI's [low, high] range straddles zero, the "
        "observed difference is not distinguishable from sampling noise "
        "given this dependence structure, at the stated percentile."
    )
    print(
        "NOTE: zero baseline is out of scope for this diagnostic -- "
        "RE-PRED.13 already found it loses to the model on MAE by a "
        "wide margin with no ambiguity; only primary and mean-reversion "
        "were flagged as open by RE-PRED.12."
    )


if __name__ == "__main__":
    main()
