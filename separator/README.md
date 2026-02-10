## Separators

Separators generate cuts to strengthen the LP relaxation. The idea is to exclude fractional points that satisfy the LP relaxation but violate valid inequalities, tightening the bound and reducing the number of branch-and-bound nodes needed.

### Contents

- `subset_row/` — Subset-row inequalities for branch-price-and-cut (see [subset_row/README.md](subset_row/README.md))