"""
Nonlinear blending (pooling problem).

Exercise 5: Build a pooling problem with bilinear constraints.

Blend raw materials through a mixing pool to make products with quality
specifications. The objective is linear (maximize profit), but the pool
quality variable introduces bilinear terms in the constraints.

Formulation:
    max  sum_p r_p * d_p  -  sum_s c_s * (x_s + sum_p z_sp)
    s.t. sum_s x_s = sum_p y_p                        (pool balance)
         lambda * sum_s x_s = sum_s q_s * x_s          (pool quality)
         lambda * y_p + sum_s q_s * z_sp <= qbar_p * d_p   for all p  (product quality)
         d_p = y_p + sum_s z_sp                         for all p  (product demand)
         x_s, y_p, z_sp >= 0,  lambda >= 0

where lambda is the pool quality, x_s is flow from source s to pool,
y_p is flow from pool to product p, and z_sp is direct bypass flow.
The terms lambda * x_s and lambda * y_p are bilinear (nonconvex NLP).
"""

from pyscipopt import Model, quicksum


def blending(sources, products):
    """Build and return a pooling/blending NLP.

    sources: list of dicts with keys "cost" and "quality"
    products: list of dicts with keys "revenue" and "max_quality"

    Return model, x, y, z, lam (not yet optimized).
    """
    n_sources = len(sources)
    n_products = len(products)

    # =========================================================================
    # EXERCISE 5: Build a pooling problem
    # =========================================================================
    #
    # The objective is linear, but the pool quality definition and
    # product quality limits involve bilinear terms (lambda * flow).
    # SCIP can handle these as nonlinear constraints.
    #
    # Return model, x, y, z, lam
    #
    # =========================================================================

    raise NotImplementedError("Exercise 5: Build a pooling/blending NLP.")
