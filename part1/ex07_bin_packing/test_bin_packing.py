#!/usr/bin/env python3
"""
Tests for Exercise 8: Bin packing.

Run:
    python test_bin_packing.py
"""

from bin_packing import bin_packing


def test_small_instance():
    """Items [6, 6, 6] with capacity 10 need 2 bins."""
    sizes = [6, 6, 6]
    capacity = 10

    model, x, y = bin_packing(sizes, capacity)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert abs(model.getObjVal() - 2.0) < 1e-6, f"Expected 2 bins, got {model.getObjVal()}"
    print("PASS: test_small_instance")


def test_all_fit_one_bin():
    """Items [1, 2, 3] with capacity 10 need 1 bin."""
    sizes = [1, 2, 3]
    capacity = 10

    model, x, y = bin_packing(sizes, capacity)
    model.hideOutput()
    model.optimize()

    assert abs(model.getObjVal() - 1.0) < 1e-6, f"Expected 1 bin, got {model.getObjVal()}"
    print("PASS: test_all_fit_one_bin")


def test_each_item_assigned():
    """Every item must be assigned to exactly one bin."""
    sizes = [5, 5, 5, 5]
    capacity = 8

    model, x, y = bin_packing(sizes, capacity)
    model.hideOutput()
    model.optimize()

    n = len(sizes)
    for i in range(n):
        total = sum(model.getVal(x[i, b]) for b in range(n))
        assert abs(total - 1.0) < 1e-6, (
            f"Item {i} assigned to {total} bins, expected 1"
        )
    print("PASS: test_each_item_assigned")


def test_capacity_respected():
    """No bin should exceed its capacity."""
    sizes = [7, 7, 6, 6, 5]
    capacity = 10

    model, x, y = bin_packing(sizes, capacity)
    model.hideOutput()
    model.optimize()

    n = len(sizes)
    for b in range(n):
        if model.getVal(y[b]) > 0.5:
            load = sum(sizes[i] * model.getVal(x[i, b]) for i in range(n))
            assert load <= capacity + 1e-6, (
                f"Bin {b} has load {load} > capacity {capacity}"
            )
    print("PASS: test_capacity_respected")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_bin_packing_instance

    sizes = random_bin_packing_instance(8, 20, seed=42)
    model, x, y = bin_packing(sizes, 20)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print("PASS: test_generated_instance")


if __name__ == "__main__":
    print("Running bin packing tests...\n")

    tests = [
        test_small_instance,
        test_all_fit_one_bin,
        test_each_item_assigned,
        test_capacity_respected,
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
