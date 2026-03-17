"""
Transportation problem.

Exercise 4: Build a transportation LP.

Given a set of suppliers with limited supply, a set of customers with
specific demands, and per-unit transportation costs, find the minimum
cost way to ship goods from suppliers to customers.

Formulation:
    min  sum_{i,j} c_{ij} * x_{ij}
    s.t. sum_j x_{ij} <= supply_i    for all suppliers i
         sum_i x_{ij} >= demand_j    for all customers j
         x_{ij} >= 0
"""

from pyscipopt import Model, quicksum


def transportation(supply, demand, costs):
    """Build and return a transportation LP.

    Args:
        supply: list of length n_suppliers — supply[i] is the capacity of supplier i.
        demand: list of length n_customers — demand[j] is the requirement of customer j.
        costs:  n_suppliers x n_customers matrix (list of lists) — costs[i][j] is the
                per-unit shipping cost from supplier i to customer j.

    Returns:
        (model, x) where x is a dict mapping (i, j) tuples to variables.
    """
    # =========================================================================
    # EXERCISE 4: Build a transportation LP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add a continuous variable x[i,j] >= 0 for each (i, j) pair
    #         Store them in a dict: x = {}
    #
    # Step 3: Add supply constraints (one per supplier i):
    #         sum over j of x[i,j] <= supply[i]
    #
    # Step 4: Add demand constraints (one per customer j):
    #         sum over i of x[i,j] >= demand[j]
    #
    # Step 5: Set objective — minimize total cost
    #
    # Return model, x
    #
    # =========================================================================

    n_suppliers = len(supply)
    n_customers = len(demand)

    model = Model("transportation")

    raise NotImplementedError("Exercise 4: Build a transportation LP.")
