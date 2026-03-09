## Subset Row Inequalities for Branch-Price-and-Cut

This directory contains the separator exercise for integrating subset row cuts into the branch-and-price framework in `../../branch_and_price/`.

### Exercises

1. **Separator** (`subset_row.py`): Implement `sepaexeclp` to find violated subset row inequalities and add them as modifiable constraints.
2. **Pricing** (`../../branch_and_price/pricing_knapsack.py`): Implement `solve_knapsack_with_subset_row_cuts` to handle subset row cut duals in the knapsack pricing problem.

The pricer and B&P wiring (`pricer.py`, `bnp.py`) are already provided.

### Running the test

From the repo root:
```bash
python part2/separator/subset_row/test_subset_row.py
```

Or from `branch_and_price/`:
```bash
python test_bpc.py
```
