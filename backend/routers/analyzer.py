from fastapi import APIRouter, HTTPException
from models.schemas import CodeInput, AnalysisResult, Language
from services.python_analyzer import PythonAnalyzer
from services.java_analyzer import JavaAnalyzer
from services.universal_analyzer import UniversalAnalyzer

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_code(input_data: CodeInput):
    try:
        functions = []
        conditions = []
        literals = []
        
        # 1. Specialized AST Analysis (High Accuracy)
        if input_data.language == Language.PYTHON:
            try:
                functions = PythonAnalyzer.analyze_code(input_data.code)
                conditions = PythonAnalyzer.get_conditions(input_data.code)
                literals = PythonAnalyzer.extract_literals(input_data.code)
            except: pass # Fallback to universal
            
        elif input_data.language == Language.JAVA:
            try:
                functions = JavaAnalyzer.analyze_code(input_data.code)
                conditions = JavaAnalyzer.get_conditions(input_data.code)
                literals = JavaAnalyzer.extract_literals(input_data.code)
            except: pass # Fallback to universal
            
        # 2. Universal Heuristic Fallback (Polyglot Support)
        if not functions:
            functions = UniversalAnalyzer.analyze_code(input_data.code, input_data.language)
            conditions = UniversalAnalyzer.get_conditions(input_data.code)
            literals = UniversalAnalyzer.extract_literals(input_data.code)
            
        if not functions:
            # If still nothing, it's likely not code or has no function signatures
            raise ValueError("No recognizable functions found in the provided code.")
            
        return AnalysisResult(
            functions=functions, 
            conditions=conditions, 
            literals=literals,
            language=input_data.language
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
