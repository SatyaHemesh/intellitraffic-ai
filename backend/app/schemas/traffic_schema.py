# backend/app/schemas/traffic_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

class TrafficRecordCreate(BaseModel):
    camera_id: str = Field(..., description="Unique ID of the CCTV camera")
    total_vehicles: int = Field(..., ge=0, description="Total number of detected vehicles")
    density_level: str = Field(..., description="Traffic density: Low, Medium, High")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TrafficRecordResponse(TrafficRecordCreate):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True