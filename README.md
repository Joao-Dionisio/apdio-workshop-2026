# APDIO Workshop 2026 — Optimization Software & Practice

A hands-on workshop for learning mathematical optimization with [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), the Python interface to the [SCIP](https://www.scipopt.org/) solver.

## Setup

```bash
python -m pip install -r requirements.txt
```

On some Linux distributions (e.g. Debian/Ubuntu), installing packages globally with `pip` is restricted. If you get an `externally-managed-environment` error, create a virtual environment first. This is probably not required for most users (Windows/macOS).

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Verify installation:

```python
from pyscipopt import Model
m = Model()
m.optimize()
print("PySCIPOpt is ready!")
```

## Structure

The workshop is divided into three parts:

### Part 1: Modeling

Build and solve MINLPs in PySCIPOpt through twelve progressively complex exercises:

1. **First Model** — build a small binary IP
2. **Solving** — optimize and inspect solutions
3. **Parameters** — time limits, gap limits, and emphasis settings
3b. **MIPLIB Instances** — load and solve real benchmark instances
4. **Transportation** — LP with supply/demand constraints
5. **Blending** — nonlinear pooling problem with bilinear constraints
6. **Set Cover** — IP with binary covering variables
7. **Knapsack** — classic 0-1 knapsack
8. **Bin Packing** — IP with assignment and capacity constraints
9. **Facility Location** — MIP with linking constraints
10. **Graph Coloring** — IP with symmetry-breaking
11. **Indicator Constraints** — big-M vs indicator formulations
12. **Benchmarking** — compare big-M vs indicator formulations at scale

All exercises are in `part1/`. Each has a stub file (with `NotImplementedError`), a test, and (for exercises 4–10) a random instance generator.

```bash
cd part1
python -m pytest  # all tests SKIP until exercises are implemented
```

### Part 2: Row Generation

Use the **Traveling Salesman Problem** to explore row generation (cutting planes via constraint handlers):

| Topic | Exercises in |
|-------|-------------|
| TSP compact (MTZ) formulation | `part2/` |
| Subtour detection | `part2/` |
| Constraint handler for SECs | `part2/` |
| Experimental comparison | `part2/` |

### Part 3: Branch-and-Price

Use the **bin packing problem** to build a full branch-and-price algorithm:

| Topic | Exercises in |
|-------|-------------|
| Column generation (knapsack pricer) | `part3/` |
| Ryan-Foster branching | `part3/` |
| Constrained pricing | `part3/` |
| Branch-price-and-cut (subset-row cuts) | `part3/` |

## Running Tests

```bash
# Part 1: Modeling
cd part1
python ex01_first_model/test_first_model.py
python ex02_solving/test_solving.py
python ex03_parameters/test_parameters.py
python ex03_transportation/test_transportation.py
python ex04_blending/test_blending.py
python ex05_set_cover/test_set_cover.py
python ex06_knapsack/test_knapsack.py
python ex07_bin_packing/test_bin_packing.py
python ex07_facility_location/test_facility_location.py
python ex08_graph_coloring/test_graph_coloring.py
python ex09_indicators/test_indicators.py
python ex10_benchmarking/test_benchmarking.py

# Part 2: Row Generation
cd part2
python test_subtour.py
python test_tsp.py

# Part 3: Branch-and-Price
cd part3
python test_initial_columns.py
python test_pricing_knapsack.py
python test_bpc.py
```
