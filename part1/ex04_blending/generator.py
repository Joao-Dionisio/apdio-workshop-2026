"""
Random blending problem instance generator.
"""

import random


def random_blending_instance(n_materials, n_qualities, seed=0):
    """
    Generate a random blending problem instance.

    Args:
        n_materials: Number of raw materials.
        n_qualities: Number of quality attributes.
        seed: Random seed for reproducibility.

    Returns:
        costs: List of per-unit costs (length n_materials).
        availability: List of max available amounts (length n_materials).
        qualities: n_materials x n_qualities matrix; qualities[i][q] is the
                   quality-q content per unit of material i.
        quality_lb: List of minimum quality requirements (length n_qualities).
        quality_ub: List of maximum quality requirements (length n_qualities).
        total_production: Total amount to produce.
    """
    random.seed(seed)

    costs = [random.randint(1, 20) for _ in range(n_materials)]
    availability = [random.randint(20, 100) for _ in range(n_materials)]

    # Quality attributes: each material has a value between 0 and 100
    qualities = [[random.randint(10, 90) for _ in range(n_qualities)]
                 for _ in range(n_materials)]

    # Quality bounds: average of qualities +/- some margin
    quality_lb = []
    quality_ub = []
    for q in range(n_qualities):
        avg = sum(qualities[i][q] for i in range(n_materials)) / n_materials
        quality_lb.append(max(0, int(avg - 15)))
        quality_ub.append(min(100, int(avg + 15)))

    total_production = min(sum(availability), 50)

    return costs, availability, qualities, quality_lb, quality_ub, total_production


if __name__ == "__main__":
    data = random_blending_instance(4, 2, seed=42)
    costs, availability, qualities, qlb, qub, total = data
    print(f"Costs: {costs}")
    print(f"Availability: {availability}")
    print(f"Qualities: {qualities}")
    print(f"Quality LB: {qlb}, UB: {qub}")
    print(f"Total production: {total}")
