"""
Random 0-1 knapsack instance generator.
"""

import random


def random_knapsack_instance(n_items, seed=0):
    """
    Generate a random 0-1 knapsack instance.

    Args:
        n_items: Number of items.
        seed: Random seed for reproducibility.

    Returns:
        weights: List of item weights (length n_items).
        values: List of item values (length n_items).
        capacity: Knapsack capacity (int).
    """
    random.seed(seed)

    weights = [random.randint(1, 30) for _ in range(n_items)]
    values = [random.randint(1, 50) for _ in range(n_items)]

    # Capacity is roughly half the total weight
    capacity = sum(weights) // 2

    return weights, values, capacity


if __name__ == "__main__":
    weights, values, capacity = random_knapsack_instance(8, seed=42)
    print(f"Weights:  {weights}")
    print(f"Values:   {values}")
    print(f"Capacity: {capacity}")
