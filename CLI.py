
import ollama
import argparse
import os  # ✅ 加个 os 导入！
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.status import Status
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List, Dict

# 初始化 Rich Console
console = Console()

# 函数定义
function_schemas = {
    "add": {
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
    "sub": {
        "type": "function",
        "function": {
            "name": "sub",
            "description": "Subtract two numbers (a - b)",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "The first number"},
                    "b": {"type": "integer", "description": "The second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
}

function_defs = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b
}

class AIAssistant:
    def __init__(self):
        self.history: List[Dict[str, str]] = []  # ✅ 上下文记忆！

    def call_ollama(self, prompt, model='gemma3:1b'):
        try:
            response = ollama.chat(model=model, messages=[{'role':'user','content':prompt}])
            return response['message']['content']
        except Exception as e:
            return f"模型调用失败: {str(e)}"

    def is_math_question(self, msg):
        check_prompt = f"""
请判断用户输入是否为数学计算问题，只返回 yes 或 no，不要其他任何文字！

例子：
输入：计算1+2 → yes
输入：1+2等于几 → yes
输入：我不爱吃牛肉 → no
输入：今天天气真好 → no

现在判断：{msg}
请只返回 yes 或 no！
""".strip()
        try:
            response = ollama.chat(model='qwen3:4b', messages=[{'role':'user','content':check_prompt}])
            return response['message']['content'].strip().lower()
        except:
            return 'no'

    def call_ollama_with_functions(self, msg):
        tool_name = self.call_ollama(msg + ",请在如下函数中选择一个最合适的返回，仅返回如下:add、sub中一个")
        tool_name = tool_name.strip().lower()

        tools = []
        if tool_name in function_schemas:
            tools.append(function_schemas[tool_name])

        if not tools:
            console.print("抱歉，我暂时只会加减！", style="yellow")
            return

        messages = [{'role': 'user', 'content': msg}]
        with Status("[cyan]思考中...[/cyan]", console=console):
            response = ollama.chat(model='qwen3:4b', messages=messages, tools=tools)

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                console.print(f"🔧 工具调用: [bold magenta]{tool_call.function.name}[/bold magenta]")
                console.print(f"  参数: [dim]{tool_call.function.arguments}[/dim]")
                func = function_defs[tool_call.function.name]
                result = func(**tool_call.function.arguments)
                console.print(f"✅ 执行结果: [bold green]{result}[/bold green]")
                solution = self.call_ollama(f"用一段话说明这个问题的思路：{msg}")
                console.print(f"💡 解决思路: {solution}")
                self.history.append({'role':'assistant','content':f"执行结果: {result}\n思路: {solution}"})
                return result

    def chat(self):
        # ✅ 1. 先清屏（看起来更干净，去掉前面的地址干扰）
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # ✅ 2. Panel 居中显示（加上 width=60，居中对齐）
        console.print(
            Panel.fit(
                "[bold cyan]AI Assistant[/bold cyan]\n[dim]输入 'quit' 或 'q' 退出[/dim]",
                title="🚀 启动",
                width=100  # 固定宽度，更美观
            ),
            justify="center"  # 整体居中！
        )
        
        while True:
            try:
                user_input = Prompt.ask("你")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("\n👋 再见！", style="bold red")
                    break
                
                self.history.append({'role':'user','content':user_input})
                
                flag = self.is_math_question(user_input)
                
                if 'yes' in flag:
                    self.call_ollama_with_functions(user_input)
                else:
                    with Status("[cyan]思考中...[/cyan]", console=console):
                        response = self.call_ollama(user_input)
                    self.history.append({'role':'assistant','content':response})
                    console.print(f"\n[bold cyan]AI[/bold cyan]: {response}\n")
                
            except KeyboardInterrupt:
                console.print("\n👋 再见！", style="bold red")
                break
            except Exception as e:
                console.print(f"⚠️ 出错了: {str(e)}", style="red")

def single_query_mode(query):
    assistant = AIAssistant()
    flag = assistant.is_math_question(query)
    if 'yes' in flag:
        assistant.call_ollama_with_functions(query)
    else:
        response = assistant.call_ollama(query)
        console.print(f"\n[bold cyan]AI[/bold cyan]: {response}\n")

def main():
    parser = argparse.ArgumentParser(description="AI Assistant - 计算器 + 聊天 (仿 Claude Code 风格)")
    parser.add_argument('--query', '-q', type=str, help="单次查询，直接传入问题")
    parser.add_argument('--chat', '-c', action='store_true', help="进入循环聊天模式")
    
    args = parser.parse_args()
    
    if args.query:
        single_query_mode(args.query)
    else:
        assistant = AIAssistant()
        assistant.chat()

if __name__ == "__main__":
    main()
