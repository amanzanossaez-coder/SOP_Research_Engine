#!/usr/bin/env python3
"""
SOP Research Engine
Personal Capacity Facts Gate Verification

RE-032.5 -- synthetic checks. RE-043.1 adds a real-pipeline section:
build_local_personal_capacity_facts_inputs() reading
data/raw/personal_capacity_facts.xlsx, evaluated for both of Armando's
real patrimonios (AMS/AML), as two independent gate calls -- per
Armando's explicit decision that they are never merged into one.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.personal_capacity_facts_gate import (
    ADEQUATE,
    CONSTRAINED,
    FACT_FIELDS,
    FIELD_INPUT_TYPES,
    NOT_MEASURABLE,
    LocalPersonalCapacityFactsInputs,
    PersonalCapacityFactsGate,
    build_local_personal_capacity_facts_inputs,
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

    # -- FIELD_INPUT_TYPES stays in sync with FACT_FIELDS --

    assert_equal(
        "field_input_types_keys",
        set(FIELD_INPUT_TYPES.keys()),
        set(FACT_FIELDS),
    )

    # -- Real pipeline: data/raw/personal_capacity_facts.xlsx, both --
    # -- patrimonios, evaluated as two independent gate calls --

    real_inputs = build_local_personal_capacity_facts_inputs()

    assert_equal(
        "real_inputs_patrimonios",
        set(real_inputs.keys()),
        {"AMS", "AML"},
    )

    ams_result = gate.evaluate(real_inputs["AMS"])
    aml_result = gate.evaluate(real_inputs["AML"])

    # AMS: as of the RE-043.1 follow-up session (2026-08-10), all nine
    # cells have a real, explicit value -- no "Pendiente" left. First
    # time this gate has ever produced ADEQUATE from real data.
    assert_equal("ams_real_state", ams_result.state, ADEQUATE)
    assert_equal("ams_real_blocked", ams_result.blocked, False)
    assert_equal("ams_real_failed_fields", ams_result.failed_fields, [])
    assert_equal("ams_real_missing_fields", ams_result.missing_fields, [])

    # AML: liquidity_adequate is a confirmed breach -- this is the same
    # finding Armando and this document already established manually
    # (dry powder 74.375 vs. suelo 125.000, both read from the sheet's
    # own formulas): AML's current liquidity sits below its own suelo,
    # even though the emergency-reserve floor (colchón) is intact. This
    # is the first time that finding has come out of the real pipeline
    # rather than manual arithmetic.
    # As of the RE-043.1 follow-up session, every other field also has
    # a real value -- CONSTRAINED here means exactly one genuine issue,
    # not a mix of failure and missing data anymore.
    assert_equal("aml_real_state", aml_result.state, CONSTRAINED)
    assert_equal("aml_real_blocked", aml_result.blocked, False)
    assert_equal(
        "aml_real_failed_fields",
        aml_result.failed_fields,
        ["liquidity_adequate"],
    )
    assert_equal("aml_real_missing_fields", aml_result.missing_fields, [])
    assert_equal(
        "aml_real_emergency_reserve_adequate",
        real_inputs["AML"].emergency_reserve_adequate,
        True,
    )
    assert_equal(
        "aml_real_income_concentration_acceptable",
        real_inputs["AML"].income_concentration_acceptable,
        True,
    )

    print("PERSONAL CAPACITY FACTS GATE : STABLE")
    print()
    print(f"ams_real_state: {ams_result.state}")
    print(f"ams_real_missing_fields: {ams_result.missing_fields}")
    print(f"aml_real_state: {aml_result.state}")
    print(f"aml_real_failed_fields: {aml_result.failed_fields}")
    print(f"aml_real_missing_fields: {aml_result.missing_fields}")


if __name__ == "__main__":
    main()
