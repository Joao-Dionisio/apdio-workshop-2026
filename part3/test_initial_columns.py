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
    print("PASS: test_correct_number")


def test_one_item_per_pattern():
    """Each pattern should contain exactly one item."""
    cols = initial_columns(4)
    for i, pat in enumerate(cols):
        assert len(pat) == 1, f"Pattern {i} has {len(pat)} items, expected 1"
    print("PASS: test_one_item_per_pattern")


def test_all_items_covered():
    """Every item should appear in exactly one pattern."""
    n = 6
    cols = initial_columns(n)
    covered = set()
    for pat in cols:
        for item in pat:
            covered.add(item)
    assert covered == set(range(n)), f"Expected items {{0..{n-1}}}, got {covered}"
    print("PASS: test_all_items_covered")


def test_single_item():
    """Edge case: single item."""
    cols = initial_columns(1)
    assert len(cols) == 1
    assert 0 in cols[0]
    print("PASS: test_single_item")


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
