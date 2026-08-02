from collections import deque
from typing import Deque, Dict, List
from mem0 import Memory

from src.config import MEMORY_CONFIG, SLIDING_WINDOW_SIZE
from src.json_store import JsonSlidingWindowStore


class SlidingWindow:
    def __init__(self, n: int = SLIDING_WINDOW_SIZE):
        if n < 1: raise ValueError("n tem de ser >= 1")

        self.n = n
        
        self.history: Deque[Dict[str, str]] = deque(maxlen=n)

        self.json = JsonSlidingWindowStore()

        # carrega o estado anterior do ficheiro, se existir
        trocas_anteriores = self.json.read()
        for conv in trocas_anteriores[-self.n:]:
            self.history.append(
                {"question": conv["question"], "answer": conv["answer"]}
            )

    def add(self, question: str, answer: str) -> None:
        self.history.append({"question": question, "answer": answer})

        self.json.write(self.get_trocas())

    def get_text(self) -> str:
        blocos: List[str] = []
        for troca in self.history:
            blocos.append(
                f"Utilizador: {troca['question']}\nAssistente: {troca['answer']}"
            )
        return "\n\n".join(blocos)

    def get_trocas(self) -> List[Dict[str, str]]:
        return list(self.history)



memory = Memory.from_config(MEMORY_CONFIG)
sliding_window = SlidingWindow()