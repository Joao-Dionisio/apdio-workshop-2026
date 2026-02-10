# PySCIPOpt Workshop -- Part 2: Advanced MIP Techniques

## Introduction

Part 2 covers advanced techniques for solving mixed-integer programs with SCIP: **row generation** (cutting planes), **column generation**, **branch-and-price**, and **branch-price-and-cut**. These methods go beyond standard branch-and-bound by dynamically adding constraints or variables during the solve, enabling us to tackle formulations that would otherwise be too large to handle.

All exercises live in existing directories outside this workshop folder:

- `row_generation/` -- TSP with compact and row-generation formulations
- `branch_and_price/` -- Bin packing with column generation and Ryan-Foster branching
- `separator/subset_row/` -- Subset-row cutting planes for set partitioning

---

## Section 1. TSP: Compact MTZ Formulation

The **Traveling Salesman Problem (TSP)** asks: given $n$ cities and pairwise distances $d_{ij}$, find the shortest tour that visits every city exactly once and returns to the start.

The Miller-Tucker-Zemlin (MTZ) formulation is a compact (polynomial-size) formulation that uses directed binary edge variables $x_{ij}$ and continuous position variables $u_i$ to eliminate subtours.

$$
\begin{align}
\min \quad & \sum_{i \neq j} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j \neq i} x_{ij} = 1 && \forall i \quad \text{(leave each city once)} \\
& \sum_{i \neq j} x_{ij} = 1 && \forall j \quad \text{(enter each city once)} \\
& u_i - u_j + n \cdot x_{ij} \leq n - 1 && \forall i,j \neq 0,\; i \neq j \quad \text{(MTZ subtour elimination)} \\
& 1 \leq u_i \leq n-1 && \forall i \neq 0 \\
& x_{ij} \in \{0,1\}
\end{align}
$$

The MTZ formulation has $O(n^2)$ variables and constraints -- no special plugins are needed. However, its LP relaxation is notoriously weak, which makes the branch-and-bound tree large.

### Reference: Compact MTZ

The MTZ formulation is already implemented in [`../row_generation/compact_mtz.py`](../row_generation/compact_mtz.py). Study it to understand the baseline before moving to row generation.

```bash
cd ../row_generation && python compact_mtz.py
```

---

## Section 2. TSP: Subtour Elimination and Row Generation

An alternative formulation for symmetric TSP uses undirected edge variables $x_e$ with degree constraints and **subtour elimination constraints** (SECs):

$$
\begin{align}
\min \quad & \sum_{e \in E} d_e x_e \\
\text{s.t.} \quad & \sum_{e \in \delta(v)} x_e = 2 && \forall v \in V \quad \text{(degree constraints)} \\
& \sum_{e \in E(S)} x_e \leq |S| - 1 && \forall S \subset V,\; 2 \leq |S| \leq n-1 \quad \text{(SECs)} \\
& x_e \in \{0, 1\}
\end{align}
$$

where $\delta(v)$ denotes the edges incident to node $v$ and $E(S)$ denotes the edges with both endpoints in $S$.

This formulation yields a much stronger LP relaxation than MTZ. The catch is that there are exponentially many SECs -- $O(2^n)$ subsets to consider. Adding them all upfront is infeasible. Instead, we use **row generation**: solve the LP with only the degree constraints, check whether the solution violates any SEC, add the violated constraints, and repeat.

### Row Generation in SCIP

SCIP supports row generation through its **constraint handler** plugin. The key callbacks are:

| Callback | Purpose |
|----------|---------|
| `conscheck` | Check if a candidate integer solution satisfies all constraints |
| `consenfolp` | Enforce constraints on the current LP solution; add cuts if violated |
| `conslock` | Declare variable locks (required; can be left empty for our purposes) |

The interaction between SCIP and the constraint handler looks like this:

```
┌─────────────────────────────────────────────────────────┐
│                    SCIP Solver                           │
├─────────────────────────────────────────────────────────┤
│  1. Solve LP relaxation (degree constraints only)       │
│  2. Branch-and-bound on fractional variables            │
│  3. For integer solutions:                              │
│     └─> Call conscheck() - is this a valid tour?        │
│         └─> If subtours found: INFEASIBLE               │
│             └─> Call consenfolp() - add SEC cuts         │
│  4. Repeat until optimal tour found                     │
└─────────────────────────────────────────────────────────┘
```

