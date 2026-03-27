#!/usr/bin/env python3
"""
Tests for Exercise 3: Solver parameters.

Run:
    python test_parameters.py
"""

import os
import tempfile
import traceback

from pyscipopt import Model
from parameters import solve_with_params, load_and_solve


REQUIRED_KEYS = {"status", "objective", "gap", "n_nodes", "time"}


def _build_simple_model():
    """Build a simple model for quick tests."""
    model = Model("Simple")
    model.hideOutput()
    x = model.addVar(name="x", vtype="B", obj=3)
    y = model.addVar(name="y", vtype="B", obj=2)
    model.addCons(x + y <= 1)
    model.setMaximize()
    return model


# ---------- solve_with_params tests ----------

def test_return_format():
    """Result should be a dict with the required keys."""
    model = _build_simple_model()
    result = solve_with_params(model, {})
    assert isinstance(result, dict), "Should return a dict"
    for key in REQUIRED_KEYS:
        assert key in result, f"Missing key: {key}"
    print("[92mPASS:[0m test_return_format")


def test_time_limit():
    """Time limit parameter should be respected."""
    model = _build_simple_model()
    result = solve_with_params(model, {"limits/time": 60})
    assert result["time"] <= 61, "Solving time should respect the limit"
    assert result["status"] == "optimal"
    print("[92mPASS:[0m test_time_limit")


def test_gap_limit():
    """Gap limit parameter should be respected."""
    model = _build_simple_model()
    result = solve_with_params(model, {"limits/gap": 0.1})
    assert result["gap"] <= 0.1 + 1e-6, f"Gap should be <= 0.1, got {result['gap']}"
    print("[92mPASS:[0m test_gap_limit")


def test_emphasis():
    """Emphasis settings should work (passed as a regular parameter)."""
    for emphasis in ["OPTIMALITY", "FEASIBILITY"]:
        model = _build_simple_model()
        result = solve_with_params(
            model, {"limits/time": 30, "emphasis/" + emphasis.lower(): 1}
        )
        assert result["status"] == "optimal", (
            f"Expected optimal with {emphasis} emphasis, got {result['status']}"
        )
    print("[92mPASS:[0m test_emphasis")


def test_no_solution_objective():
    """Objective should be None when no solution is found (e.g., infeasible)."""
    model = Model("Infeasible")
    model.hideOutput()
    x = model.addVar(name="x", vtype="B")
    model.addCons(x >= 2)  # infeasible for binary
    result = solve_with_params(model, {})
    assert result["objective"] is None, (
        f"Expected None for infeasible, got {result['objective']}"
    )
    print("[92mPASS:[0m test_no_solution_objective")


# ---------- load_and_solve tests ----------

def _write_temp_model():
    """Write a simple model to a temp LP file and return the path."""
    m = Model("Export")
    m.hideOutput()
    x = m.addVar(name="x", vtype="B", obj=3)
    y = m.addVar(name="y", vtype="B", obj=2)
    m.addCons(x + y <= 1)
    m.setMaximize()

    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "test.lp")
    m.writeProblem(filepath)
    return filepath


def test_load_and_solve():
    """Load a model from file, apply params, and solve."""
    filepath = _write_temp_model()
    result = load_and_solve(filepath, params={"limits/time": 10})
    assert isinstance(result, dict), "Should return a dict"
    for key in REQUIRED_KEYS:
        assert key in result, f"Missing key: {key}"
    assert result["status"] == "optimal", f"Expected optimal, got {result['status']}"
    assert abs(result["objective"] - 3.0) < 1e-6, (
        f"Expected obj=3, got {result['objective']}"
    )

    os.remove(filepath)
    os.rmdir(os.path.dirname(filepath))
    print("[92mPASS:[0m test_load_and_solve")


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
    print("[92mPASS:[0m test_load_no_params")


def test_load_miplib():
    """Load a MIPLIB instance if available."""
    miplib_path = os.path.join(os.path.dirname(__file__), "miplib_data", "pk1.mps.gz")
    if not os.path.exists(miplib_path):
        print("[93mSKIP:[0m test_load_miplib - miplib_data/pk1.mps.gz not found")
        return

    result = load_and_solve(miplib_path, params={"limits/time": 30})
    assert result["status"] in ("optimal", "timelimit"), (
        f"Unexpected status: {result['status']}"
    )
    assert result["objective"] is not None, "pk1 should find a solution"
    print("[92mPASS:[0m test_load_miplib")


if __name__ == "__main__":
    print("Running parameter tests...\n")

    tests = [
        test_return_format,
        test_time_limit,
        test_gap_limit,
        test_emphasis,
        test_no_solution_objective,
        test_load_and_solve,
        test_load_no_params,
        test_load_miplib,
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
