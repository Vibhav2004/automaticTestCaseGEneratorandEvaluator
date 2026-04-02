import ast
from typing import List, Dict, Any
from models.schemas import FunctionMetadata, Parameter

class PythonAnalyzer:
    @staticmethod
    def analyze_code(code: str) -> List[FunctionMetadata]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")

        # First pass: Mark method parents
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        child.parent_class = node.name

        functions = []
        # Second pass: Extract metadata
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # FILTER: Skip dunders, test helpers, and boilerplate
                if node.name.startswith('__') or node.name.startswith('test_') or node.name in ['setup', 'teardown']:
                    continue
                
                parent_class_name = getattr(node, 'parent_class', None)
                full_name = f"{parent_class_name}.{node.name}" if parent_class_name else node.name
                
                params = []
                for arg in node.args.args:
                    if arg.arg in ['self', 'cls']: # Skip instance/class decorators
                        continue
                    
                    params.append(Parameter(
                        name=arg.arg,
                        type_hint=PythonAnalyzer._get_type_hint(arg)
                    ))
                
                # Metadata extraction
                return_type = "Any"
                if node.returns:
                    try: return_type = ast.unparse(node.returns)
                    except: pass

                # PRIORITY: Logic Entry Points (Standalone) vs Class Methods
                priority = 2 if not parent_class_name else 1
                if any(kw in node.name.lower() for kw in ["run", "main", "process", "solve", "execute"]):
                    priority = 3 # Mission Critical targets

                functions.append(FunctionMetadata(
                    name=full_name,
                    parameters=params,
                    return_type=return_type,
                    docstring=ast.get_docstring(node),
                    line_number=node.lineno,
                    priority=priority
                ))
        
        return functions

    @staticmethod
    def _get_type_hint(arg: ast.arg) -> str:
        type_hint = "Any"
        if arg.annotation:
            try: type_hint = ast.unparse(arg.annotation)
            except: pass
        
        if type_hint == "Any":
            name_lower = arg.arg.lower()
            if any(k in name_lower for k in ["nums", "list", "data"]): type_hint = "List"
            elif any(k in name_lower for k in ["is_", "check"]): type_hint = "bool"
            elif any(k in name_lower for k in ["n", "i", "val", "count"]): type_hint = "int"
        return type_hint

    @staticmethod
    def get_conditions(code: str) -> List[Dict[str, Any]]:
        try: tree = ast.parse(code)
        except: return []
            
        conditions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.Assert)):
                test_node = node.test
                condition_str = ast.unparse(test_node)
                
                extracted = {
                    "type": type(node).__name__,
                    "condition": condition_str,
                    "line_number": node.lineno,
                    "variables": [],
                    "literals": []
                }
                
                for sub in ast.walk(test_node):
                    if isinstance(sub, ast.Name): extracted["variables"].append(sub.id)
                    elif isinstance(sub, ast.Constant): extracted["literals"].append(sub.value)
                    elif isinstance(sub, ast.Compare):
                        left = ast.unparse(sub.left)
                        for op, right in zip(sub.ops, sub.comparators):
                            extracted["comparison"] = {
                                "left": left,
                                "op": type(op).__name__,
                                "right": ast.unparse(right)
                            }
                conditions.append(extracted)
        return conditions

    @staticmethod
    def extract_literals(code: str) -> List[Any]:
        try: tree = ast.parse(code)
        except: return []
        literals = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float, str)) and node.value not in [None, True, False, ""]:
                    literals.add(node.value)
        return list(literals)