### Exercise 1: Subtour Detection

Implement `find_subtours()` in [`../row_generation/subtour.py`](../row_generation/subtour.py). Given a set of selected edges and the number of nodes, find all connected components. If there is more than one component, each one is a subtour.

**Hints:** Build an adjacency list from the edge set, then use DFS/BFS or Union-Find to identify connected components.

```bash
cd ../row_generation && python test_subtour.py
```

### Exercise 2: Constraint Handler

Complete the `conscheck` and `consenfolp` callbacks in [`../row_generation/conshdlr_subtour.py`](../row_generation/conshdlr_subtour.py).

- **`conscheck`**: Extract selected edges from the solution, call `find_subtours()`, return `FEASIBLE` or `INFEASIBLE`.
- **`consenfolp`**: Get LP values, find subtours among edges with $x_e > 0.5$, and for each subtour $S$ add the SEC $\sum_{e \in E(S)} x_e \leq |S| - 1$. Return `CONSADDED` if any constraint was added.

```bash
cd ../row_generation && python test_tsp.py
```

---

## Section 3. Bin Packing: Compact Formulation

We now shift to the **bin packing problem**: given items with sizes $s_i$ and bins with capacity $C$, pack all items using the fewest bins.

The compact formulation uses assignment variables $x_{ib} \in \{0,1\}$ (item $i$ goes into bin $b$) and bin-usage variables $y_b \in \{0,1\}$:

$$
\begin{align}
\min \quad & \sum_{b \in \mathcal{B}} y_b \\
\text{s.t.} \quad & \sum_{b \in \mathcal{B}} x_{ib} = 1 && \forall i \in \mathcal{I} \quad \text{(each item assigned once)} \\
& \sum_{i \in \mathcal{I}} s_i x_{ib} \leq C \, y_b && \forall b \in \mathcal{B} \quad \text{(capacity)} \\
& x_{ib} \in \{0,1\}, \quad y_b \in \{0,1\}
\end{align}
$$

This formulation is straightforward but suffers from **enormous symmetry** (permuting bin indices gives equivalent solutions) and a **weak LP relaxation**, making it impractical for large instances.

### Reference

See the compact formulation in [`../branch_and_price/compact.py`](../branch_and_price/compact.py).

---

## Section 4. Column Generation

To overcome the weaknesses of the compact formulation, we reformulate bin packing using **packings** (feasible subsets of items). Let $\mathcal{P}$ be the set of all feasible packings and let $a_i^p = 1$ if item $i$ belongs to packing $p$. The extended formulation is:

$$
\begin{align}
\min \quad & \sum_{p \in \mathcal{P}} z_p \\
\text{s.t.} \quad & \sum_{p \in \mathcal{P}} a_i^{p} z_p = 1 && \forall i \in \mathcal{I} \quad \text{(each item covered)} \\
& z_p \in \{0, 1\} && \forall p \in \mathcal{P}
\end{align}
$$

The number of feasible packings grows exponentially with the number of items, so we cannot enumerate them all. **Column generation** solves this by working with a small Restricted Master Problem (RMP) and generating new columns on-the-fly.

### Column Generation Algorithm

1. Solve the RMP (LP relaxation with a small subset of columns).
2. Obtain dual values $\pi_i$ for each covering constraint.
3. Solve a **pricing problem** to find the column with the most negative reduced cost.
4. If the reduced cost is $\geq 0$, the current LP solution is optimal. Otherwise, add the new column and go to step 1.

### Pricing Problem

The reduced cost of a new packing $a$ is $1 - \sum_{i} a_i \pi_i$. Minimizing this, subject to the capacity constraint, gives:

$$
\begin{align}
\min \quad & 1 - \sum_{i \in \mathcal{I}} a_i \pi_i \\
\text{s.t.} \quad & \sum_{i \in \mathcal{I}} s_i a_i \leq C \\
& a_i \in \{0, 1\} \quad \forall i \in \mathcal{I}
\end{align}
$$

