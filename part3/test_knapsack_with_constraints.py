from pricing_knapsack import solve_knapsack_with_constraints


def test_knapsack_with_constraints():
    sizes = [2, 3, 4, 5]
    values = [1, 2, 5, 6]
    capacity = 8
    together = {(0, 1)}
    apart = {(1, 3)}
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 6
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {3}


def test_knapsack_with_constraints2():
    sizes = [1, 2]
    values = [1, 2]
    capacity = 1
    together = {(0, 1)}
    apart = set()
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 0
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == set()


def test_knapsack_with_constraints3():
    sizes = [1, 2]
    values = [1, 2]
    capacity = 3
    together = set()
    apart = {(0, 1)}
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    expected_value = 2
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {1}


def test_together_forces_both():
    """Together constraint forces both items or neither."""
    sizes = [3, 4, 2]
    values = [5, 6, 3]
    capacity = 7
    # Together (0,1) means both must be packed or neither; size 3+4=7 fits exactly
    together = {(0, 1)}
    apart = set()
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    selected = set(result[1])
    # Either both 0,1 are in (value 11, weight 7) or neither
    if 0 in selected or 1 in selected:
        assert 0 in selected and 1 in selected, "Together items must both be selected"
    assert abs(result[0] - 11) < 1e-6


def test_apart_allows_one():
    """Apart constraint: can pick one but not both."""
    sizes = [2, 2, 5]
    values = [10, 10, 1]
    capacity = 4
    together = set()
    apart = {(0, 1)}
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    selected = set(result[1])
    # Can pick at most one of {0, 1}
    assert not ({0, 1} <= selected), "Apart items cannot both be selected"
    assert abs(result[0] - 10) < 1e-6


def test_multiple_constraints():
    """Multiple together and apart constraints simultaneously."""
    sizes = [1, 1, 1, 1]
    values = [4, 3, 2, 1]
    capacity = 3
    together = {(0, 1)}  # items 0 and 1 must go together
    apart = {(2, 3)}     # items 2 and 3 must be apart
    result = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    print("Got result:", result)

    selected = set(result[1])
    if 0 in selected or 1 in selected:
        assert 0 in selected and 1 in selected
    assert not ({2, 3} <= selected)
    # Best: {0,1,2} value=9 or {0,1,3} value=8
    assert abs(result[0] - 9) < 1e-6


if __name__ == "__main__":
    test_knapsack_with_constraints()
    test_knapsack_with_constraints2()
    test_knapsack_with_constraints3()
    test_together_forces_both()
    test_apart_allows_one()
    test_multiple_constraints()
    print("knapsack with constraints test passed!")