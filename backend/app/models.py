from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, JSON
from app.database import Base  # Updated import

class TrafficData(Base):
    __tablename__ = "traffic_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    lane = Column(Integer)
    density = Column(Integer)
    green_active = Column(Integer)  # 0 or 1 (boolean)
    green_remaining = Column(Integer)
    total_vehicles = Column(Integer)
    vehicle_counts = Column(JSON)  # Stores dictionary of vehicle counts

# Defines database table structure
# Stores all traffic parameters for each lane
# JSON column type stores dictionary of vehicle counts
# Automatic timestamp for each record