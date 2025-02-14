from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Optional

# Base schema for traffic data
class TrafficDataBase(BaseModel):
    lane: int
    density: int
    green_active: bool
    green_remaining: int
    total_vehicles: int
    vehicle_counts: Dict[str, int]

# Schema for API responses
class TrafficDataResponse(TrafficDataBase):
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Schema for all lanes combined
class AllLanesData(BaseModel):
    lane_0: TrafficDataResponse
    lane_1: TrafficDataResponse
    lane_2: TrafficDataResponse
    lane_3: TrafficDataResponse

# Schema for image response
class ImageResponse(BaseModel):
    image: str
    timestamp: datetime