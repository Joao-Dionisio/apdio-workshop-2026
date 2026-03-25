#!/usr/bin/env python3
"""
Tests for subtour detection (Exercise 1).

Run these tests to verify your find_subtours() implementation:
    python test_subtour.py

All tests should pass when Exercise 1 is correctly implemented.
"""

from subtour import find_subtours


def test_single_tour_square():
    """A valid 4-city tour should return no subtours."""
    # Square tour: 0 - 1 - 2 - 3 - 0
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    subtours = find_subtours(edges, 4)
    assert subtours == [], f"Expected no subtours for valid tour, got {subtours}"
    print("[92mPASS:[0m test_single_tour_square")


def test_single_tour_pentagon():
    """A valid 5-city tour should return no subtours."""
    # Pentagon tour: 0 - 1 - 2 - 3 - 4 - 0
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
    subtours = find_subtours(edges, 5)
    assert subtours == [], f"Expected no subtours for valid tour, got {subtours}"
    print("[92mPASS:[0m test_single_tour_pentagon")


def test_two_triangles():
    """Two disconnected triangles should return both as subtours."""
    # Triangle 1: 0 - 1 - 2 - 0
    # Triangle 2: 3 - 4 - 5 - 3
    edges = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    subtours = find_subtours(edges, 6)

    assert len(subtours) == 2, f"Expected 2 subtours, got {len(subtours)}"

    # Convert to sets for comparison
    subtour_sets = [frozenset(s) for s in subtours]
    assert frozenset({0, 1, 2}) in subtour_sets, "Missing subtour {0,1,2}"
    assert frozenset({3, 4, 5}) in subtour_sets, "Missing subtour {3,4,5}"
    print("[92mPASS:[0m test_two_triangles")


def test_three_components():
    """Three disconnected components should all be returned."""
    # Component 1: 0 - 1
    # Component 2: 2 - 3
    # Component 3: 4 - 5
    edges = [(0, 1), (2, 3), (4, 5)]
    subtours = find_subtours(edges, 6)

    assert len(subtours) == 3, f"Expected 3 subtours, got {len(subtours)}"

    subtour_sets = [frozenset(s) for s in subtours]
    assert frozenset({0, 1}) in subtour_sets
    assert frozenset({2, 3}) in subtour_sets
    assert frozenset({4, 5}) in subtour_sets
    print("[92mPASS:[0m test_three_components")


def test_isolated_node():
    """A graph with an isolated node has multiple components."""
    # Path through 0-1-2, node 3 is isolated
    edges = [(0, 1), (1, 2), (0, 2)]
    subtours = find_subtours(edges, 4)

    # Node 3 is isolated, so we have subtours
    assert len(subtours) >= 1, f"Expected subtours with isolated node, got {subtours}"

    # The connected component {0,1,2} and isolated {3} are both subtours
    all_nodes = set()
    for s in subtours:
        all_nodes.update(s)
    assert all_nodes == {0, 1, 2, 3}, f"All nodes should be in some subtour"
    print("[92mPASS:[0m test_isolated_node")


def test_empty_edges():
    """Empty edge list means all nodes are isolated components."""
    edges = []
    subtours = find_subtours(edges, 3)

    # All 3 nodes are isolated
    assert len(subtours) == 3, f"Expected 3 isolated subtours, got {len(subtours)}"
    print("[92mPASS:[0m test_empty_edges")


def test_edge_order_invariance():
    """Edge order (i,j) vs (j,i) shouldn't matter."""
    # Same tour with mixed edge directions
    edges1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
    edges2 = [(1, 0), (2, 1), (3, 2), (0, 3)]

    subtours1 = find_subtours(edges1, 4)
    subtours2 = find_subtours(edges2, 4)

    assert subtours1 == [], "edges1 should form valid tour"
    assert subtours2 == [], "edges2 should form valid tour"
    print("[92mPASS:[0m test_edge_order_invariance")


if __name__ == "__main__":
    print("Running subtour detection tests...\n")

    tests = [
        test_single_tour_square,
        test_single_tour_pentagon,
        test_two_triangles,
        test_three_components,
        test_isolated_node,
        test_empty_edges,
        test_edge_order_invariance,
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
            print(f"[91mFAIL:[0m {test.__name__}")
            if not hint:
                hint = str(e)
            failed += 1
        except Exception as e:
            print(f"[91mERROR:[0m {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    if hint:
        print(hint)
    print(f"Results: [92m{passed} passed[0m, [91m{failed} failed[0m")

    if failed == 0:
        print("All subtour detection tests passed!")
    elif failed == len(tests):
        print("\nHint: Implement find_subtours() in subtour.py to pass these tests.")
