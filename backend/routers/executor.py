from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from models.schemas import TestCase, TestExecutionResult, Language, SessionResult
from executor.executor import SecureExecutor

router = APIRouter()
executor_service = SecureExecutor()

class ExecutionRequest(BaseModel):
    code: str
    language: Language
    test_cases: List[TestCase]

@router.post("/execute", response_model=SessionResult)
async def execute_tests(req: ExecutionRequest):
    try:
        if req.language == Language.PYTHON:
            results = executor_service.execute_python(req.code, req.test_cases)
        elif req.language == Language.JAVA:
            results = executor_service.execute_java(req.code, req.test_cases)
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")
        
        # Compute stats
        total = len(results)
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        errors = sum(1 for r in results if r.status == "ERROR")
        avg_time = sum(r.execution_time for r in results) / total if total > 0 else 0
        
        return SessionResult(
            session_id="session_" + str(len(results)), # Simplified
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            error_tests=errors,
            avg_execution_time=round(avg_time, 4),
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
