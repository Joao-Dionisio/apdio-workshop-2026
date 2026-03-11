"""
Transportation problem.

Exercise 3: Build a transportation LP.

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
    """Build and return a transportation LP."""
    # =========================================================================
    # EXERCISE 4: Build a transportation LP
    # =========================================================================
    #
    # Continuous variable x[i,j] for each supplier-customer pair.
    # Supply and demand constraints per the formulation above.
    #
    # Hint: use model.addVar(name=..., vtype="C", lb=0, obj=costs[i][j])
    #
    # Return model, x
    #
    # =========================================================================

    raise NotImplementedError("Exercise 4: Build a transportation LP.")
