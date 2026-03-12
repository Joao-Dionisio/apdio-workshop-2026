#!/usr/bin/env python3
"""
Main entry point for the TSP row generation tutorial.

This script demonstrates two approaches to solving the Traveling Salesman Problem:

1. Compact MTZ formulation: Uses position variables and polynomial-size
   subtour elimination constraints. Simple but has a weak LP relaxation.

2. Row generation: Uses the stronger degree-2 formulation with exponentially
   many subtour elimination constraints added lazily. Stronger LP bound but
   requires implementing the constraint handler (Exercise 2).

Usage:
    python main.py [--compact] [--cities N] [--seed S]

Options:
    --compact   Use MTZ formulation instead of row generation
    --cities N  Number of cities (default: 20)
    --seed S    Random seed (default: 42)
"""

import argparse

from generator import random_euclidean_tsp
from compact_mtz import tsp_mtz
from tsp import tsp_rowgen, extract_tour


def main():
    parser = argparse.ArgumentParser(
        description="TSP solver comparing compact MTZ vs row generation"
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Use compact MTZ formulation instead of row generation"
    )
    parser.add_argument(
        "--cities",
        type=int,
        default=20,
        help="Number of cities (default: 20)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)"
    )
    args = parser.parse_args()

    # Generate instance
    print(f"Generating {args.cities}-city Euclidean TSP (seed={args.seed})...")
    distances = random_euclidean_tsp(args.cities, seed=args.seed)

    # Solve with chosen method
    if args.compact:
        print("\nSolving with compact MTZ formulation...")
        model, x = tsp_mtz(distances)
    else:
        print("\nSolving with row generation (lazy SECs)...")
        print("(Requires completing Exercises 1 and 2)")
        model, x = tsp_rowgen(distances)

    model.optimize()

    # Report results
    if model.getStatus() == "optimal":
        print(f"\nOptimal tour length: {model.getObjVal():.0f}")

        if args.compact:
            # Extract tour from directed MTZ formulation
            n = args.cities
            tour = [0]
            current = 0
            for _ in range(n - 1):
                for j in range(n):
                    if j != current and model.getVal(x[current, j]) > 0.5:
                        tour.append(j)
                        current = j
                        break
            tour.append(0)
        else:
            # Extract tour from undirected row generation formulation
            tour = extract_tour(model, x, args.cities)

        print(f"Tour: {' -> '.join(map(str, tour))}")
    else:
        print(f"\nSolver status: {model.getStatus()}")


if __name__ == "__main__":
    main()
