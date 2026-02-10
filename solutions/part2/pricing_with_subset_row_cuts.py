"""Solution for BPC Exercise: Pricing with subset row cuts."""

from typing import List
from pyscipopt import Model


def solve_knapsack_with_subset_row_cuts(
        sizes: List[int], values: List[float], capacity: int,
        together: set[tuple[int, int]], apart: set[tuple[int, int]],
        subset_row_cuts: list
) -> tuple[float, List[int]]:

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
