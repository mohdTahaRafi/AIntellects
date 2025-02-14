from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List
import cv2
import base64

# Import internal modules
from app.services.processor import TrafficProcessor
from app.schemas import AllLanesData, ImageResponse, TrafficDataResponse
from app.database import get_db, SessionLocal
from app.models import TrafficData

router = APIRouter(prefix="/traffic", tags=["Traffic Monitoring"])

# Initialize processor (shared instance)
processor = TrafficProcessor()

@router.on_event("startup")
async def startup_event():
    # Start processing loop when app starts
    BackgroundTasks().add_task(processor.process_and_save)

@router.get("/current", response_model=AllLanesData)
async def get_current_traffic_data():
    """
    Get real-time traffic data for all lanes
    Returns:
    - Traffic density
    - Green light status
    - Time remaining for current phase
    - Vehicle counts per type
    - Total vehicles
    """
    if not processor.current_data:
        raise HTTPException(status_code=503, detail="Data not available yet")
    return processor.current_data

@router.get("/image", response_model=ImageResponse)
async def get_current_image():
    """
    Get latest processed image with annotations
    Returns base64 encoded JPEG image and timestamp
    """
    if not processor.latest_image:
        raise HTTPException(status_code=503, detail="Image not available yet")
    
    return {
        "image": processor.latest_image,
        "timestamp": datetime.now()
    }

@router.get("/history", response_model=List[TrafficDataResponse])
async def get_historical_data(
    minutes: int = 60,
    lane: int = None,
    db: Session = Depends(get_db)
):
    """
    Get historical data from database
    Parameters:
    - minutes: Time window in minutes (max 1440 = 24hrs)
    - lane: Specific lane to filter (0-3)
    """
    # Validate input
    minutes = max(1, min(1440, minutes))  # Clamp between 1-1440
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    
    query = db.query(TrafficData).filter(
        TrafficData.timestamp >= time_threshold
    )
    
    if lane is not None:
        if lane < 0 or lane > 3:
            raise HTTPException(status_code=400, detail="Invalid lane number")
        query = query.filter(TrafficData.lane == lane)
    
    return query.order_by(TrafficData.timestamp.desc()).all()

@router.get("/latest")
async def get_latest_traffic_data(db: Session = Depends(get_db)):
    data = db.query(TrafficData).order_by(TrafficData.timestamp.desc()).limit(10).all()
    return data