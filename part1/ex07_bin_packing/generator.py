"""Random bin packing instance generator."""

import random


def random_bin_packing_instance(n_items, capacity, seed=None):
    """Generate a random bin packing instance.

    Args:
        n_items: Number of items.
        capacity: Bin capacity.
        seed: Random seed for reproducibility.

    Returns:
        sizes: List of item sizes (each between 1 and capacity).
    """
    if seed is not None:
        random.seed(seed)
    sizes = [random.randint(1, capacity) for _ in range(n_items)]
    return sizes
