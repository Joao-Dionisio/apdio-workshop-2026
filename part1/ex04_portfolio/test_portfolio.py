#!/usr/bin/env python3
"""
Tests for Exercise 4: Portfolio optimization.

Run:
    python test_portfolio.py
"""

from portfolio import portfolio


def test_two_assets():
    """Solve a 2-asset portfolio with known optimal."""
    # Asset 0: low return, low risk; Asset 1: high return, high risk
    expected_returns = [0.05, 0.10]
    covariance = [
        [0.01, 0.002],
        [0.002, 0.04],
    ]
    r_min = 0.07  # require 7% return

    model, x = portfolio(expected_returns, covariance, r_min)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Check budget constraint
    total = sum(model.getVal(x[i]) for i in range(2))
    assert abs(total - 1.0) < 1e-4, f"Budget violated: {total}"

    # Check return constraint
    ret = sum(expected_returns[i] * model.getVal(x[i]) for i in range(2))
    assert ret >= r_min - 1e-6, f"Return {ret} below target {r_min}"

    # With r_min = 0.07: x0 = 0.6, x1 = 0.4
    # return = 0.05*0.6 + 0.10*0.4 = 0.07 (binding)
    assert abs(model.getVal(x[0]) - 0.6) < 1e-3, (
        f"Expected x[0]=0.6, got {model.getVal(x[0]):.4f}"
    )

    print("PASS: test_two_assets")


def test_equal_assets():
    """Equal assets with no correlation should give equal weights."""
    n = 3
    expected_returns = [0.10, 0.10, 0.10]
    covariance = [
        [0.04, 0.0, 0.0],
        [0.0, 0.04, 0.0],
        [0.0, 0.0, 0.04],
    ]
    r_min = 0.10

    model, x = portfolio(expected_returns, covariance, r_min)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Equal variance, zero correlation, same return => equal weights
    for i in range(n):
        assert abs(model.getVal(x[i]) - 1.0 / n) < 1e-3, (
            f"Expected x[{i}]={1.0/n:.4f}, got {model.getVal(x[i]):.4f}"
        )

    print("PASS: test_equal_assets")


def test_objective_is_quadratic():
    """Verify the objective is truly quadratic (not linear)."""
    expected_returns = [0.05, 0.12]
    covariance = [
        [0.01, 0.005],
        [0.005, 0.09],
    ]
    r_min = 0.05  # low target so return constraint is not binding

    model, x = portfolio(expected_returns, covariance, r_min)
    model.hideOutput()
    model.optimize()

    # With low r_min, the optimizer should put most weight on asset 0
    # (lower variance) rather than split evenly
    assert model.getVal(x[0]) > 0.7, (
        f"Expected x[0] > 0.7 (low-risk asset), got {model.getVal(x[0]):.4f}"
    )

    # Objective should be positive (variance > 0 for any portfolio)
    assert model.getObjVal() > 0, f"Expected positive variance, got {model.getObjVal()}"

    print("PASS: test_objective_is_quadratic")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_portfolio_instance

    mu, sigma, r_min = random_portfolio_instance(5, seed=42)
    model, x = portfolio(mu, sigma, r_min)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Check constraints
    n = len(mu)
    total = sum(model.getVal(x[i]) for i in range(n))
    assert abs(total - 1.0) < 1e-4, f"Budget violated: {total}"

    ret = sum(mu[i] * model.getVal(x[i]) for i in range(n))
    assert ret >= r_min - 1e-6, f"Return {ret} below target {r_min}"

    print("PASS: test_generated_instance")


def test_generated_large():
    """Solve a larger generated instance."""
    from generator import random_portfolio_instance

    mu, sigma, r_min = random_portfolio_instance(10, seed=99)
    model, x = portfolio(mu, sigma, r_min)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Variance should be non-negative"

    # All weights in [0, 1]
    for i in range(10):
        val = model.getVal(x[i])
        assert -1e-6 <= val <= 1 + 1e-6, f"x[{i}] = {val} out of bounds"

    print("PASS: test_generated_large")


if __name__ == "__main__":
    print("Running portfolio optimization tests...\n")

    tests = [
        test_two_assets,
        test_equal_assets,
        test_objective_is_quadratic,
        test_generated_instance,
        test_generated_large,
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
