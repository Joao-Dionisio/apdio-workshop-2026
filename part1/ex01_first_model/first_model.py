"""
First model in PySCIPOpt.

Exercise 1: Build a small integer program and return the model.

Formulation:
    max  3x + 2y
    s.t. x + y  <= 1
         2x + y <= 2
         x, y in {0, 1}
"""

from pyscipopt import Model


def first_model():
    """Build and return a PySCIPOpt Model for a small binary IP.

    Returns:
        (model, x, y) — the unsolved model and the two binary variables.

    The model is:
        max  3x + 2y
        s.t. x + y  <= 1
             2x + y <= 2
             x, y in {0, 1}
    """
    # =========================================================================
    # EXERCISE 1: Build your first PySCIPOpt model
    # =========================================================================
    #
    # Step 1: Create a Model object
    #         model = Model("MyFirstModel")
    #
    # Step 2: Add binary variables x and y with their objective coefficients
    #         Use model.addVar(name=..., vtype="B", obj=...)
    #
    # Step 3: Add the two constraints
    #         Use model.addCons(...)
    #
    # Step 4: Set the objective direction to maximize
    #         Use model.setMaximize()
    #
    # Step 5: Return model, x, y
    #
    # =========================================================================

    model = Model("first_model")

    raise NotImplementedError(
        "Exercise 1: Build a small binary IP.\n"
        "Hint: Add two binary variables with obj coefficients,\n"
        "add two constraints, and call setMaximize()."
    )
