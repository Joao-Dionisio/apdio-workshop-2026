"""
Nonlinear blending (pooling problem).

Exercise 8: Build a pooling problem with bilinear constraints.

Sources flow into a pool, then out to products. Direct bypass is also allowed.
The pool quality l is the weighted average of source qualities — this creates
bilinear terms (l * x[s], l * y[p]) that make it a nonconvex NLP.

Formulation:
    max  sum_p products[p]["revenue"] * d[p]
       - sum_s sources[s]["cost"] * (x[s] + sum_p z[s,p])

    s.t. sum_s x[s] = sum_p y[p]                                   (pool balance)
         l * sum_s x[s] = sum_s sources[s]["quality"] * x[s]       (pool quality)
         l * y[p] + sum_s sources[s]["quality"] * z[s,p]
             <= products[p]["max_quality"] * d[p]                    for all p
         d[p] = y[p] + sum_s z[s,p]                                 for all p
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
    S = range(len(sources))
    P = range(len(products))

    model = Model("blending")

    # =========================================================================
    # EXERCISE 8: Build the pooling/blending NLP
    # =========================================================================
    #
    # Step 1: Create variables (all continuous, lb=0)
    #         x[s]    — source s to pool
    #         y[p]    — pool to product p
    #         z[s,p]  — direct bypass, source s to product p
    #         l       — pool quality (use name "l" since "lambda" is reserved)
    #         d[p]    — total delivery to product p
    #
    # Step 2: Set objective (maximize revenue - cost)
    #         model.setObjective(revenue - cost, "maximize")
    #
    # Step 3: Add constraints
    #         - Pool balance: quicksum(x[s] for s in S) == quicksum(y[p] for p in P)
    #         - Pool quality definition (bilinear!):
    #           l * quicksum(x[s] for s in S) == quicksum(q_s * x[s] for s in S)
    #         - Product quality (bilinear!), for each p:
    #           l * y[p] + quicksum(q_s * z[s,p] for s in S) <= max_q_p * d[p]
    #         - Product demand definition, for each p:
    #           d[p] == y[p] + quicksum(z[s,p] for s in S)
    #
    # Note: PySCIPOpt handles bilinear terms like l * x[s] natively.
    #       Just write them as Python expressions; SCIP solves the resulting
    #       nonconvex problem to global optimality via spatial branch-and-bound.
    #
    # =========================================================================

    raise NotImplementedError("Exercise 8: Build a pooling/blending NLP.")
