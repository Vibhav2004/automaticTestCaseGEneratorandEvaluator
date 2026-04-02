import re
from typing import List, Dict, Any, Optional
from models.schemas import FunctionMetadata, Parameter

class UniversalAnalyzer:
    """
    A polyglot analyzer that uses regex heuristics to extract structural metadata
    from code in almost any language.
    """
    
    @staticmethod
    def analyze_code(code: str, language: str = "other") -> List[FunctionMetadata]:
        functions = []
        
        # 1. Regex for C-style functions: type name(args) {
        # Matches: int add(int a, int b), function add(a, b), def add(a: int)
        c_style_pattern = r'(?:(?:public|private|static|async|function|def|export|class)\s+)*(?:[\w<>\[\]]+\s+)?(\w+)\s*\((.*?)\)\s*(?:[:{]|\s*->)'
        
        matches = list(re.finditer(c_style_pattern, code))
        for match in matches:
            name = match.group(1)
            raw_params = match.group(2)
            
            # Skip common keywords
            if name in ["if", "while", "for", "switch", "catch", "return", "class"]:
                continue
                
            # HEURISTIC: Internal/Magic method detection
            is_internal = name.startswith('__') or name in ["constructor", "toString", "equals", "hashCode"]
            
            params = []
            if raw_params.strip():
                param_list = raw_params.split(',')
                for p in param_list:
                    p = p.strip()
                    if not p: continue
                    parts = re.split(r'[:\s]+', p)
                    p_name = parts[0]
                    p_type = parts[1] if len(parts) > 1 else "Any"
                    
                    if len(parts) > 1 and not p.strip().endswith(p_type):
                        p_name = parts[-1]
                        p_type = parts[0]
                    params.append(Parameter(name=p_name, type_hint=p_type))
            
            # Smart Priority Scoring
            # Long functions with many params are often the "Entry Points"
            priority = 1 if not is_internal else 0
            if "schedule" in name.lower() or "process" in name.lower() or "solve" in name.lower():
                priority = 2 # Highest Priority

            functions.append(FunctionMetadata(
                name=name,
                parameters=params,
                return_type="Any",
                docstring=None,
                line_number=code.count('\n', 0, match.start()) + 1,
                priority=priority
            ))
            
        return functions

    @staticmethod
    def get_conditions(code: str) -> List[Dict[str, Any]]:
        conditions = []
        pattern = r'(?:if|while|elif|elseif)\s*\(?([\w\s.><=!&|"\'-]+)\)?'
        for match in re.finditer(pattern, code):
            cond_str = match.group(1).strip()
            comp_match = re.search(r'(\w+)\s*(==|!=|>=|<=|>|<)\s*([\w\'".-]+)', cond_str)
            extracted = {
                "type": "Condition",
                "condition": cond_str,
                "line_number": code.count('\n', 0, match.start()) + 1,
                "variables": [],
                "literals": []
            }
            if comp_match:
                extracted["comparison"] = {
                    "left": comp_match.group(1),
                    "op": comp_match.group(2),
                    "right": comp_match.group(3)
                }
                extracted["variables"].append(comp_match.group(1))
                extracted["literals"].append(comp_match.group(3))
            conditions.append(extracted)
        return conditions

    @staticmethod
    def extract_literals(code: str) -> List[Any]:
        literals = set()
        for m in re.finditer(r'\b\d+\.?\d*\b', code):
            val = m.group()
            try:
                literals.add(float(val) if '.' in val else int(val))
            except: pass
        for m in re.finditer(r'["\'](.*?)["\']', code):
            val = m.group(1)
            if val and len(val) < 50:
                literals.add(val)
        return list(literals)
