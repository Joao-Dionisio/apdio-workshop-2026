"""
Compact MTZ formulation for the Traveling Salesman Problem.

The Miller-Tucker-Zemlin (MTZ) formulation uses position variables to
eliminate subtours. While it has a polynomial number of constraints,
its LP relaxation is weaker than the exponential-size SEC formulation.
"""

from pyscipopt import Model, quicksum


def tsp_mtz(distances):
    """
    Solve TSP using the Miller-Tucker-Zemlin compact formulation.

    The MTZ formulation uses:
    - Binary variables x[i,j] indicating if edge (i,j) is in the tour
    - Continuous variables u[i] representing the position of city i in the tour

    The subtour elimination constraints are:
        u[i] - u[j] + n * x[i,j] <= n - 1  for all i,j != 0

    This ensures that if x[i,j] = 1, then u[j] >= u[i] + 1, creating a
    consistent ordering that prevents subtours.

    Args:
        distances: n x n symmetric distance matrix

    Returns:
        model: PySCIPOpt Model object
        x: dict mapping (i,j) to binary edge variables
    """
    model = Model("TSP-MTZ")
    n = len(distances)

    # Binary edge variables (directed formulation for MTZ)
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.addVar(vtype="B", obj=distances[i][j],
                                       name=f"x_{i}_{j}")

    # Position variables (continuous)
    u = {}
    for i in range(1, n):  # u[0] is fixed implicitly
        u[i] = model.addVar(vtype="C", lb=1, ub=n - 1, name=f"u_{i}")

    # Each city must be left exactly once
    for i in range(n):
        model.addCons(
            quicksum(x[i, j] for j in range(n) if j != i) == 1,
            name=f"out_{i}"
        )

    # Each city must be entered exactly once
    for j in range(n):
        model.addCons(
            quicksum(x[i, j] for i in range(n) if i != j) == 1,
            name=f"in_{j}"
        )

    # MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addCons(
                    u[i] - u[j] + n * x[i, j] <= n - 1,
                    name=f"mtz_{i}_{j}"
                )

    return model, x


if __name__ == "__main__":
    from generator import random_euclidean_tsp

    # Solve a small instance
    n_cities = 10
    distances = random_euclidean_tsp(n_cities, seed=42)

    print(f"Solving {n_cities}-city TSP with MTZ formulation...")
    model, x = tsp_mtz(distances)
    model.optimize()

    print(f"\nOptimal tour length: {model.getObjVal():.0f}")

    # Extract and print tour
    tour = [0]
    current = 0
    for _ in range(n_cities - 1):
        for j in range(n_cities):
            if j != current and model.getVal(x[current, j]) > 0.5:
                tour.append(j)
                current = j
                break
    tour.append(0)
    print(f"Tour: {' -> '.join(map(str, tour))}")
