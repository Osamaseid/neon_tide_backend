# Neon Tide Night Kayaking API

A FastAPI backend for managing lunar-responsive tour availability and dynamic fleet allocation.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

## Environment Variables (`.env`)

| Variable          | Default | Description                              |
|-------------------|---------|------------------------------------------|
| `MAX_WIND_KNOTS`  | `15`    | Safety wind threshold in knots           |
| `MOCK_WIND_SPEED` | `12`    | Simulated current wind speed (mock)      |

Set `MOCK_WIND_SPEED=16` to test the wind-block (503) response.

## Endpoints

### `POST /check-availability`

**Request body:**
```json
{
  "group_size": 3,
  "participant_weights": [180, 200, 190],
  "booking_date": "2026-02-17"
}
```

**Response:**
```json
{
  "status": "available",
  "fleet": {
    "allocations": [...],
    "vessels_used": {...},
    "vessels_remaining": {...}
  },
  "pricing": {
    "moon_phase_pct": 1.2,
    "days_from_new_moon": 0.3,
    "pricing_label": "New Moon Premium (+25%)",
    "base_price": 100.0,
    "final_price": 125.0
  }
}
```

## Fleet Manifest

| Vessel         | Count | Max Weight |
|----------------|-------|------------|
| Single Kayak   | 5     | 250 lbs    |
| Tandem Kayak   | 3     | 500 lbs    |
| Paddleboard    | 2     | 220 lbs    |

Allocation priority: single kayak → tandem kayak → paddleboard.

## Lunar Pricing

| Window                        | Adjustment |
|-------------------------------|------------|
| New Moon (±3 days)            | +25%       |
| Full Moon (>90% illumination) | −15%       |
| All other dates               | Standard   |

## Tests

```bash
# Unit tests
pytest tests/

# HTTP Client tests — open requests/api_tests.http in PyCharm and click "Run All"
```
