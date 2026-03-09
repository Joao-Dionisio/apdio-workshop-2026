"""
Random portfolio optimization instance generator.
"""

import random
import math


def random_portfolio_instance(n_assets, seed=0):
    """
    Generate a random portfolio optimization instance.

    Creates a valid positive semi-definite covariance matrix using
    random factor loadings: Sigma = F @ F^T + diag(d).

    Args:
        n_assets: Number of assets.
        seed: Random seed for reproducibility.

    Returns:
        expected_returns: List of expected returns (length n_assets).
        covariance: n x n covariance matrix (list of lists).
        r_min: Minimum required expected return.
    """
    random.seed(seed)

    # Expected returns between 2% and 15%
    expected_returns = [random.uniform(0.02, 0.15) for _ in range(n_assets)]

    # Generate PSD covariance via factor model: Sigma = F F^T + D
    n_factors = max(2, n_assets // 3)
    F = [[random.gauss(0, 0.05) for _ in range(n_factors)]
         for _ in range(n_assets)]

    covariance = [[0.0] * n_assets for _ in range(n_assets)]
    for i in range(n_assets):
        for j in range(n_assets):
            cov_ij = sum(F[i][k] * F[j][k] for k in range(n_factors))
            covariance[i][j] = cov_ij

    # Add diagonal noise to ensure strict positive definiteness
    for i in range(n_assets):
        covariance[i][i] += random.uniform(0.001, 0.01)

    # Target return: average of expected returns
    r_min = sum(expected_returns) / n_assets

    return expected_returns, covariance, r_min


if __name__ == "__main__":
    mu, sigma, r_min = random_portfolio_instance(4, seed=42)
    print(f"Expected returns: {[f'{r:.3f}' for r in mu]}")
    print(f"Min return target: {r_min:.3f}")
    print("Covariance matrix:")
    for row in sigma:
        print([f"{v:.5f}" for v in row])
