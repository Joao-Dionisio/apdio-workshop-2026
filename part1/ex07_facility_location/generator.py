"""
Random facility location instance generator.
"""

import random


def random_facility_location_instance(n_facilities, n_customers, seed=0):
    """
    Generate a random uncapacitated facility location instance.

    Args:
        n_facilities: Number of potential facility sites.
        n_customers: Number of customers.
        seed: Random seed for reproducibility.

    Returns:
        fixed_costs: List of fixed costs for opening each facility.
        connection_costs: n_facilities x n_customers cost matrix;
                         connection_costs[i][j] is the cost of serving
                         customer j from facility i.
    """
    random.seed(seed)

    fixed_costs = [random.randint(50, 200) for _ in range(n_facilities)]
    connection_costs = [
        [random.randint(1, 30) for _ in range(n_customers)]
        for _ in range(n_facilities)
    ]

    return fixed_costs, connection_costs


if __name__ == "__main__":
    fixed_costs, conn_costs = random_facility_location_instance(3, 5, seed=42)
    print(f"Fixed costs: {fixed_costs}")
    print("Connection costs:")
    for i, row in enumerate(conn_costs):
        print(f"  Facility {i}: {row}")
