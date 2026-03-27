# APDIO Workshop 2026 — Optimization Software & Practice

An APDIO-organized workshop on Optimization using [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), the Python interface to the [SCIP](https://www.scipopt.org/) solver. More information about the event [here](https://www.apdio.pt/2026/03/03/2026-apdio-workshop-optimization-software-practice/).

> **Documentation:** PySCIPOpt tutorials are available at [pyscipopt.readthedocs.io](https://pyscipopt.readthedocs.io/en/latest/tutorials/index.html).

> **Tip:** The READMEs contain syntax that only renders properly in a viewer. On GitHub they render automatically. In VS Code, press `Ctrl+Shift+V` (`Cmd+Shift+V` on Mac) to open the Markdown preview. In PyCharm, click the split editor icon (top-right of the editor) or right-click the file and select *Open Preview*.

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

The workshop is divided into three parts. It is VERY BIG, and you are not expected to complete all exercises in one sitting. Go at your own pace, and feel free to jump around the exercises. These are divided into three parts:

### Part 1: Modeling

Build and solve MINLPs in PySCIPOpt through ten progressively complex exercises:

1. **First Model** — build a small binary IP
2. **Solving** — optimize and inspect solutions
3. **Parameters** — time limits, gap limits, and emphasis settings; MIPLIB instances
4. **Transportation** — LP with supply/demand constraints
5. **Knapsack** — classic 0-1 knapsack
6. **TSP (MTZ)** — compact formulation for the Traveling Salesman Problem
7. **Graph Coloring** — IP with symmetry-breaking
8. **Blending** — nonlinear pooling problem with bilinear constraints
9. **Indicator Constraints** — big-M vs indicator formulations
10. **Benchmarking** — compare big-M vs indicator formulations at scale

All exercises are in `part1/`. Each has a stub file (with `NotImplementedError`), a test, and (for exercises 4–10) a random instance generator.

> **Prerequisites:** Part 1 requires basic Python and optimization literacy. Parts 2 and 3 require familiarity with LP duality, branch-and-bound, and LP relaxations.

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

## How It Works

Each part of the workshop follows the same flow:

1. **Slides** introduce the concepts and formulations (`slides/`).
2. **The README** in each part provides detailed explanations, mathematical formulations, and pointers to exercises (`part1/README.md`, `part2/README.md`, `part3/README.md`).
3. **Exercise stubs** contain skeleton code with `NotImplementedError` and you fill in the missing pieces.
4. **Tests** verify your implementation. Run them with `python test_*.py` or `python -m pytest`.

Work through the slides and README side by side, implementing each exercise as it comes up.

For background on SCIP itself, see the overview presentation in `slides/scip_presentation.pdf`.

## Running Tests

Each test verifies the corresponding exercise file (linked below).

```bash
# Part 1: Modeling (cd part1)
python ex01_first_model/test_first_model.py      # → first_model.py
python ex02_solving/test_solving.py               # → solving.py
python ex03_parameters/test_parameters.py         # → parameters.py
python ex04_transportation/test_transportation.py # → transportation.py
python ex05_knapsack/test_knapsack.py             # → knapsack.py
python ex06_tsp_mtz/test_tsp_mtz.py               # → tsp_mtz.py
python ex07_graph_coloring/test_graph_coloring.py # → graph_coloring.py
python ex08_blending/test_blending.py             # → blending.py
python ex09_indicators/test_indicators.py         # → indicators.py
python ex10_benchmarking/test_benchmarking.py     # → benchmarking.py

# Part 2: Row Generation (cd part2)
python test_subtour.py                            # → subtour.py
python test_tsp.py                                # → conshdlr_subtour.py

# Part 3: Branch-and-Price (cd part3)
python test_initial_columns.py                    # → initial_columns.py
python test_pricing_knapsack.py                   # → pricing_knapsack.py
python test_fractional_pairs.py                   # → ryan_foster.py
python test_knapsack_with_constraints.py          # → pricing_knapsack.py
python test_bnp.py                                # → (integration test)
python test_bpc.py                                # → subset_row.py
```