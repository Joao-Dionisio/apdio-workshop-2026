## Introduction

Part 1 of this workshop introduces PySCIPOpt through a series of progressively more complex optimization models. Starting from a minimal integer program, we build up to classic combinatorial optimization problems: transportation, blending, set cover, knapsack, facility location, and graph coloring. By the end, you will be comfortable creating models, adding variables and constraints, solving, and inspecting solutions.

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

## Section 3. Transportation Problem

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

### Exercise 3: Transportation

**Your task:** Implement the function `transportation(supply, demand, costs)` in `ex03_transportation/transportation.py`.

Return the model (not yet optimized) and a dictionary `x` mapping tuples `(i, j)` to continuous shipping variables.

**Test:** `python ex03_transportation/test_transportation.py`

## Section 4. Blending Problem

In a blending problem, a manufacturer must combine raw materials to produce a product that meets quality specifications. Each raw material $i$ has a per-unit cost $c_i$, limited availability $a_i$, and known quality attributes $q_{iq}$ for each quality dimension $q$. The blend must achieve a total production target $T$ and the average quality of the blend must fall within specified bounds.

$$
\begin{align*}
    \min \quad & \sum_{i} c_i \, x_i \\
    \text{subject to} \quad & \sum_{i} x_i = T \\
    & lb_q \cdot T \leq \sum_{i} q_{iq} \, x_i \leq ub_q \cdot T, \quad & \forall \, q \\
    & 0 \leq x_i \leq a_i, \quad & \forall \, i
\end{align*}
$$

The quality constraints deserve attention. The requirement that the average quality $\bar{q}$ of the blend satisfies $lb_q \leq \bar{q} \leq ub_q$ translates to $lb_q \cdot T \leq \sum_i q_{iq} x_i \leq ub_q \cdot T$ because $\bar{q} = \sum_i q_{iq} x_i / T$ and $\sum_i x_i = T$.

> Like the transportation problem, blending is a pure LP. These problems are common in petroleum refining, food manufacturing, and chemical engineering.

### Exercise 4: Blending

**Your task:** Implement the function `blending(costs, availability, qualities, quality_lb, quality_ub, total_production)` in `ex04_blending/blending.py`.

Return the model (not yet optimized) and a dictionary `x` mapping material index to its continuous variable.

**Test:** `python ex04_blending/test_blending.py`

## Section 5. Set Cover

The set cover problem is a fundamental integer program. Given a universe $U$ of elements and a collection of subsets $S_1, S_2, \ldots, S_n$, each with an associated cost $c_j$, select the cheapest collection of subsets whose union covers the entire universe.

$$
\begin{align*}
    \min \quad & \sum_{j} c_j \, y_j \\
    \text{subject to} \quad & \sum_{j : e \in S_j} y_j \geq 1, \quad & \forall \, e \in U \\
    & y_j \in \{0, 1\}, \quad & \forall \, j
\end{align*}
$$

This is the first IP (as opposed to LP) in the workshop. The binary variable $y_j$ indicates whether subset $j$ is selected. The covering constraints ensure that every element in the universe appears in at least one chosen subset.

> Set cover appears in many real-world settings: crew scheduling, facility placement, wireless network coverage, and feature selection, among others. The problem is NP-hard, but SCIP handles moderately sized instances efficiently.

### Exercise 5: Set Cover

**Your task:** Implement the function `set_cover(universe, subsets, costs)` in `ex05_set_cover/set_cover.py`.

Return the model (not yet optimized) and a dictionary `y` mapping subset index to its binary variable.

**Test:** `python ex05_set_cover/test_set_cover.py`

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

## Section 7. Facility Location

The uncapacitated facility location problem combines fixed costs with variable connection costs. A set of potential facility sites must be chosen, and each customer must be assigned to exactly one open facility. Opening facility $i$ incurs a fixed cost $f_i$, and serving customer $j$ from facility $i$ costs $c_{ij}$.

$$
\begin{align*}
    \min \quad & \sum_{i} f_i \, y_i + \sum_{i} \sum_{j} c_{ij} \, x_{ij} \\
    \text{subject to} \quad & \sum_{i} x_{ij} = 1, \quad & \forall \, j \\
    & x_{ij} \leq y_i, \quad & \forall \, i, j \\
    & y_i \in \{0, 1\}, \quad & \forall \, i \\
    & x_{ij} \geq 0, \quad & \forall \, i, j
\end{align*}
$$

This is a mixed-integer program (MIP): the facility opening variables $y_i$ are binary, while the assignment variables $x_{ij}$ are continuous. The linking constraints $x_{ij} \leq y_i$ enforce that a customer can only be assigned to an open facility.

> In the optimal solution, each $x_{ij}$ will naturally be 0 or 1 (each customer assigned to a single facility) even though the variables are declared continuous. This is because the constraint structure forces integrality. However, the LP relaxation at intermediate nodes of the branch-and-bound tree may have fractional $x_{ij}$ values.

### Exercise 7: Facility Location

**Your task:** Implement the function `facility_location(fixed_costs, connection_costs)` in `ex07_facility_location/facility_location.py`.

Return the model (not yet optimized), a dictionary `y` mapping facility index to its binary variable, and a dictionary `x` mapping `(i, j)` to its continuous assignment variable.

**Test:** `python ex07_facility_location/test_facility_location.py`

## Section 8. Graph Coloring

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

### Exercise 8: Graph Coloring

**Your task:** Implement the function `graph_coloring(n_nodes, edges, max_colors)` in `ex08_graph_coloring/graph_coloring.py`.

Return the model (not yet optimized), a dictionary `x` mapping `(v, k)` to its binary assignment variable, and a dictionary `w` mapping color index `k` to its binary usage variable. Include the symmetry-breaking constraints.

**Test:** `python ex08_graph_coloring/test_graph_coloring.py`

---

Once all exercises pass, proceed to **Part 2** for advanced topics: row generation, column generation, branch-and-price, and branch-price-and-cut.
