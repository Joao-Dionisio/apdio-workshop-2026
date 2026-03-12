"""
Initial columns for column generation.

Exercise 0: Generate the initial set of columns (patterns) for the
branch-and-price algorithm.

Column generation needs a feasible starting point. The simplest approach
is the one-item-per-bin strategy: for each item, create a pattern containing
only that item. This gives n initial patterns and a trivially feasible
(though poor) solution.
"""


def initial_columns(n_items):
    """
    Generate initial columns for the bin packing RMP.

    For each item i, produce a pattern containing only item i.

    Args:
        n_items: Number of items in the instance.

    Returns:
        List of lists, where each inner list contains the item indices
        in that pattern. E.g., for 3 items: [[0], [1], [2]]
    """
    # =========================================================================
    # EXERCISE 0: Generate initial columns
    # =========================================================================
    #
    # For each item i in range(n_items), create a pattern [i].
    # Return the list of all patterns.
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 0: Generate initial columns.\n"
        "Hint: Return [[0], [1], ..., [n_items-1]]"
    )
