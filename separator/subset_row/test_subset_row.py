"""
Test for subset row separator integrated with branch-price-and-cut.

Run from repo root:
    python separator/subset_row/test_subset_row.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "branch_and_price"))

from subset_row import SubsetRowSeparator
from bnp import extended_binpacking
from generator import random_bin_packing_instance


def test_bpc_small():
    """BPC on a small instance should solve to optimality."""
    capacity = 100
    sizes = random_bin_packing_instance(15, capacity, seed=42)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print(f"PASS: test_bpc_small (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


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
    """BPC on another random instance."""
    capacity = 100
    sizes = random_bin_packing_instance(15, capacity, seed=7)

    separator = SubsetRowSeparator(len(sizes))
    model, *_ = extended_binpacking(sizes, capacity, separator=separator)
    model.optimize()

    assert model.getStatus() == "optimal", f"Expected optimal, got {model.getStatus()}"
    print(f"PASS: test_bpc_different_seed (obj={model.getObjVal()}, cuts={len(separator.cuts)})")


if __name__ == "__main__":
    test_bpc_small()
    test_bpc_matches_bnp()
    test_bpc_different_seed()
    print("All subset row tests passed!")
