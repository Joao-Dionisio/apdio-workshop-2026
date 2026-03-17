"""
Indicator constraints for generator scheduling.

Exercise 9: Model a generator scheduling problem using indicator constraints.

A set of generators must meet a total electricity demand. Each generator has
a fixed startup cost, a variable cost per MW, and minimum/maximum output levels.
If a generator is turned on, it must produce at least its minimum output.

Compare two approaches:
  1. Big-M formulation (standard linearization)
  2. Indicator constraints (model.addConsIndicator)
"""

from pyscipopt import Model, quicksum


def generator_scheduling_bigm(demand, fixed_costs, var_costs, p_min, p_max):
    """Model generator scheduling using big-M constraints.

    Returns:
        (model, y, p) — the unsolved model, binary on/off dict y[i], and continuous output dict p[i].
    """
    # =========================================================================
    # EXERCISE 9a: Big-M formulation
    # =========================================================================
    #
    # Formulation:
    #   min  sum_i (fixed_costs[i] * y[i] + var_costs[i] * p[i])
    #   s.t. sum_i p[i] >= demand
    #        p[i] <= p_max[i] * y[i]     for all i
    #        p[i] >= p_min[i] * y[i]     for all i
    #        y[i] in {0,1}, p[i] >= 0
    #
    # =========================================================================

    n_generators = len(fixed_costs)

    model = Model("generator_bigm")

    raise NotImplementedError("Exercise 9a: Build the big-M formulation.")


def generator_scheduling_indicator(demand, fixed_costs, var_costs, p_min, p_max):
    """Model generator scheduling using indicator constraints.

    Returns:
        (model, y, p) — the unsolved model, binary on/off dict y[i], and continuous output dict p[i].
    """
    # =========================================================================
    # EXERCISE 9b: Indicator constraint formulation
    # =========================================================================
    #
    # Same variables and objective as big-M, but replace the linking
    # constraints with indicator constraints:
    #   model.addConsIndicator(cons, binvar)
    #
    # =========================================================================

    n_generators = len(fixed_costs)

    model = Model("generator_indicator")

    raise NotImplementedError("Exercise 9b: Build the indicator constraint formulation.")
