# Part 1: Modeling with PySCIPOpt

Part 1 of this workshop introduces PySCIPOpt through a series of progressively more complex optimization models. Starting from a minimal integer program, we build up to classic optimization problems: transportation, blending, set cover, knapsack, facility location, graph coloring, and indicator constraints. By the end, you will be comfortable creating models, adding variables and constraints, solving, and inspecting solutions.

Each section explains the problem and its mathematical formulation, then points to an exercise file where you must implement the model. Every exercise includes a test script to verify correctness.

## Section 1. Getting Started with PySCIPOpt

The fundamental workflow in PySCIPOpt follows a simple lifecycle:

1. **Create** a `Model` object.
2. **Add variables** specifying their type and objective coefficient.
3. **Add constraints** using algebraic expressions.
4. **Set the objective direction** (minimize or maximize).
5. **Optimize** the model.
6. **Query** the solution.

PySCIPOpt supports three main variable types:

| Type | Code | Description |
|------|------|-------------|
| Continuous | `"C"` | Takes any real value within bounds |
| Binary | `"B"` | Takes value 0 or 1 |
| Integer | `"I"` | Takes any integer value within bounds |

Variables are created with `model.addVar()`, constraints with `model.addCons()`, and sums over indexed expressions with the `quicksum()` helper. Here is a minimal example:

```python
from pyscipopt import Model, quicksum

model = Model("Example")
x = model.addVar(name="x", vtype="B", obj=3)
y = model.addVar(name="y", vtype="B", obj=2)
model.addCons(x + y <= 1)
model.setMaximize()
```

> The `obj` parameter in `addVar` sets the coefficient of that variable in the objective function. This avoids the need for a separate `setObjective()` call in many cases.

### Exercise 1: First Model

**Your task:** Implement the function `first_model()` in `ex01_first_model/first_model.py`.

Build the following binary integer program:

$$
\begin{align*}
    \max \quad & 3x + 2y \\
    \text{subject to} \quad & x + y \leq 1 \\
    & 2x + y \leq 2 \\
    & x, y \in \{0, 1\}
\end{align*}
$$

The function should return the model (not yet optimized) along with the two variables `x` and `y`.

**Test:** `python ex01_first_model/test_first_model.py`

## Section 2. Solving and Inspecting Solutions

Once a model is built, calling `model.optimize()` triggers the solver. After optimization, PySCIPOpt provides several methods to inspect the result:

- `model.getStatus()` returns the solving status as a string (e.g. `"optimal"`, `"infeasible"`).
- `model.getObjVal()` returns the optimal objective value.
- `model.getVal(var)` returns the value of a variable in the best solution found.
- `model.getVars()` returns the list of all variables in the model.
- `model.getNNodes()` returns the number of branch-and-bound nodes explored.
- `model.getSolvingTime()` returns the wall-clock solving time in seconds.

If you want to suppress solver output, call `model.hideOutput()` before `optimize()`.

```python
model.hideOutput()
model.optimize()

print("Status:", model.getStatus())
print("Objective:", model.getObjVal())
for var in model.getVars():
    print(f"  {var.name} = {model.getVal(var)}")
print("Nodes:", model.getNNodes())
print("Time:", model.getSolvingTime())
```

### Exercise 2: Solve and Report

**Your task:** Implement the function `solve_and_report(model)` in `ex02_solving/solving.py`.

Given a pre-built (but not yet optimized) model, optimize it and return a dictionary with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `"status"` | `str` | Solving status |
| `"objective"` | `float` | Optimal objective value |
| `"variables"` | `dict` | Mapping of variable name to its value |
| `"n_nodes"` | `int` | Number of B&B nodes explored |
| `"time"` | `float` | Solving time in seconds |

**Test:** `python ex02_solving/test_solving.py`

## Section 3. Solver Parameters

SCIP exposes hundreds of parameters that control the solving process. In this exercise you will learn to set the most important ones: time limits, optimality gap limits, and emphasis settings. You will also learn to load models from standard file formats.

