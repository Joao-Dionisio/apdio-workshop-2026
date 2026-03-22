#!/usr/bin/env python3
"""
Integration tests for TSP row generation.

These tests verify that the row generation approach produces the same
optimal solution as the compact MTZ formulation.

Run these tests after completing Exercises 1 and 2:
    python test_tsp.py
"""

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen, extract_tour


def test_small_tsp():
    """Test row generation on a small 10-city instance."""
    print("Testing 10-city TSP...")

    distances = random_euclidean_tsp(10, seed=0)

    # Solve with MTZ (reference)
    model_mtz, x_mtz = tsp_mtz(distances)
    model_mtz.hideOutput()  # Suppress solver output
    model_mtz.optimize()
    opt_mtz = model_mtz.getObjVal()
    print(f"  MTZ optimal: {opt_mtz:.0f}")

    # Solve with row generation
    model_rg, x_rg = tsp_rowgen(distances)
    model_rg.hideOutput()
    model_rg.optimize()
    opt_rg = model_rg.getObjVal()
    print(f"  Row generation optimal: {opt_rg:.0f}")

    # Compare
    assert abs(opt_mtz - opt_rg) < 1e-6, \
        f"Solutions differ: MTZ={opt_mtz}, RowGen={opt_rg}"

    print("PASS: test_small_tsp")
    return opt_rg


def test_medium_tsp():
    """Test row generation on a medium 20-city instance."""
    print("\nTesting 20-city TSP...")

    distances = random_euclidean_tsp(20, seed=123)

    # Solve with MTZ (reference)
    model_mtz, _ = tsp_mtz(distances)
    model_mtz.hideOutput()
    model_mtz.optimize()
    opt_mtz = model_mtz.getObjVal()
    print(f"  MTZ optimal: {opt_mtz:.0f}")

    # Solve with row generation
    model_rg, x_rg = tsp_rowgen(distances)
    model_rg.hideOutput()
    model_rg.optimize()
    opt_rg = model_rg.getObjVal()
    print(f"  Row generation optimal: {opt_rg:.0f}")

    # Compare
    assert abs(opt_mtz - opt_rg) < 1e-6, \
        f"Solutions differ: MTZ={opt_mtz}, RowGen={opt_rg}"

    # Verify tour extraction
    tour = extract_tour(model_rg, x_rg, 20)
    assert len(tour) == 21, f"Tour should have n+1 cities, got {len(tour)}"
    assert tour[0] == tour[-1] == 0, "Tour should start and end at city 0"
    assert set(tour[:-1]) == set(range(20)), "Tour should visit all cities"

    print("PASS: test_medium_tsp")
    return opt_rg


def test_tour_validity():
    """Verify that extracted tour is valid and matches objective."""
    print("\nTesting tour validity...")

    n = 15
    distances = random_euclidean_tsp(n, seed=456)

    model, x = tsp_rowgen(distances)
    model.hideOutput()
    model.optimize()

    tour = extract_tour(model, x, n)

    # Check tour properties
    assert len(tour) == n + 1, f"Tour length should be {n+1}"
    assert tour[0] == tour[-1], "Tour should be a cycle"
    assert len(set(tour[:-1])) == n, "Tour should visit each city exactly once"

    # Verify tour cost matches objective
    tour_cost = sum(
        distances[tour[i]][tour[i + 1]]
        for i in range(n)
    )
    obj_val = model.getObjVal()

    assert abs(tour_cost - obj_val) < 1e-6, \
        f"Tour cost {tour_cost} doesn't match objective {obj_val}"

    print(f"  Tour: {' -> '.join(map(str, tour[:6]))} ... (length={tour_cost:.0f})")
    print("PASS: test_tour_validity")


def test_deterministic():
    """Same seed should give same result."""
    print("\nTesting determinism...")

    distances = random_euclidean_tsp(12, seed=789)

    results = []
    for i in range(2):
        model, _ = tsp_rowgen(distances)
        model.hideOutput()
        model.optimize()
        results.append(model.getObjVal())

    assert results[0] == results[1], \
        f"Same instance gave different results: {results}"

    print("PASS: test_deterministic")


if __name__ == "__main__":
    print("Running TSP integration tests...\n")
    print("=" * 50)

    tests = [
        test_small_tsp,
        test_medium_tsp,
        test_tour_validity,
        test_deterministic,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"SKIP: {test.__name__} - Exercise not implemented yet")
            print(f"      Hint: Complete Exercises 1 and 2 (and Exercise 6 in Part 1) first.")
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

    if failed == 0:
        print("\nAll tests passed! Row generation is working correctly.")
    else:
        print("\nSome tests failed. Make sure Exercises 1 and 2 (and Exercise 6 in Part 1) are complete.")
