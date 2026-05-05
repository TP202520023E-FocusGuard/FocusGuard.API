from pydantic import BaseModel, ConfigDict
from typing import Optional

class LeisureTimeResponse(BaseModel):
    weekday: int  # The day of the week (0 = Monday, 6 = Sunday)
    day: str      # The name of the day (e.g., 'Monday', 'Tuesday')
    total_hours: float  # Total leisure time (in hours) for that day

    model_config = ConfigDict(from_attributes=True)