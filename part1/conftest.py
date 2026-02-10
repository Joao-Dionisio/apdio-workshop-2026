"""
Pytest configuration for Part 1 exercises.

- Adds each test's directory to sys.path so local imports work.
- Clears cached modules to avoid cross-exercise import conflicts.
- Converts NotImplementedError into pytest.skip (exercises not yet solved).
"""

import sys
import os
import pytest

# Module names used across multiple exercises (each has a different generator)
_LOCAL_MODULES = {
    "generator", "first_model", "solving", "transportation", "blending",
    "set_cover", "knapsack", "facility_location", "graph_coloring",
}


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Ensure each test's own directory is first on sys.path and clear caches."""
    test_dir = os.path.dirname(str(item.fspath))

    # Remove stale cached modules so each exercise gets its own imports
    for mod_name in list(sys.modules):
        if mod_name in _LOCAL_MODULES:
            del sys.modules[mod_name]

    # Put this test's directory at the front
    if test_dir in sys.path:
        sys.path.remove(test_dir)
    sys.path.insert(0, test_dir)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """Convert NotImplementedError into pytest.skip."""
    try:
        item.runtest()
    except NotImplementedError as e:
        pytest.skip(f"Exercise not implemented yet: {e}")
    except Exception:
        raise
    else:
        return True
