"""
Nonlinear blending (pooling problem).

Sources flow into a pool, then out to products. Direct bypass is also allowed.
The pool quality l is the weighted average of source qualities — this creates
bilinear terms that make it a nonconvex NLP.

    max  revenue - cost
    s.t. sum_s x[s] = sum_p y[p]                              (pool balance)
         l * sum_s x[s] = sum_s q_s * x[s]                    (pool quality)
         l * y[p] + sum_s q_s * z[s,p] <= max_q_p * d[p]      for all p
         d[p] = y[p] + sum_s z[s,p]                            for all p

PySCIPOpt handles bilinear terms (l * x[s]) natively.
"""

from pyscipopt import Model, quicksum


def blending(sources, products):
    """Build and return a pooling/blending NLP.

    Args:
        sources:  list of dicts with keys "cost" and "quality".
        products: list of dicts with keys "revenue" and "max_quality".

    Variables: x[s] (source→pool), y[p] (pool→product), z[s,p] (bypass),
              l (pool quality), d[p] (total delivery).

    Returns:
        (model, x, y, z, l)
    """
    S = range(len(sources))
    P = range(len(products))

    model = Model("blending")

    # EXERCISE 8: Create variables, set objective, add constraints

    raise NotImplementedError("Exercise 8: Build a pooling/blending NLP.")
