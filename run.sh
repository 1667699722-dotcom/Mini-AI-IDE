source venv/bin/activate
# 打包！
pyinstaller --onefile --name ai-assistant --hidden-import rich --hidden-import ollama CLI.py