Key methods:

- `model.setParam("limits/time", seconds)` — stop after a time limit
- `model.setParam("limits/gap", gap)` — stop when the relative optimality gap is small enough
- `model.setEmphasis(emphasis)` — set a solving emphasis (e.g. `"OPTIMALITY"`, `"FEASIBILITY"`)
- `model.readProblem(filepath)` — load a model from an MPS or LP file
- `model.getGap()` — get the relative gap between primal and dual bound

### Exercise 3: Parameters

**Your task:** Implement the four functions in `ex03_parameters/parameters.py`:

| Function | What it does |
|----------|-------------|
| `solve_with_time_limit(model, time_limit)` | Set a time limit and solve |
| `solve_with_gap_limit(model, gap)` | Set a gap limit and solve |
| `solve_with_emphasis(model, emphasis)` | Set an emphasis and solve |
| `load_and_solve(filepath, params)` | Load a model from file and solve with optional parameters |

Each function returns a dictionary with the relevant statistics (status, objective, gap, time, n_nodes).

**Test:** `python ex03_parameters/test_parameters.py`

### Exercise 3b: MIPLIB Instances

[MIPLIB](https://miplib.zib.de) is the standard benchmark library for mixed-integer programming. Six small instances are included in `ex03_parameters/miplib_data/`:

| Instance | Rows | Cols | Description |
|----------|------|------|-------------|
| `p0033` | 16 | 33 | Capital budgeting |
| `enigma` | 21 | 100 | Puzzle |
| `flugpl` | 18 | 18 | Flight planning |
| `misc03` | 96 | 160 | Miscellaneous |
| `stein27` | 118 | 27 | Steiner triple |
| `gen-ip054` | 30 | 30 | General IP |

**Your task:** Use `model.readProblem()` and `load_and_solve()` from Exercise 3 to load and solve these instances. Collect status, objective, time, nodes, and gap for each.

## Section 4. Transportation Problem

The transportation problem is one of the earliest applications of linear programming. A set of suppliers, each with a limited supply, must ship goods to a set of customers, each with a specific demand. Shipping one unit from supplier $i$ to customer $j$ costs $c_{ij}$. The goal is to satisfy all demands at minimum total shipping cost.

$$
\begin{align*}
    \min \quad & \sum_{i \in S} \sum_{j \in D} c_{ij} \, x_{ij} \\
    \text{subject to} \quad & \sum_{j \in D} x_{ij} \leq s_i, \quad & \forall \, i \in S \\
    & \sum_{i \in S} x_{ij} \geq d_j, \quad & \forall \, j \in D \\
    & x_{ij} \geq 0, \quad & \forall \, i \in S, \, j \in D
\end{align*}
$$

where $s_i$ is the supply at source $i$ and $d_j$ is the demand at customer $j$. For the problem to be feasible, total supply must be at least as large as total demand.

> This is a pure LP (no integer variables). The constraint matrix of a transportation problem has a special structure (it is totally unimodular), so the LP relaxation always gives an integer optimal solution.

In PySCIPOpt, the data for this problem is naturally represented with Python lists. The cost matrix `costs[i][j]` gives the per-unit cost, `supply[i]` the available amount at each source, and `demand[j]` the required amount at each destination.

### Exercise 4: Transportation

**Your task:** Implement the function `transportation(supply, demand, costs)` in `ex03_transportation/transportation.py`.

Return the model (not yet optimized) and a dictionary `x` mapping tuples `(i, j)` to continuous shipping variables.

**Test:** `python ex03_transportation/test_transportation.py`

## Section 5. Nonlinear Blending (Pooling Problem)

The pooling problem is a classic nonlinear optimization problem from the process industry. Raw materials with known qualities are blended through a mixing pool to produce products that must meet quality specifications. The pool has an unknown quality that depends on the input mix, introducing bilinear terms.

$$
\begin{align*}
    \max \quad & \sum_{p} r_p \, d_p - \sum_{s} c_s \left( x_s + \sum_{p} z_{sp} \right) \\
    \text{subject to} \quad & \sum_{s} x_s = \sum_{p} y_p && \text{(pool balance)} \\
    & \lambda \sum_{s} x_s = \sum_{s} q_s \, x_s && \text{(pool quality definition)} \\
    & \lambda \, y_p + \sum_{s} q_s \, z_{sp} \leq \bar{q}_p \, d_p && \forall \, p \quad \text{(product quality)} \\
    & d_p = y_p + \sum_{s} z_{sp} && \forall \, p \quad \text{(product demand)} \\
    & x_s, y_p, z_{sp}, \lambda \geq 0
\end{align*}
$$

where $\lambda$ is the pool quality, $x_s$ is the flow from source $s$ to the pool, $y_p$ is the flow from the pool to product $p$, and $z_{sp}$ is the direct bypass flow from source $s$ to product $p$. The terms $\lambda \cdot x_s$ and $\lambda \cdot y_p$ are bilinear (nonconvex).

> Unlike previous exercises, this involves **bilinear constraints** — products of two continuous variables. PySCIPOpt supports these as nonlinear constraints. SCIP uses spatial branch-and-bound to solve nonconvex problems to global optimality.

### Exercise 5: Blending

**Your task:** Implement the function `blending(sources, products)` in `ex04_blending/blending.py`.

Return the model (not yet optimized) and the variables `x`, `y`, `z`, `lam`.

**Test:** `python ex04_blending/test_blending.py`

<!-- Section: Set Cover (optional bonus exercise, not covered in slides)

## Set Cover

The set cover problem is a fundamental integer program. Given a universe $U$ of elements and a collection of subsets $S_1, S_2, \ldots, S_n$, each with an associated cost $c_j$, select the cheapest collection of subsets whose union covers the entire universe.

**Your task:** Implement `set_cover(universe, subsets, costs)` in `ex05_set_cover/set_cover.py`.

**Test:** `python ex05_set_cover/test_set_cover.py`
-->

## Section 6. 0-1 Knapsack

The 0-1 knapsack problem is perhaps the most studied problem in combinatorial optimization. Given a set of items, each with a weight $w_i$ and a value $v_i$, and a knapsack with capacity $C$, select items to maximize total value without exceeding the capacity.

$$
\begin{align*}
    \max \quad & \sum_{i} v_i \, x_i \\
    \text{subject to} \quad & \sum_{i} w_i \, x_i \leq C \\
    & x_i \in \{0, 1\}, \quad & \forall \, i
\end{align*}
$$

Despite its simplicity, the knapsack problem has widespread applications: capital budgeting, cargo loading, resource allocation, and as a subproblem in column generation (as seen in Part 2 of this workshop with branch-and-price).

> The LP relaxation of the knapsack problem has a simple greedy solution: sort items by value-to-weight ratio and pack greedily. The gap between the LP relaxation and the IP optimum is typically small, making branch-and-bound very effective.

### Exercise 6: Knapsack

**Your task:** Implement the function `knapsack(weights, values, capacity)` in `ex06_knapsack/knapsack.py`.

Return the model (not yet optimized) and a dictionary `x` mapping item index to its binary variable.

**Test:** `python ex06_knapsack/test_knapsack.py`

## Section 7. Bin Packing

The bin packing problem asks how to pack a set of items with given sizes into the fewest number of identical bins without exceeding their capacity. It is closely related to the knapsack problem but shifts the focus from selecting valuable items to efficiently distributing all items.

Assuming an upper bound of $n$ bins (one per item):

$$
\begin{align*}
    \min \quad & \sum_{b} y_b \\
    \text{subject to} \quad & \sum_{b} x_{ib} = 1, \quad & \forall \, i \quad \text{(assignment)} \\
    & \sum_{i} s_i \, x_{ib} \leq C \, y_b, \quad & \forall \, b \quad \text{(capacity)} \\
    & x_{ib} \in \{0, 1\}, \quad & \forall \, i, b \\
    & y_b \in \{0, 1\}, \quad & \forall \, b
\end{align*}
$$

The binary variable $y_b$ indicates whether bin $b$ is used, and $x_{ib}$ indicates whether item $i$ is assigned to bin $b$. The capacity constraints link both: items can only be assigned to open bins, and the total size in each bin cannot exceed $C$.

> This compact formulation suffers from symmetry — any permutation of bin labels yields an equivalent solution. In Part 2, we will see how branch-and-price with column generation can solve bin packing much more efficiently by working with packing patterns instead of item-to-bin assignments.

### Exercise 7: Bin Packing

**Your task:** Implement the function `bin_packing(sizes, capacity)` in `ex07_bin_packing/bin_packing.py`.

Return the model (not yet optimized), a dictionary `x` mapping `(i, b)` to binary assignment variables, and a dictionary `y` mapping bin index `b` to binary usage variables.

**Test:** `python ex07_bin_packing/test_bin_packing.py`

<!-- Section: Facility Location (optional bonus exercise, not covered in slides)

## Facility Location

The uncapacitated facility location problem combines fixed costs with variable connection costs.

**Your task:** Implement `facility_location(fixed_costs, connection_costs)` in `ex07_facility_location/facility_location.py`.

**Test:** `python ex07_facility_location/test_facility_location.py`
-->

## Section 8. TSP — Compact MTZ Formulation

The Traveling Salesman Problem (TSP) asks for the shortest tour that visits each city exactly once and returns to the start. The Miller-Tucker-Zemlin (MTZ) formulation uses position variables $u_i$ to eliminate subtours with a polynomial number of constraints:

$$
\begin{align*}
    \min \quad & \sum_{i \neq j} d_{ij} \, x_{ij} \\
    \text{subject to} \quad & \sum_{j \neq i} x_{ij} = 1 \quad \forall \, i \\
    & \sum_{i \neq j} x_{ij} = 1 \quad \forall \, j \\
    & u_i - u_j + n \, x_{ij} \leq n - 1 \quad \forall \, i, j \neq 0 \\
    & 1 \leq u_i \leq n - 1 \quad \forall \, i \neq 0 \\
    & x_{ij} \in \{0, 1\}
\end{align*}
$$

The MTZ constraints enforce a consistent ordering of cities, preventing subtours. This formulation is easy to implement but has a weak LP relaxation. In Part 2, you will see how row generation with stronger subtour elimination constraints can solve TSP much more efficiently.

### Exercise 8: TSP (MTZ)

**Your task:** Implement the function `tsp_mtz(distances)` in `ex11_tsp_mtz/tsp_mtz.py`.

Return the model (not yet optimized) and a dictionary `x` mapping `(i, j)` to binary edge variables.

**Test:** `python ex11_tsp_mtz/test_tsp_mtz.py`

## Section 9. Graph Coloring

Given an undirected graph $G = (V, E)$, the graph coloring problem asks for an assignment of colors to nodes such that no two adjacent nodes share the same color, using the minimum number of colors. This minimum is called the chromatic number $\chi(G)$.

We introduce binary variables $x_{vk}$ (node $v$ receives color $k$) and $w_k$ (color $k$ is used), with $K$ as an upper bound on the number of colors:

$$
\begin{align*}
    \min \quad & \sum_{k=1}^{K} w_k \\
    \text{subject to} \quad & \sum_{k=1}^{K} x_{vk} = 1, \quad & \forall \, v \in V \\
    & x_{uk} + x_{vk} \leq w_k, \quad & \forall \, (u, v) \in E, \, \forall \, k \\
    & x_{vk} \in \{0, 1\}, \quad & \forall \, v \in V, \, \forall \, k \\
    & w_k \in \{0, 1\}, \quad & \forall \, k
\end{align*}
$$

The first set of constraints ensures every node gets exactly one color. The conflict constraints prevent adjacent nodes from sharing a color, while simultaneously linking color usage: if any node uses color $k$, then $w_k = 1$.

This formulation suffers from symmetry. Any permutation of color labels yields an equivalent solution. A simple symmetry-breaking technique is to impose an ordering on the colors:

$$
w_k \geq w_{k+1}, \quad \forall \, k = 1, \ldots, K-1
$$

This forces colors to be "used in order" (color 1 before color 2, etc.), eliminating many symmetric solutions from the search space and significantly improving solver performance.

> Graph coloring is NP-hard and notoriously difficult for IP solvers due to the inherent symmetry. Symmetry-breaking constraints are essential for practical performance. For large instances, specialized approaches such as column generation (where each column represents an independent set) are often preferred.

### Exercise 9: Graph Coloring

**Your task:** Implement the function `graph_coloring(n_nodes, edges, max_colors)` in `ex08_graph_coloring/graph_coloring.py`.

Return the model (not yet optimized), a dictionary `x` mapping `(v, k)` to its binary assignment variable, and a dictionary `w` mapping color index `k` to its binary usage variable. Include the symmetry-breaking constraints.

**Test:** `python ex08_graph_coloring/test_graph_coloring.py`

## Section 10. Indicator Constraints

Indicator constraints are a modeling tool for conditional logic: "if binary variable $y = 1$, then constraint $g(x) \leq 0$ must hold." The traditional approach is big-M linearization, which replaces the conditional with $g(x) \leq M(1 - y)$ for a large constant $M$. This works but introduces numerical difficulties and weakens the LP relaxation.

SCIP supports indicator constraints natively via `model.addConsIndicator()`, avoiding the need for big-M constants entirely. The solver handles the disjunction internally, often producing tighter relaxations and better performance.

We model a generator scheduling problem: a set of generators must meet a total electricity demand. Each generator $i$ has a fixed startup cost $f_i$, a variable cost $c_i$ per MW, and minimum/maximum output levels $[\underline{p}_i, \bar{p}_i]$. If a generator is on ($y_i = 1$), it must produce at least $\underline{p}_i$.

$$
\begin{align*}
    \min \quad & \sum_{i} f_i \, y_i + \sum_{i} c_i \, p_i \\
    \text{subject to} \quad & \sum_{i} p_i \geq D \\
    & p_i \leq \bar{p}_i \, y_i \quad & \forall \, i \\
    & y_i = 1 \implies p_i \geq \underline{p}_i \quad & \forall \, i \\
    & y_i \in \{0, 1\}, \; p_i \geq 0 \quad & \forall \, i
\end{align*}
$$

### Exercise 10: Indicator Constraints

**Your task:** Implement both formulations in `ex09_indicators/indicators.py`:

- `generator_scheduling_bigm(...)` — use big-M constraints: $p_i \geq \underline{p}_i \, y_i$
- `generator_scheduling_indicator(...)` — use `model.addConsIndicator()` for the minimum output constraint

Both functions return `model, y, p` (not yet optimized).

**Test:** `python ex09_indicators/test_indicators.py`

## Section 11. Benchmarking Formulations

Modeling is only half the story — understanding how your formulation affects solver performance is equally important. In this exercise you will systematically compare the big-M and indicator formulations from Exercise 11 on random instances of increasing size.

For each instance, collect:

- Solving time
- Number of branch-and-bound nodes
- Optimality gap

**Your task:** Implement `benchmark_formulation()` and `compare_formulations()` in `ex10_benchmarking/benchmarking.py`. Use `print_results()` to display the comparison table.

**Run:** `python ex10_benchmarking/benchmarking.py`
**Test:** `python ex10_benchmarking/test_benchmarking.py`

---

Once all exercises pass, proceed to **Part 2** (row generation for TSP) and **Part 3** (branch-and-price for bin packing).
