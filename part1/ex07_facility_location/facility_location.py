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
    """Build and return an uncapacitated facility location MIP."""
    m = len(fixed_costs)
    n = len(connection_costs[0])

    # =========================================================================
    # EXERCISE 9: Build a facility location MIP
    # =========================================================================
    #
    # You need two types of variables. What connects the opening
    # decisions to the customer assignments?
    #
    # Return model, y, x
    #
    # =========================================================================

    raise NotImplementedError("Exercise 9: Build a facility location MIP.")
