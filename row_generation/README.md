# Row Generation for the Traveling Salesman Problem

This tutorial demonstrates **row generation** (cutting planes / lazy constraints) using the symmetric Traveling Salesman Problem (TSP). Row generation is the dual concept to column generation: instead of adding variables dynamically, we add constraints dynamically.

## The Traveling Salesman Problem

Given $n$ cities and distances $d_{ij}$ between each pair, find the shortest tour that visits each city exactly once and returns to the starting city.

For symmetric TSP: $d_{ij} = d_{ji}$ (undirected edges).

---

## 1. Compact MTZ Formulation

The Miller-Tucker-Zemlin (MTZ) formulation uses position variables to eliminate subtours with a polynomial number of constraints.

### Variables
- $x_{ij} \in \{0, 1\}$: 1 if edge $(i,j)$ is in the tour
- $u_i \in \mathbb{R}$: position of city $i$ in the tour (for $i \neq 0$)

### Formulation

$$
\begin{align}
\min \quad & \sum_{i \neq j} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j \neq i} x_{ij} = 1 && \forall i \quad \text{(leave each city once)} \\
& \sum_{i \neq j} x_{ij} = 1 && \forall j \quad \text{(enter each city once)} \\
& u_i - u_j + n \cdot x_{ij} \leq n - 1 && \forall i,j \neq 0, i \neq j \quad \text{(MTZ)} \\
& 1 \leq u_i \leq n-1 && \forall i \neq 0 \\
& x_{ij} \in \{0,1\}
\end{align}
$$

### Properties
- **Polynomial size**: $O(n^2)$ variables and constraints
- **Weak LP relaxation**: The LP bound is typically far from optimal
- **Easy to implement**: No special callbacks needed

### Usage
```bash
python compact_mtz.py
# or
python main.py --compact
```

---

## 2. Edge Formulation with Subtour Elimination Constraints

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

## 3. Row Generation (Cutting Planes)

Instead of adding all $2^n$ SECs upfront, we:
1. Solve with only degree constraints
2. Check if solution has subtours
3. Add SECs for violated subtours
4. Repeat until no violations

This is implemented via a **constraint handler** in SCIP.

### 3.1 Subtour Detection

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

### 3.2 Constraint Handler

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

### 3.3 How It Works Together

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

## 4. Bonus Exercises

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

## File Structure

```
row_generation/
├── README.md              # This file
├── generator.py           # Random TSP instance generator
├── compact_mtz.py         # MTZ formulation (reference)
├── subtour.py             # Exercise 1: Subtour detection
├── conshdlr_subtour.py    # Exercise 2: Constraint handler
├── tsp.py                 # Main TSP model with row generation
├── main.py                # Entry point
├── test_subtour.py        # Tests for Exercise 1
└── test_tsp.py            # Integration tests
```

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

## Verification Checklist

1. [ ] `python compact_mtz.py` runs successfully
2. [ ] After Exercise 1: `python test_subtour.py` passes
3. [ ] After Exercise 2: `python test_tsp.py` passes
4. [ ] Both methods give same optimal value on same instance

---

## References

- Miller, Tucker, Zemlin (1960): "Integer Programming Formulation of Traveling Salesman Problems"
- Dantzig, Fulkerson, Johnson (1954): "Solution of a Large-Scale Traveling-Salesman Problem"
- Applegate, Bixby, Chvátal, Cook (2006): "The Traveling Salesman Problem: A Computational Study"
