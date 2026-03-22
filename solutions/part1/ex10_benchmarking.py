"""Solution for Exercise 10: Benchmarking Formulations."""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "part1", "ex09_indicators"))
from ex09_indicators import indicators  # noqa: E402


def generate_instance(n_generators, seed=42):
    rng = random.Random(seed)

    fixed_costs = [rng.randint(50, 200) for _ in range(n_generators)]
    var_costs = [rng.randint(5, 20) for _ in range(n_generators)]
    p_max = [rng.randint(100, 500) for _ in range(n_generators)]
    p_min = [rng.randint(20, p_max[i] // 2) for i in range(n_generators)]
    demand = int(0.6 * sum(p_max))

    return demand, fixed_costs, var_costs, p_min, p_max


def benchmark_formulation(build_fn, demand, fixed_costs, var_costs, p_min, p_max,
                          time_limit=60.0):
    model, y, p = build_fn(demand, fixed_costs, var_costs, p_min, p_max)
    model.hideOutput()
    model.setParam("limits/time", time_limit)
    model.optimize()

    objective = None
    if model.getNSols() > 0:
        objective = model.getObjVal()

    return {
        "status": model.getStatus(),
        "objective": objective,
        "time": model.getSolvingTime(),
        "n_nodes": model.getNNodes(),
        "gap": model.getGap(),
    }


def compare_formulations(sizes, seed=42, time_limit=60.0):
    from indicators import generator_scheduling_bigm, generator_scheduling_indicator

    results = []
    for size in sizes:
        demand, fixed_costs, var_costs, p_min, p_max = generate_instance(size, seed)
        bigm = benchmark_formulation(
            generator_scheduling_bigm,
            demand, fixed_costs, var_costs, p_min, p_max, time_limit
        )
        indicator = benchmark_formulation(
            generator_scheduling_indicator,
            demand, fixed_costs, var_costs, p_min, p_max, time_limit
        )
        results.append({"n": size, "bigm": bigm, "indicator": indicator})

    return results
