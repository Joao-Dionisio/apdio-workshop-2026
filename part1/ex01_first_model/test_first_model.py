#!/usr/bin/env python3
"""
Tests for Exercise 1: First Model.

Run:
    python test_first_model.py
"""

import traceback

from first_model import first_model


def test_optimal_value():
    """Optimal objective should be 3."""
    model, x, y = first_model()
    model.optimize()
    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert abs(model.getObjVal() - 3.0) < 1e-6, f"Expected obj=3, got {model.getObjVal()}"
    print("[92mPASS:[0m test_optimal_value")


def test_optimal_solution():
    """Optimal solution should be x=1, y=0."""
    model, x, y = first_model()
    model.optimize()
    assert model.getVal(x) > 0.5, f"Expected x=1, got {model.getVal(x)}"
    assert model.getVal(y) < 0.5, f"Expected y=0, got {model.getVal(y)}"
    print("[92mPASS:[0m test_optimal_solution")


def test_model_structure():
    """Model should have 2 variables and 2 constraints."""
    model, x, y = first_model()
    assert model.getNVars() == 2, f"Expected 2 variables, got {model.getNVars()}"
    assert model.getNConss() == 2, f"Expected 2 constraints, got {model.getNConss()}"
    print("[92mPASS:[0m test_model_structure")


if __name__ == "__main__":
    print("Running first model tests...\n")

    tests = [
        test_optimal_value,
        test_optimal_solution,
        test_model_structure,
    ]

    passed = 0
    failed = 0
    hint = ""

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"[93mSKIP:[0m {test.__name__} - Exercise not implemented yet")
            if not hint:
                hint = str(e)
            failed += 1
        except AssertionError as e:
            print(f"[91mFAIL:[0m {test.__name__} - {e}")
            failed += 1
        except Exception as e:
            print(f"[91mERROR:[0m {test.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    if hint:
        print(hint)
    print(f"Results: [92m{passed} passed[0m, [91m{failed} failed[0m")
