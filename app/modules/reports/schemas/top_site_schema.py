from pydantic import BaseModel, ConfigDict
from typing import Optional

class TopSiteResponse(BaseModel):
    name: str
    visits: int

    time_hours: float
    time_minutes: Optional[float] = None

    category: Optional[str] = None
    trend: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)