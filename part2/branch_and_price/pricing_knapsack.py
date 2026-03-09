from typing import List

from pyscipopt import Model


def pricing_solver(sizes: List[int], capacity: int, dual_solution: dict[int, float], together: set[tuple[int, int]],
                   apart: set[tuple[int, int]], subset_row_cuts=None) -> tuple[float, List[int]]:
    """
    Solve the pricing problem for the knapsack problem (with branching constraints)

    Parameters:
    sizes: List[int] - the sizes of the items
    capacity: int - the capacity of the knapsack
    dual_solution: dict[int, float] - the dual solution of the linear relaxation
    together: set[tuple[int, int]] - the pairs of items that must be together
    apart: set[tuple[int, int]] - the pairs of items that must be apart
    subset_row_cuts: list of (triple, dual_value) for active subset row cuts, or None

    Returns:
    tuple[float, List[int]] - the minimum reduced cost and the packing of the items
    """

    profits = [dual_solution[i] for i in range(len(sizes))]
    if subset_row_cuts:
        result = solve_knapsack_with_subset_row_cuts(
            sizes, profits, capacity, together, apart, subset_row_cuts)
    elif len(together) > 0 or len(apart) > 0:
        result = solve_knapsack_with_constraints(sizes, profits, capacity, together, apart)
    else:
        result = solve_knapsack(sizes, profits, capacity)

    min_red_cost = 1 - result[0]

    return min_red_cost, result[1]


def solve_knapsack(sizes: List[int], values: List[float], capacity: int) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    m = Model("knapsack")
    m.hideOutput()
    x = {}
    for i in range(len(sizes)):
        x[i] = m.addVar(vtype="B", name=f"x{i}", obj=values[i])

    m.addCons(sum(sizes[i] * x[i] for i in range(len(sizes))) <= capacity)

    m.setMaximize()
    m.optimize()

    packing = [i for i in range(len(sizes)) if m.getVal(x[i]) > 0.5]
    return m.getObjVal(), packing


def solve_knapsack_with_constraints(
        sizes: List[int], values: List[float], capacity: int, together: set[tuple[int, int]],
        apart: set[tuple[int, int]]
) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem with branching constraints

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack
    together: set[tuple[int, int]] - the pairs of items that must be together
    apart: set[tuple[int, int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """

    m = Model("knapsack_with_constraints")
    m.hideOutput()

    x = {}
    for i in range(len(sizes)):
        x[i] = m.addVar(vtype="B", name=f"x{i}", obj=values[i])

    m.addCons(sum(sizes[i] * x[i] for i in range(len(sizes))) <= capacity)

    for i, j in together:
        m.addCons(x[i] == x[j])

    for i, j in apart:
        m.addCons(x[i] + x[j] <= 1)

    m.setMaximize()

    m.optimize()

    packing = [i for i in range(len(sizes)) if m.getVal(x[i]) > 0.5]
    return m.getObjVal(), packing


def solve_knapsack_with_subset_row_cuts(
        sizes: List[int], values: List[float], capacity: int,
        together: set[tuple[int, int]], apart: set[tuple[int, int]],
        subset_row_cuts: list
) -> tuple[float, List[int]]:
    """
    Solve the knapsack pricing problem with branching + subset row cuts.

    This extends solve_knapsack_with_constraints to also handle
    subset row cut duals in the pricing problem.

    For each active subset row cut on triple S = {i, j, k} with dual μ_S:
    - Add binary variable z_S with objective coefficient μ_S
    - Add constraint: z_S >= x_i + x_j + x_k - 1
      (forces z_S = 1 when 2+ items from S are selected)

    Since μ_S <= 0, the solver naturally sets z_S = 0 when possible,
    penalizing patterns that cover 2+ items from any cut triple.

    Parameters:
    sizes: List[int] - item sizes
    values: List[float] - item profits (dual values)
    capacity: int - bin capacity
    together: set[tuple[int, int]] - pairs that must be together
    apart: set[tuple[int, int]] - pairs that must be apart
    subset_row_cuts: list of (triple, dual_value) for active subset row cuts

    Returns:
    tuple[float, List[int]] - optimal value and selected items
    """
    # =========================================================================
    # EXERCISE: Implement pricing with subset row cuts
    # =========================================================================
    #
    # Start from solve_knapsack_with_constraints and add:
    #
    # For each (triple, dual) in subset_row_cuts:
    #     i, j, k = triple
    #     z = m.addVar(vtype="B", obj=dual)          # penalty variable
    #     m.addCons(z >= x[i] + x[j] + x[k] - 1)    # active when 2+ selected
    #
    # The rest is identical to solve_knapsack_with_constraints.
    #
    # =========================================================================

    raise NotImplementedError(
        "BPC Exercise: Implement pricing with subset row cuts.\n"
        "Extend the knapsack to add a penalty variable z_S for each cut\n"
        "with constraint z_S >= x_i + x_j + x_k - 1."
    )