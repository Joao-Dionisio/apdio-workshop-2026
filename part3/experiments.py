#!/usr/bin/env python3
"""
Computational experiments: Compact vs Branch-and-Price for Bin Packing.

Exercise: Run both formulations on increasing instance sizes and compare
solving time, number of branch-and-bound nodes, and LP relaxation bound.

Fill in the missing code below, then run:
    python experiments.py

You should observe that:
- The compact formulation suffers from symmetry and scales poorly
- Branch-and-price has a much tighter LP relaxation
- The compact LP bound is often far from the integer optimum
- Branch-and-price explores far fewer nodes
"""

from time import time

from generator import random_bin_packing_instance
from compact import binpacking_compact
from bnp import extended_binpacking


def solve_compact(sizes, capacity, time_limit=300):
    """
    Solve bin packing with the compact formulation and collect statistics.

    Args:
        sizes: List of item sizes
        capacity: Bin capacity
        time_limit: Time limit in seconds

    Returns:
        dict with keys: obj, time, nodes, lp_bound, status
    """
    model = binpacking_compact(sizes, capacity)
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


def solve_bnp(sizes, capacity, time_limit=300):
    """
    Solve bin packing with branch-and-price and collect statistics.

    Args:
        sizes: List of item sizes
        capacity: Bin capacity
        time_limit: Time limit in seconds

    Returns:
        dict with keys: obj, time, nodes, lp_bound, status
    """
    model, *_ = extended_binpacking(sizes, capacity)
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
    Compare compact formulation and branch-and-price across instance sizes.

    TODO: Complete this function.

    For each instance size in `sizes`, generate a random bin packing instance
    and solve it with both formulations. Collect and print:
    - Solving time
    - Number of B&B nodes
    - LP relaxation bound (dual bound)
    - Optimal objective value

    Print a formatted table at the end.
    """
    sizes = [15, 25, 35, 50, 75, 100]
    capacity = 100
    seed = 42
    time_limit = 120

    # =========================================================================
    # EXERCISE: Run computational experiments
    # =========================================================================
    #
    # For each n in sizes:
    #   1. Generate an instance:
    #      items = random_bin_packing_instance(n, capacity, seed=seed)
    #   2. Solve with compact: solve_compact(items, capacity, time_limit)
    #   3. Solve with BnP:     solve_bnp(items, capacity, time_limit)
    #   4. Store the results
    #
    # Then print a comparison table with columns:
    #   n | Compact time | Compact nodes | BnP time | BnP nodes |
    #       Compact LP | BnP LP | Opt
    #
    # Hints:
    #   - Use f-strings with alignment for clean formatting
    #   - Handle the case where a solver hits the time limit (status != "optimal")
    #   - Compare LP bounds: the compact LP bound is typically much weaker
    #   - For large n, the compact formulation may time out
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise: Implement the experiment loop and print a comparison table.\n"
        "Compare compact vs branch-and-price on instances of increasing size."
    )


if __name__ == "__main__":
    run_experiments()
