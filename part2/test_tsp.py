#!/usr/bin/env python3
"""
Integration tests for TSP row generation.

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

    print("\x1b[92mPASS:\x1b[0m test_small_tsp")
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

    print("\x1b[92mPASS:\x1b[0m test_medium_tsp")
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
    print("\x1b[92mPASS:\x1b[0m test_tour_validity")


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

    print("\x1b[92mPASS:\x1b[0m test_deterministic")


def _check_conshdlr_implemented():
    """Pre-check that conscheck/consenfolp don't raise NotImplementedError."""
    from conshdlr_subtour import SubtourElimination
    dummy_x = {(0, 1): None}
    hdlr = SubtourElimination(dummy_x, 2)
    for method, args in [("conscheck", ([], None, None, None, None, None)),
                         ("consenfolp", ([], 0, False))]:
        try:
            getattr(hdlr, method)(*args)
        except NotImplementedError:
            return False, method
        except Exception:
            pass
    return True, None


if __name__ == "__main__":
    print("Running TSP integration tests...\n")
    print("=" * 50)

    ready, missing = _check_conshdlr_implemented()
    if not ready:
        print(f"SKIP: {missing} is not implemented yet.")
        print("Complete Exercise 2 (conshdlr_subtour.py) before running these tests.")
        exit(0)

    tests = [
        test_small_tsp,
        test_medium_tsp,
        test_tour_validity,
        test_deterministic,
    ]

    passed = 0
    failed = 0
    hint = ""

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"\x1b[93mSKIP:\x1b[0m {test.__name__} - Exercise not implemented yet")
            if not hint:
                hint = "Hint: Complete Exercises 1 and 2 (and Exercise 6 in Part 1) first."
            failed += 1
        except AssertionError as e:
            print(f"\x1b[91mFAIL:\x1b[0m {test.__name__}")
            if not hint:
                hint = str(e)
            failed += 1
        except Exception as e:
            print(f"\x1b[91mERROR:\x1b[0m {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    if hint:
        print(hint)
    print(f"Results: \x1b[92m{passed} passed\x1b[0m, \x1b[91m{failed} failed\x1b[0m")

    if failed == 0:
        print("\nAll tests passed! Row generation is working correctly.")
