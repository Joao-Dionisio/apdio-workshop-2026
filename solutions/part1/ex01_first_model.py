"""Solution for Exercise 1: First Model."""

from pyscipopt import Model


def first_model():
    model = Model("FirstModel")

    x = model.addVar(name="x", vtype="B", obj=3)
    y = model.addVar(name="y", vtype="B", obj=2)

    model.addCons(x + y <= 1)
    model.addCons(2 * x + y <= 2)

    model.setMaximize()

    return model, x, y
