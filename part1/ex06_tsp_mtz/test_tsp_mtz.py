#!/usr/bin/env python3
"""
Tests for Exercise 8: TSP compact MTZ formulation.

Run:
    python test_tsp_mtz.py
"""

import math
import random
import traceback

from tsp_mtz import tsp_mtz


def random_euclidean_tsp(n_cities, seed=None, grid_size=100):
    """
    Generate a random Euclidean TSP instance with integer distances.

    Args:
        n_cities: Number of cities
        seed: Random seed for reproducibility
        grid_size: Cities are placed in [0, grid_size] x [0, grid_size]

    Returns:
        distances: n x n symmetric distance matrix (list of lists)
    """
    if seed is not None:
        random.seed(seed)

    # Generate random coordinates
    coords = [(random.uniform(0, grid_size), random.uniform(0, grid_size))
              for _ in range(n_cities)]

    n = len(coords)
    distances = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist = int(round(math.sqrt(dx * dx + dy * dy)))
            distances[i][j] = dist
            distances[j][i] = dist

    return distances


def test_small_instance():
    """Solve a 5-city instance and verify it's a valid tour."""
    distances = random_euclidean_tsp(5, seed=42)
    model, x = tsp_mtz(distances)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal"
    n = len(distances)

    # Check that exactly n edges are selected
    selected = [(i, j) for (i, j), var in x.items() if model.getVal(var) > 0.5]
    assert len(selected) == n, f"Expected {n} edges, got {len(selected)}"

    # Check that each city is visited exactly once
    out_degree = [0] * n
    in_degree = [0] * n
    for i, j in selected:
        out_degree[i] += 1
        in_degree[j] += 1
    assert all(d == 1 for d in out_degree), "Not every city is left exactly once"
    assert all(d == 1 for d in in_degree), "Not every city is entered exactly once"

    # Check connectivity (single tour, no subtours)
    next_city = {i: j for i, j in selected}
    visited = set()
    current = 0
    while current not in visited:
        visited.add(current)
        current = next_city[current]
    assert len(visited) == n, f"Tour visits {len(visited)} cities, expected {n}"

    print(f"PASS: test_small_instance (obj={model.getObjVal():.0f})")


def test_10_cities():
    """Solve a 10-city instance."""
    distances = random_euclidean_tsp(10, seed=7)
    model, x = tsp_mtz(distances)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal"
    print(f"PASS: test_10_cities (obj={model.getObjVal():.0f}, "
          f"nodes={model.getNNodes()}, time={model.getSolvingTime():.2f}s)")


if __name__ == "__main__":
    print("Running TSP MTZ tests...\n")

    tests = [test_small_instance, test_10_cities]
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
