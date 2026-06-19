# /Users/liuhuachao/Documents/trae_projects/internet/tools.py
"""
工具函数模块 —— 任何 Python 脚本都能 import 这里的函数

用法示例:
    from tools import add, mul, FUNCTIONS, TOOLS_SCHEMA
    print(add(100, 200))        # 直接调用
    func = FUNCTIONS["mul"]     # 通过名字动态查找
    schema = TOOLS_SCHEMA       # 拿给大模型的描述
"""
import math
# ========== 工具描述（给大模型看的 schema） ==========
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "The first number"},
                    "b": {"type": "integer", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sub",
            "description": "Subtract two numbers (a minus b)",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "The first number (minuend)"},
                    "b": {"type": "integer", "description": "The second number (subtrahend)"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mul",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "The first number"},
                    "b": {"type": "integer", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "div",
            "description": "Divide two numbers (a divided by b)",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The dividend"},
                    "b": {"type": "number", "description": "The divisor (cannot be zero)"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sqrt",
            "description": "Calculate the square root of a number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The number to square root"}
                },
                "required": ["a"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pow",
            "description": "Calculate a number raised to the power of another number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The base number"},
                    "b": {"type": "number", "description": "The exponent"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log",
            "description": "Calculate the logarithm of a number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The number to log"}
                },
                "required": ["a"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_array",
            "description": "Sort an array of numbers in ascending or descending order. Returns the sorted array.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arr": {
                        "type": "array",
                        "description": "The array of numbers to sort",
                        "items": {"type": "number"}
                    },
                    "descending": {
                        "type": "boolean",
                        "description": "If true, sort from largest to smallest. Default is false (ascending)."
                    }
                },
                "required": ["arr"]
            }
        }
    }
]


# ========== 工具实现 ==========
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def sub(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b

def mul(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

def div(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return "Error: division by zero"
    return a / b

def sqrt(a: float) -> float:
    """Calculate the square root of a number."""
    return math.sqrt(a)

def pow(a: float, b: float) -> float:
    """Calculate a number to the power of another number."""
    return a ** b

def log(a: float) -> float:
    """Calculate the natural logarithm of a number."""
    return math.log(a)

def sort_array(arr: list, descending: bool = False) -> list:
    """Sort an array of numbers in ascending (default) or descending order."""
    return sorted(arr, reverse=descending)



# 函数映射表：函数名 -> 函数对象（供动态调用）
FUNCTIONS = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "sqrt": sqrt,
    "pow": pow,
    "log": log,
    "sort_array": sort_array,
}