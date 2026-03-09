from ryan_foster import all_fractional_pairs

def test_fractional_pairs():
    patterns_with_vals = [
        ([0, 1, 2], 0.5),
        ([0], 0.5),
        ([1, 2], 0.5),
    ]

    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)

    assert len(pairs) == 2

    pairs = [set(pair) for pair in pairs]
    assert {0, 1} in pairs
    assert {0, 2} in pairs


def test_fractional_pairs2():
    patterns_with_vals = [
        ([0, 1, 2, 3], 0.5),
        ([0, 1], 0.5),
        ([2, 3], 0.5),
    ]

    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)

    assert len(pairs) == 4

    pairs = [set(pair) for pair in pairs]
    assert {0, 2} in pairs
    assert {0, 3} in pairs
    assert {1, 2} in pairs
    assert {1, 3} in pairs


def test_no_fractional_pairs():
    """All pair values are integer (0 or 1), so no fractional pairs."""
    patterns_with_vals = [
        ([0, 1], 1.0),
        ([2, 3], 1.0),
    ]
    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)
    assert len(pairs) == 0


def test_single_item_patterns():
    """Single-item patterns produce no pairs at all."""
    patterns_with_vals = [
        ([0], 0.5),
        ([1], 0.5),
        ([2], 0.5),
    ]
    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)
    assert len(pairs) == 0


def test_three_patterns_overlap():
    """Three patterns with overlapping items."""
    patterns_with_vals = [
        ([0, 1], 0.4),
        ([1, 2], 0.3),
        ([0, 2], 0.3),
    ]
    pairs = all_fractional_pairs(patterns_with_vals)
    print("Got pairs:", pairs)

    pairs = [set(pair) for pair in pairs]
    # pair (0,1): 0.4 + 0 + 0 = 0.4, fractional
    # pair (1,2): 0 + 0.3 + 0 = 0.3, fractional
    # pair (0,2): 0 + 0 + 0.3 = 0.3, fractional
    assert len(pairs) == 3
    assert {0, 1} in pairs
    assert {1, 2} in pairs
    assert {0, 2} in pairs


if __name__ == "__main__":
    test_fractional_pairs()
    test_fractional_pairs2()
    test_no_fractional_pairs()
    test_single_item_patterns()
    test_three_patterns_overlap()
    print("Fractional pairs test passed!")