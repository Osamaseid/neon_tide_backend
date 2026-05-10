from datetime import datetime

import ephem

from app.config import BASE_PRICE, FULL_MOON_DISCOUNT, NEW_MOON_PREMIUM


def _days_from_new_moon(date: datetime) -> float:
    """
    Calculate the minimum day distance between the given date and the nearest new moon.

    Uses ephem's Dublin Julian Day arithmetic: subtracting two ephem.Date values
    yields a float representing fractional days elapsed.

    Args:
        date: A naive datetime representing the booking date.

    Returns:
        Fractional days to the nearest new moon (previous or next), rounded to 2 dp.
    """
    d = ephem.Date(date)
    days_since = float(d - ephem.previous_new_moon(d))
    days_until = float(ephem.next_new_moon(d) - d)
    return min(days_since, days_until)


def calculate_lunar_price(booking_date: str) -> dict:
    """
    Derive tour pricing based on the lunar phase for a given booking date.

    Pricing rules:
    - New Moon window (within ±3 days of a new moon): +25% premium.
    - Full Moon (moon illumination > 90%): -15% discount.
    - All other dates: standard base price.

    Uses ``datetime.fromisoformat`` for efficient ISO 8601 parsing.

    Args:
        booking_date: ISO 8601 date string (``YYYY-MM-DD``).

    Returns:
        A dict containing moon_phase_pct, days_from_new_moon, pricing_label,
        base_price, and final_price.
    """
    date = datetime.fromisoformat(booking_date)
    moon = ephem.Moon(date)
    phase: float = round(float(moon.phase), 2)
    days_to_new = round(_days_from_new_moon(date), 2)

    price = BASE_PRICE
    label = "Standard"

    if days_to_new <= 3:
        price *= NEW_MOON_PREMIUM
        label = "New Moon Premium (+25%)"
    elif phase > 90:
        price *= FULL_MOON_DISCOUNT
        label = "Full Moon Discount (-15%)"

    return {
        "moon_phase_pct": phase,
        "days_from_new_moon": days_to_new,
        "pricing_label": label,
        "base_price": BASE_PRICE,
        "final_price": round(price, 2),
    }
