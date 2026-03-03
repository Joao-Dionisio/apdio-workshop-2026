"""
Test for Branch-Price-and-Cut.

Run from branch_and_price/:
    python test_bpc.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "separator", "subset_row"))

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


if __name__ == "__main__":
    test_bpc()
    test_bpc_different_seed()
    print("BPC test passed!")
