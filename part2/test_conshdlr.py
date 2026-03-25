#!/usr/bin/env python3
"""
Tests for the constraint handler (Exercise 2a and 2b).

Run:  python test_conshdlr.py
"""

from pyscipopt import Model, quicksum, SCIP_RESULT
from conshdlr_subtour import SubtourElimination
from generator import random_euclidean_tsp
from subtour import find_subtours


def _check_implemented(method_name):
    """Check if a conshdlr method is implemented before running SCIP."""
    dummy_x = {(0, 1): None}
    hdlr = SubtourElimination(dummy_x, 2)
    try:
        if method_name == "conscheck":
            hdlr.conscheck([], None, None, None, None, None)
        elif method_name == "consenfolp":
            hdlr.consenfolp([], 0, False)
    except NotImplementedError:
        return False
    except Exception:
        # Any other error means the code exists (may fail on dummy data)
        return True
    return True


def _build_model_with_conshdlr(distances):
    """Build a TSP model with degree constraints + constraint handler."""
    model = Model("TSP-test")
    n = len(distances)

    x = {}
    for i in range(n):
        for j in range(i + 1, n):
            x[i, j] = model.addVar(vtype="B", obj=distances[i][j], name=f"x_{i}_{j}")

    for i in range(n):
        incident = [x[min(i, j), max(i, j)] for j in range(n) if i != j]
        model.addCons(quicksum(incident) == 2)

    conshdlr = SubtourElimination(x, n)
    model.includeConshdlr(
        conshdlr, "subtour", "SEC handler",
        sepapriority=0, enfopriority=-1, chckpriority=-1,
        sepafreq=-1, propfreq=-1, eagerfreq=-1,
        maxprerounds=0, delaysepa=False, delayprop=False, needscons=False,
    )
    return model, x, n


def test_conscheck():
    """Exercise 2a: conscheck should accept valid tours and reject subtours."""
    if not _check_implemented("conscheck"):
        raise NotImplementedError("Exercise 2a: conscheck not yet implemented.")

    print("Testing conscheck (Exercise 2a)...")

    distances = random_euclidean_tsp(8, seed=42)
    model, x, n = _build_model_with_conshdlr(distances)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", \
        f"Model should be optimal, got {model.getStatus()}"

    # If conscheck works, SCIP found an optimal valid tour (no subtours)
    sol = model.getBestSol()
    selected = [(i, j) for (i, j) in x if model.getSolVal(sol, x[i, j]) > 0.5]
    assert len(selected) == n, \
        f"Tour should have {n} edges, got {len(selected)}"

    print("\x1b[92mPASS:\x1b[0m test_conscheck")


def test_consenfolp():
    """Exercise 2b: consenfolp should add SECs and produce an optimal tour."""
    if not _check_implemented("conscheck"):
        raise NotImplementedError("Exercise 2a must be implemented first.")
    if not _check_implemented("consenfolp"):
        raise NotImplementedError("Exercise 2b: consenfolp not yet implemented.")

    print("\nTesting consenfolp (Exercise 2b)...")

    distances = random_euclidean_tsp(10, seed=0)
    model, x, n = _build_model_with_conshdlr(distances)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", \
        f"Model should be optimal, got {model.getStatus()}"

    # Verify solution is a connected tour
    sol = model.getBestSol()
    selected = [(i, j) for (i, j) in x if model.getSolVal(sol, x[i, j]) > 0.5]
    subtours = find_subtours(selected, n)
    assert subtours == [], \
        f"Optimal solution should have no subtours, got {subtours}"

    print(f"  Optimal tour length: {model.getObjVal():.0f}")
    print("\x1b[92mPASS:\x1b[0m test_consenfolp")


if __name__ == "__main__":
    print("Running constraint handler tests...\n")
    print("=" * 50)

    tests = [test_conscheck, test_consenfolp]
    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"\x1b[93mSKIP:\x1b[0m {test.__name__} — {e}")
            failed += 1
        except (AssertionError, AssertionError) as e:
            print(f"\x1b[91mFAIL:\x1b[0m {test.__name__}")
            print(f"       {e}")
            failed += 1
        except Exception as e:
            print(f"\x1b[91mERROR:\x1b[0m {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Results: \x1b[92m{passed} passed\x1b[0m, \x1b[91m{failed} failed\x1b[0m")
