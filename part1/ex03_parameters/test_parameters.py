#!/usr/bin/env python3
"""
Tests for Exercise 3: Solver parameters.

Run:
    python test_parameters.py
"""

import os
import tempfile

from pyscipopt import Model
from parameters import (
    solve_with_time_limit,
    solve_with_gap_limit,
    solve_with_emphasis,
    load_and_solve,
)


def _build_hard_model():
    """Build a bin packing instance that takes some effort to solve."""
    import random
    random.seed(42)

    n_items = 40
    capacity = 100
    sizes = [random.randint(20, 80) for _ in range(n_items)]
    n_bins = n_items  # upper bound

    model = Model("BinPacking")
    model.hideOutput()

    x = {}
    y = {}
    for b in range(n_bins):
        y[b] = model.addVar(name=f"y_{b}", vtype="B", obj=1)
        for i in range(n_items):
            x[i, b] = model.addVar(name=f"x_{i}_{b}", vtype="B")

    for i in range(n_items):
        model.addCons(
            sum(x[i, b] for b in range(n_bins)) == 1,
            name=f"assign_{i}",
        )

    for b in range(n_bins):
        model.addCons(
            sum(sizes[i] * x[i, b] for i in range(n_items)) <= capacity * y[b],
            name=f"capacity_{b}",
        )

    # Symmetry breaking: order bins
    for b in range(n_bins - 1):
        model.addCons(y[b] >= y[b + 1], name=f"sym_{b}")

    return model


def _build_simple_model():
    """Build a simple model for quick tests."""
    model = Model("Simple")
    model.hideOutput()
    x = model.addVar(name="x", vtype="B", obj=3)
    y = model.addVar(name="y", vtype="B", obj=2)
    model.addCons(x + y <= 1)
    model.setMaximize()
    return model


def test_time_limit():
    """Time limit should be respected."""
    model = _build_simple_model()
    result = solve_with_time_limit(model, time_limit=60)
    assert isinstance(result, dict), "Should return a dict"
    assert "status" in result, "Missing key: status"
    assert "objective" in result, "Missing key: objective"
    assert "gap" in result, "Missing key: gap"
    assert "time" in result, "Missing key: time"
    assert result["time"] <= 61, "Solving time should respect the limit"
    print("PASS: test_time_limit")


def test_gap_limit():
    """Gap limit should stop early."""
    model = _build_simple_model()
    result = solve_with_gap_limit(model, gap=0.1)
    assert isinstance(result, dict), "Should return a dict"
    assert "status" in result, "Missing key: status"
    assert "objective" in result, "Missing key: objective"
    assert "gap" in result, "Missing key: gap"
    assert "n_nodes" in result, "Missing key: n_nodes"
    assert result["gap"] <= 0.1 + 1e-6, f"Gap should be <= 0.1, got {result['gap']}"
    print("PASS: test_gap_limit")


def test_emphasis():
    """Emphasis setting should not crash and return valid results."""
    model = _build_simple_model()
    result = solve_with_emphasis(model, "OPTIMALITY")
    assert isinstance(result, dict), "Should return a dict"
    assert "status" in result, "Missing key: status"
    assert "n_nodes" in result, "Missing key: n_nodes"
    assert "time" in result, "Missing key: time"
    print("PASS: test_emphasis")


def test_feasibility_emphasis():
    """Feasibility emphasis should also work."""
    model = _build_simple_model()
    result = solve_with_emphasis(model, "FEASIBILITY")
    assert result["status"] == "optimal", f"Expected optimal, got {result['status']}"
    print("PASS: test_feasibility_emphasis")


def test_load_and_solve():
    """Load a model from an LP file and solve it."""
    # Create a temporary LP file from a simple model
    m = Model("Export")
    m.hideOutput()
    x = m.addVar(name="x", vtype="B", obj=3)
    y = m.addVar(name="y", vtype="B", obj=2)
    m.addCons(x + y <= 1)
    m.setMaximize()

    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "test.lp")
    m.writeProblem(filepath)

    result = load_and_solve(filepath, params={"limits/time": 10})
    assert isinstance(result, dict), "Should return a dict"
    assert "status" in result, "Missing key: status"
    assert "objective" in result, "Missing key: objective"
    assert result["status"] == "optimal", f"Expected optimal, got {result['status']}"
    assert abs(result["objective"] - 3.0) < 1e-6, (
        f"Expected obj=3, got {result['objective']}"
    )

    os.remove(filepath)
    os.rmdir(tmpdir)
    print("PASS: test_load_and_solve")


def test_load_no_params():
    """Load and solve without extra parameters."""
    m = Model("Export2")
    m.hideOutput()
    x = m.addVar(name="x", vtype="I", obj=1, lb=0, ub=10)
    m.addCons(x >= 5)

    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "test2.lp")
    m.writeProblem(filepath)

    result = load_and_solve(filepath)
    assert result["status"] == "optimal", f"Expected optimal, got {result['status']}"
    assert abs(result["objective"] - 5.0) < 1e-6, (
        f"Expected obj=5, got {result['objective']}"
    )

    os.remove(filepath)
    os.rmdir(tmpdir)
    print("PASS: test_load_no_params")


if __name__ == "__main__":
    print("Running parameter tests...\n")

    tests = [
        test_time_limit,
        test_gap_limit,
        test_emphasis,
        test_feasibility_emphasis,
        test_load_and_solve,
        test_load_no_params,
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
