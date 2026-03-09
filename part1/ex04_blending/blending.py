"""
Blending problem.

Exercise 4: Build a blending LP.

A manufacturer must blend raw materials to produce a product that meets
quality specifications. Each material has a cost, limited availability,
and known quality attributes. The blend must satisfy both a total
production target and upper/lower bounds on each quality attribute.

Formulation:
    min  sum_i c_i * x_i
    s.t. sum_i x_i = T                                    (total production)
         sum_i q_{iq} * x_i >= lb_q * T   for all q       (quality lower bound)
         sum_i q_{iq} * x_i <= ub_q * T   for all q       (quality upper bound)
         0 <= x_i <= a_i                  for all i       (availability)
"""

from pyscipopt import Model, quicksum


def blending(costs, availability, qualities, quality_lb, quality_ub,
             total_production):
    """
    Build and return a blending LP.

    Args:
        costs: List of per-unit costs (length m).
        availability: List of max available amounts (length m).
        qualities: m x p matrix; qualities[i][q] is the quality-q
                   content per unit of material i.
        quality_lb: List of minimum quality requirements (length p).
                    Expressed as fractions of total production, i.e.
                    the average quality must be >= quality_lb[q].
        quality_ub: List of maximum quality requirements (length p).
        total_production: Total amount to produce.

    Returns:
        model: A PySCIPOpt Model (not yet optimized).
        x: Dict mapping material index i to continuous variable.
    """
    # =========================================================================
    # EXERCISE 4: Build a blending LP
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Add continuous variables x[i] in [0, availability[i]]
    #         with objective coefficient costs[i]
    #
    # Step 3: Add the total production constraint
    #         sum_i x[i] == total_production
    #
    # Step 4: Add quality constraints for each quality attribute q:
    #         Lower: sum_i qualities[i][q] * x[i] >= quality_lb[q] * T
    #         Upper: sum_i qualities[i][q] * x[i] <= quality_ub[q] * T
    #
    # Step 5: Return model, x
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 4: Build a blending LP.\n"
        "Hint: Variables bounded by availability, quality constraints on the blend."
    )
