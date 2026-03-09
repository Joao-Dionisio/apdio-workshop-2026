"""Solution for Exercise 3: TSP computational experiments."""

from time import time

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen


def solve_and_collect(build_fn, distances, time_limit=300):
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
    sizes = [8, 10, 12, 15, 18, 20]
    seed = 42
    time_limit = 120

    results = []

    for n in sizes:
        print(f"Solving n={n}...", end=" ", flush=True)
        distances = random_euclidean_tsp(n, seed=seed)

        mtz = solve_and_collect(tsp_mtz, distances, time_limit)
        sec = solve_and_collect(tsp_rowgen, distances, time_limit)
        results.append((n, mtz, sec))
        print("done")

    # Print table
    header = f"{'n':>4} | {'MTZ time':>9} {'MTZ nodes':>10} {'MTZ LP':>8} | {'SEC time':>9} {'SEC nodes':>10} {'SEC LP':>8} | {'Opt':>6}"
    print()
    print(header)
    print("-" * len(header))

    for n, mtz, sec in results:
        def fmt(r):
            t = f"{r['time']:8.2f}s"
            nd = f"{r['nodes']:>10}"
            lp = f"{r['lp_bound']:8.1f}"
            return t, nd, lp

        mt, mn, ml = fmt(mtz)
        st, sn, sl = fmt(sec)
        opt = f"{mtz['obj']:.0f}" if mtz["obj"] else "---"

        print(f"{n:>4} | {mt} {mn} {ml} | {st} {sn} {sl} | {opt:>6}")


if __name__ == "__main__":
    run_experiments()
