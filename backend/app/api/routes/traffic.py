# backend/app/api/routes/traffic.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.traffic_schema import TrafficRecordCreate, TrafficRecordResponse
from app.database import get_database

router = APIRouter(prefix="/api/traffic", tags=["Traffic Analytics"])

@router.post("/log", response_model=dict)
async def log_traffic_data(record: TrafficRecordCreate):
    """
    Endpoint for the AI Pipeline to send real-time traffic data.
    """
    db = get_database()
    collection = db["traffic_logs"]
    
    record_dict = record.model_dump()
    result = await collection.insert_one(record_dict)
    
    if result.inserted_id:
        return {"status": "success", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to log traffic data")

@router.get("/latest", response_model=List[TrafficRecordCreate])
async def get_latest_traffic(camera_id: str = None, limit: int = 10):
    """
    Endpoint for the React Dashboard to fetch the most recent traffic stats.
    """
    db = get_database()
    collection = db["traffic_logs"]
    
    query = {"camera_id": camera_id} if camera_id else {}
    cursor = collection.find(query).sort("timestamp", -1).limit(limit)
    
    records = await cursor.to_list(length=limit)
    return records