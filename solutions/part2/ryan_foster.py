from typing import List
from pyscipopt import Branchrule, SCIP_RESULT


class RyanFoster(Branchrule):
    def __init__(self, *args, **kwargs):
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

        # Left subproblem: enforce that pair is in the same bin
        left_node = self.model.createChild(0, 0)

        self.branching_decisions[left_node.getNumber()] = {
            "together": parent_together.union({chosen_pair}),
            "apart": parent_apart
        }

        # Right subproblem: enforce that pair is in different bins
        right_node = self.model.createChild(0, 0)

        self.branching_decisions[right_node.getNumber()] = {
            "together": parent_together,
            "apart": parent_apart.union({chosen_pair})
        }

        return {"result": SCIP_RESULT.BRANCHED}


def all_fractional_pairs(patterns_with_vals: List[tuple[List[int], float]]) -> List[tuple[int, int]]:
    pairs = {}
    for pattern, val in patterns_with_vals:
        for i in range(len(pattern)):
            for j in range(i + 1, len(pattern)):
                if pattern[i] < pattern[j]:
                    pair = (pattern[i], pattern[j])
                    if pair not in pairs:
                        pairs[pair] = val
                    else:
                        pairs[pair] += val

    return [pair for pair, val in pairs.items() if 1e-6 < val < 1 - 1e-6]


def choose_fractional_pair(patterns_with_vals: List[tuple[List[int], float]]) -> tuple[int, int]:
    first_pair = all_fractional_pairs(patterns_with_vals)[0]
    return first_pair
