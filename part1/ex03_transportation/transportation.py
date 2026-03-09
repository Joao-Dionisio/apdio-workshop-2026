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
    """
    Build and return a transportation LP.

    Args:
        supply: List of supply amounts, length m (one per supplier).
        demand: List of demand amounts, length n (one per customer).
        costs: m x n cost matrix (list of lists); costs[i][j] is
               the per-unit cost of shipping from supplier i to customer j.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        x: Dict mapping (i, j) to continuous shipping variables.
    """
    # =========================================================================
    # EXERCISE 3: Build a transportation LP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add continuous variables x[i, j] >= 0 for each supplier-customer
    #         pair, with objective coefficient costs[i][j]
    #         Use model.addVar(name=..., vtype="C", lb=0, obj=costs[i][j])
    #
    # Step 3: Add supply constraints — each supplier ships at most supply[i]
    #         sum_j x[i,j] <= supply[i]   for all i
    #
    # Step 4: Add demand constraints — each customer receives at least demand[j]
    #         sum_i x[i,j] >= demand[j]   for all j
    #
    # Step 5: Return model, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3: Build a transportation LP.\n"
        "Hint: Continuous variables x[i,j] with supply and demand constraints."
    )
