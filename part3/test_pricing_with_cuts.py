"""
Test for pricing with subset row cuts.

Run from branch_and_price/:
    python test_pricing_with_cuts.py
"""
from pricing_knapsack import solve_knapsack_with_subset_row_cuts


def test_no_cuts_matches_base():
    """With empty cuts, should match solve_knapsack_with_constraints."""
    from pricing_knapsack import solve_knapsack_with_constraints

    sizes = [2, 3, 4, 5]
    values = [1, 2, 5, 6]
    capacity = 8
    together = {(0, 1)}
    apart = {(1, 3)}

    base = solve_knapsack_with_constraints(sizes, values, capacity, together, apart)
    with_cuts = solve_knapsack_with_subset_row_cuts(
        sizes, values, capacity, together, apart, subset_row_cuts=[])

    assert abs(base[0] - with_cuts[0]) < 1e-6, (
        f"Empty cuts should match base: {base[0]} vs {with_cuts[0]}")
    print("[92mPASS:[0m test_no_cuts_matches_base")


def test_cut_penalizes_pattern():
    """A subset row cut with negative dual should penalize 2+ item overlap."""
    sizes = [3, 3, 3, 5]
    values = [2.0, 2.0, 2.0, 3.0]
    capacity = 10

    # Without cuts: optimal = items {0,1,2} with value 6 (weight 9 <= 10)
    # or {0,1,3} with value 7 (weight 11 > 10), so {0,1,2} is best with all-in
    # Actually: {2,3} = value 5, weight 8; {0,1,2} = value 6, weight 9; {0,3} = value 5, weight 8
    # Best without cuts: {0,1,2} with value 6

    # With cut on (0,1,2) with dual -10: penalize selecting 2+ of {0,1,2}
    # {0,1,2}: z=1, obj = 6 + (-10) = -4 (terrible)
    # {0,3}: z=0 (only item 0 from triple), obj = 5
    # {3}: z=0, obj = 3
    cuts = [((0, 1, 2), -10.0)]
    obj, packing = solve_knapsack_with_subset_row_cuts(
        sizes, values, capacity, set(), set(), cuts)

    # With the heavy penalty, solver should avoid picking 2+ of {0,1,2}
    overlap = len(set(packing) & {0, 1, 2})
    assert overlap <= 1, f"Cut should discourage picking 2+ of {{0,1,2}}, got {packing}"
    print(f"[92mPASS:[0m test_cut_penalizes_pattern (packing={packing}, obj={obj})")


if __name__ == "__main__":
    test_no_cuts_matches_base()
    test_cut_penalizes_pattern()
    print("All pricing with cuts tests passed!")
