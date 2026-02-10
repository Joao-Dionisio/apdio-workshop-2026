#!/usr/bin/env python3
"""
Tests for Exercise 4: Blending problem.

Run:
    python test_blending.py
"""

from blending import blending


def test_small_instance():
    """Solve a small blending problem with known optimal."""
    # 2 materials, 1 quality attribute
    costs = [3, 5]
    availability = [40, 40]
    qualities = [[30], [70]]  # material 0 has quality 30, material 1 has 70
    quality_lb = [40]  # average quality >= 40
    quality_ub = [60]  # average quality <= 60
    total_production = 20

    model, x = blending(costs, availability, qualities, quality_lb, quality_ub,
                        total_production)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Cheapest: use as much material 0 (cost 3) as quality allows
    # quality_lb: 30*x0 + 70*x1 >= 40*20 = 800
    # x0 + x1 = 20 => x1 = 20 - x0
    # 30*x0 + 70*(20 - x0) >= 800 => -40*x0 >= -600 => x0 <= 15
    # quality_ub: 30*x0 + 70*(20 - x0) <= 60*20 = 1200 => -40*x0 <= -200 => x0 >= 5
    # Max x0 = 15, x1 = 5 => cost = 3*15 + 5*5 = 45 + 25 = 70
    assert abs(model.getObjVal() - 70.0) < 1e-4, (
        f"Expected obj=70, got {model.getObjVal()}"
    )
    print("PASS: test_small_instance")


def test_quality_bounds_met():
    """Quality bounds should be satisfied in the solution."""
    costs = [2, 8]
    availability = [50, 50]
    qualities = [[20], [80]]
    quality_lb = [45]
    quality_ub = [55]
    total_production = 30

    model, x = blending(costs, availability, qualities, quality_lb, quality_ub,
                        total_production)
    model.hideOutput()
    model.optimize()

    # Check quality bounds
    total_quality = sum(
        qualities[i][0] * model.getVal(x[i]) for i in range(2)
    )
    T = total_production
    assert total_quality >= quality_lb[0] * T - 1e-6, "Quality lower bound violated"
    assert total_quality <= quality_ub[0] * T + 1e-6, "Quality upper bound violated"
    print("PASS: test_quality_bounds_met")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_blending_instance

    data = random_blending_instance(4, 2, seed=42)
    costs, availability, qualities, qlb, qub, total = data
    model, x = blending(costs, availability, qualities, qlb, qub, total)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print("PASS: test_generated_instance")


if __name__ == "__main__":
    print("Running blending tests...\n")

    tests = [
        test_small_instance,
        test_quality_bounds_met,
        test_generated_instance,
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
