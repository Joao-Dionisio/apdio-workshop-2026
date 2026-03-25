"""
Subset Row Separator for Branch-Price-and-Cut.

For a triple S = {i, j, k}, at most one bin can contain 2+ items from S:
    sum_{p : |p ∩ S| >= 2} λ_p <= 1

Cuts must be added as modifiable constraints (so the pricer can update them).
"""

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

        Hint: Use self.model.getLPColsData() to get columns.
              Parse pattern from var.name (e.g. "[1, 3, 5]").
              Use modifiable=True in addCons().

        Returns:
            {"result": SCIP_RESULT.SEPARATED} or DIDNOTFIND
        """
        # EXERCISE: Implement subset row separation

        raise NotImplementedError("Implement subset row separation.")
