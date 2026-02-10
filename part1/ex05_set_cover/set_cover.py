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
    """
    Build and return a set cover IP.

    Args:
        universe: Set of elements to cover.
        subsets: List of sets, each a subset of universe.
        costs: List of costs (one per subset).

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        y: Dict mapping subset index j to binary variable.

    Raises:
        NotImplementedError: This is Exercise 5 — implement the model.
    """
    # =========================================================================
    # EXERCISE 5: Build a set cover IP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add a binary variable y[j] for each subset j with obj=costs[j]
    #
    # Step 3: For each element e in the universe, add a covering constraint:
    #         sum of y[j] for all j where e is in subsets[j] >= 1
    #
    # Step 4: Set objective to minimize
    #
    # Step 5: Return model, y
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 5: Build a set cover IP.\n"
        "Hint: Binary variable per subset, one covering constraint per element."
    )
