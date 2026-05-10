import os

from dotenv import load_dotenv
from fastapi import HTTPException

from app.config import MAX_WIND_KNOTS

load_dotenv()

# In production replace with a live weather API call.
# Reads from env so tests can override via MOCK_WIND_SPEED.
_wind_speed: float = float(os.getenv("MOCK_WIND_SPEED", 12))


def validate_weather() -> None:
    """
    Enforce the wind speed safety threshold before allowing a booking.

    Reads the current wind speed from the ``MOCK_WIND_SPEED`` environment variable
    (default 12 knots). In production this value should be replaced with a live
    call to a weather API (e.g. Open-Meteo or OpenWeatherMap).

    The safety threshold is sourced from ``MAX_WIND_KNOTS`` in ``app.config``
    and can be overridden via the ``MAX_WIND_KNOTS`` environment variable.

    Raises:
        HTTPException(503): When wind speed exceeds the configured safety limit,
                            indicating the tour is temporarily unavailable.
    """
    if _wind_speed > MAX_WIND_KNOTS:
        raise HTTPException(
            status_code=503,
            detail=(
                f"Tour unavailable: wind speed {_wind_speed} kn "
                f"exceeds safety limit of {MAX_WIND_KNOTS} kn."
            ),
        )
