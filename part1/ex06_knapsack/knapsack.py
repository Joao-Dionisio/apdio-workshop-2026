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
    """Build and return a 0-1 knapsack IP."""
    # =========================================================================
    # EXERCISE 7: Build a 0-1 knapsack IP
    # =========================================================================
    #
    # This is a maximization problem — don't forget the objective sense.
    #
    # Return model, x
    #
    # =========================================================================

    raise NotImplementedError("Exercise 7: Build a 0-1 knapsack IP.")
