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

    Use: Model(), addVar(vtype="B", obj=...), addCons(), setMaximize()
    """
    # EXERCISE 1: Build the model and return model, x, y

    m = Model()
    x = m.addVar(vtype="B", obj=3)
    y = m.addVar(vtype="B", obj=2)
    m.addCons(x + y <= 1)
    m.addCons(2 * x + y <= 2)
    m.setMaximize()

    return m, x, y
    raise NotImplementedError("Exercise 1: Build a small binary IP.")
