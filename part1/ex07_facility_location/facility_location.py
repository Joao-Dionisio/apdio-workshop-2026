"""
Uncapacitated facility location problem.

Exercise 7: Build a facility location MIP.

Given a set of potential facility sites (each with a fixed opening cost)
and a set of customers (each to be served by exactly one facility),
choose which facilities to open and assign customers to minimize total cost.

Formulation:
    min  sum_i f_i * y_i  +  sum_{i,j} c_{ij} * x_{ij}
    s.t. sum_i x_{ij} = 1        for all customers j     (assignment)
         x_{ij} <= y_i            for all i, j            (linking)
         y_i in {0, 1}            for all facilities i
         x_{ij} >= 0              for all i, j
"""

from pyscipopt import Model, quicksum


def facility_location(fixed_costs, connection_costs):
    """
    Build and return an uncapacitated facility location MIP.

    Args:
        fixed_costs: List of fixed opening costs (length m).
        connection_costs: m x n cost matrix; connection_costs[i][j] is
                         the cost of serving customer j from facility i.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        y: Dict mapping facility index i to binary variable (open/close).
        x: Dict mapping (i, j) to continuous variable (assignment fraction).
    """
    m = len(fixed_costs)
    n = len(connection_costs[0])

    # =========================================================================
    # EXERCISE 7: Build a facility location MIP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add binary variables y[i] for each facility with obj=fixed_costs[i]
    #
    # Step 3: Add continuous variables x[i, j] in [0, 1] for each
    #         facility-customer pair with obj=connection_costs[i][j]
    #
    # Step 4: Assignment constraints — each customer served by exactly one facility
    #         sum_i x[i, j] == 1   for all j
    #
    # Step 5: Linking constraints — can only assign to open facilities
    #         x[i, j] <= y[i]     for all i, j
    #
    # Step 6: Return model, y, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 7: Build a facility location MIP.\n"
        "Hint: Binary y[i] for opening, continuous x[i,j] for assignment,\n"
        "linking constraints x[i,j] <= y[i]."
    )
