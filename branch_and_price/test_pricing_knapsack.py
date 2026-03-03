from pricing_knapsack import solve_knapsack, solve_knapsack_with_constraints

def test_solve_knapsack():
    sizes = [2, 3, 4, 5]
    values = [1, 2, 5, 6]
    capacity = 8
    result = solve_knapsack(sizes, values, capacity)
    print("Got result:", result)

    expected_value = 8
    assert abs(result[0] - expected_value) < 1e-6
    assert set(result[1]) == {1, 3}

    capacity = 0
    result = solve_knapsack(sizes, values, capacity)
    assert abs(result[0] - 0) < 1e-6


def test_single_item_fits():
    """Single item that fits in the knapsack."""
    sizes = [5]
    values = [10]
    capacity = 5
    result = solve_knapsack(sizes, values, capacity)
    assert abs(result[0] - 10) < 1e-6
    assert set(result[1]) == {0}


def test_all_items_fit():
    """All items fit in the knapsack."""
    sizes = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 10
    result = solve_knapsack(sizes, values, capacity)
    assert abs(result[0] - 15) < 1e-6
    assert set(result[1]) == {0, 1, 2}


def test_no_items_fit():
    """No items fit (all too heavy)."""
    sizes = [10, 20, 30]
    values = [5, 10, 15]
    capacity = 5
    result = solve_knapsack(sizes, values, capacity)
    assert abs(result[0] - 0) < 1e-6
    assert set(result[1]) == set()


def test_equal_ratios():
    """Items with equal value-to-weight ratios."""
    sizes = [3, 6, 9]
    values = [3, 6, 9]
    capacity = 12
    result = solve_knapsack(sizes, values, capacity)
    # Optimal: items 0+2 (size=12, value=12) or 1+0 (size=9, value=9)
    assert abs(result[0] - 12) < 1e-6
    assert sum(sizes[i] for i in result[1]) <= capacity


if __name__ == "__main__":
    test_solve_knapsack()
    test_single_item_fits()
    test_all_items_fit()
    test_no_items_fit()
    test_equal_ratios()
    print("knapsack test passed!")
