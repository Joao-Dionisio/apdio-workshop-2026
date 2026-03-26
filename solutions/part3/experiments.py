"""Solution for Exercise 3.4: Computational Experiments."""

from time import time

from generator import random_bin_packing_instance
from compact import binpacking_compact
from bnp import extended_binpacking


def solve_compact(sizes, capacity, time_limit=300):
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
    """Compare compact formulation and branch-and-price across instance sizes."""

    sizes = [15, 25, 35, 50, 75, 100]
    capacity = 100
    seed = 42
    time_limit = 120

    results = []
    for n in sizes:
        items = random_bin_packing_instance(n, capacity, seed=seed)
        compact = solve_compact(items, capacity, time_limit)
        bnp = solve_bnp(items, capacity, time_limit)
        results.append((n, compact, bnp))

    header = (f"{'n':>5} | {'C time':>8} | {'C nodes':>8} | {'C LP':>8} | "
              f"{'BnP time':>8} | {'BnP nodes':>9} | {'BnP LP':>8} | {'Opt':>5}")
    print(header)
    print("-" * len(header))

    for n, compact, bnp in results:
        c_time = f"{compact['time']:.2f}s"
        c_nodes = str(compact["nodes"])
        c_lp = f"{compact['lp_bound']:.2f}"
        c_obj = compact["obj"]

        b_time = f"{bnp['time']:.2f}s"
        b_nodes = str(bnp["nodes"])
        b_lp = f"{bnp['lp_bound']:.2f}"
        b_obj = bnp["obj"]

        opt = f"{b_obj:.0f}" if b_obj is not None else (f"{c_obj:.0f}" if c_obj is not None else "---")

        if compact["status"] != "optimal":
            c_time = ">TL"
            opt_str = opt if b_obj is not None else "---"
        else:
            opt_str = opt

        if bnp["status"] != "optimal":
            b_time = ">TL"

        print(f"{n:>5} | {c_time:>8} | {c_nodes:>8} | {c_lp:>8} | "
              f"{b_time:>8} | {b_nodes:>9} | {b_lp:>8} | {opt_str:>5}")


if __name__ == "__main__":
    run_experiments()
