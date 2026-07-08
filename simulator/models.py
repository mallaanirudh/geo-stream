from datetime import datetime
from pydantic import BaseModel
class Telemetry(BaseModel):
    device_id: int
    timestamp: datetime
    latitude: float
    longitude: float
    speed: float
    temperature: float
    battery: float