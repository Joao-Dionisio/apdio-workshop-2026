# APDIO Workshop 2026 — Optimization Software & Practice

A hands-on workshop for learning mathematical optimization with [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), the Python interface to the [SCIP](https://www.scipopt.org/) solver.

## Setup

```bash
pip install pyscipopt
```

Verify installation:

```python
from pyscipopt import Model
m = Model()
print("PySCIPOpt is ready!")
```

## Structure

The workshop is divided into two parts:

### Part 1: Modeling Basics

Learn to formulate and solve optimization problems using PySCIPOpt. Covers LPs, IPs, and MIPs through eight progressively complex exercises:

1. **First Model** — build a small binary IP
2. **Solving** — optimize and inspect solutions
3. **Transportation** — LP with supply/demand constraints
4. **Blending** — LP with quality specifications
5. **Set Cover** — first IP with binary variables
6. **Knapsack** — classic 0-1 knapsack
7. **Facility Location** — MIP with linking constraints
8. **Graph Coloring** — IP with symmetry

All exercises are in `part1/`. Each has a stub file (with `NotImplementedError`), a test, and (for exercises 3–8) a random instance generator.

```bash
cd part1
pytest  # all tests SKIP until exercises are implemented
```

### Part 2: Advanced Techniques

Covers row generation, column generation, branch-and-price, and branch-price-and-cut using the TSP and bin packing problems:

| Topic | Exercises in |
|-------|-------------|
| TSP compact formulation | `row_generation/` |
| Subtour elimination & constraint handlers | `row_generation/` |
| Bin packing column generation | `branch_and_price/` |
| Ryan-Foster branching | `branch_and_price/` |
| Branch-price-and-cut | `separator/subset_row/` |

The Part 2 README and slides provide the narrative arc connecting these exercises.

## Schedule

| Block | Content | Duration |
|-------|---------|----------|
| Part 1 — Lecture | Slides: modeling basics | 30 min |
| Part 1 — Hands-on | Exercises 1–8 | 90 min |
| Break | | 15 min |
| Part 2 — Lecture | Slides: advanced techniques | 45 min |
| Part 2 — Hands-on | Row generation + B&P exercises | 90 min |

## Running Tests

```bash
# Part 1 (all in part1/)
cd part1
python ex01_first_model/test_first_model.py
python ex02_solving/test_solving.py
python ex03_transportation/test_transportation.py
python ex04_blending/test_blending.py
python ex05_set_cover/test_set_cover.py
python ex06_knapsack/test_knapsack.py
python ex07_facility_location/test_facility_location.py
python ex08_graph_coloring/test_graph_coloring.py

# Part 2 (exercises in existing directories)
cd row_generation && python test_subtour.py
cd branch_and_price && python test_knapsack.py
cd separator/subset_row && python test_subset_row.py
```

## Slides

Presentation slides are in LaTeX Beamer format:

```bash
cd part1/slides && pdflatex part1.tex
cd part2/slides && pdflatex part2.tex
```

## File Structure

```
apdio-workshop-2026/
├── README.md                          # This file
├── part1/
│   ├── README.md                      # Theory + exercises narrative
│   ├── conftest.py                    # pytest configuration
│   ├── slides/
│   │   └── part1.tex                  # Beamer presentation
│   ├── ex01_first_model/
│   ├── ex02_solving/
│   ├── ex03_transportation/
│   ├── ex04_blending/
│   ├── ex05_set_cover/
│   ├── ex06_knapsack/
│   ├── ex07_facility_location/
│   └── ex08_graph_coloring/
├── part2/
│   ├── README.md                      # Narrative linking exercise dirs
│   └── slides/
│       └── part2.tex                  # Beamer presentation
├── row_generation/                    # Part 2: TSP exercises
├── branch_and_price/                  # Part 2: Bin packing B&P exercises
└── separator/
    └── subset_row/                    # Part 2: BPC exercises
```
