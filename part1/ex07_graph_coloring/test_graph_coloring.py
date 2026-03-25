#!/usr/bin/env python3
"""
Tests for Exercise 7: Graph coloring.

Run:
    python test_graph_coloring.py
"""

import random
import traceback

from graph_coloring import graph_coloring


def random_graph_coloring_instance(n_nodes, edge_prob=0.3, seed=0):
    """
    Generate a random graph for coloring (Erdos-Renyi model).

    Args:
        n_nodes: Number of nodes.
        edge_prob: Probability that each edge exists.
        seed: Random seed for reproducibility.

    Returns:
        n_nodes: Number of nodes.
        edges: List of (i, j) tuples with i < j.
    """
    random.seed(seed)

    edges = []
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < edge_prob:
                edges.append((i, j))

    return n_nodes, edges


def petersen_graph():
    """
    Return the Petersen graph (10 nodes, 15 edges, chromatic number = 3).

    Returns:
        n_nodes: 10
        edges: List of 15 edges.
    """
    edges = [
        # Outer cycle
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
        # Inner pentagram
        (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
        # Spokes
        (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    ]
    return 10, edges


def test_triangle():
    """A triangle (K3) needs exactly 3 colors."""
    n_nodes = 3
    edges = [(0, 1), (0, 2), (1, 2)]
    max_colors = 3

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert abs(model.getObjVal() - 3.0) < 1e-4, (
        f"Expected chromatic number 3, got {model.getObjVal()}"
    )
    print("[92mPASS:[0m test_triangle")


def test_bipartite():
    """A path on 4 nodes (bipartite) needs 2 colors."""
    n_nodes = 4
    edges = [(0, 1), (1, 2), (2, 3)]
    max_colors = 4

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert abs(model.getObjVal() - 2.0) < 1e-4, (
        f"Expected chromatic number 2, got {model.getObjVal()}"
    )
    print("[92mPASS:[0m test_bipartite")


def test_no_adjacent_share_color():
    """No two adjacent nodes should share a color."""
    n_nodes = 5
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    max_colors = 5

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    # Extract coloring
    coloring = {}
    for v in range(n_nodes):
        for k in range(max_colors):
            if model.getVal(x[v, k]) > 0.5:
                coloring[v] = k
                break

    for u, v in edges:
        assert coloring[u] != coloring[v], (
            f"Adjacent nodes {u} and {v} both have color {coloring[u]}"
        )
    print("[92mPASS:[0m test_no_adjacent_share_color")


def test_petersen_graph():
    """The Petersen graph has chromatic number 3."""
    n_nodes, edges = petersen_graph()
    max_colors = n_nodes

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert abs(model.getObjVal() - 3.0) < 1e-4, (
        f"Expected chromatic number 3 for Petersen graph, got {model.getObjVal()}"
    )
    print("[92mPASS:[0m test_petersen_graph")


def test_complete_graph_k4():
    """K4 (complete graph on 4 nodes) needs exactly 4 colors."""
    n_nodes = 4
    edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    max_colors = 4

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert abs(model.getObjVal() - 4.0) < 1e-4, (
        f"Expected chromatic number 4 for K4, got {model.getObjVal()}"
    )
    print("[92mPASS:[0m test_complete_graph_k4")


def test_generated_sparse():
    """Solve a randomly generated sparse graph."""
    n_nodes, edges = random_graph_coloring_instance(8, edge_prob=0.3, seed=42)
    max_colors = n_nodes

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"

    # Verify no adjacent nodes share a color
    coloring = {}
    for v in range(n_nodes):
        for k in range(max_colors):
            if model.getVal(x[v, k]) > 0.5:
                coloring[v] = k
                break
    for u, v in edges:
        assert coloring[u] != coloring[v], (
            f"Adjacent nodes {u} and {v} both have color {coloring[u]}"
        )
    print("[92mPASS:[0m test_generated_sparse")


def test_generated_dense():
    """Solve a randomly generated dense graph."""
    n_nodes, edges = random_graph_coloring_instance(6, edge_prob=0.6, seed=99)
    max_colors = n_nodes

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert model.getObjVal() >= 1, "Should need at least 1 color"
    print("[92mPASS:[0m test_generated_dense")


if __name__ == "__main__":
    print("Running graph coloring tests...\n")

    tests = [
        test_triangle,
        test_bipartite,
        test_no_adjacent_share_color,
        test_petersen_graph,
        test_complete_graph_k4,
        test_generated_sparse,
        test_generated_dense,
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
