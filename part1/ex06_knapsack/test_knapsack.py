#!/usr/bin/env python3
"""
Tests for Exercise 6: 0-1 Knapsack.

Run:
    python test_knapsack.py
"""

from knapsack import knapsack


def test_small_instance():
    """Solve a small knapsack with known optimal."""
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 7

    model, x = knapsack(weights, values, capacity)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Items 0 (w=2,v=3) + 2 (w=4,v=5) = w=6 <= 7, v=8
    # Items 1 (w=3,v=4) + 2 (w=4,v=5) = w=7 <= 7, v=9
    assert abs(model.getObjVal() - 9.0) < 1e-4, (
        f"Expected obj=9, got {model.getObjVal()}"
    )
    print("PASS: test_small_instance")


def test_capacity_respected():
    """Selected items should not exceed capacity."""
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    model, x = knapsack(weights, values, capacity)
    model.hideOutput()
    model.optimize()

    total_weight = sum(
        weights[i] * model.getVal(x[i]) for i in range(3)
    )
    assert total_weight <= capacity + 1e-6, (
        f"Weight {total_weight} exceeds capacity {capacity}"
    )
    print("PASS: test_capacity_respected")


def test_classic_instance():
    """Classic knapsack: weights [10,20,30], values [60,100,120], cap 50."""
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    model, x = knapsack(weights, values, capacity)
    model.hideOutput()
    model.optimize()

    # Optimal: items 1+2 (w=50, v=220)
    assert abs(model.getObjVal() - 220.0) < 1e-4, (
        f"Expected obj=220, got {model.getObjVal()}"
    )
    print("PASS: test_classic_instance")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_knapsack_instance

    weights, values, capacity = random_knapsack_instance(10, seed=42)
    model, x = knapsack(weights, values, capacity)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Objective should be non-negative"
    print("PASS: test_generated_instance")


if __name__ == "__main__":
    print("Running knapsack tests...\n")

    tests = [
        test_small_instance,
        test_capacity_respected,
        test_classic_instance,
        test_generated_instance,
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
            print(f"      {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
