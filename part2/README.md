# Part 2: Row Generation for the Traveling Salesman Problem

This tutorial demonstrates **row generation** (cutting planes / lazy constraints) using the symmetric Traveling Salesman Problem (TSP). Row generation is the dual concept to column generation: instead of adding variables dynamically, we add constraints dynamically.

## The Traveling Salesman Problem

Given $n$ cities and distances $d_{ij}$ between each pair, find the shortest tour that visits each city exactly once and returns to the starting city.

For symmetric TSP: $d_{ij} = d_{ji}$ (undirected edges).

> **Prerequisite:** Complete Exercise 13 (TSP MTZ) in Part 1 first. The compact formulation is used here as a baseline for comparison.

---

## 1. Edge Formulation with Subtour Elimination Constraints

For symmetric TSP, we use undirected edge variables with degree constraints and subtour elimination constraints (SECs).

### Variables
- $x_e \in \{0, 1\}$ for each edge $e = \{i, j\}$

### Formulation

$$
\begin{align}
\min \quad & \sum_{e \in E} d_e x_e \\
\text{s.t.} \quad & \sum_{e \in \delta(i)} x_e = 2 && \forall i \in V \quad \text{(degree constraints)} \\
& \sum_{e \in E(S)} x_e \leq |S| - 1 && \forall S \subset V, 2 \leq |S| \leq n-1 \quad \text{(SECs)} \\
& x_e \in \{0, 1\}
\end{align}
$$

Where:
- $\delta(i)$ = edges incident to node $i$
- $E(S)$ = edges with both endpoints in $S$

### Properties
- **Exponentially many SECs**: $O(2^n)$ constraints
- **Strong LP relaxation**: Much tighter than MTZ
- **Row generation needed**: Add SECs on-the-fly as violations are found

---

## 2. Row Generation (Cutting Planes)

Instead of adding all $2^n$ SECs upfront, we:
1. Solve with only degree constraints
2. Check if solution has subtours
3. Add SECs for violated subtours
4. Repeat until no violations

This is implemented via a **constraint handler** in SCIP.

### 2.1 Subtour Detection

Given an integer solution (selected edges), we need to detect subtours:

1. Build a graph from selected edges
2. Find connected components (using DFS, BFS, or Union-Find)
3. If multiple components exist, each is a subtour

**Example:**
```
Selected edges: {(0,1), (1,2), (2,0), (3,4), (4,5), (5,3)}
Components: {0,1,2} and {3,4,5}
Both are subtours (violate SECs)
```

#### Exercise 1: Implement Subtour Detection

Complete `find_subtours()` in `subtour.py`:

```python
def find_subtours(selected_edges, n_nodes):
    """
    Find connected components in the graph defined by selected_edges.

    Returns: List of sets (subtours), or [] if single valid tour.
    """
    # Your implementation here
```

**Hints:**
- Build an adjacency list from edges
- Use DFS/BFS to find connected components
- Alternative: Union-Find data structure

**Test your implementation:**
```bash
python test_subtour.py
```

### 2.2 Constraint Handler

SCIP's constraint handler interface allows adding constraints lazily:

| Callback | Purpose |
|----------|---------|
| `conscheck` | Verify if a solution is feasible |
| `consenfolp` | Enforce constraints, add cuts if violated |
| `conslock` | Lock variables (required, can be empty) |

#### Exercise 2: Implement the Constraint Handler

Complete the callbacks in `conshdlr_subtour.py`:

**Part A: `conscheck`**
```python
def conscheck(self, constraints, solution, ...):
    # 1. Extract selected edges from solution
    # 2. Call find_subtours()
    # 3. Return FEASIBLE or INFEASIBLE
```

**Part B: `consenfolp`**
```python
def consenfolp(self, constraints, nusefulconss, solinfeasible):
    # 1. Get LP solution values
    # 2. Find subtours in edges with x > 0.5
    # 3. For each subtour S, add SEC:
    #    sum_{e in E(S)} x_e <= |S| - 1
    # 4. Return FEASIBLE or CONSADDED
```

**Test your implementation:**
```bash
python test_tsp.py
```

### 2.3 How It Works Together

```
┌─────────────────────────────────────────────────────────┐
│                    SCIP Solver                          │
├─────────────────────────────────────────────────────────┤
│  1. Solve LP relaxation (degree constraints only)       │
│  2. Branch-and-bound on fractional variables            │
│  3. For integer solutions:                              │
│     └─> Call conscheck() - is this a valid tour?        │
│         └─> If subtours found: INFEASIBLE               │
│             └─> Call consenfolp() - add SEC cuts        │
│  4. Repeat until optimal tour found                     │
└─────────────────────────────────────────────────────────┘
```

---

## Exercise 3: Computational Experiments (MTZ vs Row Generation)

Now that both formulations work, compare them experimentally. Complete `experiments.py`:

```bash
python experiments.py
```

Solve the same TSP instances with MTZ and row generation across increasing sizes. Print a comparison table with solving time, B&B nodes, and LP bound.

**Questions to answer:**
- How does the LP relaxation bound compare between the two formulations?
- At what instance size does the difference in B&B nodes become significant?
- Which formulation is faster for small instances? For large instances?

---

## 3. Bonus Exercises

### 4.1 Min-Cut Separation (Advanced)

For fractional LP solutions, connected components may not detect violations. Use min-cut:

1. For each node pair $(s, t)$, compute min-cut with capacities = $x_e$ values
2. If min-cut < 2, add violated SEC

### 4.2 Stronger Valid Inequalities

Beyond SECs, other cuts can strengthen the LP:
- **2-matching inequalities**: Handle "comb" structures
- **Comb inequalities**: Generalization of 2-matching

### 4.3 Alternative Compact Formulations

- **DFJ (Dantzig-Fulkerson-Johnson)**: Original SEC formulation
- **Flow-based**: Single-commodity or multi-commodity flow

---

## Quick Start

```bash
# Run MTZ formulation (works immediately)
python main.py --compact --cities 15

# After completing exercises, run row generation
python main.py --cities 15

# Compare both on same instance
python main.py --compact --cities 20 --seed 42
python main.py --cities 20 --seed 42
```

---

## References

- Miller, Tucker, Zemlin (1960): "Integer Programming Formulation of Traveling Salesman Problems"
- Dantzig, Fulkerson, Johnson (1954): "Solution of a Large-Scale Traveling-Salesman Problem"
- Applegate, Bixby, Chvátal, Cook (2006): "The Traveling Salesman Problem: A Computational Study"
