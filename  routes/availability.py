from fastapi import APIRouter, HTTPException

from app.schemas import AvailabilityRequest
from app.fleet_logic import allocate_vessels
from app.lunar_logic import calculate_lunar_price
from app.weather_guard import validate_weather_conditions

router = APIRouter()


@router.post("/check-availability")
def check_availability(
    request: AvailabilityRequest
):

    validate_weather_conditions()

    if (
        request.group_size
        != len(request.participant_weights)
    ):
        raise HTTPException(
            status_code=400,
            detail="Group size mismatch."
        )

    try:

        fleet_data = allocate_vessels(
            request.participant_weights
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    lunar_data = calculate_lunar_price(
        request.booking_date
    )

    return {
        "fleet": fleet_data,
        "pricing": lunar_data
    }