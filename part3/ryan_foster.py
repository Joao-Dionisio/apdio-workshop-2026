from typing import List
from pyscipopt import Branchrule, SCIP_RESULT


class RyanFoster(Branchrule):
    def __init__(self, *args, **kwargs):
        """
        Branching decisions stored per node: {"together": set, "apart": set}
        """
        super().__init__(*args, **kwargs)
        self.branching_decisions = {
            1: {  # root node
                "together": set(),
                "apart": set(),
            }
        }

    def branchexeclp(self, allowaddcons):
        lpcands, lpcandssol, *_ = self.model.getLPBranchCands()

        patterns_with_vals = [
            (eval(var.name.replace("t_", "")), val) for var, val in zip(lpcands, lpcandssol)
        ]

        chosen_pair = choose_fractional_pair(patterns_with_vals)

        parent_together = set()
        parent_apart = set()

        parent = self.model.getCurrentNode()
        if parent:
            parent_together = set(self.branching_decisions[parent.getNumber()]["together"])
            parent_apart = set(self.branching_decisions[parent.getNumber()]["apart"])

        left_node = self.model.createChild(0, 0)
        right_node = self.model.createChild(0, 0)

        # EXERCISE: Set together/apart for each child node
        raise NotImplementedError(
            "What should together and apart be for each child node?"
        )
        # self.branching_decisions[left_node.getNumber()] = {
        #     "together": ?,
        #     "apart": ?
        # }
        # self.branching_decisions[right_node.getNumber()] = {
        #     "together": ?,
        #     "apart": ?
        # }

        return {"result": SCIP_RESULT.BRANCHED}


def all_fractional_pairs(patterns_with_vals: List[tuple[List[int], float]]) -> List[tuple[int, int]]:
    """Find all pairs of items that are fractional in the LP solution."""

    raise NotImplementedError("Implement this function")


def choose_fractional_pair(patterns_with_vals: List[tuple[List[int], float]]) -> tuple[int, int]:
    """Choose a fractional pair to branch on."""

    first_pair = all_fractional_pairs(patterns_with_vals)[0]
    return first_pair
