#!/usr/bin/env python3
"""
Tests for Exercise 2: Solving and inspecting solutions.

Run:
    python test_solving.py
"""

import traceback

from pyscipopt import Model
from solving import solve_and_report


def _build_test_model():
    """Build a simple model for testing: max 3x + 2y, x+y<=1, x,y binary."""
    model = Model("TestModel")
    model.hideOutput()
    x = model.addVar(name="x", vtype="B", obj=3)
    y = model.addVar(name="y", vtype="B", obj=2)
    model.addCons(x + y <= 1)
    model.setMaximize()
    return model


def test_status():
    """Solve should return optimal status."""
    model = _build_test_model()
    result = solve_and_report(model)
    assert result["status"] == "optimal", f"Expected optimal, got {result['status']}"
    print("PASS: test_status")


def test_objective():
    """Optimal objective should be 3."""
    model = _build_test_model()
    result = solve_and_report(model)
    assert abs(result["objective"] - 3.0) < 1e-6, (
        f"Expected obj=3, got {result['objective']}"
    )
    print("PASS: test_objective")


def test_variables():
    """Variable values should be a dict with correct entries."""
    model = _build_test_model()
    result = solve_and_report(model)
    assert isinstance(result["variables"], dict), "variables should be a dict"
    assert "x" in result["variables"], "x should be in variables"
    assert result["variables"]["x"] > 0.5, f"Expected x=1, got {result['variables']['x']}"
    print("PASS: test_variables")


def test_statistics():
    """Statistics should be non-negative."""
    model = _build_test_model()
    result = solve_and_report(model)
    assert result["n_nodes"] >= 0, f"n_nodes should be >= 0, got {result['n_nodes']}"
    assert result["time"] >= 0, f"time should be >= 0, got {result['time']}"
    print("PASS: test_statistics")


def test_required_keys():
    """Result should have all required keys."""
    model = _build_test_model()
    result = solve_and_report(model)
    for key in ["status", "objective", "variables", "n_nodes", "time"]:
        assert key in result, f"Missing key: {key}"
    print("PASS: test_required_keys")


if __name__ == "__main__":
    print("Running solving tests...\n")

    tests = [
        test_status,
        test_objective,
        test_variables,
        test_statistics,
        test_required_keys,
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
