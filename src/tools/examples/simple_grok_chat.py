# examples/simple_grok_chat.py
from src.core.xai_client import create_chat

chat = create_chat()
chat.append(user("Explain closed-loop homestead in 2 sentences."))

# Non-streaming
response = chat.sample(temperature=0.7, max_tokens=200)
print("Full response:", response.content)

# Streaming version
print("\nStreaming:")
for chunk in chat.stream():
    print(chunk.content, end="", flush=True)
print()
