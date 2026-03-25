"""
Indicator constraints for generator scheduling.

Each generator has a fixed startup cost, variable cost per MW, and min/max output.
If on, it must produce at least its minimum output.

Compare: big-M formulation vs indicator constraints (model.addConsIndicator).
"""

from pyscipopt import Model, quicksum


def generator_scheduling_bigm(demand, fixed_costs, var_costs, p_min, p_max):
    """Model generator scheduling using big-M constraints.

    Returns:
        (model, y, p) — model, binary on/off dict y[i], continuous output dict p[i].

    Formulation:
        min  sum_i (fixed_costs[i]*y[i] + var_costs[i]*p[i])
        s.t. sum_i p[i] >= demand
             p_min[i]*y[i] <= p[i] <= p_max[i]*y[i]
    """
    # EXERCISE 9a: Big-M formulation

    n_generators = len(fixed_costs)

    model = Model("generator_bigm")

    raise NotImplementedError("Exercise 9a: Build the big-M formulation.")


def generator_scheduling_indicator(demand, fixed_costs, var_costs, p_min, p_max):
    """Model generator scheduling using indicator constraints.

    Same as big-M, but replace linking constraints with:
        model.addConsIndicator(cons, binvar)

    Returns:
        (model, y, p)
    """
    # EXERCISE 9b: Indicator constraint formulation

    n_generators = len(fixed_costs)

    model = Model("generator_indicator")

    raise NotImplementedError("Exercise 9b: Build the indicator constraint formulation.")
