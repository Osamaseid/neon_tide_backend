from typing import List

from pydantic import BaseModel, Field, field_validator


class AvailabilityRequest(BaseModel):
    group_size: int = Field(..., ge=1, le=11, description="Number of participants (1–11)")
    participant_weights: List[float] = Field(..., description="Weight of each participant in lbs")
    booking_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO date YYYY-MM-DD")

    @field_validator("participant_weights")
    @classmethod
    def weights_must_be_positive(cls, v: List[float]) -> List[float]:
        if any(w <= 0 for w in v):
            raise ValueError("All participant weights must be positive.")
        return v
