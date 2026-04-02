from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class EchoModel(BaseModel):
    message: str
    data: Dict[str, Any]

@router.get("/hello")
async def say_hello():
    return {
        "status": "success",
        "message": "Welcome to AutoTestAI Sample API",
        "description": "This endpoint is used to verify the API Tester connectivity."
    }

@router.get("/metrics")
async def get_mock_metrics():
    return {
        "cpu_usage": "15%",
        "memory_free": "2.4GB",
        "active_sessions": 42,
        "uptime_seconds": 3600
    }

@router.post("/echo", response_model=EchoModel)
async def echo_data(request: EchoModel):
    return {
        "message": f"Server received: {request.message}",
        "data": request.data
    }

@router.put("/update-config")
async def update_config(config: Dict[str, Any]):
    return {
        "status": "updated",
        "new_config": config,
        "timestamp": "2026-02-23T15:25:00Z"
    }

@router.delete("/resource/{item_id}")
async def delete_resource(item_id: int):
    if item_id > 1000:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {
        "status": "deleted",
        "id": item_id
    }
