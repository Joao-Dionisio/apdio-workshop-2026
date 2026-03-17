#!/usr/bin/env python3
"""
Tests for Exercise 5: Nonlinear blending (pooling problem).

Run:
    python test_blending.py
"""

import traceback

from blending import blending


# Simple instance: 2 sources, 2 products, 1 pool
SOURCES = [
    {"cost": 1.0, "quality": 3.0},
    {"cost": 2.0, "quality": 1.0},
]

PRODUCTS = [
    {"revenue": 5.0, "max_quality": 2.5},
    {"revenue": 4.0, "max_quality": 1.5},
]


def test_builds():
    """Model should build without error."""
    model, x, y, z, lam = blending(SOURCES, PRODUCTS)
    assert model is not None, "Model should not be None"
    print("PASS: test_builds")


def test_solves():
    """Model should solve to optimality."""
    model, x, y, z, lam = blending(SOURCES, PRODUCTS)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print(f"PASS: test_solves (obj={model.getObjVal():.2f})")


def test_quality_respected():
    """Product quality limits should be satisfied."""
    model, x, y, z, lam = blending(SOURCES, PRODUCTS)
    model.hideOutput()
    model.optimize()

    n_s = len(SOURCES)
    n_p = len(PRODUCTS)
    lam_val = model.getVal(lam)

    for p in range(n_p):
        y_val = model.getVal(y[p])
        bypass_quality = sum(
            SOURCES[s]["quality"] * model.getVal(z[s, p]) for s in range(n_s)
        )
        d_p = y_val + sum(model.getVal(z[s, p]) for s in range(n_s))
        if d_p > 1e-6:
            effective_quality = (lam_val * y_val + bypass_quality) / d_p
            assert effective_quality <= PRODUCTS[p]["max_quality"] + 1e-4, (
                f"Product {p}: quality {effective_quality:.3f} > "
                f"max {PRODUCTS[p]['max_quality']}"
            )
    print("PASS: test_quality_respected")


def test_positive_profit():
    """Optimal profit should be positive for this instance."""
    model, x, y, z, lam = blending(SOURCES, PRODUCTS)
    model.hideOutput()
    model.optimize()
    assert model.getObjVal() > 0, f"Expected positive profit, got {model.getObjVal()}"
    print(f"PASS: test_positive_profit (profit={model.getObjVal():.2f})")


if __name__ == "__main__":
    print("Running blending tests...\n")

    tests = [
        test_builds,
        test_solves,
        test_quality_respected,
        test_positive_profit,
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
