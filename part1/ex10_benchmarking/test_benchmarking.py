#!/usr/bin/env python3
"""
Tests for Exercise 12: Benchmarking formulations.

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
    print("PASS: test_generate_instance")


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
    print(f"PASS: test_benchmark_single (obj={stats['objective']:.1f}, "
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
    print("PASS: test_compare_small")


if __name__ == "__main__":
    print("Running benchmarking tests...\n")

    tests = [
        test_generate_instance,
        test_benchmark_single,
        test_compare_small,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"SKIP: {test.__name__} - Exercise not implemented yet")
            print(f"      {e}")
            failed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__}")
            traceback.print_exc()
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
