# APDIO Workshop 2026 — Optimization Software & Practice

A hands-on workshop for learning mathematical optimization with [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), the Python interface to the [SCIP](https://www.scipopt.org/) solver.

## Setup

```bash
python -m pip install pyscipopt
```

On some Linux distributions (e.g. Debian/Ubuntu), installing packages globally with `pip` is restricted. If you get an `externally-managed-environment` error, create a virtual environment first. This is probably not required for most users (Windows/macOS).

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install pyscipopt
```

Verify installation:

```python
from pyscipopt import Model
m = Model()
m.optimize()
print("PySCIPOpt is ready!")
```

## Structure

The workshop is divided into two parts:

### Part 1: Modeling Basics

Learn to formulate and solve optimization problems using PySCIPOpt. Covers LPs, IPs, and MIPs through eight progressively complex exercises:

1. **First Model** — build a small binary IP
2. **Solving** — optimize and inspect solutions
3. **Transportation** — LP with supply/demand constraints
4. **Portfolio Optimization** — QP with quadratic objective
5. **Set Cover** — first IP with binary variables
6. **Knapsack** — classic 0-1 knapsack
7. **Facility Location** — MIP with linking constraints
8. **Graph Coloring** — IP with symmetry

All exercises are in `part1/`. Each has a stub file (with `NotImplementedError`), a test, and (for exercises 3–8) a random instance generator.

```bash
cd part1
python -m pytest  # all tests SKIP until exercises are implemented
```

### Part 2: Advanced Techniques

Covers row generation, column generation, branch-and-price, and branch-price-and-cut using the TSP and bin packing problems:

| Topic | Exercises in |
|-------|-------------|
| TSP compact formulation | `part2/row_generation/` |
| Subtour elimination & constraint handlers | `part2/row_generation/` |
| Bin packing column generation | `part2/branch_and_price/` |
| Ryan-Foster branching | `part2/branch_and_price/` |
| Branch-price-and-cut | `part2/branch_and_price/` |

The Part 2 README and slides provide the narrative arc connecting these exercises.

## Running Tests

```bash
# Part 1 (all in part1/)
cd part1
python ex01_first_model/test_first_model.py
python ex02_solving/test_solving.py
python ex03_transportation/test_transportation.py
python ex04_portfolio/test_portfolio.py
python ex05_set_cover/test_set_cover.py
python ex06_knapsack/test_knapsack.py
python ex07_facility_location/test_facility_location.py
python ex08_graph_coloring/test_graph_coloring.py

# Part 2 (exercises in existing directories)
cd part2/row_generation && python test_subtour.py
cd part2/branch_and_price && python test_pricing_knapsack.py
cd part2/branch_and_price && python test_bpc.py
```

