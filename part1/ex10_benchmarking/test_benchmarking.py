#!/usr/bin/env python3
"""
Tests for Exercise 10: Benchmarking formulations.

Run:
    python test_benchmarking.py
"""

import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ex09_indicators"))

from benchmarking import (
    generate_instance,
    benchmark_formulation,
    compare_formulations,
)
from indicators import generator_scheduling_bigm


def test_generate_instance():
    """Instance generator produces valid data."""
    demand, fc, vc, pmin, pmax = generate_instance(20, seed=0)
    assert len(fc) == 20
    assert len(vc) == 20
    assert all(pmin[i] <= pmax[i] for i in range(20))
    assert demand > 0
    print("[92mPASS:[0m test_generate_instance")


def test_benchmark_single():
    """benchmark_formulation returns correct keys."""
    demand, fc, vc, pmin, pmax = generate_instance(10, seed=1)
    stats = benchmark_formulation(
        generator_scheduling_bigm, demand, fc, vc, pmin, pmax, time_limit=30.0
    )
    assert isinstance(stats, dict)
    for key in ["status", "objective", "time", "n_nodes", "gap"]:
        assert key in stats, f"Missing key: {key}"
    assert stats["status"] in ("optimal", "timelimit")
    assert stats["time"] >= 0
    assert stats["n_nodes"] >= 0
    print(f"[92mPASS:[0m test_benchmark_single (obj={stats['objective']:.1f}, "
          f"time={stats['time']:.2f}s, nodes={stats['n_nodes']})")


def test_compare_small():
    """compare_formulations runs on small instances."""
    results = compare_formulations([5, 10], seed=42, time_limit=30.0)
    assert len(results) == 2
    for r in results:
        assert "n" in r
        assert "bigm" in r
        assert "indicator" in r
        assert r["bigm"]["status"] in ("optimal", "timelimit")
        assert r["indicator"]["status"] in ("optimal", "timelimit")
    print("[92mPASS:[0m test_compare_small")


if __name__ == "__main__":
    print("Running benchmarking tests...\n")

    tests = [
        test_generate_instance,
        test_benchmark_single,
        test_compare_small,
    ]

    passed = 0
    failed = 0
    hint = ""

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"[93mSKIP:[0m {test.__name__} - Exercise not implemented yet")
            if not hint:
                hint = str(e)
            failed += 1
        except AssertionError as e:
            print(f"[91mFAIL:[0m {test.__name__} - {e}")
            failed += 1
        except Exception as e:
            print(f"[91mERROR:[0m {test.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    if hint:
        print(hint)
    print(f"Results: [92m{passed} passed[0m, [91m{failed} failed[0m")
