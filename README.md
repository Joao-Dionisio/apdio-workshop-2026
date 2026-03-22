# APDIO Workshop 2026 — Optimization Software & Practice

An APDIO-organized workshop on Optimization using [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), the Python interface to the [SCIP](https://www.scipopt.org/) solver. More information about the event [here](https://www.apdio.pt/2026/03/03/2026-apdio-workshop-optimization-software-practice/).

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

## How It Works

Each part of the workshop follows the same flow:

1. **Slides** introduce the concepts and formulations (`slides/`).
2. **The README** in each part provides detailed explanations, mathematical formulations, and pointers to exercises (`part1/README.md`, `part2/README.md`, `part3/README.md`).
3. **Exercise stubs** contain skeleton code with `NotImplementedError` and you fill in the missing pieces.
4. **Tests** verify your implementation. Run them with `python test_*.py` or `python -m pytest`.

Work through the slides and README side by side, implementing each exercise as it comes up.

## Structure

The workshop is divided into three parts. It is VERY BIG, and you are not expected to complete all exercises in one sitting. Go at your own pace, and feel free to jump around the exercises. These are divided into three parts:

### Part 1: Modeling

Build and solve MINLPs in PySCIPOpt through progressively complex exercises:

1. **First Model** — build a small binary IP
2. **Solving** — optimize and inspect solutions
3. **Parameters** — time limits, gap limits, and emphasis settings
   - **MIPLIB Instances** — load and solve real benchmark instances
4. **Transportation** — LP with supply/demand constraints
5. **Blending** — nonlinear pooling problem with bilinear constraints
6. **Knapsack** — classic 0-1 knapsack
7. **Bin Packing** — IP with assignment and capacity constraints
8. **TSP (MTZ)** — compact formulation for the Traveling Salesman Problem
9. **Graph Coloring** — IP with symmetry-breaking
10. **Indicator Constraints** — big-M vs indicator formulations
11. **Benchmarking** — compare big-M vs indicator formulations at scale

All exercises are in `part1/`. Each has a stub file (with `NotImplementedError`), a test, and (for exercises 4–10) a random instance generator.

### Part 2: Row Generation

Use the **Traveling Salesman Problem** to explore row generation (cutting planes via constraint handlers):

| Topic | Exercises in |
|-------|-------------|
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
python ex04_transportation/test_transportation.py
python ex08_blending/test_blending.py
python ex05_knapsack/test_knapsack.py
python ex07_graph_coloring/test_graph_coloring.py
python ex09_indicators/test_indicators.py
python ex10_benchmarking/test_benchmarking.py
python ex06_tsp_mtz/test_tsp_mtz.py

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
