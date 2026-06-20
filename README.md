<p style="font-size: 48px; text-align: center;">🧰 toolkit-agent</p>

<p style="font-size: 20px; text-align: center; opacity: 0.8;">
  一个轻量级 Python 框架，让大模型通过调用外部工具完成任务
</p>

<p style="font-size: 16px; text-align: center; opacity: 0.6;">
  A lightweight Python framework for letting LLMs accomplish tasks via tool-calling
</p>

---

## 📖 概述 / Overview

### 中文

toolkit-agent 是一个极简的 **AI 代理框架**，采用 **大脑 + 小脑** 的生物神经系统类比设计：

1. **定义工具** — 写一个 Python 函数，附上一份 JSON schema 描述
2. **模型选工具** — 大模型根据用户问题，从工具列表中选择合适的工具
3. **本地执行** — 在你的机器上执行代码，把结果回传给模型
4. **多步推理** — 模型可以连续调用多个工具，一步步解决复杂问题

这正是 OpenAI Code Interpreter、Claude Tools 等产品的核心原理。不同的是，**工具的实现完全在你本地，不受平台限制，可以随意扩展：数学函数、文件读写、C 扩展、自定义 API 调用……

### English

toolkit-agent is a minimal **LLM agent framework** designed using a **brain + cerebellum** biological nervous system analogy:

1. **Define tools** — Write a Python function with a JSON schema description
2. **Model chooses tools** — The LLM picks appropriate tools based on user input
3. **Local execution** — Code runs on your machine, results sent back to the model
4. **Multi-step reasoning** — The model can chain multiple tool calls to solve complex problems

This is exactly how OpenAI Code Interpreter, Claude Tools, and similar products work. The difference: **tool implementation is entirely local** — no platform lock-in, freely extensible with math functions, file I/O, C extensions, custom API calls...

---

## 🏗️ 架构 / Architecture

### 中文

项目采用 **大脑 + 小脑** 的生物神经系统类比架构：

| 部件 / Component | 代码 / Code | 类比 / Analogy | 职责 / Responsibility |
|---|---|---|---|
| 🧠 **大脑** | `toolkit_agent.py` + 大模型 | 总指挥 | 任务理解、分解、调度工具 |
| 🗺️ **地图小脑** | `get_position` | 定位/地图 | 位置名 → 坐标查询 |
| 🦵 **运动小脑** | `navigate_grid` | 腿 | 空间导航、路径规划 |
| 🤚 **动作小脑** | `do_task` | 手 | 原子化动作执行 |

简单来说，`toolkit_agent.py` 负责调度（大脑），`tools.py` 负责干活（各种小脑）。你可以随意往 `tools.py` 里加新工具（数学计算、文件读写、外部 API、甚至用 ctypes 引入 C 扩展），主程序一行都不用改。

### English

The project uses a **brain + cerebellum** biological nervous system analogy:

| Component | Code | Analogy | Responsibility |
|---|---|---|---|
| 🧠 **Brain** | `toolkit_agent.py` + LLM | Commander | Task understanding, decomposition, tool orchestration |
| 🗺️ **Map cerebellum** | `get_position` | Location/Map | Name → coordinate lookup |
| 🦵 **Motor cerebellum** | `navigate_grid` | Legs | Spatial navigation, path planning |
| 🤚 **Action cerebellum** | `do_task` | Hands | Atomic action execution |

In short, `toolkit_agent.py` handles orchestration (the brain), and `tools.py` handles the actual work (various cerebellums). You can freely add new tools to `tools.py` (math operations, file I/O, external API calls, even C extensions via ctypes) without touching the main program.

---

## ⚙️ 核心机制 / How It Works

### 中文

一次完整的工具调用循环分为以下几步：

1. 你输入一个问题，主程序把它发送给大模型，同时附上所有工具的 JSON schema 描述。
2. 大模型读到这些描述后，判断哪些工具可以解决问题。它会返回一个结构化的工具调用请求（包含工具名和参数）。
3. 主程序从工具映射表里找到对应的 Python 函数，用模型给出的参数去调用它。
4. 函数执行后，主程序把结果回传给大模型。
5. 大模型收到结果后，可以继续选择调用下一个工具，或者直接给出最终回答。
6. 如果还需要工具就回到第 2 步继续循环；如果不需要了，就把自然语言回答返回给你。

整个过程对用户是透明的——你只管提问，其余的都由主程序自动处理。

### English

One complete tool-call cycle works as follows:

1. You type a question. The main program sends it to the LLM, along with the JSON schema descriptions of all available tools.
2. The LLM reads these descriptions and decides which tools can help solve the problem. It returns a structured tool-call request containing tool names and arguments.
3. The main program looks up the corresponding Python function from the function map, then calls it with the model's arguments.
4. After the function runs, the main program sends the result back to the LLM.
5. The LLM, now armed with the result, can either choose to call another tool, or produce a final natural-language answer.
6. If more tools are needed, the loop goes back to step 2; otherwise, the LLM returns its final answer to you.

The entire process is transparent to the user — you just ask questions, and the main program handles everything else automatically.

---

## 🛠️ 内置工具 / Built-in Tools

### 数学计算 / Math

| 工具 / Tool | 说明 / Description |
|---|---|
| `add(arr)` | 数组求和（支持任意多个数）/ Sum any number of values |
| `sub(a, b)` | 减法 / Subtraction |
| `mul(a, b)` | 乘法 / Multiplication |
| `div(a, b)` | 除法 / Division |
| `sqrt(a)` | 平方根 / Square root |
| `pow(a, b)` | 幂运算 / Power |
| `log(a)` | 自然对数 / Natural logarithm |
| `sort_array(arr, descending)` | 数组排序 / Sort array |

### 安全与哈希 / Security & Hash

| 工具 / Tool | 说明 / Description |
|---|---|
| `hash_string(text, algorithm)` | 字符串哈希 / Hash a string (md5, sha1, sha256, sha512) |
| `hash_file(filename, algorithm)` | 文件哈希 / Hash a file |
| `compare_strings(a, b)` | 安全字符串比较（防时序攻击）/ Safe string comparison (timing-attack proof) |

### 文件与代码执行 / File & Code Interpreter

| 工具 / Tool | 说明 / Description |
|---|---|
| `write_file(filename, content)` | 写文件到 `workspace/` / Write file to `workspace/` |
| `read_file(filename)` | 从 `workspace/` 读文件 / Read file from `workspace/` |
| `run_python(filename)` | 执行 Python 脚本（子进程，有超时保护）/ Execute Python script in subprocess with timeout |

> **重要**：脚本内部可以直接 `from tools import add, sqrt, sort_array, ...` 来复用已有的工具函数，无需重写。

### 导航与动作 / Navigation & Actions

| 工具 / Tool | 类比 / Analogy | 说明 / Description |
|---|---|---|
| `get_position(location_name, map_data)` | 🗺️ 地图/定位 | 查询位置坐标（位置名→坐标） / Look up coordinates by name |
| `navigate_grid(start, target, grid_size, obstacles)` | 🦵 腿 | 网格导航 / Navigate on a grid |
| `do_task(instruction, env_data)` | 🤚 手 | 原子化动作执行 / Execute atomic actions |

---

## 📦 安装 / Installation

### 中文

1. **克隆项目**

```bash
git clone <your-repo-url>
cd toolkit-agent
```

2. **安装依赖**

```bash
pip3 install openai
```

3. **配置 API 密钥**（任选其一）：

```bash
# DeepSeek
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://api.deepseek.com/v1"
export MODEL="deepseek-chat"

# 或：硅基流动 / SiliconFlow
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://api.siliconflow.cn/v1"
export MODEL="Qwen/Qwen2.5-7B-Instruct"

# 或：通义千问
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MODEL="qwen3-max"
```

4. **运行**

```bash
python3 toolkit_agent.py
```

### English

1. **Clone the project**

```bash
git clone <your-repo-url>
cd toolkit-agent
```

2. **Install dependencies**

```bash
pip3 install openai
```

3. **Configure API key** (choose one):

