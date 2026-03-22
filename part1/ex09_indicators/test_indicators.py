#!/usr/bin/env python3
"""
Tests for Exercise 9: Indicator constraints for generator scheduling.

Run:
    python test_indicators.py
"""

import traceback

from indicators import generator_scheduling_bigm, generator_scheduling_indicator


# Test data: 5 generators, demand = 500 MW
DEMAND = 500
FIXED_COSTS = [100, 80, 120, 90, 150]
VAR_COSTS = [10, 12, 8, 11, 7]
P_MIN = [50, 40, 60, 30, 80]
P_MAX = [200, 150, 250, 180, 300]


def _solve(model, y, p):
    """Solve and extract results."""
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    n = len(y)
    obj = model.getObjVal()
    on = [model.getVal(y[i]) > 0.5 for i in range(n)]
    output = [model.getVal(p[i]) for i in range(n)]
    return obj, on, output


def test_bigm_feasible():
    """Big-M formulation should find optimal solution."""
    model, y, p = generator_scheduling_bigm(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    obj, on, output = _solve(model, y, p)
    assert obj > 0, "Objective should be positive"
    total = sum(output)
    assert total >= DEMAND - 1e-6, f"Demand not met: {total} < {DEMAND}"
    print(f"PASS: test_bigm_feasible (obj={obj:.1f})")


def test_bigm_min_output():
    """If a generator is on, its output should be >= p_min."""
    model, y, p = generator_scheduling_bigm(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    obj, on, output = _solve(model, y, p)
    for i in range(len(on)):
        if on[i]:
            assert output[i] >= P_MIN[i] - 1e-6, (
                f"Generator {i} is on but output {output[i]:.1f} < p_min {P_MIN[i]}"
            )
        else:
            assert output[i] <= 1e-6, (
                f"Generator {i} is off but output {output[i]:.1f} > 0"
            )
    print("PASS: test_bigm_min_output")


def test_indicator_feasible():
    """Indicator formulation should find optimal solution."""
    model, y, p = generator_scheduling_indicator(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    obj, on, output = _solve(model, y, p)
    assert obj > 0, "Objective should be positive"
    total = sum(output)
    assert total >= DEMAND - 1e-6, f"Demand not met: {total} < {DEMAND}"
    print(f"PASS: test_indicator_feasible (obj={obj:.1f})")


def test_indicator_min_output():
    """If a generator is on, its output should be >= p_min."""
    model, y, p = generator_scheduling_indicator(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    obj, on, output = _solve(model, y, p)
    for i in range(len(on)):
        if on[i]:
            assert output[i] >= P_MIN[i] - 1e-6, (
                f"Generator {i} is on but output {output[i]:.1f} < p_min {P_MIN[i]}"
            )
        else:
            assert output[i] <= 1e-6, (
                f"Generator {i} is off but output {output[i]:.1f} > 0"
            )
    print("PASS: test_indicator_min_output")


def test_same_objective():
    """Both formulations should yield the same optimal objective."""
    model1, y1, p1 = generator_scheduling_bigm(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    model1.hideOutput()
    model1.optimize()
    obj1 = model1.getObjVal()

    model2, y2, p2 = generator_scheduling_indicator(
        DEMAND, FIXED_COSTS, VAR_COSTS, P_MIN, P_MAX
    )
    model2.hideOutput()
    model2.optimize()
    obj2 = model2.getObjVal()

    assert abs(obj1 - obj2) < 1e-4, (
        f"Objectives differ: big-M={obj1:.2f}, indicator={obj2:.2f}"
    )
    print(f"PASS: test_same_objective (both={obj1:.1f})")


if __name__ == "__main__":
    print("Running indicator constraint tests...\n")

    tests = [
        test_bigm_feasible,
        test_bigm_min_output,
        test_indicator_feasible,
        test_indicator_min_output,
        test_same_objective,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"SKIP: {test.__name__} - Exercise not implemented yet")
            print(f"      {e}")
            failed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__}")
            traceback.print_exc()
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
