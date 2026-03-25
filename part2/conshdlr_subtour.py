"""
Constraint handler for subtour elimination in TSP.

Callbacks:
- conscheck: verify integer solutions are valid tours
- consenfolp: add SECs when subtours are found
"""

from pyscipopt import Conshdlr, SCIP_RESULT, quicksum

from subtour import find_subtours


class SubtourElimination(Conshdlr):

    def __init__(self, x_vars, n_nodes):
        """
        Args:
            x_vars: dict mapping (i, j) with i < j to SCIP binary edge variables.
            n_nodes: number of cities.
        """
        self.x = x_vars
        self.n = n_nodes

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        """Check if a solution forms a single Hamiltonian tour."""
        # EXERCISE 2a: Implement solution checking
        #
        # 1. Extract selected edges: use self.model.getSolVal(solution, var) > 0.5
        # 2. Call find_subtours(selected_edges, self.n)
        # 3. Return {"result": SCIP_RESULT.FEASIBLE} or INFEASIBLE

        raise NotImplementedError("Exercise 2a: Implement conscheck.")

    def consenfolp(self, constraints, nusefulconss, solinfeasible):
        """Enforce LP solution by adding violated SECs."""
        # EXERCISE 2b: Implement constraint enforcement
        #
        # 1. Extract edges with self.model.getVal(var) > 0.5
        # 2. Call find_subtours()
        # 3. For each subtour S, add: sum_{(i,j) in E(S)} x[i,j] <= |S| - 1
        #    using self.model.addCons(quicksum(...) <= ...)
        # 4. Return {"result": SCIP_RESULT.CONSADDED} or FEASIBLE

        raise NotImplementedError("Exercise 2b: Add SECs for each subtour found.")

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass
