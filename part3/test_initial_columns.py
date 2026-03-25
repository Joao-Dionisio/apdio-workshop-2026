#!/usr/bin/env python3
"""
Tests for Exercise 0: Initial Columns.

Run:
    python test_initial_columns.py
"""

from initial_columns import initial_columns


def test_correct_number():
    """Should produce one pattern per item."""
    cols = initial_columns(5)
    assert len(cols) == 5, f"Expected 5 patterns, got {len(cols)}"
    print("[92mPASS:[0m test_correct_number")


def test_one_item_per_pattern():
    """Each pattern should contain exactly one item."""
    cols = initial_columns(4)
    for i, pat in enumerate(cols):
        assert len(pat) == 1, f"Pattern {i} has {len(pat)} items, expected 1"
    print("[92mPASS:[0m test_one_item_per_pattern")


def test_all_items_covered():
    """Every item should appear in exactly one pattern."""
    n = 6
    cols = initial_columns(n)
    covered = set()
    for pat in cols:
        for item in pat:
            covered.add(item)
    assert covered == set(range(n)), f"Expected items {{0..{n-1}}}, got {covered}"
    print("[92mPASS:[0m test_all_items_covered")


def test_single_item():
    """Edge case: single item."""
    cols = initial_columns(1)
    assert len(cols) == 1
    assert 0 in cols[0]
    print("[92mPASS:[0m test_single_item")


if __name__ == "__main__":
    print("Running initial columns tests...\n")

    tests = [
        test_correct_number,
        test_one_item_per_pattern,
        test_all_items_covered,
        test_single_item,
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
