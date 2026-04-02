import javalang
from typing import List, Dict, Any
from models.schemas import FunctionMetadata, Parameter

class JavaAnalyzer:
    @staticmethod
    def analyze_code(code: str) -> List[FunctionMetadata]:
        try:
            tree = javalang.parse.parse(code)
        except Exception as e:
            # javalang can be picky about snippets, try parsing as a fragment if it fails
            try:
                # Add a dummy class wrapper if it looks like just a method
                if "class" not in code:
                    wrapped_code = f"public class Temp {{ {code} }}"
                    tree = javalang.parse.parse(wrapped_code)
                else:
                    raise e
            except Exception as e2:
                raise ValueError(f"Invalid Java code: {str(e2)}")

        functions = []
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            params = []
            for param in node.parameters:
                type_name = param.type.name
                if hasattr(param.type, 'dimensions') and param.type.dimensions:
                    type_name += "[]" * len(param.type.dimensions)
                
                params.append(Parameter(
                    name=param.name,
                    type_hint=type_name
                ))
            
            return_type = "void"
            if node.return_type:
                return_type = node.return_type.name
            
            functions.append(FunctionMetadata(
                name=node.name,
                parameters=params,
                return_type=return_type,
                docstring=None, # javalang doesn't easily extract javadoc here
                line_number=node.position.line if node.position else 0
            ))
            
        return functions

    @staticmethod
    def get_conditions(code: str) -> List[Dict[str, Any]]:
        """Deep AST analysis for Java conditions."""
        try:
            tree = javalang.parse.parse(code)
        except:
            # Fallback for snippets
            try:
                wrapped = f"public class T {{ void m() {{ {code} }} }}"
                tree = javalang.parse.parse(wrapped)
            except:
                return []
            
        conditions = []
        for path, node in tree.filter(javalang.tree.IfStatement):
            cond_node = node.condition
            extracted = {
                "type": "If",
                "condition": str(cond_node),
                "line_number": node.position.line if node.position else 0,
                "variables": [],
                "literals": []
            }
            
            # Recursive descent into the condition tree
            def walk_node(n):
                if isinstance(n, javalang.tree.MemberReference):
                    extracted["variables"].append(n.member)
                elif isinstance(n, javalang.tree.Literal):
                    extracted["literals"].append(n.value)
                elif isinstance(n, javalang.tree.BinaryOperation):
                    walk_node(n.operandl)
                    walk_node(n.operandr)
                    extracted["comparison"] = {
                        "op": n.operator,
                        "left": str(n.operandl),
                        "right": str(n.operandr)
                    }

            walk_node(cond_node)
            conditions.append(extracted)
        return conditions

    @staticmethod
    def extract_literals(code: str) -> List[Any]:
        try:
            tree = javalang.parse.parse(code)
        except:
            return []
        
        literals = set()
        for path, node in tree.filter(javalang.tree.Literal):
            val = node.value
            # Basic cleanup of Java literals
            if val.endswith('f') or val.endswith('F') or val.endswith('L') or val.endswith('l'):
                val = val[:-1]
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            
            try:
                if '.' in val: literals.add(float(val))
                else: literals.add(int(val))
            except:
                if val: literals.add(val)
        
        return list(literals)
