#!/usr/bin/env python3
"""
Tests for Exercise 4: Transportation problem.

Run:
    python test_transportation.py
"""

from transportation import transportation


def test_small_instance():
    """Solve a small balanced transportation problem."""
    supply = [20, 30]
    demand = [25, 25]
    costs = [
        [4, 8],
        [6, 3],
    ]
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Optimal: ship 20 from S0->C0, 5 from S1->C0, 25 from S1->C1 = 80+30+75 = 185
    # Actually: S0->C0: 20 (cost 80), S1->C0: 5 (cost 30), S1->C1: 25 (cost 75) = 185
    assert abs(model.getObjVal() - 185.0) < 1e-4, (
        f"Expected obj=185, got {model.getObjVal()}"
    )
    print("PASS: test_small_instance")


def test_supply_constraints():
    """Supply constraints should be respected."""
    supply = [10, 10]
    demand = [10, 10]
    costs = [[1, 100], [100, 1]]
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    # Check supply not exceeded
    for i in range(2):
        shipped = sum(model.getVal(x[i, j]) for j in range(2))
        assert shipped <= supply[i] + 1e-6, (
            f"Supplier {i} shipped {shipped} > supply {supply[i]}"
        )
    print("PASS: test_supply_constraints")


def test_demand_constraints():
    """Demand constraints should be met."""
    supply = [10, 10]
    demand = [10, 10]
    costs = [[1, 100], [100, 1]]
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    # Check demand met
    for j in range(2):
        received = sum(model.getVal(x[i, j]) for i in range(2))
        assert received >= demand[j] - 1e-6, (
            f"Customer {j} received {received} < demand {demand[j]}"
        )
    print("PASS: test_demand_constraints")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_transportation_instance

    supply, demand, costs = random_transportation_instance(3, 4, seed=42)
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Objective should be non-negative"
    print("PASS: test_generated_instance")


def test_generated_larger():
    """Solve a larger generated instance (5 suppliers, 8 customers)."""
    from generator import random_transportation_instance

    supply, demand, costs = random_transportation_instance(5, 8, seed=99)
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Verify all demand is met
    n_suppliers, n_customers = len(supply), len(demand)
    for j in range(n_customers):
        received = sum(model.getVal(x[i, j]) for i in range(n_suppliers))
        assert received >= demand[j] - 1e-6, f"Customer {j} demand not met"
    print("PASS: test_generated_larger")


def test_generated_unbalanced():
    """Solve an instance with few suppliers and many customers."""
    from generator import random_transportation_instance

    supply, demand, costs = random_transportation_instance(2, 6, seed=7)
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Objective should be non-negative"
    print("PASS: test_generated_unbalanced")


if __name__ == "__main__":
    print("Running transportation tests...\n")

    tests = [
        test_small_instance,
        test_supply_constraints,
        test_demand_constraints,
        test_generated_instance,
        test_generated_larger,
        test_generated_unbalanced,
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
