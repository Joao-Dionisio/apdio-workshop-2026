"""
Transportation problem.

    min  sum_{i,j} c_{ij} * x_{ij}
    s.t. sum_j x_{ij} <= supply_i    for all suppliers i
         sum_i x_{ij} >= demand_j    for all customers j
         x_{ij} >= 0
"""

from pyscipopt import Model, quicksum


def transportation(supply, demand, costs):
    """Build and return a transportation LP.

    Args:
        supply: list — supply[i] is the capacity of supplier i.
        demand: list — demand[j] is the requirement of customer j.
        costs:  matrix (list of lists) — costs[i][j] is the shipping cost.

    Returns:
        (model, x) where x is a dict mapping (i, j) tuples to continuous
        variables, e.g. x[0, 2] is the shipment from supplier 0 to customer 2.

    Hints:
        - Use vtype="C" for continuous variables.
        - Use quicksum() to build constraint left-hand sides.
    """
    # EXERCISE 4: Build the LP — variables, supply/demand constraints, objective

    n_suppliers = len(supply)
    n_customers = len(demand)

    model = Model("transportation")

    raise NotImplementedError("Exercise 4: Build a transportation LP.")
