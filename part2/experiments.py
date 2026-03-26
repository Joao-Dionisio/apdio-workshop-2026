#!/usr/bin/env python3
"""
Computational experiments: MTZ vs Row Generation for TSP.

Compare both formulations on increasing instance sizes.

Run:  python experiments.py
"""

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen


def lp_bound(build_fn, distances):
    """Solve the LP relaxation and return the bound."""
    model, x = build_fn(distances)
    for v in model.getVars():
        if v.vtype() != 'CONTINUOUS':
            model.chgVarType(v, 'CONTINUOUS')
    model.hideOutput()
    model.optimize()
    return model.getObjVal()


def solve_and_collect(build_fn, distances, time_limit=30):
    """Solve a TSP instance and return statistics."""
    model, x = build_fn(distances)
    model.hideOutput()
    model.setParam("limits/time", time_limit)
    model.optimize()

    return {
        "obj": model.getObjVal() if model.getStatus() == "optimal" else None,
        "time": model.getSolvingTime(),
        "nodes": model.getNNodes(),
        "status": model.getStatus(),
    }


def run_experiments():
    """Compare MTZ and row generation across instance sizes."""
    sizes = [8, 10, 12, 15, 18, 20, 25, 30]
    seed = 42
    time_limit = 30

    results = []
    for n in sizes:
        print(f"Solving n={n}...", end=" ", flush=True)
        distances = random_euclidean_tsp(n, seed=seed)

        mtz_lp = lp_bound(tsp_mtz, distances)
        sec_lp = lp_bound(tsp_rowgen, distances)
        mtz = solve_and_collect(tsp_mtz, distances, time_limit)
        sec = solve_and_collect(tsp_rowgen, distances, time_limit)

        results.append({
            "n": n, "mtz": mtz, "sec": sec,
            "mtz_lp": mtz_lp, "sec_lp": sec_lp,
        })
        print("done")

    print()
    print_results(results)
    return results


def print_results(results):
    """Print experiment results as a formatted table."""
    row_fmt = "{:>4s} | {:>8s} {:>7s} {:>8s} | {:>8s} {:>7s} {:>8s} | {:>6s}"
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
        opt = sec.get("obj") or mtz.get("obj")
        opt_str = f"{opt:.0f}" if opt else "---"
        print(row_fmt.format(
            str(r["n"]),
            f"{mtz['time']:.2f}s", str(mtz["nodes"]),
            f"{r['mtz_lp']:.1f}",
            f"{sec['time']:.2f}s", str(sec["nodes"]),
            f"{r['sec_lp']:.1f}",
            opt_str,
        ))
    print(sep)


def plot_results(results):
    """Plot bar charts comparing MTZ vs Row Generation."""
    import matplotlib.pyplot as plt

    ns = [r["n"] for r in results]
    mtz_times = [r["mtz"]["time"] for r in results]
    sec_times = [r["sec"]["time"] for r in results]
    mtz_lps = [r["mtz_lp"] for r in results]
    sec_lps = [r["sec_lp"] for r in results]
    opts = [r["sec"].get("obj") or r["mtz"].get("obj") or 0 for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    x = range(len(ns))
    w = 0.35

    # Solving time
    ax = axes[0]
    ax.bar([i - w/2 for i in x], mtz_times, w, label='MTZ', color='#CC7700')
    ax.bar([i + w/2 for i in x], sec_times, w, label='Row Gen', color='#336699')
    ax.set_xticks(x)
    ax.set_xticklabels(ns)
    ax.set_xlabel('Cities')
    ax.set_ylabel('Time (s)')
    ax.set_title('Solving Time')
    ax.legend()

    # LP bound vs optimal
    ax = axes[1]
    ax.plot(x, opts, 'k--o', label='Optimal', markersize=5)
    ax.plot(x, mtz_lps, 's-', label='MTZ LP', color='#CC7700')
    ax.plot(x, sec_lps, 'D-', label='SEC LP', color='#336699')
    ax.set_xticks(x)
    ax.set_xticklabels(ns)
    ax.set_xlabel('Cities')
    ax.set_ylabel('Objective')
    ax.set_title('LP Relaxation Bound')
    ax.legend()

    # LP gap
    ax = axes[2]
    mtz_gaps = [100 * (o - lp) / o if o else 0 for o, lp in zip(opts, mtz_lps)]
    sec_gaps = [100 * (o - lp) / o if o else 0 for o, lp in zip(opts, sec_lps)]
    ax.bar([i - w/2 for i in x], mtz_gaps, w, label='MTZ', color='#CC7700')
    ax.bar([i + w/2 for i in x], sec_gaps, w, label='Row Gen', color='#336699')
    ax.set_xticks(x)
    ax.set_xticklabels(ns)
    ax.set_xlabel('Cities')
    ax.set_ylabel('LP Gap (%)')
    ax.set_title('LP Relaxation Gap')
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = run_experiments()
    try:
        plot_results(results)
    except ImportError:
        print("(install matplotlib to see plots)")
