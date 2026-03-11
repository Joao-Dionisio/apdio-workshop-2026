"""
Bin packing problem.

Exercise 8: Build a bin packing IP.

Given a set of items with sizes and a collection of bins with a fixed capacity,
assign each item to exactly one bin so that no bin's capacity is exceeded,
using the minimum number of bins.

Formulation:
    min  sum_b y_b
    s.t. sum_b x_{ib} = 1           for all items i      (assignment)
         sum_i s_i * x_{ib} <= C * y_b   for all bins b  (capacity)
         x_{ib} in {0, 1}
         y_b in {0, 1}
"""

from pyscipopt import Model, quicksum


def bin_packing(sizes, capacity):
    """Build and return a bin packing IP.

    Args:
        sizes: List of item sizes.
        capacity: Capacity of each bin.

    Returns:
        model: PySCIPOpt Model (not yet optimized).
        x: Dict mapping (i, b) to binary assignment variables.
        y: Dict mapping bin index b to binary usage variables.
    """
    n = len(sizes)

    # =========================================================================
    # EXERCISE 8: Build a bin packing IP
    # =========================================================================
    #
    # Use n as an upper bound on the number of bins (one item per bin).
    #
    # Variables:
    #   y[b] in {0,1}: whether bin b is used
    #   x[i,b] in {0,1}: whether item i is assigned to bin b
    #
    # Constraints:
    #   1. Each item is assigned to exactly one bin
    #   2. The total size of items in each bin does not exceed the capacity
    #      (only if the bin is open)
    #
    # Objective: minimize the number of bins used
    #
    # Return model, x, y
    #
    # =========================================================================

    raise NotImplementedError("Exercise 8: Build a bin packing IP.")
