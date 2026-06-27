import ollama

from src.config import DEFAULT_MODEL


def chat_with_llm(message: str) -> str:
    response = ollama.chat(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "user", "content": message}
        ],
    )

    return response.message.content