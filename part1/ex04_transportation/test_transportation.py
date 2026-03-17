#!/usr/bin/env python3
"""
Tests for Exercise 4: Transportation problem.

Run:
    python test_transportation.py
"""

import random
import traceback

from transportation import transportation


def random_transportation_instance(n_suppliers, n_customers, seed=0):
    """
    Generate a random transportation problem instance.

    Args:
        n_suppliers: Number of suppliers.
        n_customers: Number of customers.
        seed: Random seed for reproducibility.

    Returns:
        supply: List of supply amounts (length n_suppliers).
        demand: List of demand amounts (length n_customers).
        costs: n_suppliers x n_customers cost matrix (list of lists).
    """
    random.seed(seed)

    # Generate supply and demand ensuring feasibility (total supply >= total demand)
    supply = [random.randint(10, 50) for _ in range(n_suppliers)]
    demand = [random.randint(5, 30) for _ in range(n_customers)]

    # Scale supply so that total supply = total demand (balanced)
    total_demand = sum(demand)
    total_supply = sum(supply)
    scale = total_demand / total_supply
    supply = [int(round(s * scale)) for s in supply]

    # Adjust to make exactly balanced
    diff = total_demand - sum(supply)
    supply[0] += diff

    # Random transportation costs
    costs = [[random.randint(1, 20) for _ in range(n_customers)]
             for _ in range(n_suppliers)]

    return supply, demand, costs


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
    supply, demand, costs = random_transportation_instance(3, 4, seed=42)
    model, x = transportation(supply, demand, costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Objective should be non-negative"
    print("PASS: test_generated_instance")


def test_generated_larger():
    """Solve a larger generated instance (5 suppliers, 8 customers)."""
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
            traceback.print_exc()
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
