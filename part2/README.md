# PySCIPOpt Workshop -- Part 2: Advanced MIP Techniques

Part 2 covers advanced techniques for solving mixed-integer programs with SCIP: **row generation** (cutting planes), **column generation**, **branch-and-price**, and **branch-price-and-cut**. These methods go beyond standard branch-and-bound by dynamically adding constraints or variables during the solve, enabling us to tackle formulations that would otherwise be too large to handle.

Each section lives in its own subdirectory with a detailed README, exercises, and tests.

---

## [Row Generation](row_generation/README.md) — TSP

We use the **Traveling Salesman Problem** to explore compact vs row-generation formulations. You will implement the MTZ formulation, then build a constraint handler that adds subtour elimination constraints on the fly, and finally compare both approaches experimentally.

```bash
cd row_generation
```

---

## [Branch-and-Price](branch_and_price/README.md) — Bin Packing

We use the **bin packing problem** to build a full branch-and-price algorithm from scratch: a knapsack pricer for column generation, Ryan-Foster branching, and constrained pricing. You will then compare the extended formulation against the compact one. Finally, you will strengthen it with subset-row cutting planes to obtain a **branch-price-and-cut** algorithm.

> **Good to know:** For a comprehensive reference on branch-and-price, see [*Branch-and-Price*](https://link.springer.com/book/10.1007/978-3-031-96917-1) (Springer, 2025).

```bash
cd branch_and_price
```

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
