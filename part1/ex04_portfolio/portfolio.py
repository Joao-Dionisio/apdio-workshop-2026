"""
Portfolio optimization.

Exercise 4: Build a portfolio optimization model (QP).

An investor wants to allocate capital among n assets to minimize
portfolio risk (variance) while achieving a minimum expected return.

Formulation:
    min  t
    s.t. t >= sum_i sum_j sigma_ij * x_i * x_j    (variance)
         sum_i mu_i * x_i >= r_min                 (return target)
         sum_i x_i = 1                              (budget)
         0 <= x_i <= 1                              (no short-selling)

where sigma_ij is the covariance between assets i and j, mu_i is the
expected return of asset i, and r_min is the minimum required return.
The auxiliary variable t is used because SCIP requires a linear objective.
"""

from pyscipopt import Model, quicksum


def portfolio(expected_returns, covariance, r_min):
    """
    Build and return a portfolio optimization QP.

    Args:
        expected_returns: List of expected returns for each asset (length n).
        covariance: n x n covariance matrix (list of lists).
                    covariance[i][j] is Cov(asset_i, asset_j).
        r_min: Minimum required expected return for the portfolio.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        x: Dict mapping asset index i to continuous variable.
    """
    # =========================================================================
    # EXERCISE 4: Build a portfolio optimization QP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add continuous variables x[i] in [0, 1] for each asset
    #
    # Step 3: Add an auxiliary variable t >= 0 with objective coefficient 1
    #         (SCIP does not support nonlinear objectives directly,
    #          so we minimize t and constrain t >= variance)
    #
    # Step 4: Add the budget constraint
    #         sum_i x[i] == 1
    #
    # Step 5: Add the return constraint
    #         sum_i expected_returns[i] * x[i] >= r_min
    #
    # Step 6: Add the quadratic constraint linking t to the variance
    #         t >= sum_i sum_j covariance[i][j] * x[i] * x[j]
    #
    # Step 7: Return model, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 4: Build a portfolio optimization QP.\n"
        "Hint: Use an auxiliary variable t with obj=1 and a quadratic\n"
        "constraint t >= x^T Sigma x (SCIP needs a linear objective)."
    )
