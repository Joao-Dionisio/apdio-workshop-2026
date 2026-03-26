#!/usr/bin/env python3
"""
Integration tests for TSP row generation.

Tests exercises 1, 2a, 2b, and the full pipeline.
Run:  python test_tsp.py
"""

from conshdlr_subtour import SubtourElimination
from generator import random_euclidean_tsp
from subtour import find_subtours


def _is_implemented(method_name):
    """Check if a conshdlr method is implemented (avoid SCIP crash)."""
    hdlr = SubtourElimination(2)
    args = {"conscheck": ([], None, None, None, None, None),
            "consenfolp": ([], 0, False)}[method_name]
    try:
        getattr(hdlr, method_name)(*args)
    except NotImplementedError:
        return False
    except Exception:
        pass
    return True


def test_subtour_detection():
    """Exercise 1: find_subtours detects connected components."""
    # Valid tour
    assert find_subtours([(0,1),(1,2),(2,3),(3,0)], 4) == []

    # Two subtours
    subtours = find_subtours([(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)], 6)
    assert len(subtours) == 2
    sets = [frozenset(s) for s in subtours]
    assert frozenset({0,1,2}) in sets
    assert frozenset({3,4,5}) in sets

    print("\x1b[92mPASS:\x1b[0m test_subtour_detection")


def test_conscheck():
    """Exercise 2a: conscheck accepts valid tours, rejects subtours."""
    if not _is_implemented("conscheck"):
        raise NotImplementedError("Exercise 2a: conscheck not implemented yet.")

    from pyscipopt import Model, quicksum

    n = 4
    model = Model("test-conscheck")
    model.hideOutput()
    x = {}
    for i in range(n):
        for j in range(i + 1, n):
            x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")
    # Need at least one constraint for model to be valid
    for i in range(n):
        incident = [x[min(i, j), max(i, j)] for j in range(n) if i != j]
        model.addCons(quicksum(incident) == 2)

    model.data = x
    hdlr = SubtourElimination(n)
    model.includeConshdlr(
        hdlr, "subtour", "test",
        sepapriority=0, enfopriority=-1, chckpriority=-1,
        sepafreq=-1, propfreq=-1, eagerfreq=-1,
        maxprerounds=0, delaysepa=False, delayprop=False, needscons=False,
    )

    # Test 1: valid tour 0-1-2-3-0 should pass checkSol
    sol = model.createSol()
    tour_edges = [(0,1), (1,2), (2,3), (0,3)]
    for (i, j) in tour_edges:
        model.setSolVal(sol, x[i, j], 1.0)
    accepted = model.checkSol(sol, printreason=False)
    model.freeSol(sol)
    assert accepted, "Valid tour should be accepted by conscheck"

    # Test 2: subtours {0,1} + {2,3} should fail checkSol
    sol2 = model.createSol()
    for (i, j) in [(0,1), (2,3)]:
        model.setSolVal(sol2, x[i, j], 1.0)
    accepted2 = model.checkSol(sol2, printreason=False)
    model.freeSol(sol2)
    assert not accepted2, "Subtours should be rejected by conscheck"

    print("\x1b[92mPASS:\x1b[0m test_conscheck")


def test_consenfolp():
    """Exercise 2b: consenfolp adds SECs, producing a valid optimal tour."""
    if not _is_implemented("conscheck"):
        raise NotImplementedError("Exercise 2a: conscheck not implemented yet.")
    if not _is_implemented("consenfolp"):
        raise NotImplementedError("Exercise 2b: consenfolp not implemented yet.")

    distances = random_euclidean_tsp(10, seed=0)
    from tsp import tsp_rowgen
    model, x = tsp_rowgen(distances)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal"
    sol = model.getBestSol()
    selected = [(i,j) for (i,j) in x if model.getSolVal(sol, x[i,j]) > 0.5]
    subtours = find_subtours(selected, 10)
    assert subtours == [], f"Should have no subtours, got {subtours}"

    print("\x1b[92mPASS:\x1b[0m test_consenfolp")


def test_matches_mtz():
    """Full pipeline: row generation should match the MTZ optimal value."""
    if not _is_implemented("conscheck"):
        raise NotImplementedError("Exercise 2a: conscheck not implemented yet.")
    if not _is_implemented("consenfolp"):
        raise NotImplementedError("Exercise 2b: consenfolp not implemented yet.")

    from compact_mtz import tsp_mtz
    from tsp import tsp_rowgen

    distances = random_euclidean_tsp(12, seed=123)

    model_mtz, _ = tsp_mtz(distances)
    model_mtz.hideOutput()
    model_mtz.optimize()
    opt_mtz = model_mtz.getObjVal()

    model_rg, _ = tsp_rowgen(distances)
    model_rg.hideOutput()
    model_rg.optimize()
    if model_rg.getStatus() != "optimal":
        raise AssertionError(f"Row generation model status: {model_rg.getStatus()}")
    opt_rg = model_rg.getObjVal()

    assert abs(opt_mtz - opt_rg) < 1e-6, \
        f"MTZ={opt_mtz:.0f}, RowGen={opt_rg:.0f}"

    print("\x1b[92mPASS:\x1b[0m test_matches_mtz")


if __name__ == "__main__":
    print("Running TSP tests...\n")
    print("=" * 50)

    tests = [
        test_subtour_detection,
        test_conscheck,
        test_consenfolp,
        test_matches_mtz,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"\x1b[93mSKIP:\x1b[0m {test.__name__} — {e}")
            failed += 1
        except AssertionError as e:
            print(f"\x1b[91mFAIL:\x1b[0m {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"\x1b[91mERROR:\x1b[0m {test.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Results: \x1b[92m{passed} passed\x1b[0m, \x1b[91m{failed} failed\x1b[0m")
