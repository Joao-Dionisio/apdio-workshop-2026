"""
Benchmarking formulations.

Exercise 10: Generate random generator scheduling instances of increasing size
and compare big-M vs indicator formulations.
"""

import os
import random
from pyscipopt import Model


def generate_instance(n_generators, seed=42):
    """Generate a random generator scheduling instance.

    Args:
        n_generators: number of generators.
        seed: random seed for reproducibility.

    Returns:
        (demand, fixed_costs, var_costs, p_min, p_max) where:
            demand:      int — total demand (~60% of total capacity)
            fixed_costs: list of length n_generators — startup cost per generator
            var_costs:   list of length n_generators — per-MW cost per generator
            p_min:       list of length n_generators — minimum output if on
            p_max:       list of length n_generators — maximum output
    """
    # =========================================================================
    # EXERCISE 10a: Generate a random instance
    # =========================================================================
    #
    # Use random.Random(seed) for reproducibility.
    #
    # For each generator i:
    #   fixed_costs[i] — random int in [50, 200]
    #   var_costs[i]   — random int in [5, 20]
    #   p_max[i]       — random int in [100, 500]
    #   p_min[i]       — random int in [20, p_max[i] // 2]
    #
    # demand = int(0.6 * sum(p_max))
    #
    # Return (demand, fixed_costs, var_costs, p_min, p_max)
    #
    # =========================================================================

    raise NotImplementedError("Exercise 10a: Implement generate_instance.")


def benchmark_formulation(build_fn, demand, fixed_costs, var_costs, p_min, p_max,
                          time_limit=60.0):
    """Solve a formulation and return statistics.

    Args:
        build_fn: function(demand, fixed_costs, var_costs, p_min, p_max)
                  that returns (model, y, p)
        time_limit: maximum solving time in seconds

    Returns:
        dict with keys: objective, time, n_nodes, gap, status
    """
    # =========================================================================
    # EXERCISE: Build the model, set a time limit, solve, and collect stats.
    #
    # Steps:
    #   1. Call build_fn to get model, y, p
    #   2. Suppress output with model.hideOutput()
    #   3. Set the time limit: model.setParam("limits/time", time_limit)
    #   4. Solve with model.optimize()
    #   5. Return a dict with:
    #      - "status":    model.getStatus()
    #      - "objective":  model.getObjVal() if status is "optimal" or
    #                      "timelimit", else None
    #      - "time":      model.getSolvingTime()
    #      - "n_nodes":   model.getNNodes()
    #      - "gap":       model.getGap()
    # =========================================================================

    raise NotImplementedError("Exercise 10b: Implement benchmark_formulation.")


def compare_formulations(sizes, seed=42, time_limit=60.0):
    """Compare big-M vs indicator on instances of increasing size.

    Args:
        sizes: list of ints (number of generators per instance)
        seed: random seed for reproducibility
        time_limit: per-instance time limit

    Returns:
        list of dicts, each with keys: n, bigm (stats dict), indicator (stats dict)
    """
    # Import the formulations from Exercise 9
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ex09_indicators"))
    from indicators import generator_scheduling_bigm, generator_scheduling_indicator

    # =========================================================================
    # EXERCISE 10b: For each size in sizes:
    #   1. Generate an instance with generate_instance(size, seed)
    #   2. Benchmark both formulations using benchmark_formulation()
    #   3. Collect results as a list of dicts:
    #      {"n": size, "bigm": stats_dict, "indicator": stats_dict}
    #   4. Call print_results(results) to display the comparison table
    #      (already implemented below — just call it!)
    #
    # Return the results list.
    # =========================================================================

    raise NotImplementedError("Exercise 10b: Implement compare_formulations.")


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
