"""
Nonlinear blending (pooling problem).

Exercise 8: Build a pooling problem with bilinear constraints.

Sources flow into a pool, then out to products. Direct bypass is also allowed.
The pool quality l is the weighted average of source qualities — this creates
bilinear terms (l * x[s], l * y[p]) that make it a nonconvex NLP.

See the slides and README for the full formulation.
"""

from pyscipopt import Model, quicksum


def blending(sources, products):
    """Build and return a pooling/blending NLP.

    Args:
        sources:  list of dicts with keys "cost" and "quality".
        products: list of dicts with keys "revenue" and "max_quality".

    Variables to create:
        x[s]    — flow from source s to pool          (>= 0)
        y[p]    — flow from pool to product p          (>= 0)
        z[s,p]  — direct bypass, source s to product p (>= 0)
        l       — pool quality (continuous, >= 0)
        d[p]    — total delivery to product p  = y[p] + sum_s z[s,p]

    Returns:
        (model, x, y, z, l) — the unsolved model and variable dicts/variable.
    """
    n_sources = len(sources)
    n_products = len(products)

    model = Model("blending")

    raise NotImplementedError("Exercise 8: Build a pooling/blending NLP.")
