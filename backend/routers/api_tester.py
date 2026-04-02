from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
from typing import Optional, Dict, Any

router = APIRouter()

class ApiRequest(BaseModel):
    method: str
    url: str
    body: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None

class ApiResponse(BaseModel):
    status_code: int
    data: Any
    headers: Dict[str, str]
    time_ms: float

@router.post("/test-api", response_model=ApiResponse)
async def test_api(request: ApiRequest):
    async with httpx.AsyncClient() as client:
        import time
        start_time = time.time()
        
        try:
            method = request.method.upper()
            if method == "GET":
                response = await client.get(request.url, headers=request.headers)
            elif method == "POST":
                response = await client.post(request.url, json=request.body, headers=request.headers)
            elif method == "PUT":
                response = await client.put(request.url, json=request.body, headers=request.headers)
            elif method == "DELETE":
                response = await client.delete(request.url, headers=request.headers)
            else:
                raise HTTPException(status_code=400, detail="Invalid HTTP method")
            
            end_time = time.time()
            
            # Try to parse JSON data
            try:
                data = response.json()
            except:
                data = response.text

            return ApiResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                time_ms=round((end_time - start_time) * 1000, 2)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
