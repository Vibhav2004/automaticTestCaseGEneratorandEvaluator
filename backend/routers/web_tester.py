from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from services import web_tester_service
import uuid
import datetime

router = APIRouter()

class WebTestRequest(BaseModel):
    url: str

class WebTestResult(BaseModel):
    session_id: str
    url: str
    timestamp: str
    tasks: list

@router.post("/test-website", response_model=WebTestResult)
async def test_website(request: WebTestRequest):
    """
    Automated Website Testing: Clicks, Forms, Scrolling, Navigation.
    """
    try:
        session_id = str(uuid.uuid4())
        results = await web_tester_service.run_web_test(request.url)
        
        return {
            "session_id": session_id,
            "url": request.url,
            "timestamp": datetime.datetime.now().isoformat(),
            "tasks": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
