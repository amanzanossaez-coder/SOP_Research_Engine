#!/usr/bin/env python3
"""
SOP Research Engine
Personal Capacity Facts Gate Verification

RE-032.5 -- synthetic checks only. Unlike EvidenceQualityGate or
RegimeComparabilityGate, there is no real-pipeline data source for
Personal Capacity facts anywhere in this repository, so there is no
real-pipeline dry-run section here -- that is a stated limitation, not
an oversight.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.personal_capacity_facts_gate import (
    ADEQUATE,
    CONSTRAINED,
    FACT_FIELDS,
    NOT_MEASURABLE,
    LocalPersonalCapacityFactsInputs,
    PersonalCapacityFactsGate,
)


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def main() -> None:

    gate = PersonalCapacityFactsGate()

    # -- All nine unmeasured --

    all_none = gate.evaluate(LocalPersonalCapacityFactsInputs())
    assert_equal("all_none_state", all_none.state, NOT_MEASURABLE)
    assert_equal("all_none_blocked", all_none.blocked, False)
    assert_equal("all_none_missing_count", len(all_none.missing_fields), 9)
    assert_equal("all_none_failed_count", len(all_none.failed_fields), 0)

    # -- All nine adequate --

    all_true = gate.evaluate(
        LocalPersonalCapacityFactsInputs(**{
            name: True for name in FACT_FIELDS
        })
    )
    assert_equal("all_true_state", all_true.state, ADEQUATE)
    assert_equal("all_true_blocked", all_true.blocked, False)
    assert_equal("all_true_missing_count", len(all_true.missing_fields), 0)
    assert_equal("all_true_failed_count", len(all_true.failed_fields), 0)

    # -- One regular fact fails, rest adequate --

    one_regular_fail = gate.evaluate(
        LocalPersonalCapacityFactsInputs(**{
            **{name: True for name in FACT_FIELDS},
            "debt_service_manageable": False,
        })
    )
    assert_equal("one_regular_fail_state", one_regular_fail.state, CONSTRAINED)
    assert_equal("one_regular_fail_blocked", one_regular_fail.blocked, False)
    assert_equal(
        "one_regular_fail_failed_fields",
        one_regular_fail.failed_fields,
        ["debt_service_manageable"],
    )
    assert_equal(
        "one_regular_fail_blocking_fields",
        one_regular_fail.blocking_fields,
        [],
    )

    # -- Emergency reserve breached, rest adequate: CONSTRAINED + blocked --

    reserve_fail = gate.evaluate(
        LocalPersonalCapacityFactsInputs(**{
            **{name: True for name in FACT_FIELDS},
            "emergency_reserve_adequate": False,
        })
    )
    assert_equal("reserve_fail_state", reserve_fail.state, CONSTRAINED)
    assert_equal("reserve_fail_blocked", reserve_fail.blocked, True)
    assert_equal(
        "reserve_fail_blocking_fields",
        reserve_fail.blocking_fields,
        ["emergency_reserve_adequate"],
    )
    assert_equal(
        "reserve_fail_failed_fields",
        reserve_fail.failed_fields,
        ["emergency_reserve_adequate"],
    )

    # -- Reserve unmeasured (not confirmed breach), rest adequate --

    reserve_unmeasured = gate.evaluate(
        LocalPersonalCapacityFactsInputs(**{
            **{name: True for name in FACT_FIELDS},
            "emergency_reserve_adequate": None,
        })
    )
    assert_equal("reserve_unmeasured_state", reserve_unmeasured.state, NOT_MEASURABLE)
    assert_equal("reserve_unmeasured_blocked", reserve_unmeasured.blocked, False)
    assert_equal(
        "reserve_unmeasured_missing_fields",
        reserve_unmeasured.missing_fields,
        ["emergency_reserve_adequate"],
    )

    # -- Mixed: some True, some None, no False -- breach never inferred --

    partial = gate.evaluate(
        LocalPersonalCapacityFactsInputs(
            liquidity_adequate=True,
            debt_service_manageable=True,
        )
    )
    assert_equal("partial_state", partial.state, NOT_MEASURABLE)
    assert_equal("partial_blocked", partial.blocked, False)
    assert_equal("partial_missing_count", len(partial.missing_fields), 7)

    # -- Failure dominates missing data: one False + several None --

    fail_plus_missing = gate.evaluate(
        LocalPersonalCapacityFactsInputs(
            liquidity_adequate=False,
        )
    )
    assert_equal("fail_plus_missing_state", fail_plus_missing.state, CONSTRAINED)
    assert_equal(
        "fail_plus_missing_failed_fields",
        fail_plus_missing.failed_fields,
        ["liquidity_adequate"],
    )
    assert_equal(
        "fail_plus_missing_missing_count",
        len(fail_plus_missing.missing_fields),
        8,
    )

    # -- Multiple failures including reserve: both dimensions triggered --

    multi_fail = gate.evaluate(
        LocalPersonalCapacityFactsInputs(**{
            **{name: True for name in FACT_FIELDS},
            "emergency_reserve_adequate": False,
            "debt_service_manageable": False,
        })
    )
    assert_equal("multi_fail_state", multi_fail.state, CONSTRAINED)
    assert_equal("multi_fail_blocked", multi_fail.blocked, True)
    assert_equal(
        "multi_fail_failed_fields",
        sorted(multi_fail.failed_fields),
        sorted(["emergency_reserve_adequate", "debt_service_manageable"]),
    )
    assert_equal(
        "multi_fail_blocking_fields",
        multi_fail.blocking_fields,
        ["emergency_reserve_adequate"],
    )

    print("PERSONAL CAPACITY FACTS GATE : STABLE")
    print()
    print("NOTE: synthetic checks only -- no real-pipeline dry-run exists")
    print("for this gate. No verifiable fact is tracked anywhere in this")
    print("repository; all nine live outside the Research Engine.")


if __name__ == "__main__":
    main()
