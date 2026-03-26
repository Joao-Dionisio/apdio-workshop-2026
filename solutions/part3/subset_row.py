"""Solution for Exercise 5: Subset Row Separator."""

import itertools
from pyscipopt import Sepa, SCIP_RESULT, quicksum


class SubsetRowSeparator(Sepa):

    def __init__(self, n_items):
        self.n_items = n_items
        self.cuts = []  # List of (constraint, (i, j, k))

    def sepaexeclp(self):
        """Separate subset row inequalities from the current LP solution.

        For each triple not already cut, check if sum of covering patterns > 1.
        If so, add as a modifiable constraint.
        """
        cols = self.model.getLPColsData()
        patterns = []
        for col in cols:
            var = col.getVar()
            val = col.getPrimsol()
            if val < 1e-6:
                continue
            name = var.name.replace("t_", "")
            try:
                pattern = set(eval(name))
            except Exception:
                continue
            patterns.append((var, pattern, val))

        existing = {triple for _, triple in self.cuts}
        found = False

        for i, j, k in itertools.combinations(range(self.n_items), 3):
            if (i, j, k) in existing:
                continue
            triple_set = {i, j, k}
            lhs = sum(val for _, pat, val in patterns
                      if len(pat & triple_set) >= 2)
            if lhs > 1 + 1e-6:
                affected = [var for var, pat, _ in patterns
                            if len(pat & triple_set) >= 2]
                cons = self.model.addCons(
                    quicksum(affected) <= 1,
                    modifiable=True,
                )
                self.cuts.append((cons, (i, j, k)))
                found = True

        if found:
            return {"result": SCIP_RESULT.SEPARATED}
        return {"result": SCIP_RESULT.DIDNOTFIND}
