"""
Solving a model and inspecting solutions.

Exercise 2: Solve a given model and extract solution information.

Given a pre-built PySCIPOpt Model, optimize it and return a dictionary
containing the solution status, objective value, variable values,
number of branch-and-bound nodes, and solving time.
"""

from pyscipopt import Model


def solve_and_report(model):
    """Optimize the given model and return solution statistics."""
    # =========================================================================
    # EXERCISE 2: Solve and inspect a model
    # =========================================================================
    #
    # Step 1: Optimize the model
    #         model.optimize()
    #
    # Step 2: Get the solving status
    #         model.getStatus()  ->  "optimal", "infeasible", etc.
    #
    # Step 3: Get the objective value
    #         model.getObjVal()
    #
    # Step 4: Get variable values
    #         Iterate over model.getVars() and call model.getVal(var)
    #         Use var.name as the key
    #
    # Step 5: Get statistics
    #         model.getNNodes()  -> number of B&B nodes
    #         model.getSolvingTime()  -> time in seconds
    #
    # Step 6: Return the dictionary
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 2: Solve the model and return solution statistics.\n"
        "Hint: Call model.optimize(), then use getStatus(), getObjVal(),\n"
        "getVars(), getVal(), getNNodes(), getSolvingTime()."
    )
