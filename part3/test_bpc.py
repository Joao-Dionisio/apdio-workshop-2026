"""
Test for Branch-Price-and-Cut.

Run from branch_and_price/:
    python test_bpc.py
"""
from bnp import extended_binpacking
from generator import random_bin_packing_instance
from subset_row import SubsetRowSeparator


def test_bpc():
    """BPC should solve a small instance to optimality."""
    capacity = 100
    sizes = random_bin_packing_instance(20, capacity)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 1, f"Expected at least 1 bin, got {model.getObjVal()}"
    print(f"PASS: test_bpc (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


def test_bpc_matches_bnp():
    """BPC should give same or better objective than B&P."""
    capacity = 100
    sizes = random_bin_packing_instance(20, capacity, seed=0)

    # B&P without cuts
    model_bnp, *_ = extended_binpacking(sizes, capacity)
    model_bnp.optimize()
    obj_bnp = model_bnp.getObjVal()

    # BPC with cuts
    separator = SubsetRowSeparator(len(sizes))
    model_bpc, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model_bpc.optimize()
    obj_bpc = model_bpc.getObjVal()

    assert obj_bpc <= obj_bnp + 1e-6, (
        f"BPC obj ({obj_bpc}) should be <= B&P obj ({obj_bnp})")
    print(f"PASS: test_bpc_matches_bnp (B&P={obj_bnp}, BPC={obj_bpc}, cuts={len(separator.cuts)})")


def test_bpc_different_seed():
    """BPC on a different small instance."""
    capacity = 100
    sizes = random_bin_packing_instance(20, capacity, seed=42)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    assert model.getObjVal() >= 1, f"Expected at least 1 bin, got {model.getObjVal()}"
    print(f"PASS: test_bpc_different_seed (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


def test_bpc_small():
    """BPC on a small 15-item instance."""
    capacity = 100
    sizes = random_bin_packing_instance(15, capacity, seed=42)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print(f"PASS: test_bpc_small (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


def test_bpc_seed7():
    """BPC on another random instance."""
    capacity = 100
    sizes = random_bin_packing_instance(15, capacity, seed=7)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print(f"PASS: test_bpc_seed7 (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


if __name__ == "__main__":
    tests = [test_bpc, test_bpc_matches_bnp, test_bpc_different_seed,
             test_bpc_small, test_bpc_seed7]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except NotImplementedError as e:
            print(f"SKIP: {test.__name__} - Exercise not implemented yet")
            print(f"      {e}")
            failed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__}")
            print(f"      {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}")
            print(f"       {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
