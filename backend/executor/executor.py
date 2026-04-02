import subprocess
import time
import os
import tempfile
import sys
import json
import traceback
import psutil
from typing import List, Dict, Any
from models.schemas import TestExecutionResult, TestCase, Language

class SecureExecutor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def execute_python(self, code: str, test_cases: List[TestCase]) -> List[TestExecutionResult]:
        results = []
        for test in test_cases:
            start_time = time.time()
            try:
                # 1. PREPARE WRAPPER
                params_json = json.dumps(test.input_params)
                wrapper = self._generate_python_wrapper(code, test.function_name, params_json)
                
                # 2. SELECTION OF EXECUTION ENGINE (Corporate Standard: Docker)
                # For this implementation, we use Subprocess with strict Resource Limits
                # as a reliable baseline, but prepared for Docker integration.
                
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as tmp:
                    tmp.write(wrapper)
                    tmp_path = tmp.name

                process = subprocess.Popen(
                    [sys.executable, tmp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Monitor memory in real-time
                max_mem = 0
                try:
                    p = psutil.Process(process.pid)
                    stdout, stderr = "", ""
                    
                    # Manual wait with resource sampling
                    while process.poll() is None:
                        try:
                            max_mem = max(max_mem, p.memory_info().rss / (1024 * 1024))
                            if max_mem > 512: # 512MB Limit
                                process.kill()
                                raise MemoryError("Memory Limit Exceeded (512MB)")
                        except: pass
                        time.sleep(0.1)
                        if time.time() - start_time > self.timeout:
                            process.kill()
                            raise subprocess.TimeoutExpired(process.args, self.timeout)
                            
                    stdout, stderr = process.communicate()
                    
                    # 3. PARSE RESULTS
                    status, actual_output, exception_trace = self._parse_process_output(process.returncode, stdout, stderr)
                    diagnosis = self._diagnose_error(exception_trace) if status != "PASS" else None
                    
                    results.append(TestExecutionResult(
                        test_id=test.test_id,
                        input_values=test.input_params,
                        actual_output=actual_output,
                        execution_time=round(time.time() - start_time, 4),
                        memory_usage=round(max_mem, 2),
                        status=status,
                        exception_trace=exception_trace,
                        diagnosis=diagnosis,
                        stdout=stdout,
                        stderr=stderr
                    ))

                except (subprocess.TimeoutExpired, MemoryError) as e:
                    trace = str(e)
                    results.append(TestExecutionResult(
                        test_id=test.test_id,
                        input_values=test.input_params,
                        execution_time=self.timeout,
                        memory_usage=round(max_mem, 2),
                        status="ERROR",
                        exception_trace=trace,
                        diagnosis=self._diagnose_error(trace)
                    ))
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                        
            except Exception as e:
                results.append(TestExecutionResult(
                    test_id=test.test_id,
                    input_values=test.input_params,
                    execution_time=0.0,
                    memory_usage=0.0,
                    status="ERROR",
                    exception_trace=str(e)
                ))
        return results

    def _generate_python_wrapper(self, user_code: str, func_name: str, params_json: str) -> str:
        return f"""
{user_code}

import json
import sys
import math
import random
import collections

def run_test():
    try:
        all_args = json.loads({repr(params_json)})
        args = {{k: v for k, v in all_args.items() if not k.startswith('_')}}
        
        # Resolve target: Handle 'Class.method', 'Class.__init__', or 'function'
        parts = "{func_name}".split('.')
        target_name = parts[0]
        target = globals().get(target_name)
        
        if not target:
            raise NameError(f"Target '{{target_name}}' not found")

        if len(parts) > 1:
            method_name = parts[1]
            if method_name == "__init__" and isinstance(target, type):
                # If testing constructor, the 'func' is the class itself
                func = target
            else:
                # If it's a class, try to instantiate it with NO args for instance methods
                # If that fails (needs args), we assume it's a static/class method lookup
                if isinstance(target, type):
                    try:
                        instance = target()
                        func = getattr(instance, method_name)
                    except:
                        func = getattr(target, method_name)
                else:
                    func = getattr(target, method_name)
        else:
            func = target
            
        if not func: raise NameError(f"Function '{{func_name}}' could not be resolved")
        
        result = func(**args)
        
        # Intelligent Property Checking
        self_validating_checks(result, "{func_name}", args)
        
        print("---RESULT---")
        print(json.dumps(result))
    except AssertionError as e:
        print("---FAIL---")
        print(str(e))
        sys.exit(2)
    except Exception as e:
        print("---ERROR---")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)

def self_validating_checks(result, name, args):
    name = name.lower()
    # Contract: Sort functions
    if "sort" in name and isinstance(result, list):
        if result != sorted(result):
            raise AssertionError("Inconsistency: List is not sorted after operation")
    # Contract: Search functions
    if any(k in name for k in ["find", "search", "index"]) and "target" in args:
        target = args["target"]
        for k in ["arr", "nums", "list"]:
            if k in args and isinstance(args[k], list):
                if result != -1 and args[k][result] != target:
                    raise AssertionError(f"Invalid Index: Found {{args[k][result]}} at {{result}}, expected {{target}}")

if __name__ == "__main__":
    run_test()
"""

    def _parse_process_output(self, returncode, stdout, stderr):
        if returncode == 0:
            status = "PASS"
        elif returncode == 2 or "---FAIL---" in stdout:
            status = "FAIL"
        else:
            status = "ERROR"
            
        actual_output = None
        exception_trace = None
        
        if "---RESULT---" in stdout:
            actual_output = stdout.split("---RESULT---")[1].strip()
        
        if status == "ERROR":
            exception_trace = stdout if "---ERROR---" in stdout else stderr
        elif status == "FAIL":
            exception_trace = stdout.split("---FAIL---")[1].strip() if "---FAIL---" in stdout else "Assertion Failed"
            
        return status, actual_output, exception_trace

    def _diagnose_error(self, trace: str) -> str:
        if not trace: return "Unexpected system failure."
        
        # CORPORATE HEURISTICS
        if "IndexError" in trace:
            return "Potential Boundary Error: The code tried to access a list index that is out of range. Check loops for 'off-by-one' errors."
        if "KeyError" in trace:
            return "Structural Error: The code expected a dictionary key that wasn't provided. Ensure all expected attributes are initialized."
        if "TypeError" in trace:
            if "NoneType" in trace:
                return "Null Pointer Alert: An operation was performed on 'None'. Check if your function handles empty/null inputs gracefully."
            return "Contract Mismatch: The function received an unexpected data type. Verify parameter type hints."
        if "ZeroDivisionError" in trace:
            return "Math Error: Illegal division by zero. Ensure denominators are validated before calculation."
        if "RecursionError" in trace:
            return "Infinite Logic: Maximum recursion depth exceeded. Check your recursive base cases."
        if "TimeoutExpired" in trace or "Time Limit" in trace:
            return "Efficiency Alert: The logic is too slow or contains an infinite loop. Optimization required."
        if "MemoryError" in trace:
            return "Resource Alert: The algorithm consumed more than 512MB RAM. Check for massive object allocation."
        if "AssertionError" in trace:
            return "Logic Validation Failed: The code finished but failed a structural integrity check (e.g. data loss during merge)."
            
        return "Unknown Execution Error: Review the traceback for specific structural flaws."

    def execute_java(self, code: str, test_cases: List[TestCase]) -> List[TestExecutionResult]:
        import re
        results = []
        
        # 1. Extract class name (allowing optional public/final etc)
        class_match = re.search(r"(?:public\s+)?class\s+(\w+)", code)
        class_name = class_match.group(1) if class_match else "Solution"
        
        # If no class name found, wrap it
        if not class_match:
            code = f"public class {class_name} {{ \n{code}\n }}"

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_file = os.path.join(tmp_dir, f"{class_name}.java")
            with open(source_file, "w", encoding='utf-8') as f:
                f.write(code)

            # 2. Compile
            compile_process = subprocess.Popen(
                ["javac", f"{class_name}.java"],
                cwd=tmp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout_comp, stderr_comp = compile_process.communicate()
            
            if compile_process.returncode != 0:
                for test in test_cases:
                    results.append(TestExecutionResult(
                        test_id=test.test_id,
                        input_values=test.input_params,
                        execution_time=0.0,
                        memory_usage=0.0,
                        status="ERROR",
                        exception_trace=f"Compilation Error (User Code):\n{stderr_comp}"
                    ))
                return results

            # 3. Execute each test case
            for test in test_cases:
                start_time = time.time()
                try:
                    # Create a tiny runner class that uses reflection to call the target method
                    # This avoids complex argument parsing in Java.
                    arg_keys = ", ".join([f"\"{k}\"" for k in test.input_params.keys() if not k.startswith('_')])
                    
                    # Manual type handling for simple types in the runner
                    # For a production system, we'd use a JSON library like Jackson or Gson
                    # For this demo, we'll pass args as strings and let the runner convert.
                    
                    def to_java_literal(v):
                        if isinstance(v, list):
                            return f"Arrays.asList({', '.join(to_java_literal(x) for x in v)})"
                        if isinstance(v, str):
                            return json.dumps(v)
                        if isinstance(v, bool):
                            return str(v).lower()
                        if v is None:
                            return "null"
                        return str(v)

                    invoke_logic = ""
                    for k, v in test.input_params.items():
                        if k.startswith('_'): continue
                        invoke_logic += f"inputs.put(\"{k}\", {to_java_literal(v)});\n"

                    runner_code = f"""
import java.lang.reflect.*;
import java.util.*;
import java.util.stream.*;

public class TestRunner {{
    public static void main(String[] args) {{
        try {{
            String methodName = "{test.function_name}";
            Class<?> cls = Class.forName("{class_name}");
            
            Method targetMethod = null;
            Method[] methods = cls.getDeclaredMethods();
            for (Method m : methods) {{
                if (m.getName().equals(methodName) && !m.getName().equals("main")) {{
                    targetMethod = m;
                    break;
                }}
            }}
            
            if (targetMethod == null) throw new Exception("Method " + methodName + " not found");
            
            targetMethod.setAccessible(true);
            int paramCount = targetMethod.getParameterCount();
            Object[] paramValues = new Object[paramCount];
            Class<?>[] paramTypes = targetMethod.getParameterTypes();
            
            Map<String, Object> inputs = new LinkedHashMap<>();
            {invoke_logic}
            
            Object[] inputVals = inputs.values().toArray();
            for (int i = 0; i < paramCount; i++) {{
                if (i < inputVals.length) {{
                    paramValues[i] = castValue(inputVals[i], paramTypes[i]);
                }}
            }}

            Object instance = null;
            if (!Modifier.isStatic(targetMethod.getModifiers())) {{
                instance = cls.getDeclaredConstructor().newInstance();
            }}
            
            Object result = targetMethod.invoke(instance, paramValues);
            
            // Property Check: If parameters contain 'target' and it's a search method
            boolean isSearchName = methodName.toLowerCase().contains("search") || 
                                   methodName.toLowerCase().contains("find") || 
                                   methodName.toLowerCase().contains("index") || 
                                   methodName.toLowerCase().contains("binary");

            if (isSearchName && inputs.containsKey("target") && result instanceof Integer) {{
                int idx = (Integer)result;
                if (idx != -1) {{
                    for (String key : new String[] {{"nums", "arr", "list", "data"}}) {{
                        if (inputs.containsKey(key) && inputs.get(key) instanceof List) {{
                            List<?> list = (List<?>)inputs.get(key);
                            if (idx >= 0 && idx < list.size()) {{
                                Object found = list.get(idx);
                                Object target = inputs.get("target");
                                if (!String.valueOf(found).equals(String.valueOf(target))) {{
                                    throw new AssertionError("Search property failed: Index " + idx + " contains " + found + " but target is " + target);
                                }}
                            }}
                        }}
                    }}
                }}
            }}

            System.out.println("---RESULT---");
            if (result != null && result.getClass().isArray()) {{
                if (result instanceof int[]) System.out.println(Arrays.toString((int[])result));
                else if (result instanceof long[]) System.out.println(Arrays.toString((long[])result));
                else if (result instanceof double[]) System.out.println(Arrays.toString((double[])result));
                else if (result instanceof float[]) System.out.println(Arrays.toString((float[])result));
                else if (result instanceof boolean[]) System.out.println(Arrays.toString((boolean[])result));
                else if (result instanceof Object[]) System.out.println(Arrays.deepToString((Object[])result));
                else System.out.println(result);
            }} else {{
                System.out.println(result);
            }}
        }} catch (InvocationTargetException e) {{
            Throwable cause = e.getCause();
            if (cause instanceof AssertionError) {{
                System.out.println("---FAIL---");
                System.out.println(cause.getMessage());
                System.exit(2);
            }} else {{
                System.out.println("---ERROR---");
                if (cause != null) cause.printStackTrace(System.out);
                else e.printStackTrace(System.out);
                System.exit(1);
            }}
        }} catch (Exception e) {{
            System.out.println("---ERROR---");
            e.printStackTrace(System.out);
            System.exit(1);
        }}
    }}
    
    private static Object castValue(Object val, Class<?> type) {{
        if (val == null) return null;
        if (type.isArray()) {{
            if (val instanceof List) {{
                List<?> list = (List<?>) val;
                Class<?> componentType = type.getComponentType();
                Object array = Array.newInstance(componentType, list.size());
                for (int i = 0; i < list.size(); i++) {{
                    Array.set(array, i, castValue(list.get(i), componentType));
                }}
                return array;
            }}
        }}

        if (type.isAssignableFrom(val.getClass())) return val;
        
        String s = String.valueOf(val);
        if (type == int.class || type == Integer.class) return (int)Double.parseDouble(s);
        if (type == double.class || type == Double.class) return Double.parseDouble(s);
        if (type == float.class || type == Float.class) return Float.parseFloat(s);
        if (type == long.class || type == Long.class) return (long)Double.parseDouble(s);
        if (type == boolean.class || type == Boolean.class) return Boolean.parseBoolean(s);
        if (type == String.class) return s;
        return val;
    }}
}}
"""
                    runner_file = os.path.join(tmp_dir, "TestRunner.java")
                    with open(runner_file, "w") as f:
                        f.write(runner_code)
                    
                    # Compile runner
                    cp_sep = ";" if sys.platform == "win32" else ":"
                    subprocess.run(["javac", "-cp", f".{cp_sep}.", "TestRunner.java"], cwd=tmp_dir, capture_output=True)
                    
                    # Run
                    run_process = subprocess.Popen(
                        ["java", "-cp", f".{cp_sep}.", "TestRunner"],
                        cwd=tmp_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    try:
                        stdout, stderr = run_process.communicate(timeout=self.timeout)
                        if run_process.returncode == 0:
                            status = "PASS"
                        elif run_process.returncode == 2 or "---FAIL---" in stdout:
                            status = "FAIL"
                        else:
                            status = "ERROR"
                        
                        actual_output = None
                        exception_trace = None
                        
                        if "---RESULT---" in stdout:
                            actual_output = stdout.split("---RESULT---")[1].strip()
                        
                        if status == "ERROR":
                            exception_trace = stdout if "---ERROR---" in stdout else stderr
                        elif status == "FAIL":
                            exception_trace = stdout.split("---FAIL---")[1].strip() if "---FAIL---" in stdout else "Assertion Failed"
                        
                        diagnosis = self._diagnose_error(exception_trace) if status != "PASS" else None
                            
                        results.append(TestExecutionResult(
                            test_id=test.test_id,
                            input_values=test.input_params,
                            actual_output=actual_output,
                            execution_time=round(time.time() - start_time, 4),
                            memory_usage=0.0,
                            status=status,
                            exception_trace=exception_trace,
                            diagnosis=diagnosis,
                            stdout=stdout,
                            stderr=stderr
                        ))
                    except subprocess.TimeoutExpired:
                        run_process.kill()
                        results.append(TestExecutionResult(
                            test_id=test.test_id,
                            input_values=test.input_params,
                            execution_time=self.timeout,
                            memory_usage=0.0,
                            status="ERROR",
                            exception_trace="Time Limit Exceeded",
                            diagnosis=self._diagnose_error("TimeoutExpired")
                        ))
                except Exception as e:
                    results.append(TestExecutionResult(
                        test_id=test.test_id,
                        input_values=test.input_params,
                        execution_time=0.0,
                        memory_usage=0.0,
                        status="ERROR",
                        exception_trace=str(e)
                    ))
        
        return results
