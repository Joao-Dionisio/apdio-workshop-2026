"""Solution for bin packing computational experiments."""

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
    sizes = [15, 25, 35, 50, 75, 100]
    capacity = 100
    seed = 42
    time_limit = 120

    results = []

    for n in sizes:
        print(f"Solving n={n}...", end=" ", flush=True)
        items = random_bin_packing_instance(n, capacity, seed=seed)

        compact = solve_compact(items, capacity, time_limit)
        bnp = solve_bnp(items, capacity, time_limit)
        results.append((n, compact, bnp))
        print("done")

    # Print table
    header = (
        f"{'n':>4} | {'Compact time':>13} {'Compact nodes':>14} {'Compact LP':>11} | "
        f"{'BnP time':>9} {'BnP nodes':>10} {'BnP LP':>7} | {'Opt':>4}"
    )
    print()
    print(header)
    print("-" * len(header))

    for n, compact, bnp in results:
        def fmt_time(r):
            if r["status"] == "optimal":
                return f"{r['time']:8.2f}s"
            return f">{time_limit:>5}s TL"

        ct = fmt_time(compact)
        cn = f"{compact['nodes']:>14}"
        cl = f"{compact['lp_bound']:11.2f}"

        bt = fmt_time(bnp)
        bn = f"{bnp['nodes']:>10}"
        bl = f"{bnp['lp_bound']:7.2f}"

        opt = f"{bnp['obj']:.0f}" if bnp["obj"] else "---"

        print(f"{n:>4} | {ct} {cn} {cl} | {bt} {bn} {bl} | {opt:>4}")


if __name__ == "__main__":
    run_experiments()
