from fastapi import APIRouter, HTTPException

from app.fleet_logic import allocate_vessels
from app.logger_config import logger
from app.lunar_logic import calculate_lunar_price
from app.schemas import AvailabilityRequest
from app.weather_guard import validate_weather

router = APIRouter(tags=["Availability"])


@router.post("/check-availability", summary="Check tour availability and pricing")
def check_availability(request: AvailabilityRequest) -> dict:
    validate_weather()

    if request.group_size != len(request.participant_weights):
        raise HTTPException(
            status_code=422,
            detail="group_size must equal the number of entries in participant_weights.",
        )

    # Sanitize user input before logging to prevent log injection (CWE-117)
    safe_date = request.booking_date.replace("\n", "").replace("\r", "")
    logger.info("Availability check | date=%s | group=%d", safe_date, request.group_size)

    try:
        fleet_data = allocate_vessels(request.participant_weights)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    lunar_data = calculate_lunar_price(request.booking_date)

    return {
        "status": "available",
        "fleet": fleet_data,
        "pricing": lunar_data,
    }
