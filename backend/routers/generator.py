from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from models.schemas import FunctionMetadata, TestCase
from generator.test_generator import DynamicTestGenerator

router = APIRouter()
generator_service = DynamicTestGenerator()

class GenerateRequest(BaseModel):
    functions: List[FunctionMetadata]
    conditions: List[Dict[str, Any]] = []
    literals: List[Any] = []

@router.post("/generate-tests", response_model=List[TestCase])
async def generate_tests(req: GenerateRequest):
    try:
        all_tests = []
        for func in req.functions:
            tests = generator_service.generate(func, req.conditions, req.literals)
            all_tests.extend(tests)
        return all_tests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")
