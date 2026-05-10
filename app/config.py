from typing import TypedDict


class VesselSpec(TypedDict):
    count: int
    max_weight: float
    capacity: int  # persons per vessel


FLEET_MANIFEST: dict[str, VesselSpec] = {
    "single_kayak":  {"count": 5, "max_weight": 250.0, "capacity": 1},
    "tandem_kayak":  {"count": 3, "max_weight": 500.0, "capacity": 2},
    "paddleboard":   {"count": 2, "max_weight": 220.0, "capacity": 1},
}

BASE_PRICE: float = 100.0
NEW_MOON_PREMIUM: float = 1.25
FULL_MOON_DISCOUNT: float = 0.85
NEW_MOON_PHASE_MAX: float = 6.5   # % illumination — tight new-moon window
FULL_MOON_PHASE_MIN: float = 93.5

MAX_WIND_KNOTS: float = 15.0
