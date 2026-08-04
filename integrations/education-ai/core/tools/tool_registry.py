#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·明夷-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# core/tools/tool_registry.py
# 龍魂 · 工具注册中心 · Function Calling基础设施

import inspect
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"

class ToolCategory(Enum):
    """工具分类"""
    CALCULATION = "calculation"      # 计算
    SEARCH = "search"                # 搜索
    DATA_ANALYSIS = "data_analysis"  # 数据分析
    CODE_EXECUTION = "code_execution" # 代码执行
    FILE_OPERATION = "file_operation" # 文件操作
    EXTERNAL_API = "external_api"    # 外部API


@dataclass
class ToolSchema:
    """工具Schema（OpenAI Function Calling格式）"""
    name: str
    description: str
    category: ToolCategory
    parameters: Dict              # JSON Schema
    required: List[str]
    handler: Callable
    dangerous: bool = False       # 是否危险操作
    dna_signature: str = ""
    
    def __post_init__(self):
        if not self.dna_signature:
            self.dna_signature = self._sign_data()
    
    def _sign_data(self) -> str:
        payload = f"{self.name}-{self.category.value}-{self.description[:20]}"
        return f"SM3-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"
    
    def to_openai_format(self) -> Dict[str, Any]:
        """转换为OpenAI Function Calling格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required
                }
            }
        }


class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self.tools: Dict[str, ToolSchema] = {}
        self.categories: Dict[ToolCategory, List[str]] = {cat: [] for cat in ToolCategory}
    
    def register(self, 
                 name: str,
                 description: str,
                 category: ToolCategory,
                 parameters: Dict[str, Any],
                 required: List[str],
                 dangerous: bool = False):
        """注册工具装饰器"""
        def decorator(func: Callable):
            tool = ToolSchema(
                name=name,
                description=description,
                category=category,
                parameters=parameters,
                required=required,
                handler=func,
                dangerous=dangerous
            )
            self.tools[name] = tool
            self.categories[category].append(name)
            return func
        return decorator
    
    def get_tool(self, name: str) -> Optional[ToolSchema]:
        """获取工具"""
        return self.tools.get(name)
    
    def list_tools(self, category: Optional[ToolCategory] = None) -> List[ToolSchema]:
        """列出工具"""
        if category:
            return [self.tools[name] for name in self.categories[category]]
        return list(self.tools.values())
    
    def get_schemas(self) -> List[Dict]:
        """获取所有Schema（用于LLM Function Calling）"""
        return [tool.to_openai_format() for tool in self.tools.values()]
    
    def execute(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具"""
        tool = self.tools.get(name)
        if not tool:
            return {
                "error": f"工具未找到: {name}",
                "status": "failed"
            }
        
        # 参数验证
        validation = self._validate_params(tool, arguments)
        if not validation["valid"]:
            return {
                "error": validation["error"],
                "status": "failed"
            }
        
        # 危险操作审计
        if tool.dangerous:
            print(f"[龍魂·审计] 危险操作: {name}({arguments})")
        
        try:
            result = tool.handler(**arguments)
            return {
                "result": result,
                "status": "success",
                "tool": name,
                "dna": tool.dna_signature
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "tool": name
            }
    
    def _validate_params(self, tool: ToolSchema, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """参数验证"""
        for req in tool.required:
            if req not in arguments:
                return {
                    "valid": False,
                    "error": f"缺少必填参数: {req}"
                }
        
        for key, value in arguments.items():
            if key in tool.parameters:
                expected_type = tool.parameters[key].get("type", "string")
                if expected_type == "number" and not isinstance(value, (int, float)):
                    return {
                        "valid": False,
                        "error": f"参数 {key} 应为数字类型"
                    }
        
        return {"valid": True}


# === 全局注册中心 ===
registry = ToolRegistry()


# === 教育工具定义 ===

@registry.register(
    name="calculate_math",
    description="执行数学计算，支持基本运算和三角函数",
    category=ToolCategory.CALCULATION,
    parameters={
        "expression": {
            "type": "string",
            "description": "数学表达式，如 '2 + 2 * 3' 或 'sin(30)'"
        }
    },
    required=["expression"]
)
def calculate_math(expression: str) -> str:
    """数学计算工具"""
    import math
    import ast
    
    allowed_names = {
        "abs": abs, "max": max, "min": min,
        "pow": pow, "sqrt": math.sqrt,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "log": math.log, "log10": math.log10,
        "pi": math.pi, "e": math.e
    }
    
    try:
        tree = ast.parse(expression, mode='eval')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name) or node.func.id not in allowed_names:
                    raise ValueError(f"不允许的函数调用: {node.func}")
        
        result = eval(compile(tree, '', 'eval'), {"__builtins__": {}}, allowed_names)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@registry.register(
    name="solve_equation",
    description="求解方程，支持一元二次方程等",
    category=ToolCategory.CALCULATION,
    parameters={
        "equation": {
            "type": "string",
            "description": "方程表达式，如 'x^2 + 5*x + 6 = 0'"
        },
        "variable": {
            "type": "string",
            "description": "变量名，如 'x'"
        }
    },
    required=["equation", "variable"]
)
def solve_equation(equation: str, variable: str) -> str:
    """方程求解工具"""
    try:
        from sympy import symbols, solve, Eq, parse_expr
        
        var = symbols(variable)
        if '=' in equation:
            left, right = equation.split('=')
            eq = Eq(parse_expr(left), parse_expr(right))
        else:
            eq = parse_expr(equation)
        
        solutions = solve(eq, var)
        
        if not solutions:
            return "方程无解"
        
        result = f"方程 {equation} 的解:\n"
        for i, sol in enumerate(solutions, 1):
            result += f"  x{i} = {sol}\n"
        
        return result
    except ImportError:
        return "错误: 请安装sympy库 (pip install sympy)"
    except Exception as e:
        return f"求解错误: {str(e)}"


