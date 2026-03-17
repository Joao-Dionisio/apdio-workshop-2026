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

    results = []
    for n in sizes:
        print(f"Solving n={n}...", end=" ", flush=True)
        distances = random_euclidean_tsp(n, seed=seed)
        mtz = solve_and_collect(tsp_mtz, distances, time_limit)
        sec = solve_and_collect(tsp_rowgen, distances, time_limit)
        results.append({"n": n, "mtz": mtz, "sec": sec})
        print("done")

    print()
    print_results(results)


def print_results(results):
    """Print experiment results as a formatted table."""
    row_fmt = "{:>4s} | {:>9s} {:>7s} {:>8s} | {:>9s} {:>7s} {:>8s} | {:>6s}"
    header = row_fmt.format(
        "n", "MTZ time", "nodes", "LP bound",
        "SEC time", "nodes", "LP bound", "opt",
    )
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in results:
        mtz, sec = r["mtz"], r["sec"]
        opt = f"{sec['obj']:.0f}" if sec["obj"] is not None else "---"
        print(row_fmt.format(
            str(r["n"]),
            f"{mtz['time']:.2f}s", str(mtz["nodes"]),
            f"{mtz['lp_bound']:.1f}",
            f"{sec['time']:.2f}s", str(sec["nodes"]),
            f"{sec['lp_bound']:.1f}",
            opt,
        ))
    print(sep)


if __name__ == "__main__":
    run_experiments()