Rearranging the objective, this is equivalent to maximizing $\sum_i a_i \pi_i$ subject to the capacity constraint -- a **knapsack problem**. When the optimal reduced cost is $\geq 0$, no improving column exists and the LP is solved to optimality.

### Pricer Plugin

In SCIP, column generation is handled by the **pricer** plugin. The key callbacks are:

- `pricerredcost`: Called at each LP iteration to generate columns with negative reduced cost.
- `pricerfarkas`: Called when the RMP is infeasible to generate columns that restore feasibility.

See the pricer infrastructure in [`../branch_and_price/pricer.py`](../branch_and_price/pricer.py).

### Exercise 3: Knapsack Pricing

Implement `solve_knapsack()` in [`../branch_and_price/pricing_knapsack.py`](../branch_and_price/pricing_knapsack.py). Build a MIP that solves the 0-1 knapsack problem and return a tuple `(optimal_value, list_of_selected_items)`.

```bash
cd ../branch_and_price && python test_pricing_knapsack.py
```

---

## Section 5. Branch-and-Price

Column generation solves the LP relaxation, but we still need to find integer solutions. Embedding column generation inside branch-and-bound gives us **branch-and-price**.

### Why Standard Branching Fails

Standard variable branching (setting $z_p = 0$ or $z_p = 1$) creates highly unbalanced trees:

- $z_p = 1$: forces one specific packing out of exponentially many -- very restrictive.
- $z_p = 0$: forbids one specific packing out of exponentially many -- barely restrictive at all.

### Ryan-Foster Branching

The standard approach for bin packing is **Ryan-Foster branching**. Instead of branching on individual packing variables, we branch on **pairs of items** $(i, j)$:

- **Together branch**: Items $i$ and $j$ must appear in the same bin.
- **Apart branch**: Items $i$ and $j$ must appear in different bins.

This creates a much more balanced search tree. To find a pair to branch on, we compute the implicit pair variable $x_{ij} = \sum_{p : i \in p,\, j \in p} z_p$ and choose a pair where $x_{ij}$ is fractional (strictly between 0 and 1).

### Enforcing Branching Decisions in Pricing

The pricing problem must respect all branching decisions accumulated along the path from the root to the current node:

- **Together** $(i, j)$: If item $i$ is in the packing, then item $j$ must also be in the packing (and vice versa).
- **Apart** $(i, j)$: Items $i$ and $j$ cannot both be in the packing.

These constraints are added directly to the knapsack pricing problem.

### Exercise 4: Fractional Pairs

Implement `all_fractional_pairs()` in [`../branch_and_price/ryan_foster.py`](../branch_and_price/ryan_foster.py). Given the current LP solution (patterns and their values), compute the implicit pair values and return all pairs whose value is fractional.

```bash
cd ../branch_and_price && python test_fractional_pairs.py
```

### Exercise 5: Branching Decisions

Complete the child-node creation logic in [`../branch_and_price/ryan_foster.py`](../branch_and_price/ryan_foster.py). Each child node must inherit the branching decisions of its parent and add the chosen pair to either the "together" set or the "apart" set.

### Exercise 6: Constrained Pricing

Implement `solve_knapsack_with_constraints()` in [`../branch_and_price/pricing_knapsack.py`](../branch_and_price/pricing_knapsack.py). Extend your knapsack solver to enforce the together and apart constraints from Ryan-Foster branching. Remember: apart constraints forbid both items being selected, but they do not forbid both being absent.

```bash
cd ../branch_and_price && python test_knapsack_with_constraints.py
```

After completing Exercises 3--6, you can run the full branch-and-price algorithm:

```bash
cd ../branch_and_price && python test_bnp.py
```

---

## Section 6. Branch-Price-and-Cut

Branch-and-price can be further strengthened by adding **cutting planes** during the solve, yielding a **branch-price-and-cut** algorithm. Cuts tighten the LP relaxation at each node, potentially reducing the number of nodes explored.

### Subset-Row Inequalities

For set partitioning problems (like the master problem in bin packing), a natural family of cuts are the **subset-row inequalities**. Given three columns $z_p, z_q, z_r$ whose LP values sum to more than 1, the inequality

