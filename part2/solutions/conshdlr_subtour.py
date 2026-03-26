"""Solution for Exercise 2: Constraint handler for subtour elimination."""

from pyscipopt import Conshdlr, SCIP_RESULT, quicksum

from subtour import find_subtours


class SubtourElimination(Conshdlr):

    def __init__(self, n_nodes):
        self.n = n_nodes

    def _get_edges(self, sol):
        x = self.model.data
        return [
            (i, j) for (i, j) in x
            if self.model.isFeasPositive(self.model.getSolVal(sol, x[i, j]))
        ]

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        subtours = find_subtours(self._get_edges(solution), self.n)

        if subtours:
            return {"result": SCIP_RESULT.INFEASIBLE}
        return {"result": SCIP_RESULT.FEASIBLE}

    def consenfolp(self, constraints, nusefulconss, solinfeasible):
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
