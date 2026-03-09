"""
0-1 Knapsack problem.

Exercise 6: Build a 0-1 knapsack IP.

Given a set of items, each with a weight and a value, and a knapsack
with limited capacity, select items to maximize total value without
exceeding capacity.

Formulation:
    max  sum_i v_i * x_i
    s.t. sum_i w_i * x_i <= C
         x_i in {0, 1}         for all i
"""

from pyscipopt import Model, quicksum


def knapsack(weights, values, capacity):
    """
    Build and return a 0-1 knapsack IP.

    Args:
        weights: List of item weights (length n).
        values: List of item values (length n).
        capacity: Knapsack capacity.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        x: Dict mapping item index i to binary variable.
    """
    # =========================================================================
    # EXERCISE 6: Build a 0-1 knapsack IP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add a binary variable x[i] for each item i with obj=values[i]
    #
    # Step 3: Add the capacity constraint:
    #         sum_i weights[i] * x[i] <= capacity
    #
    # Step 4: Set objective to maximize
    #
    # Step 5: Return model, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 6: Build a 0-1 knapsack IP.\n"
        "Hint: Binary variable per item, one capacity constraint."
    )
