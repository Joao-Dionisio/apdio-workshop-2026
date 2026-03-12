"""
Random TSP instance generator.

This module provides functions to generate random Euclidean TSP instances
with symmetric integer distances.
"""

import random
import math


def random_euclidean_tsp(n_cities, seed=None, grid_size=100):
    """
    Generate a random Euclidean TSP instance with integer distances.

    Args:
        n_cities: Number of cities
        seed: Random seed for reproducibility
        grid_size: Cities are placed in [0, grid_size] x [0, grid_size]

    Returns:
        distances: n x n symmetric distance matrix (list of lists)
    """
    if seed is not None:
        random.seed(seed)

    # Generate random coordinates
    coords = [(random.uniform(0, grid_size), random.uniform(0, grid_size))
              for _ in range(n_cities)]

    return distance_matrix_from_coords(coords)


def distance_matrix_from_coords(coords):
    """
    Compute Euclidean distance matrix from (x, y) coordinates.

    Args:
        coords: List of (x, y) tuples

    Returns:
        distances: n x n symmetric distance matrix with integer distances
    """
    n = len(coords)
    distances = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist = int(round(math.sqrt(dx * dx + dy * dy)))
            distances[i][j] = dist
            distances[j][i] = dist

    return distances


if __name__ == "__main__":
    # Demo: generate and print a small instance
    distances = random_euclidean_tsp(5, seed=42)
    print("Distance matrix for 5 cities:")
    for row in distances:
        print(row)
