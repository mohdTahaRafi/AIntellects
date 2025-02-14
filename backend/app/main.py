from fastapi import FastAPI, BackgroundTasks
from app.services.processor import TrafficProcessor
from app.routes import traffic  # Import the traffic router
from app.database import engine, Base  # Import engine and Base

app = FastAPI()
processor = TrafficProcessor()  # Single instance

# Create database tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    # Start processing loop when app starts
    BackgroundTasks().add_task(processor.process_and_save)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Adaptive Traffic Control System API"}

# Include the traffic router
app.include_router(traffic.router)

@app.get("/data")
async def get_realtime_data():
    return processor.current_data

@app.get("/image")
async def get_latest_image():
    return {"image": processor.latest_image}