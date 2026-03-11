#!/usr/bin/env python3
"""
Tests for Exercise 6: Set cover problem.

Run:
    python test_set_cover.py
"""

from set_cover import set_cover


def test_small_instance():
    """Solve a small set cover with known optimal."""
    universe = {0, 1, 2, 3}
    subsets = [
        {0, 1, 2},  # covers 0, 1, 2
        {1, 3},      # covers 1, 3
        {2, 3},      # covers 2, 3
        {0, 1, 2, 3},  # covers everything
    ]
    costs = [3, 2, 2, 5]

    model, y = set_cover(universe, subsets, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Optimal: subsets 0 and 1 (cost 3+2=5) or subsets 0 and 2 (cost 3+2=5)
    assert abs(model.getObjVal() - 5.0) < 1e-4, (
        f"Expected obj=5, got {model.getObjVal()}"
    )
    print("PASS: test_small_instance")


def test_all_elements_covered():
    """Every element should be covered by at least one selected subset."""
    universe = {0, 1, 2, 3, 4}
    subsets = [
        {0, 1},
        {2, 3},
        {3, 4},
        {0, 2, 4},
    ]
    costs = [1, 1, 1, 1]

    model, y = set_cover(universe, subsets, costs)
    model.hideOutput()
    model.optimize()

    selected = [j for j in range(len(subsets)) if model.getVal(y[j]) > 0.5]
    covered = set()
    for j in selected:
        covered |= subsets[j]

    assert covered == universe, (
        f"Not all elements covered: covered={covered}, universe={universe}"
    )
    print("PASS: test_all_elements_covered")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_set_cover_instance

    universe, subsets, costs = random_set_cover_instance(10, 8, seed=42)
    model, y = set_cover(universe, subsets, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    selected = [j for j in range(len(subsets)) if model.getVal(y[j]) > 0.5]
    covered = set()
    for j in selected:
        covered |= subsets[j]
    assert covered == universe, "Generated instance: not all elements covered"
    print("PASS: test_generated_instance")


def test_generated_larger():
    """Solve a larger generated instance (20 elements, 15 subsets)."""
    from generator import random_set_cover_instance

    universe, subsets, costs = random_set_cover_instance(20, 15, seed=99)
    model, y = set_cover(universe, subsets, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    selected = [j for j in range(len(subsets)) if model.getVal(y[j]) > 0.5]
    covered = set()
    for j in selected:
        covered |= subsets[j]
    assert covered == universe, "Not all elements covered"
    print("PASS: test_generated_larger")


def test_generated_many_subsets():
    """Solve an instance with many subsets relative to universe size."""
    from generator import random_set_cover_instance

    universe, subsets, costs = random_set_cover_instance(8, 20, seed=7)
    model, y = set_cover(universe, subsets, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    selected = [j for j in range(len(subsets)) if model.getVal(y[j]) > 0.5]
    covered = set()
    for j in selected:
        covered |= subsets[j]
    assert covered == universe, "Not all elements covered"
    print("PASS: test_generated_many_subsets")


if __name__ == "__main__":
    print("Running set cover tests...\n")

    tests = [
        test_small_instance,
        test_all_elements_covered,
        test_generated_instance,
        test_generated_larger,
        test_generated_many_subsets,
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
