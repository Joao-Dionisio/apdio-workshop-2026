"""Solution for Exercise 2: Subtour Elimination Constraint Handler."""

from pyscipopt import Conshdlr, SCIP_RESULT, quicksum

from subtour import find_subtours


class SubtourElimination(Conshdlr):

    def __init__(self, x_vars, n_nodes):
        self.x = x_vars
        self.n = n_nodes

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        selected = [
            (i, j) for (i, j), var in self.x.items()
            if self.model.getSolVal(solution, var) > 0.5
        ]
        subtours = find_subtours(selected, self.n)

        if not subtours:
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}

    def consenfolp(self, constraints, nusefulconss, solinfeasible):
        selected = [
            (i, j) for (i, j), var in self.x.items()
            if self.model.getVal(var) > 0.5
        ]
        subtours = find_subtours(selected, self.n)

        if not subtours:
            return {"result": SCIP_RESULT.FEASIBLE}

        for S in subtours:
            self.model.addCons(
                quicksum(
                    self.x[i, j]
                    for (i, j) in self.x
                    if i in S and j in S
                ) <= len(S) - 1
            )

        return {"result": SCIP_RESULT.CONSADDED}

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass
