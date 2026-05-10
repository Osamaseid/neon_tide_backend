import pytest

from app.fleet_logic import allocate_vessels


def test_single_kayak_allocation():
    result = allocate_vessels([180.0, 200.0, 220.0])
    assert len(result["allocations"]) == 3
    assert all(a["vessel"] == "single_kayak" for a in result["allocations"])


def test_tandem_kayak_used_when_singles_full():
    # 5 singles filled, 6th person must go to tandem
    weights = [200.0] * 6
    result = allocate_vessels(weights)
    vessels = [a["vessel"] for a in result["allocations"]]
    assert "tandem_kayak" in vessels


def test_overweight_for_all_vessels():
    with pytest.raises(ValueError, match="Fleet capacity exceeded"):
        allocate_vessels([600.0])


def test_capacity_exceeded():
    # 5 singles + 6 tandem slots + 2 paddleboards = 13 max; 14 should fail
    with pytest.raises(ValueError):
        allocate_vessels([150.0] * 14)


def test_vessels_used_count():
    result = allocate_vessels([180.0])
    assert result["vessels_used"]["single_kayak"] == 1


def test_tandem_pair_combined_weight():
    result = allocate_vessels([130.0] * 6)
    tandem_allocs = [a for a in result["allocations"] if a["vessel"] == "tandem_kayak"]
    for alloc in tandem_allocs:
        assert sum(alloc["weights"]) <= 500.0


def test_paddleboard_fallback():
    # Fill 5 singles + 6 tandem slots (3 tandems × 2), 12th person (180 lbs) goes to paddleboard
    # Singles: 5 × 200 lbs. Tandems: pair (220+220), (220+220), (220+220) = 6 slots.
    weights = [200.0] * 5 + [220.0] * 6 + [180.0]
    result = allocate_vessels(weights)
    pb_allocs = [a for a in result["allocations"] if a["vessel"] == "paddleboard"]
    assert len(pb_allocs) >= 1
