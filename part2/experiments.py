#!/usr/bin/env python3
"""
Computational experiments: MTZ vs Row Generation for TSP.

Exercise 3: Run both formulations on increasing instance sizes and compare
solving time, number of branch-and-bound nodes, and LP relaxation bound.

Fill in the missing code below, then run:
    python experiments.py

You should observe that:
- MTZ is faster to build but has a weaker LP relaxation
- Row generation has a tighter LP bound and explores fewer nodes
- The gap widens as instance size grows
"""

from time import time

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen


def solve_and_collect(build_fn, distances, time_limit=300):
    """
    Solve a TSP instance and collect statistics.

    Args:
        build_fn: Function that takes distances and returns (model, x)
        distances: Distance matrix
        time_limit: Time limit in seconds (default: 300)

    Returns:
        dict with keys: obj, time, nodes, lp_bound, status
    """
    model, x = build_fn(distances)
    model.hideOutput()
    model.setParam("limits/time", time_limit)

    start = time()
    model.optimize()
    wall_time = time() - start

    return {
        "obj": model.getObjVal() if model.getStatus() == "optimal" else None,
        "time": wall_time,
        "nodes": model.getNNodes(),
        "lp_bound": model.getDualbound(),
        "status": model.getStatus(),
    }


def run_experiments():
    """
    Compare MTZ and row generation across different instance sizes.

    TODO: Complete this function.

    For each instance size in `sizes`, generate a random TSP instance
    and solve it with both formulations. Collect and print:
    - Solving time
    - Number of B&B nodes
    - LP relaxation bound (dual bound)
    - Optimal objective value

    Print a formatted table at the end.
    """
    sizes = [8, 10, 12, 15, 18, 20]
    seed = 42
    time_limit = 120

    # =========================================================================
    # EXERCISE 3: Run computational experiments
    # =========================================================================
    #
    # For each n in sizes:
    #   1. Generate an instance with random_euclidean_tsp(n, seed=seed)
    #   2. Solve with MTZ:   solve_and_collect(tsp_mtz, distances, time_limit)
    #   3. Solve with SEC:   solve_and_collect(tsp_rowgen, distances, time_limit)
    #   4. Store the results
    #
    # Then print a comparison table with columns:
    #   n | MTZ time | MTZ nodes | SEC time | SEC nodes | MTZ LP | SEC LP | Opt
    #
    # Hints:
    #   - Use f-strings with alignment for clean formatting
    #   - Handle the case where a solver hits the time limit (status != "optimal")
    #   - The LP bound (dual bound) reveals the strength of each relaxation
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3: Implement the experiment loop and print a comparison table.\n"
        "Compare MTZ vs SEC on instances of increasing size."
    )


if __name__ == "__main__":
    run_experiments()
