"""
0-1 Knapsack problem.

    max  sum_i v_i * x_i
    s.t. sum_i w_i * x_i <= C
         x_i in {0, 1}
"""

from pyscipopt import Model, quicksum


def knapsack(weights, values, capacity):
    """Build and return a 0-1 knapsack IP.

    Returns:
        (model, x) — model and dict mapping item index to binary variable.
    """
    # EXERCISE 5: Build the knapsack IP (maximization)

    n_items = len(weights)

    model = Model("knapsack")

    raise NotImplementedError("Exercise 5: Build a 0-1 knapsack IP.")
