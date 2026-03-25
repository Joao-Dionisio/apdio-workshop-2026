from bnp import extended_binpacking
from generator import random_bin_packing_instance

def test_bnp():
    capacity = 100
    sizes = random_bin_packing_instance(100, capacity)

    model, *_ = extended_binpacking(sizes, capacity)
    model.optimize()

    assert abs(model.getObjVal() - 52) < 1e-6


def test_bnp_small():
    """Small instance (20 items) should solve quickly."""
    capacity = 100
    sizes = random_bin_packing_instance(20, capacity, seed=42)

    model, *_ = extended_binpacking(sizes, capacity)
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert model.getObjVal() >= 1, f"Expected at least 1 bin, got {model.getObjVal()}"
    print(f"[92mPASS:[0m test_bnp_small (obj={model.getObjVal()})")


def test_bnp_different_seed():
    """Different random instance with seed=7."""
    capacity = 100
    sizes = random_bin_packing_instance(50, capacity, seed=7)

    model, *_ = extended_binpacking(sizes, capacity)
    model.optimize()

    status = model.getStatus()
    assert status == "optimal", f"Expected optimal, got {status}"
    assert model.getObjVal() >= 1, f"Expected at least 1 bin, got {model.getObjVal()}"
    print(f"[92mPASS:[0m test_bnp_different_seed (obj={model.getObjVal()})")


if __name__ == "__main__":
    test_bnp()
    test_bnp_small()
    test_bnp_different_seed()
    print("bnp test passed!")