import random
import uuid
import math
import json
from typing import List, Any, Dict, Set
from models.schemas import FunctionMetadata, TestCase, Parameter

class DynamicTestGenerator:
    def __init__(self):
        self.defaults = {
            "int": 10,
            "float": 10.5,
            "str": "test_data",
            "bool": True,
            "List": [1, 2, 3],
            "Dict": {"key": "val"}
        }

    def generate(self, func_meta: FunctionMetadata, conditions: List[Dict[str, Any]] = None, literals: List[Any] = None) -> List[TestCase]:
        is_low_val = hasattr(func_meta, 'priority') and func_meta.priority == 0
        all_inputs = self._get_input_combinations(func_meta.parameters, conditions, literals)
        if is_low_val:
            all_inputs = all_inputs[:3]

        test_cases = []
        for inputs in all_inputs:
            test_cases.append(TestCase(
                test_id=str(uuid.uuid4())[:8],
                function_name=func_meta.name,
                input_params=inputs,
                strategy=inputs.get("_strategy", "Contextual")
            ))
        return test_cases

    def _get_input_combinations(self, parameters: List[Parameter], conditions: List[Dict[str, Any]] = None, literals: List[Any] = None) -> List[Dict[str, Any]]:
        results = []
        base_template = {p.name: self._get_default_for_type(p.type_hint, p.name) for p in parameters}

        # 1. STRUCTURAL SMOKE TEST (Happy Path)
        case_happy = base_template.copy()
        case_happy["_strategy"] = "Structural Recommendation (Happy Path)"
        results.append(case_happy)

        # 2. SYSTEMATIC NULL & EMPTY INJECTION
        for p in parameters:
            case_null = base_template.copy()
            case_null[p.name] = None
            case_null["_strategy"] = f"Stability: Null Check ({p.name})"
            results.append(case_null)
            
            type_lower = p.type_hint.lower()
            if any(k in type_lower for k in ["list", "str", "[]", "dict"]):
                case_empty = base_template.copy()
                case_empty[p.name] = [] if "list" in type_lower or "[]" in type_lower else "" if "str" in type_lower else {}
                case_empty["_strategy"] = f"Stability: Empty Check ({p.name})"
                results.append(case_empty)

        # 3. BOUNDARY & SYSTEM LIMITS
        for p in parameters:
            type_lower = p.type_hint.lower()
            if "int" in type_lower or "float" in type_lower:
                for val in [0, -1, 1, 2**31-1, -2**31, float('inf'), float('nan')]:
                    if "int" in type_lower and (isinstance(val, float) and not val.is_integer()): continue
                    case = base_template.copy()
                    case[p.name] = val
                    case["_strategy"] = "Robustness: System Boundary"
                    results.append(case)

        # 4. BRANCH COVERAGE
        if conditions:
            for cond in conditions:
                comp = cond.get("comparison")
                if comp:
                    left_var = comp.get("left")
                    right_val = comp.get("right")
                    tp = next((p for p in parameters if p.name == left_var), None)
                    if tp:
                        try:
                            # Use JSON parsing for safety over eval
                            val = json.loads(right_val.replace("'", '"')) if right_val not in ["null", "True", "False"] else eval(right_val)
                            if isinstance(val, (int, float)):
                                for off in [-1, 0, 1]:
                                    c = base_template.copy()
                                    c[tp.name] = val + off
                                    c["_strategy"] = f"Coverage: Branch [{cond['condition']}]"
                                    results.append(c)
                        except: pass

        # 5. RANDOMIZED CHAOS (Fuzzing)
        for _ in range(5):
            case = {p.name: self._gen_fuzz_value(p.type_hint, p.name) for p in parameters}
            case["_strategy"] = "Security: Randomized Chaos"
            results.append(case)

        return self._unique_cases(results)

    def _get_default_for_type(self, type_str: str, name: str = "") -> Any:
        ts = type_str.lower()
        nm = name.lower()
        if "list" in ts or "[]" in ts:
            if any(k in nm for k in ["tasks", "data", "items", "entries"]):
                return [{"task_id": 1, "priority": 10, "duration": 5}, {"task_id": 2, "priority": 1, "duration": 60}]
            return [1, 2, 3]
        if "dict" in ts or "{}" in ts: return {"key": "val"}
        if "int" in ts: return 10
        if "str" in ts: return "test_data"
        if "bool" in ts: return True
        return None

    def _gen_fuzz_value(self, type_str: str, name: str = "") -> Any:
        ts = type_str.lower()
        nm = name.lower()
        if "list" in ts or "[]" in ts:
            if any(k in nm for k in ["tasks", "data", "items"]):
                return [{"task_id": random.randint(1,100), "priority": random.randint(1,10), "duration": random.randint(1,100)} for _ in range(2)]
            return [random.randint(0, 100) for _ in range(2)]
        if "int" in ts: return random.randint(-1000, 1000)
        return random.choice([True, False, None, "chaos"])

    def _unique_cases(self, cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique = []
        seen = set()
        for c in cases:
            items = {k: v for k, v in c.items() if not k.startswith('_')}
            h = str(sorted(items.items()))
            if h not in seen:
                seen.add(h)
                unique.append(c)
        return unique
