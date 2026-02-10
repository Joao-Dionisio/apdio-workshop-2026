"""
Random set cover instance generator.
"""

import random


def random_set_cover_instance(n_elements, n_subsets, seed=0):
    """
    Generate a random set cover instance.

    Ensures every element is covered by at least one subset.

    Args:
        n_elements: Size of the universe.
        n_subsets: Number of available subsets.
        seed: Random seed for reproducibility.

    Returns:
        universe: Set of elements {0, 1, ..., n_elements - 1}.
        subsets: List of sets, each a subset of universe.
        costs: List of costs (one per subset).
    """
    random.seed(seed)

    universe = set(range(n_elements))

    # Generate random subsets, each element included with probability 0.3
    subsets = []
    for _ in range(n_subsets):
        s = {e for e in universe if random.random() < 0.3}
        if len(s) == 0:
            s = {random.choice(list(universe))}
        subsets.append(s)

    # Ensure every element is covered by at least one subset
    covered = set()
    for s in subsets:
        covered |= s
    for e in universe - covered:
        idx = random.randint(0, n_subsets - 1)
        subsets[idx].add(e)

    costs = [random.randint(1, 10) for _ in range(n_subsets)]

    return universe, subsets, costs


if __name__ == "__main__":
    universe, subsets, costs = random_set_cover_instance(8, 6, seed=42)
    print(f"Universe: {universe}")
    for i, (s, c) in enumerate(zip(subsets, costs)):
        print(f"  Subset {i}: {s}  (cost {c})")
