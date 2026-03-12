"""
Compact MTZ formulation for the Traveling Salesman Problem.

Exercise 13: Implement the MTZ formulation.

The Miller-Tucker-Zemlin (MTZ) formulation uses position variables to
eliminate subtours. While it has a polynomial number of constraints,
its LP relaxation is weaker than the exponential-size SEC formulation.

Your task: Build the directed formulation with binary edge variables
x[i,j], continuous position variables u[i], degree constraints, and
the MTZ subtour elimination constraints.
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
    # =========================================================================
    # EXERCISE 13: Build the MTZ formulation for TSP
    # =========================================================================
    #
    # Step 1: Create a Model and get n from the distance matrix
    #
    # Step 2: Add binary variables x[i,j] for each pair i != j
    #         with objective coefficient distances[i][j]
    #
    # Step 3: Add continuous position variables u[i] for i = 1, ..., n-1
    #         with bounds 1 <= u[i] <= n-1  (u[0] is fixed implicitly)
    #
    # Step 4: Add out-degree constraints — each city is left exactly once
    #         sum_j x[i,j] == 1   for all i
    #
    # Step 5: Add in-degree constraints — each city is entered exactly once
    #         sum_i x[i,j] == 1   for all j
    #
    # Step 6: Add MTZ subtour elimination constraints
    #         u[i] - u[j] + n * x[i,j] <= n - 1   for all i,j != 0, i != j
    #
    # Step 7: Return model, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 13: Build the MTZ formulation for TSP.\n"
        "Hint: Directed binary x[i,j], continuous position u[i],\n"
        "degree constraints, and MTZ subtour elimination."
    )


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
