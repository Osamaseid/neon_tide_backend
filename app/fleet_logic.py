from typing import List

from app.config import FLEET_MANIFEST


def allocate_vessels(participant_weights: List[float]) -> dict:
    """
    Assign participants to vessels using a greedy weight-first strategy.

    Allocation priority: single_kayak → tandem_kayak → paddleboard.

    Single pass: each participant is placed in a single kayak if their weight
    is within the 250 lb limit and singles remain in inventory.

    Tandem pass: remaining participants are sorted and paired heaviest-with-lightest.
    If a pair's combined weight exceeds 500 lbs, the heaviest is assigned solo to a
    tandem slot. Participants who cannot fit any tandem configuration are deferred.

    Paddleboard pass: deferred participants are assigned to paddleboards (220 lb limit).

    Args:
        participant_weights: List of individual participant weights in lbs.

    Returns:
        A dict with:
        - ``allocations``: list of {vessel, weights} assignment records.
        - ``vessels_used``: count of each vessel type consumed.
        - ``vessels_remaining``: remaining inventory per vessel type.

    Raises:
        ValueError: If one or more participants cannot be assigned to any vessel,
                    either due to weight exceeding all limits or fleet exhaustion.
    """
    remaining = list(participant_weights)
    allocations: list[dict] = []
    inventory = {k: v["count"] for k, v in FLEET_MANIFEST.items()}

    # --- Singles pass ---
    still_unassigned: list[float] = []
    for w in remaining:
        if inventory["single_kayak"] > 0 and w <= FLEET_MANIFEST["single_kayak"]["max_weight"]:
            allocations.append({"vessel": "single_kayak", "weights": [w]})
            inventory["single_kayak"] -= 1
        else:
            still_unassigned.append(w)
    remaining = still_unassigned

    # --- Tandem pass: greedy pair (heaviest + lightest) ---
    still_unassigned = []
    tandem_max = FLEET_MANIFEST["tandem_kayak"]["max_weight"]
    remaining_sorted = sorted(remaining)

    while remaining_sorted and inventory["tandem_kayak"] > 0:
        heaviest = remaining_sorted.pop()  # largest
        if not remaining_sorted:
            # lone heavy person — try to fit solo in tandem
            if heaviest <= tandem_max:
                allocations.append({"vessel": "tandem_kayak", "weights": [heaviest]})
                inventory["tandem_kayak"] -= 1
            else:
                still_unassigned.append(heaviest)
            break
        lightest = remaining_sorted[0]
        if heaviest + lightest <= tandem_max:
            remaining_sorted.pop(0)
            allocations.append({"vessel": "tandem_kayak", "weights": [heaviest, lightest]})
            inventory["tandem_kayak"] -= 1
        elif heaviest <= tandem_max:
            # pair doesn't fit together; assign heaviest solo
            allocations.append({"vessel": "tandem_kayak", "weights": [heaviest]})
            inventory["tandem_kayak"] -= 1
        else:
            still_unassigned.append(heaviest)

    still_unassigned.extend(remaining_sorted)
    remaining = still_unassigned

    # --- Paddleboard pass ---
    still_unassigned = []
    for w in remaining:
        if inventory["paddleboard"] > 0 and w <= FLEET_MANIFEST["paddleboard"]["max_weight"]:
            allocations.append({"vessel": "paddleboard", "weights": [w]})
            inventory["paddleboard"] -= 1
        else:
            still_unassigned.append(w)

    if still_unassigned:
        raise ValueError(
            f"Fleet capacity exceeded. Could not assign {len(still_unassigned)} participant(s): "
            f"{still_unassigned}"
        )

    return {
        "allocations": allocations,
        "vessels_used": {
            k: FLEET_MANIFEST[k]["count"] - inventory[k]
            for k in FLEET_MANIFEST
        },
        "vessels_remaining": inventory,
    }
