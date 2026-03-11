"""
Solver parameters and emphasis settings.

Exercise 3: Experiment with SCIP's solver parameters.

Given a PySCIPOpt Model, apply parameter settings and compare
their effect on solving behavior.
"""

from pyscipopt import Model


def solve_with_time_limit(model, time_limit):
    """Set a time limit and solve the model. Return a dict with
    status, objective, gap, and time."""
    # =========================================================================
    # EXERCISE 3a: Solve with a time limit
    # =========================================================================
    #
    # Step 1: Set the time limit parameter
    #         model.setParam("limits/time", time_limit)
    #
    # Step 2: Optimize the model
    #
    # Step 3: Get the status, objective, gap, and time
    #         model.getStatus()
    #         model.getObjVal()  — only if a solution exists (getNSols() > 0)
    #         model.getGap()
    #         model.getSolvingTime()
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3a: Set a time limit and solve the model.\n"
        "Hint: Use model.setParam('limits/time', time_limit)"
    )


def solve_with_gap_limit(model, gap):
    """Set an optimality gap limit and solve the model. Return a dict with
    status, objective, gap, and n_nodes."""
    # =========================================================================
    # EXERCISE 3b: Solve with an optimality gap limit
    # =========================================================================
    #
    # Step 1: Set the gap limit parameter
    #         model.setParam("limits/gap", gap)
    #
    # Step 2: Optimize and return results
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3b: Set a gap limit and solve the model.\n"
        "Hint: Use model.setParam('limits/gap', gap)"
    )


def solve_with_emphasis(model, emphasis):
    """Set an emphasis setting and solve the model. Return a dict with
    status, objective, n_nodes, and time."""
    # =========================================================================
    # EXERCISE 3c: Solve with an emphasis setting
    # =========================================================================
    #
    # Step 1: Set the emphasis
    #         model.setEmphasis(emphasis)
    #
    # Step 2: Optimize and return results
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3c: Set an emphasis setting and solve the model.\n"
        "Hint: Use model.setEmphasis(emphasis)"
    )


def load_and_solve(filepath, params=None):
    """Load a model from an MPS or LP file, apply parameters, and solve.
    Return a dict with status, objective, gap, n_nodes, and time."""
    # =========================================================================
    # EXERCISE 3d: Load a model from file and solve with parameters
    # =========================================================================
    #
    # Step 1: Create a Model
    #
    # Step 2: Read the file
    #         model.readProblem(filepath)
    #
    # Step 3: Apply parameters from the dict (if provided)
    #         for name, value in params.items():
    #             model.setParam(name, value)
    #
    # Step 4: Optimize and return results
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3d: Load a model from file and solve with parameters.\n"
        "Hint: Use model.readProblem(filepath) to load, then setParam for each parameter."
    )
