"""
Compact MTZ formulation for the Traveling Salesman Problem.

Exercise 6: Implement the MTZ formulation.

Variables:
    x[i,j] — binary, 1 if the tour goes directly from city i to city j.
              Directed: x[i,j] and x[j,i] are separate variables.
              Only defined for i != j.

    u[i]   — continuous, position of city i in the tour.
              Only for cities 1, ..., n-1  (NOT city 0).
              City 0 is the depot and is implicitly at position 0.
              Bounds: 1 <= u[i] <= n-1.

Args (from the input):
    distances: n x n matrix (list of lists). distances[i][j] is the
               distance from city i to city j.  Cities are 0-indexed.

Formulation:
    min  sum_{i != j} distances[i][j] * x[i,j]

    s.t. sum_{j != i} x[i,j] = 1              for all i        (leave once)
         sum_{i != j} x[i,j] = 1              for all j        (enter once)
         u[i] - u[j] + n*x[i,j] <= n - 1      for i,j in 1..n-1, i != j
         x[i,j] in {0, 1}

Note: the MTZ constraints only involve cities 1..n-1 (not the depot).
"""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    """Build the MTZ formulation for TSP.

    Args:
        distances: n x n distance matrix (0-indexed cities).

    Returns:
        (model, x) where x is a dict mapping (i, j) to binary variables (i != j).
    """
    # =========================================================================
    # EXERCISE 6: Build the MTZ formulation for TSP
    # =========================================================================
    #
    # Step 1: Create a Model and get n from the distance matrix
    #         n = len(distances)
    #
    # Step 2: Add binary variables x[i,j] for each pair i != j
    #         with objective coefficient distances[i][j]
    #
    # Step 3: Add continuous position variables u[i] for i = 1, ..., n-1
    #         with bounds 1 <= u[i] <= n-1
    #         (city 0 is the depot — no u variable needed for it)
    #
    # Step 4: Add out-degree constraints — each city is left exactly once
    #         sum_{j != i} x[i,j] == 1   for all i
    #
    # Step 5: Add in-degree constraints — each city is entered exactly once
    #         sum_{i != j} x[i,j] == 1   for all j
    #
    # Step 6: Add MTZ subtour elimination constraints
    #         u[i] - u[j] + n * x[i,j] <= n - 1
    #         for all i, j in {1, ..., n-1} with i != j
    #         (only non-depot cities!)
    #
    # Step 7: Return model, x
    #
    # =========================================================================

    n_cities = len(distances)

    model = Model("tsp_mtz")

    raise NotImplementedError(
        "Exercise 6: Build the MTZ formulation for TSP.\n"
        "Hint: Directed binary x[i,j] for i != j, continuous position u[i]\n"
        "for i = 1..n-1, degree constraints, and MTZ subtour elimination."
    )