@registry.register(
    name="search_knowledge",
    description="搜索教育知识库中的相关内容",
    category=ToolCategory.SEARCH,
    parameters={
        "query": {
            "type": "string",
            "description": "搜索查询关键词"
        },
        "top_k": {
            "type": "number",
            "description": "返回结果数量",
            "default": 5
        }
    },
    required=["query"]
)
def search_knowledge(query: str, top_k: int = 5) -> str:
    """知识搜索工具 - 接入RAG服务"""
    return f"搜索 '{query}' 的结果（需接入RAG服务）:\n1. 相关知识点A\n2. 相关知识点B\n3. 相关知识点C"


@registry.register(
    name="generate_quiz",
    description="生成练习题",
    category=ToolCategory.DATA_ANALYSIS,
    parameters={
        "topic": {
            "type": "string",
            "description": "题目主题"
        },
        "difficulty": {
            "type": "string",
            "description": "难度: easy/medium/hard",
            "enum": ["easy", "medium", "hard"]
        },
        "count": {
            "type": "number",
            "description": "题目数量",
            "default": 5
        }
    },
    required=["topic", "difficulty"]
)
def generate_quiz(topic: str, difficulty: str, count: int = 5) -> str:
    """生成练习题"""
    questions = []
    for i in range(1, count + 1):
        questions.append(f"{i}. [{difficulty}] {topic} 相关练习题（接入LLM后生成真实题目）")
    return "\n".join(questions)


@registry.register(
    name="execute_python",
    description="执行Python代码（沙箱环境）",
    category=ToolCategory.CODE_EXECUTION,
    parameters={
        "code": {
            "type": "string",
            "description": "Python代码"
        }
    },
    required=["code"],
    dangerous=True
)
def execute_python(code: str) -> str:
    """Python代码沙箱执行"""
    import io
    import sys
    
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    try:
        forbidden = ["import os", "import sys", "open(", "eval(", "exec(",
                     "import subprocess", "import shutil", "__import__"]
        for f in forbidden:
            if f in code:
                return f"错误: 包含禁止的操作 '{f}'"
        
        exec(code, {"__builtins__": {
            "print": print, "range": range, "len": len,
            "int": int, "float": float, "str": str, "list": list[Any],
            "dict": dict[str, Any], "set": set[str], "tuple": tuple[Any, ...], "bool": bool,
            "abs": abs, "max": max, "min": min, "sum": sum,
            "round": round, "sorted": sorted, "zip": zip,
            "enumerate": enumerate, "map": map, "filter": filter
        }}, {})
        output = buffer.getvalue()
        return output or "执行完成（无输出）"
    except Exception as e:
        return f"执行错误: {str(e)}"
    finally:
        sys.stdout = old_stdout


# === 使用示例 ===
if __name__ == "__main__":
    print("=== 龍魂工具注册中心 ===")
    for tool in registry.list_tools():
        print(f"[{tool.category.value}] {tool.name}: {tool.description}")
        print(f"  参数: {list(tool.parameters.keys())}")
        print(f"  签名: {tool.dna_signature}\n")
    
    print("=== 工具执行测试 ===")
    
    result = registry.execute("calculate_math", {"expression": "sqrt(16) + pow(2, 3)"})
    print(f"calculate_math: {result}")
    
    result = registry.execute("solve_equation", {"equation": "x^2 + 5*x + 6 = 0", "variable": "x"})
    print(f"\nsolve_equation: {result}")
    
    result = registry.execute("generate_quiz", {"topic": "二次函数", "difficulty": "medium", "count": 3})
    print(f"\ngenerate_quiz:\n{result}")
    
    print("\n=== OpenAI Function Schema ===")
    schemas = registry.get_schemas()
    print(json.dumps(schemas, indent=2, ensure_ascii=False))
