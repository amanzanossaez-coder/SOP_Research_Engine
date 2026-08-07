#!/usr/bin/env python3
"""
SOP Research Engine
Regime Comparability Gate Verification

Functional smoke test for the isolated RE-036.1 gate structure -- the
first implementation of the boundary documented in RE-031.1.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.regime_comparability_gate import (
    COMPARABLE,
    NOT_COMPARABLE,
    NOT_MEASURABLE,
    LocalRegimeComparabilityInputs,
    RegimeComparabilityGate,
    _dimension_covered,
    build_local_regime_comparability_inputs,
)
from engine.drawdown_engine import run_drawdown_engine
from engine.research_engine import ResearchEngine


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected}, got {actual}"
        )


def assert_in(label: str, actual, expected) -> None:

    if actual not in expected:
        raise AssertionError(
            f"{label}: expected one of {expected}, got {actual}"
        )


def assert_contains_fragment(
    label: str,
    values: list[str],
    fragment: str,
) -> None:

    if not any(fragment in value for value in values):
        raise AssertionError(
            f"{label}: expected an explanation containing {fragment!r}, "
            f"got {values!r}"
        )


def main() -> None:

    gate = RegimeComparabilityGate()

    # -- _dimension_covered(), isolated --

    assert_equal(
        "covered_inside_range",
        _dimension_covered(1.5, [1.0, 2.0, 1.2]),
        True,
    )
    assert_equal(
        "covered_below_range",
        _dimension_covered(0.5, [1.0, 2.0, 1.2]),
        False,
    )
    assert_equal(
        "covered_above_range",
        _dimension_covered(2.5, [1.0, 2.0, 1.2]),
        False,
    )
    assert_equal(
        "covered_on_boundary",
        _dimension_covered(1.0, [1.0, 2.0, 1.2]),
        True,
    )
    assert_equal(
        "covered_today_none",
        _dimension_covered(None, [1.0, 2.0]),
        None,
    )
    assert_equal(
        "covered_no_match_values",
        _dimension_covered(1.5, []),
        None,
    )
    assert_equal(
        "covered_match_values_all_none",
        _dimension_covered(1.5, [None, None]),
        None,
    )

    # -- Gate states, synthetic --

    not_measurable = gate.evaluate(LocalRegimeComparabilityInputs())

    assert_equal("not_measurable_state", not_measurable.state, NOT_MEASURABLE)

    comparable = gate.evaluate(
        LocalRegimeComparabilityInputs(
            cape_covered=True,
            inflation_covered=True,
            interest_rate_covered=True,
        )
    )

    assert_equal("comparable_state", comparable.state, COMPARABLE)

    not_comparable = gate.evaluate(
        LocalRegimeComparabilityInputs(
            cape_covered=True,
            inflation_covered=False,
            interest_rate_covered=True,
        )
    )

    assert_equal("not_comparable_state", not_comparable.state, NOT_COMPARABLE)
    assert_contains_fragment(
        "not_comparable_explanations",
        not_comparable.explanations,
        "inflation",
    )

    partial_measurement = gate.evaluate(
        LocalRegimeComparabilityInputs(
            cape_covered=True,
            inflation_covered=None,
            interest_rate_covered=None,
        )
    )

    assert_equal(
        "partial_measurement_state",
        partial_measurement.state,
        COMPARABLE,
    )

    # -- Real pipeline, structural only: this iteration makes no claim
    # about what today's real snapshot/matches produce, only that the
    # builder runs and returns well-typed Optional[bool] fields.

    dataset = run_drawdown_engine()
    research = ResearchEngine().run(dataset)

    real_local = build_local_regime_comparability_inputs(
        research.snapshot,
        research.evidence,
    )

    for field_name in ("cape_covered", "inflation_covered", "interest_rate_covered"):

        value = getattr(real_local, field_name)

        if value is not None and not isinstance(value, bool):
            raise AssertionError(
                f"real_local.{field_name}: expected None or bool, "
                f"got {value!r}"
            )

    real_result = gate.evaluate(real_local)

    assert_in(
        "real_result_state",
        real_result.state,
        {NOT_MEASURABLE, COMPARABLE, NOT_COMPARABLE},
    )

    print("REGIME COMPARABILITY GATE : STABLE")
    print(f"real_local: {real_local}")
    print(f"real_result_state: {real_result.state}")
    print(f"real_result_explanations: {real_result.explanations}")
    print(
        "NOTE: real_local/real_result values are NOT canonical claims -- "
        "this iteration only verifies the gate runs and returns "
        "well-formed output on the live pipeline."
    )


if __name__ == "__main__":
    main()
