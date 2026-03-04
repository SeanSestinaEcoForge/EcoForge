# src/tools/examples/simple_grok_chat.py
from src.core.xai_client import create_chat

chat = create_chat()

# Fixed: use dict format instead of undefined 'user'
chat.append({"role": "user", "content": "Explain closed-loop homestead in 2 sentences."})

response = chat.sample()
print("Response:", response.content)
