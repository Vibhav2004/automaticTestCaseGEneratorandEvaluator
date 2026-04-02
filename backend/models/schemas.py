from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Language(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    OTHER = "other"

class CodeInput(BaseModel):
    code: str
    language: Language

class Parameter(BaseModel):
    name: str
    type_hint: Optional[str] = "Any"

class FunctionMetadata(BaseModel):
    name: str
    parameters: List[Parameter]
    return_type: Optional[str] = "Any"
    docstring: Optional[str] = None
    line_number: int

class AnalysisResult(BaseModel):
    functions: List[FunctionMetadata]
    conditions: List[Dict[str, Any]] = []
    literals: List[Any] = []
    language: str

class TestCase(BaseModel):
    test_id: str
    function_name: str
    input_params: Dict[str, Any]
    expected_output: Optional[Any] = None
    strategy: str  # BVA, EP, Fuzzing, etc.

class TestExecutionResult(BaseModel):
    test_id: str
    input_values: Dict[str, Any]
    actual_output: Optional[Any] = None
    execution_time: float
    memory_usage: float
    status: str  # PASS, FAIL, ERROR
    exception_trace: Optional[str] = None
    diagnosis: Optional[str] = None # Human-readable error explanation
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""

class SessionResult(BaseModel):
    session_id: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_tests: int
    avg_execution_time: float
    results: List[TestExecutionResult]
