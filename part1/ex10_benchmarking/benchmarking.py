"""
Benchmarking formulations.

Generate random generator scheduling instances and compare big-M vs indicators.
"""

import os
import random
from pyscipopt import Model


def generate_instance(n_generators, seed=42):
    """Generate a random generator scheduling instance.

    Returns:
        (demand, fixed_costs, var_costs, p_min, p_max)

    Use random.Random(seed). Per generator:
        fixed_costs: [50, 200], var_costs: [5, 20],
        p_max: [100, 500], p_min: [20, p_max//2]
    demand = int(0.6 * sum(p_max))
    """
    # EXERCISE 10a: Generate a random instance

    raise NotImplementedError("Exercise 10a: Implement generate_instance.")


def benchmark_formulation(build_fn, demand, fixed_costs, var_costs, p_min, p_max,
                          time_limit=60.0):
    """Solve a formulation and return statistics.

    Returns:
        dict with keys: objective, time, n_nodes, gap, status
    """
    # EXERCISE 10b: Build, set time limit, solve, collect stats

    raise NotImplementedError("Exercise 10b: Implement benchmark_formulation.")


def compare_formulations(sizes, seed=42, time_limit=60.0):
    """Compare big-M vs indicator on instances of increasing size.

    Returns:
        list of dicts: {"n": size, "bigm": stats, "indicator": stats}
    """
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ex09_indicators"))
    from indicators import generator_scheduling_bigm, generator_scheduling_indicator

    # EXERCISE 10c: Loop over sizes, generate instances, benchmark both

    raise NotImplementedError("Exercise 10c: Implement compare_formulations.")


def print_results(results):
    """Print benchmark results as a formatted table."""
    row_fmt = "{:>5s} | {:>10s} {:>7s} {:>7s} | {:>10s} {:>7s} {:>7s} | {:>7s}"
    header = row_fmt.format("n", "Big-M time", "nodes", "gap",
                            "Indic time", "nodes", "gap", "speedup")
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in results:
        bm = r["bigm"]
        ind = r["indicator"]
        speedup = bm["time"] / ind["time"] if ind["time"] > 0.01 else float("inf")
        print(row_fmt.format(
            str(r["n"]),
            f"{bm['time']:.2f}s", str(bm["n_nodes"]), f"{bm['gap']:.2%}",
            f"{ind['time']:.2f}s", str(ind["n_nodes"]), f"{ind['gap']:.2%}",
            f"{speedup:.1f}x",
        ))
    print(sep)


if __name__ == "__main__":
    try:
        results = compare_formulations([10, 20, 50, 100, 200])
        print_results(results)
    except NotImplementedError as e:
        print(f"Not implemented: {e}")
