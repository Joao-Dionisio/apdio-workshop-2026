"""Solution for Exercises 1, 4, 6: Knapsack Pricing."""

from typing import List

from pyscipopt import Model


def pricing_solver(sizes: List[int], capacity: int, dual_solution: dict[int, float], together: set[tuple[int, int]],
                   apart: set[tuple[int, int]], subset_row_cuts=None) -> tuple[float, List[int]]:
    """
    Solve the pricing problem (knapsack with branching constraints).

    Returns:
        (min_reduced_cost, packing)
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
    """Solve the basic knapsack problem. Returns (optimal_value, packing)."""

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
    """Solve knapsack with branching constraints.

    Together: x[i] == x[j].  Apart: x[i] + x[j] <= 1.
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
    """Solve knapsack pricing with branching + subset row cuts.

    For each (triple, dual) in subset_row_cuts:
        z = addVar(vtype="B", obj=dual)
        addCons(z >= x[i] + x[j] + x[k] - 1)
    """

    m = Model("knapsack_with_cuts")
    m.hideOutput()

    x = {}
    for i in range(len(sizes)):
        x[i] = m.addVar(vtype="B", name=f"x{i}", obj=values[i])

    m.addCons(sum(sizes[i] * x[i] for i in range(len(sizes))) <= capacity)

    for i, j in together:
        m.addCons(x[i] == x[j])

    for i, j in apart:
        m.addCons(x[i] + x[j] <= 1)

    for triple, dual in subset_row_cuts:
        i, j, k = triple
        z = m.addVar(vtype="B", obj=dual)
        m.addCons(z >= x[i] + x[j] + x[k] - 1)

    m.setMaximize()
    m.optimize()

    packing = [i for i in range(len(sizes)) if m.getVal(x[i]) > 0.5]
    return m.getObjVal(), packing
