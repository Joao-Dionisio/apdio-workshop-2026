"""Solution for Exercise 0: Initial Columns."""


def initial_columns(n_items):
    """Generate initial columns for the bin packing RMP.

    Returns:
        List of lists, e.g. for 3 items: [[0], [1], [2]]
    """
    return [[i] for i in range(n_items)]
