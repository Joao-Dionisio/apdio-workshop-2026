"""
Solver parameters.

Exercise 3: Learn to configure SCIP before solving.

Two functions, each teaching a distinct skill:
  (a) solve_with_params  — apply parameter settings to an existing model
  (b) load_and_solve     — read a model from file, configure, and solve
"""

from pyscipopt import Model


def solve_with_params(model, params):
    """Apply SCIP parameters, solve, and return results.

    Args:
        model:  A pre-built (unsolved) PySCIPOpt Model.
        params: A dict mapping SCIP parameter names to values, e.g.
                {"limits/time": 60, "limits/gap": 0.01}

    Returns:
        A dict with keys:
            "status"    — str, e.g. "optimal", "timelimit" (model.getStatus())
            "objective" — float or None if no solution found
            "gap"       — float (model.getGap()), 0.0 if optimal
            "n_nodes"   — int  (model.getNNodes())
            "time"      — float in seconds (model.getSolvingTime())
    """
    # =========================================================================
    # EXERCISE 3a: Apply parameters and solve
    # =========================================================================
    #
    # Step 1: Apply each parameter from the dict
    #         model.setParam(name, value)
    #
    # Step 2: Optimize
    #
    # Step 3: Build and return the results dict
    #         - Use model.getNSols() > 0 to check if a solution exists
    #           before calling getObjVal()
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3a: Apply parameters from the dict and solve the model.\n"
        "Hint: loop over params.items() and call model.setParam(name, value)."
    )


def load_and_solve(filepath, params=None):
    """Load a model from an MPS/LP file, apply parameters, and solve.

    Args:
        filepath: Path to an .mps, .mps.gz, .lp, or .lp.gz file.
        params:   Optional dict of SCIP parameters (same format as above).

    Returns:
        Same dict format as solve_with_params:
            "status", "objective", "gap", "n_nodes", "time"
    """
    # =========================================================================
    # EXERCISE 3b: Load from file and solve
    # =========================================================================
    #
    # Step 1: Create a new Model()
    #
    # Step 2: Load the problem
    #         model.readProblem(filepath)
    #
    # Step 3: Apply parameters (if provided) and solve
    #         Hint: you can call solve_with_params() here!
    #
    # =========================================================================

    raise NotImplementedError(
        "Exercise 3b: Load a model from file and solve.\n"
        "Hint: Model(), readProblem(filepath), then reuse solve_with_params()."
    )
