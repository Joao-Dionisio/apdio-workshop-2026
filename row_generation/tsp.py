"""
TSP with row generation (lazy subtour elimination constraints).

This module implements the edge-based TSP formulation with exponentially
many subtour elimination constraints (SECs) added lazily via a constraint
handler.

The formulation:
    min  sum_{i<j} d_ij * x_ij
    s.t. sum_{j: j!=i} x_ij = 2          for all i  (degree constraints)
         sum_{e in E(S)} x_e <= |S| - 1  for all S  (SECs, added lazily)
         x_ij in {0, 1}

The SECs ensure that no proper subset S forms a subtour. Since there are
exponentially many such constraints, we add them on-the-fly using the
SubtourElimination constraint handler.
"""

from pyscipopt import Model, quicksum

from conshdlr_subtour import SubtourElimination


def tsp_rowgen(distances):
    """
    Create a TSP model with lazy subtour elimination constraints.

    This formulation uses:
    - Binary variables x[i,j] for each edge (i < j for symmetric TSP)
    - Degree-2 constraints ensuring each city has exactly 2 incident edges
    - SECs added lazily via the SubtourElimination constraint handler

    Args:
        distances: n x n symmetric distance matrix

    Returns:
        model: PySCIPOpt Model object
        x: dict mapping (i, j) with i < j to binary edge variables
    """
    model = Model("TSP-RowGen")
    n = len(distances)

    # Binary edge variables (only i < j for symmetric TSP)
    x = {}
    for i in range(n):
        for j in range(i + 1, n):
            x[i, j] = model.addVar(
                vtype="B",
                obj=distances[i][j],
                name=f"x_{i}_{j}"
            )

    # Degree constraints: each city must have exactly 2 incident edges
    for i in range(n):
        incident_edges = []
        for j in range(n):
            if i != j:
                # Get the edge variable (always stored with smaller index first)
                edge_key = (min(i, j), max(i, j))
                incident_edges.append(x[edge_key])

        model.addCons(
            quicksum(incident_edges) == 2,
            name=f"degree_{i}"
        )

    # Include the subtour elimination constraint handler
    conshdlr = SubtourElimination(x, n)
    model.includeConshdlr(
        conshdlr,
        "subtour",
        "Lazy subtour elimination constraints",
        sepapriority=0,       # Separation priority
        enfopriority=-1,      # Enforcement priority (negative = called late)
        chckpriority=-1,      # Checking priority
        sepafreq=-1,          # Separation frequency (-1 = only at root)
        propfreq=-1,          # Propagation frequency (-1 = disabled)
        eagerfreq=-1,         # Eager evaluation frequency
        maxprerounds=0,       # Max presolving rounds
        delaysepa=False,      # Delay separation
        delayprop=False,      # Delay propagation
        needscons=False       # Handler doesn't need explicit constraints
    )

    return model, x


def extract_tour(model, x, n):
    """
    Extract the tour from a solved TSP model.

    Args:
        model: Solved PySCIPOpt Model
        x: Edge variables dict
        n: Number of cities

    Returns:
        List of cities in tour order, starting and ending with 0
    """
    # Build adjacency from selected edges
    adj = {i: [] for i in range(n)}
    for (i, j), var in x.items():
        if model.getVal(var) > 0.5:
            adj[i].append(j)
            adj[j].append(i)

    # Trace tour starting from city 0
    tour = [0]
    prev = -1
    current = 0

    for _ in range(n - 1):
        for neighbor in adj[current]:
            if neighbor != prev:
                tour.append(neighbor)
                prev = current
                current = neighbor
                break

    tour.append(0)  # Return to start
    return tour


if __name__ == "__main__":
    from generator import random_euclidean_tsp

    # Solve a small instance
    n_cities = 10
    distances = random_euclidean_tsp(n_cities, seed=42)

    print(f"Solving {n_cities}-city TSP with row generation...")
    model, x = tsp_rowgen(distances)
    model.optimize()

    print(f"\nOptimal tour length: {model.getObjVal():.0f}")

    tour = extract_tour(model, x, n_cities)
    print(f"Tour: {' -> '.join(map(str, tour))}")
