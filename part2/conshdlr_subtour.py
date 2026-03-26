"""
Constraint handler for subtour elimination in TSP.

Callbacks:
- conscheck: verify integer solutions are valid tours
- consenfolp: add SECs when subtours are found
"""

from pyscipopt import Conshdlr, SCIP_RESULT, quicksum

from subtour import find_subtours


class SubtourElimination(Conshdlr):

    def __init__(self, n_nodes):
        """
        Args:
            n_nodes: number of cities.

        Edge variables are accessed via self.model.data (set before solving).
        """
        self.n = n_nodes

    def _get_edges(self, sol):
        """Extract edges with positive value from a solution."""
        x = self.model.data
        return [
            (i, j) for (i, j) in x
            if self.model.isFeasPositive(self.model.getSolVal(sol, x[i, j]))
        ]

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        """Check if a solution forms a single Hamiltonian tour."""
        subtours = find_subtours(self._get_edges(solution), self.n)

        if subtours:
            return {"result": SCIP_RESULT.INFEASIBLE}
        return {"result": SCIP_RESULT.FEASIBLE}

    def consenfolp(self, constraints, nusefulconss, solinfeasible):
        """Enforce LP solution by adding violated SECs."""
        x = self.model.data
        subtours = find_subtours(self._get_edges(None), self.n)

        if not subtours:
            return {"result": SCIP_RESULT.FEASIBLE}

        for S in subtours:
            self.model.addCons(
                quicksum(x[i, j] for i in S for j in S if j > i)
                <= len(S) - 1
            )

        return {"result": SCIP_RESULT.CONSADDED}

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass
