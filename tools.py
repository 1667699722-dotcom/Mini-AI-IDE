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
import os
import subprocess
import sys
import hashlib
import hmac

# ========== 工作区路径（文件读写/脚本执行都限制在这里） ==========
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# 安全：解析路径后必须仍在 workspace 里，防止路径穿越
def _safe_path(filename: str) -> str:
    safe = os.path.normpath(os.path.join(WORKSPACE_DIR, filename))
    if not safe.startswith(WORKSPACE_DIR):
        raise ValueError(f"Invalid filename: {filename} (path traversal not allowed)")
    return safe

# ========== 工具描述（给大模型看的 schema） ==========
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two or more numbers together. Takes an array of numbers and returns their sum. Use this instead of calling add(a,b) repeatedly — one call with an array [1,2,3,4] is enough.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arr": {
                        "type": "array",
                        "description": "Array of numbers to add together, e.g. [1, 2, 3] or [3.14, 2.71, 1.41]",
                        "items": {"type": "number"}
                    }
                },
                "required": ["arr"]
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
    },
    {
        "type": "function",
        "function": {
            "name": "compare_strings",
            "description": "Compare two strings for equality. Uses constant-time comparison to prevent timing attacks (safe for passwords/keys).",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "First string to compare"
                    },
                    "b": {
                        "type": "string",
                        "description": "Second string to compare"
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hash_string",
            "description": "Calculate hash of a string. Supports md5, sha1, sha256, sha512 (default is sha256).",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The string to hash"
                    },
                    "algorithm": {
                        "type": "string",
                        "description": "Hash algorithm to use (md5, sha1, sha256, sha512). Default: sha256",
                        "enum": ["md5", "sha1", "sha256", "sha512"]
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hash_file",
            "description": "Calculate hash of a file from workspace. Supports large files (reads in chunks to avoid memory issues).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename in workspace to hash"
                    },
                    "algorithm": {
                        "type": "string",
                        "description": "Hash algorithm to use (md5, sha1, sha256, sha512). Default: sha256",
                        "enum": ["md5", "sha1", "sha256", "sha512"]
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file in the workspace directory. If the file exists, it will be overwritten. Use this to save data, notes, or Python scripts. IMPORTANT: When writing Python code can import reusable functions from tools via 'from tools import <function_name>'. Pick appropriate functions from tools.FUNCTIONS — e.g. add, sub, mul, div, sqrt, pow, log, sort_array, write_file, read_file, run_python. Reuse them instead of reimplementing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The filename (relative to workspace dir), e.g. 'my_script.py' or 'notes.txt'"
                    },
                    "content": {
                        "type": "string",
                        "description": "The file content to write. For Python code, include the full script here."
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the content of a file from the workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The filename to read (relative to workspace dir)"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Execute a Python script file that was previously written to the workspace directory via write_file. Returns the combined stdout and stderr output. Has a time limit (the script cannot run forever). IMPORTANT: always write the script first with write_file, then call this tool with that filename.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The Python script filename in the workspace dir, e.g. 'my_script.py'"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum seconds the script is allowed to run. Default 15 seconds."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_position",
            "description": "Get coordinates of a named location. Pass a location name (e.g. 'kitchen', 'trash_bin', 'table') and get its [x,y] coordinates. Returns None if location not found.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location to find (e.g. 'kitchen', 'trash_bin', 'table')"
                    },
                    "map_data": {
                        "type": "object",
                        "description": "Optional map data (key: location_name, value: [x,y] coordinates). If not provided, uses default map."
                    }
                },
                "required": ["location_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "navigate_grid",
            "description": "Navigate on a grid from start position to target position. Moves step by step until reaching the target or hitting obstacles. Returns the path taken.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "array",
                        "description": "Start position [x, y]",
                        "items": {"type": "integer"}
                    },
                    "target": {
                        "type": "array",
                        "description": "Target position [x, y]",
                        "items": {"type": "integer"}
                    },
                    "grid_size": {
                        "type": "integer",
                        "description": "Size of the grid (grid_size x grid_size). Default: 10"
                    },
                    "obstacles": {
                        "type": "array",
                        "description": "List of obstacle positions [[x1,y1], [x2,y2], ...]. Default: empty"
                    }
                },
                "required": ["start", "target"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "do_task",
            "description": "Generic task execution engine. Reads instruction + environment data, outputs action tokens with completion status codes. Status codes: 00=task true not done, 01=task true executing, 10=task true completed (terminate), 11=task false (terminate). Recurses until status is 10 or 11.",
            "parameters": {
                "type": "object",
                "properties": {
                    "instruction": {
                        "type": "string",
                        "description": "Natural language instruction from the model, e.g. 'move to position (5,5) and grab the object'"
                    },
                    "env_data": {
                        "type": "object",
                        "description": "External environment data (arbitrary dict), e.g. {'position': [0,0], 'objects': ['box'], 'battery': 80}"
                    }
                },
                "required": ["instruction", "env_data"]
            }
        }
    }
]


