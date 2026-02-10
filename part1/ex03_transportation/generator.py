"""
Random transportation problem instance generator.
"""

import random


def random_transportation_instance(n_suppliers, n_customers, seed=0):
    """
    Generate a random transportation problem instance.

    Args:
        n_suppliers: Number of suppliers.
        n_customers: Number of customers.
        seed: Random seed for reproducibility.

    Returns:
        supply: List of supply amounts (length n_suppliers).
        demand: List of demand amounts (length n_customers).
        costs: n_suppliers x n_customers cost matrix (list of lists).
    """
    random.seed(seed)

    # Generate supply and demand ensuring feasibility (total supply >= total demand)
    supply = [random.randint(10, 50) for _ in range(n_suppliers)]
    demand = [random.randint(5, 30) for _ in range(n_customers)]

    # Scale supply so that total supply = total demand (balanced)
    total_demand = sum(demand)
    total_supply = sum(supply)
    scale = total_demand / total_supply
    supply = [int(round(s * scale)) for s in supply]

    # Adjust to make exactly balanced
    diff = total_demand - sum(supply)
    supply[0] += diff

    # Random transportation costs
    costs = [[random.randint(1, 20) for _ in range(n_customers)]
             for _ in range(n_suppliers)]

    return supply, demand, costs


if __name__ == "__main__":
    supply, demand, costs = random_transportation_instance(3, 4, seed=42)
    print(f"Supply: {supply}")
    print(f"Demand: {demand}")
    print("Costs:")
    for row in costs:
        print(f"  {row}")
