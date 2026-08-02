import ollama

from src.config import DEFAULT_MODEL, DEFAULT_OPTIONS, SYSTEM_PROMPT

def chat_with_llm(message: str) -> str:
    response = ollama.chat(
        model=DEFAULT_MODEL,
        options=DEFAULT_OPTIONS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
    )

    return response.message.content