$$
z_p + z_q + z_r \leq 1
$$

is valid because at most one packing from any conflicting triple can be selected in an integer solution.

More generally, for any subset $S$ of rows (items) with $|S| = 3$, we consider all columns covering at least two items in $S$. If the sum of their LP values exceeds 1, we can add the cut.

### Separator Plugin

In SCIP, cutting planes are managed by the **separator** plugin. The key callback is:

- `sepaexeclp`: Called at each LP solution to search for violated inequalities. Returns `SEPARATED` if a cut was added, `DIDNOTFIND` otherwise.

### Exercise 7: Subset-Row Separator

Implement the subset-row separator in [`../separator/subset_row/subset_row.py`](../separator/subset_row/subset_row.py). Enumerate triples of fractional LP variables and add a cut when their values sum to more than 1.

```bash
cd ../separator/subset_row && python test_subset_row.py
```

---

## Section 7. Bonus Exercises

The `branch_and_price` directory contains several self-paced bonus exercises for improving the vanilla branch-and-price implementation. You may complete them in any order.

- **Dual Stabilization**: Smooth the dual values across column generation iterations to reduce the yo-yo effect and improve convergence.
- **Better Initialization**: Use heuristics (e.g., first-fit decreasing) to provide better initial columns than the one-item-per-bin solution.
- **Handling Numerics**: Debug and fix the infinite loop that appears on larger instances (200 items) due to numerical precision issues in reduced cost checking.
- **Speeding Up Pricing**: Add multiple columns per pricing iteration and explore faster knapsack algorithms.
- **Different-Sized Bins**: Extend the implementation to handle bins of varying capacities.
- **Lagrangian Bound**: Compute and return a Lagrangian lower bound from the pricer to help SCIP prune the search tree.
- **Removing Together Constraints**: Replace together-branching constraints by merging items, reducing the pricing problem size.

See [`../branch_and_price/README.md`](../branch_and_price/README.md) for detailed descriptions of each bonus exercise.

---

## Verification Checklist

- [ ] **Reference**: `cd ../row_generation && python compact_mtz.py` runs successfully
- [ ] **Exercise 1**: `cd ../row_generation && python test_subtour.py` passes
- [ ] **Exercise 2**: `cd ../row_generation && python test_tsp.py` passes
- [ ] **Exercise 3**: `cd ../branch_and_price && python test_pricing_knapsack.py` passes
- [ ] **Exercise 4**: `cd ../branch_and_price && python test_fractional_pairs.py` passes
- [ ] **Exercise 5**: Branching decisions correctly propagated (verified via Exercise 6)
- [ ] **Exercise 6**: `cd ../branch_and_price && python test_knapsack_with_constraints.py` passes
- [ ] **Exercise 7**: `cd ../separator/subset_row && python test_subset_row.py` passes
- [ ] **Integration**: `cd ../branch_and_price && python test_bnp.py` passes

---

## References

- Miller, Tucker, Zemlin (1960). "Integer Programming Formulation of Traveling Salesman Problems." *Journal of the ACM*.
- Dantzig, Fulkerson, Johnson (1954). "Solution of a Large-Scale Traveling-Salesman Problem." *Operations Research*.
- Gilmore, Gomory (1961). "A Linear Programming Approach to the Cutting-Stock Problem." *Operations Research*.
- Ryan, Foster (1981). "An Integer Programming Approach to Scheduling." *Computer Scheduling of Public Transport*.
- Jepsen, Petersen, Spoorendonk, Pisinger (2008). "Subset-Row Inequalities Applied to the Vehicle-Routing Problem with Time Windows." *Operations Research*.
- Desrosiers, Lubbecke (2005). "A Primer in Column Generation." In *Column Generation*, Springer.
- [SCIP documentation: Pricer plugin](https://www.scipopt.org/doc/html/PRICER.php)
- [SCIP documentation: Constraint handler plugin](https://www.scipopt.org/doc/html/CONS.php)
- [SCIP documentation: Separator plugin](https://www.scipopt.org/doc/html/SEPA.php)
