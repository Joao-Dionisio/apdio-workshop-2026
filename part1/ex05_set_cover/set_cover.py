"""
Set cover problem.

Exercise 5: Build a set cover IP.

Given a universe of elements and a collection of subsets (each with a cost),
select the minimum-cost collection of subsets that covers every element.

Formulation:
    min  sum_j c_j * y_j
    s.t. sum_{j : e in S_j} y_j >= 1   for all e in U
         y_j in {0, 1}                  for all j
"""

from pyscipopt import Model, quicksum


def set_cover(universe, subsets, costs):
    """Build and return a set cover IP."""
    # =========================================================================
    # EXERCISE 6: Build a set cover IP
    # =========================================================================
    #
    # One binary variable per subset. Think about what constraint
    # ensures every element in the universe is covered.
    #
    # Return model, y
    #
    # =========================================================================

    raise NotImplementedError("Exercise 6: Build a set cover IP.")