# ========== 工具实现 ==========
def add(arr: list) -> float:
    """Add two or more numbers together. Takes an array and returns their sum."""
    total = 0
    for x in arr:
        total += x
    return total

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

def hash_string(text: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a string."""
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(text.encode("utf-8"))
    return hash_obj.hexdigest()

def compare_strings(a: str, b: str) -> bool:
    """Compare two strings using constant-time comparison."""
    return hmac.compare_digest(a, b)

def hash_file(filename: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file from workspace."""
    path = _safe_path(filename)
    hash_obj = hashlib.new(algorithm)
    chunk_size = 65536  # 64 KB chunks
    with open(path, "rb") as f:
        chunk = f.read(chunk_size)
        while chunk:
            hash_obj.update(chunk)
            chunk = f.read(chunk_size)
    return hash_obj.hexdigest()

def write_file(filename: str, content: str) -> str:
    """Write content to a file in workspace/. Returns a confirmation message."""
    path = _safe_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {filename} ({len(content)} chars, saved in workspace/)"

def read_file(filename: str) -> str:
    """Read content of a file from workspace/."""
    path = _safe_path(filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return f"--- content of {filename} ---\n{content}"

def run_python(filename: str, timeout: int = 15) -> str:
    """Execute a Python script in workspace/. Returns stdout+stderr."""
    path = _safe_path(filename)
    if not os.path.exists(path):
        return f"Error: file '{filename}' not found in workspace. Use write_file first."
    try:
        # 把项目根目录加入 PYTHONPATH，让脚本可以 import tools
        env = os.environ.copy()
        project_root = os.path.dirname(os.path.abspath(__file__))
        old_pp = env.get("PYTHONPATH", "")
        if old_pp:
            env["PYTHONPATH"] = project_root + ":" + old_pp
        else:
            env["PYTHONPATH"] = project_root
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=timeout,
            cwd=WORKSPACE_DIR,
            env=env,
        )
        output = (result.stdout or "") + (result.stderr or "")
        status = "OK" if result.returncode == 0 else f"exit code {result.returncode}"
        return f"[ran {filename} — {status}]\n{output.rstrip() if output.strip() else '(no output)'}"
    except subprocess.TimeoutExpired:
        return f"Error: script exceeded {timeout}s time limit"
    except Exception as e:
        return f"Error running script: {e}"


def navigate_grid(start: list, target: list, grid_size: int = 10, obstacles: list = None) -> str:
    """Navigate on a grid from start to target, step by step."""
    if obstacles is None:
        obstacles = []
    obstacles_set = set(tuple(o) for o in obstacles)

    current = list(start)
    path = [list(current)]
    steps = 0
    max_steps = grid_size * grid_size * 2

    log = [f"🚀 开始导航：从 {start} 到 {target}"]
    log.append(f"网格大小: {grid_size}x{grid_size}")
    log.append(f"障碍物: {obstacles if obstacles else '无'}")
    log.append("-" * 50)

    while steps < max_steps:
        if current == target:
            log.append(f"✅ 到达目的地！共走了 {steps} 步")
            log.append(f"路径: {path}")
            return "\n".join(log)

        # 简单的贪心算法：优先向目标方向移动
        dx = target[0] - current[0]
        dy = target[1] - current[1]

        # 尝试的移动方向（优先级：向目标方向优先）
        directions = []
        if dx > 0:
            directions.append([1, 0])
        elif dx < 0:
            directions.append([-1, 0])
        if dy > 0:
            directions.append([0, 1])
        elif dy < 0:
            directions.append([0, -1])
        # 备选方向
        directions.extend([[1, 0], [-1, 0], [0, 1], [0, -1]])

        moved = False
        for d in directions:
            next_pos = [current[0] + d[0], current[1] + d[1]]

            # 检查边界
            if next_pos[0] < 0 or next_pos[0] >= grid_size or next_pos[1] < 0 or next_pos[1] >= grid_size:
                continue
            # 检查障碍物
            if tuple(next_pos) in obstacles_set:
                continue
            # 检查是否已经走过（避免死循环）
            if next_pos in path:
                continue

            # 移动！
            current = next_pos
            path.append(list(current))
            steps += 1
            log.append(f"第 {steps} 步: 移动到 {current}")
            moved = True
            break

        if not moved:
            log.append(f"❌ 无法继续移动！被困在 {current}")
            log.append(f"已走路径: {path}")
            return "\n".join(log)

    log.append(f"❌ 超过最大步数限制 ({max_steps} 步)")
    return "\n".join(log)


def get_position(location_name: str, map_data: dict = None) -> str:
    """
    🗺️ Get coordinates of a named location.
    Default map is a simple office layout; pass custom map_data to override.
    """
    default_map = {
        "start": [0, 0],
        "kitchen": [3, 5],
        "trash_bin": [2, 1],
        "table": [6, 8],
        "trash_station": [9, 9],
        "exit": [0, 9]
    }
    active_map = map_data or default_map
    location_name = location_name.lower().replace(" ", "_")
    pos = active_map.get(location_name)
    if pos:
        return f"Location '{location_name}' is at {pos}"
    else:
        return f"Location '{location_name}' not found. Available locations: {list(active_map.keys())}"


# ========== 泛化干活函数：递归执行引擎 ==========
# 注意：navigate_grid 是空间问题求解器，本函数是特定场景任务执行引擎
# 两者完全独立，互不调用，互不依赖

def _llm_map(instruction: str, env_data: dict, step: int, state: dict) -> tuple:
    """
    [占位接口] 外部大模型映射函数
    输入: 指令 + 环境数据 + 当前步数 + 状态字典
    输出: (动作 token, 状态码)

    状态码约定：
      00 = 任务为真，未完成  → 继续递归
      01 = 任务为真，执行中  → 继续递归
      10 = 任务为真，已完成  → 终止
      11 = 任务为假        → 终止

    TODO: 接入具体大模型 API。当前为最小兜底逻辑，
          便于架构先跑通，未来直接替换此处即可。
    """
    # —— 大模型接口留空 ——
    # 以下仅为最小可运行骨架，不包含任何业务逻辑
    # 真实替换时：把 instruction/env_data/step/state
    # 喂给 LLM，让它返回 (action_token, status_code)
    # ————————————————————

    # 兜底：空指令视为任务为假；其他走 00→01→10 的简单推进
    if not instruction.strip():
        return ("NO_OP", "11")

    # 简单推进状态机（仅为让架构能跑）
    if step == 0:
        status = "00"
    elif step < 3:
        status = "01"
    else:
        status = "10"

    token = f"ACT_{step}"
    return (token, status)


def do_task(instruction: str, env_data: dict) -> str:
    """
    泛化干活函数：递归执行引擎
    输入: 语言指令 + 环境数据（任意 dict）
    输出: 动作 token 序列 + 最终状态码

    核心：递归调用 _llm_map 获取 (token, status)，
         直到 status == 10 或 11 才终止。
    与 navigate_grid 完全解耦：导航是空间问题，本函数是场景任务问题。
    """
    output_lines = []
    output_lines.append(f"🔧 干活引擎启动")
    output_lines.append(f"指令: {instruction}")
    output_lines.append(f"环境: {env_data}")
    output_lines.append("-" * 50)

    def _recurse(step: int, state: dict) -> None:
        """递归核心：每步只依赖 _llm_map 的映射结果"""
        token, status = _llm_map(instruction, env_data, step, state)

        output_lines.append(f"[{step:02d}] token={token}  status={status}")

        # 终止条件：10 或 11
        if status in ("10", "11"):
            status_text = {"10": "✅ 任务完成", "11": "❌ 任务为假"}
            output_lines.append("-" * 50)
            output_lines.append(f"{status_text[status]} | 总步数: {step}")
            return

        # 状态累积（留给未来 LLM 使用）
        state[f"step_{step}"] = token
        state["last_token"] = token

        # 安全上限：防止 LLM 出现 bug 时无限递归
        if step >= 99:
            output_lines.append(f"[99] token=SAFE_STOP  status=10")
            output_lines.append("-" * 50)
            output_lines.append(f"✅ 达到安全步数上限 | 总步数: 99")
            return

        _recurse(step + 1, state)

    _recurse(0, {})
    return "\n".join(output_lines)


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
    "hash_string": hash_string,
    "compare_strings": compare_strings,
    "hash_file": hash_file,
    "write_file": write_file,
    "read_file": read_file,
    "run_python": run_python,
    "get_position": get_position,
    "navigate_grid": navigate_grid,
    "do_task": do_task,
}