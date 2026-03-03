#!/usr/bin/env python3
"""
Tests for Exercise 7: Facility location.

Run:
    python test_facility_location.py
"""

from facility_location import facility_location


def test_small_instance():
    """Solve a small facility location with known optimal."""
    fixed_costs = [100, 150]
    connection_costs = [
        [10, 20, 30],  # facility 0
        [30, 10, 10],  # facility 1
    ]

    model, y, x = facility_location(fixed_costs, connection_costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Open facility 0 only: 100 + 10 + 20 + 30 = 160
    # Open facility 1 only: 150 + 30 + 10 + 10 = 200
    # Open both: 250 + 10 + 10 + 10 = 280
    # Best with selective: open 0 (cost 100) serve C0 (10), open 1 (cost 150) serve C1,C2 (10+10)
    #   total = 100 + 150 + 10 + 10 + 10 = 280
    # Actually: open 0 only = 100 + 10 + 20 + 30 = 160
    assert abs(model.getObjVal() - 160.0) < 1e-4, (
        f"Expected obj=160, got {model.getObjVal()}"
    )
    print("PASS: test_small_instance")


def test_linking_constraints():
    """Customers should only be assigned to open facilities."""
    fixed_costs = [100, 100]
    connection_costs = [
        [1, 1],
        [1, 1],
    ]

    model, y, x = facility_location(fixed_costs, connection_costs)
    model.hideOutput()
    model.optimize()

    for i in range(2):
        for j in range(2):
            assert model.getVal(x[i, j]) <= model.getVal(y[i]) + 1e-6, (
                f"x[{i},{j}]={model.getVal(x[i,j])} > y[{i}]={model.getVal(y[i])}"
            )
    print("PASS: test_linking_constraints")


def test_all_customers_served():
    """Every customer must be assigned to exactly one facility."""
    fixed_costs = [50, 80, 60]
    connection_costs = [
        [5, 15, 10],
        [15, 5, 10],
        [10, 10, 5],
    ]

    model, y, x = facility_location(fixed_costs, connection_costs)
    model.hideOutput()
    model.optimize()

    n_customers = 3
    for j in range(n_customers):
        total_assigned = sum(
            model.getVal(x[i, j]) for i in range(3)
        )
        assert abs(total_assigned - 1.0) < 1e-6, (
            f"Customer {j} assignment = {total_assigned}, expected 1.0"
        )
    print("PASS: test_all_customers_served")


def test_generated_instance():
    """Solve a generated instance."""
    from generator import random_facility_location_instance

    fixed_costs, conn_costs = random_facility_location_instance(4, 6, seed=42)
    model, y, x = facility_location(fixed_costs, conn_costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print("PASS: test_generated_instance")


def test_generated_larger():
    """Solve a larger generated instance (6 facilities, 10 customers)."""
    from generator import random_facility_location_instance

    fixed_costs, conn_costs = random_facility_location_instance(6, 10, seed=99)
    model, y, x = facility_location(fixed_costs, conn_costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"

    # Verify all customers served
    n_facilities, n_customers = len(fixed_costs), len(conn_costs[0])
    for j in range(n_customers):
        total_assigned = sum(model.getVal(x[i, j]) for i in range(n_facilities))
        assert abs(total_assigned - 1.0) < 1e-6, (
            f"Customer {j} assignment = {total_assigned}, expected 1.0"
        )
    print("PASS: test_generated_larger")


def test_generated_many_facilities():
    """Solve an instance with many facilities and few customers."""
    from generator import random_facility_location_instance

    fixed_costs, conn_costs = random_facility_location_instance(8, 5, seed=7)
    model, y, x = facility_location(fixed_costs, conn_costs)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 0, "Objective should be non-negative"
    print("PASS: test_generated_many_facilities")


if __name__ == "__main__":
    print("Running facility location tests...\n")

    tests = [
        test_small_instance,
        test_linking_constraints,
        test_all_customers_served,
        test_generated_instance,
        test_generated_larger,
        test_generated_many_facilities,
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
