import ollama

from src.config import DEFAULT_MODEL, DEFAULT_OPTIONS, SYSTEM_PROMPT

def chat_with_llm(message: str, history: list[dict], long_term: list) -> str:
    
    # Formata as memórias para texto legível
    memory_context = ""
    if long_term:
        formatted = "\n".join(f"- {m['memory']}" for m in long_term)
        memory_context = f"\n\nRelevant things you remember about the user:\n{formatted}"

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + memory_context  # <-- injecta aqui
        }
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = ollama.chat(
        model=DEFAULT_MODEL,
        options=DEFAULT_OPTIONS,
        messages=messages
    )

    return response.message.content