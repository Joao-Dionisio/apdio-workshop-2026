#!/usr/bin/env python3
"""
Tests for Exercise 8: Graph coloring.

Run:
    python test_graph_coloring.py
"""

from graph_coloring import graph_coloring


def test_triangle():
    """A triangle (K3) needs exactly 3 colors."""
    n_nodes = 3
    edges = [(0, 1), (0, 2), (1, 2)]
    max_colors = 3

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert abs(model.getObjVal() - 3.0) < 1e-4, (
        f"Expected chromatic number 3, got {model.getObjVal()}"
    )
    print("PASS: test_triangle")


def test_bipartite():
    """A path on 4 nodes (bipartite) needs 2 colors."""
    n_nodes = 4
    edges = [(0, 1), (1, 2), (2, 3)]
    max_colors = 4

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert abs(model.getObjVal() - 2.0) < 1e-4, (
        f"Expected chromatic number 2, got {model.getObjVal()}"
    )
    print("PASS: test_bipartite")


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
    print("PASS: test_no_adjacent_share_color")


def test_petersen_graph():
    """The Petersen graph has chromatic number 3."""
    from generator import petersen_graph

    n_nodes, edges = petersen_graph()
    max_colors = n_nodes

    model, x, w = graph_coloring(n_nodes, edges, max_colors)
    model.hideOutput()
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert abs(model.getObjVal() - 3.0) < 1e-4, (
        f"Expected chromatic number 3 for Petersen graph, got {model.getObjVal()}"
    )
    print("PASS: test_petersen_graph")


if __name__ == "__main__":
    print("Running graph coloring tests...\n")

    tests = [
        test_triangle,
        test_bipartite,
        test_no_adjacent_share_color,
        test_petersen_graph,
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
            print(f"      {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
