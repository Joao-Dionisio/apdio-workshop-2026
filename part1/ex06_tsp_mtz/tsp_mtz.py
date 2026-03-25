"""
Compact MTZ formulation for the Traveling Salesman Problem.

Variables:
    x[i,j] in {0,1} — directed edge from i to j (i != j)
    u[i] in [1, n-1] — position of city i (only for i = 1..n-1, not depot 0)

Formulation:
    min  sum_{i != j} d[i][j] * x[i,j]
    s.t. sum_{j != i} x[i,j] = 1              for all i    (leave once)
         sum_{i != j} x[i,j] = 1              for all j    (enter once)
         u[i] - u[j] + n*x[i,j] <= n - 1      for i,j in 1..n-1, i != j
"""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    """Build the MTZ formulation for TSP.

    Args:
        distances: n x n distance matrix (0-indexed cities).

    Returns:
        (model, x) where x maps (i, j) to binary variables (i != j).
    """
    # EXERCISE 6: Build the MTZ formulation
    # Don't forget: MTZ constraints only involve cities 1..n-1 (not depot 0)

    n_cities = len(distances)

    model = Model("tsp_mtz")

    raise NotImplementedError("Exercise 6: Build the MTZ formulation for TSP.")