```bash
# DeepSeek
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://api.deepseek.com/v1"
export MODEL="deepseek-chat"

# or: SiliconFlow
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://api.siliconflow.cn/v1"
export MODEL="Qwen/Qwen2.5-7B-Instruct"

# or: Qwen / 通义千问
export API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MODEL="qwen3-max"
```

4. **Run**

```bash
python3 toolkit_agent.py
```

---

## 🚀 使用示例 / Usage Examples

### 示例 1：多步数学计算 / Multi-step math

```
你: 100加200，再把结果乘以3，最后开平方
第 1 轮
  [工具调用] add({'arr': [100, 200]})
  [执行结果] 300
第 2 轮
  [工具调用] mul({'a': 300, 'b': 3})
  [执行结果] 900
第 3 轮
  [工具调用] sqrt({'a': 900})
  [执行结果] 30.0
AI: 最终结果约为 30。
```

### 示例 2：导航与动作任务 / Navigation and actions task

```
你: 去厨房拿一杯水，放到桌子上
第 1 轮
  [工具调用] get_position({'location_name': 'kitchen'})
  [执行结果] Location 'kitchen' is at [3,5]
第 2 轮
  [工具调用] navigate_grid({'start': [0,0], 'target': [3,5]})
  [执行结果] (导航日志...)
第 3 轮
  [工具调用] do_task({'instruction': 'grab a cup of water'})
  [执行结果] (动作执行日志...)
...
```

---

## 🔧 扩展指南：添加新工具 / Adding New Tools

只需在 `tools.py` 中**改三处**：

### 中文

```python
# ① 在 TOOLS_SCHEMA 中加 schema
{
    "type": "function",
    "function": {
        "name": "factorial",
        "description": "Calculate the factorial of a number (n!)",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {"type": "integer", "description": "The number to compute factorial for"}
            },
            "required": ["n"]
        }
    }
}

# ② 加函数实现
def factorial(n: int) -> int:
    """Calculate n!"""
    import math
    return math.factorial(n)

# ③ 加进映射表
FUNCTIONS = {
    ...,
    "factorial": factorial,
}
```

完事，`toolkit_agent.py` 一行都不用改。

### English

Just **three changes** in `tools.py`:

```python
# ① Add schema to TOOLS_SCHEMA
{
    "type": "function",
    "function": {
        "name": "factorial",
        "description": "Calculate the factorial of a number (n!)",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {"type": "integer", "description": "The number to compute factorial for"}
            },
            "required": ["n"]
        }
    }
}

# ② Add function implementation
def factorial(n: int) -> int:
    """Calculate n!"""
    import math
    return math.factorial(n)

# ③ Add to function map
FUNCTIONS = {
    ...,
    "factorial": factorial,
}
```

That's it — no changes needed in `toolkit_agent.py`.

---

## 🌐 支持的大模型 / Supported LLMs

任何兼容 OpenAI 协议的 API 都能用 / Works with any OpenAI-compatible API:

| 服务商 / Provider | 模型示例 / Example Model | BASE_URL |
|---|---|---|
| DeepSeek | `deepseek-chat` | `https://api.deepseek.com/v1` |
| 硅基流动 / SiliconFlow | `Qwen/Qwen2.5-7B-Instruct` | `https://api.siliconflow.cn/v1` |
| 通义千问 / Qwen | `qwen3-max` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| OpenAI | `gpt-4o-mini` | `https://api.openai.com/v1` |
| Ollama（本地 / local） | `qwen3:4b` | `http://localhost:11434/v1` |

---

## 📂 项目结构 / Project Structure

```
toolkit-agent/
├── toolkit_agent.py    # 主程序：与大模型对话 / Main: chat with LLM
├── tools.py           # 工具模块：函数 + schema + 映射表 / Tools module: functions + schemas + function map
├── run.sh             # 一键启动脚本 / One-click startup script (API key here)
├── workspace/         # 脚本读写工作区 / Workspace for write_file / run_python
└── README.md           # 本文件 / This file
```

---

## 📝 开源协议 / License

MIT
