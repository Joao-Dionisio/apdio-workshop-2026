"""
First model in PySCIPOpt.

    max  3x + 2y
    s.t. x + y  <= 1
         2x + y <= 2
         x, y in {0, 1}
"""

from pyscipopt import Model


def first_model():
    """Build and return (model, x, y) for the binary IP above.

    Steps:
        1. Create a Model:          model = Model("first")
        2. Add binary variables:    x = model.addVar(name="x", vtype="B")
                                    (do the same for y)
        3. Set the objective:       model.setObjective(3*x + 2*y, "maximize")
        4. Add the two constraints: model.addCons(x + y <= 1)
                                    (do the same for the second constraint)
        5. Return:                  return model, x, y
    """
    # EXERCISE 1: Build the model and return model, x, y

    raise NotImplementedError("Exercise 1: Build a small binary IP.")
