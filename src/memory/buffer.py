from abc import ABC, abstractmethod
from collections import deque

from src.memory.json_store import JsonSlidingWindowStore


def estimate_tokens(text: str) -> int:
    return int(len(text) / 2.5)


class Buffer(ABC):
    """
    Lista das mensagens mais antigas para as mais novas, mais antigas primeiro
    """
    def __init__(self, n: int, json_name: str):
        # Basic vars
        self.n = n
        self.json = JsonSlidingWindowStore(json_name=json_name)

        # Memory object vars
        self.history: deque[dict[str, str]] = deque()

        # load previous exchanges if they exist
        previous_exchanges = self.json.read()
        for exchange in previous_exchanges:
            self.history.append(
                {"question": exchange["question"], "answer": exchange["answer"]}
            )


    def add(self, question: str, answer: str) -> None:
        """
        Adds a new question/answer exchange to the buffer
        """
        self.history.append({"question": question, "answer": answer})

    def pop(self) -> dict[str, str]:
        """
        Pops the oldest exchange from the front of the buffer
        """
        return self.history.popleft()

    def update_json(self):
        """
        Updates the json
        """
        self.json.write(self.get_history())

    @abstractmethod
    def _exceeds_limit(self) -> bool:
        """
        Each subclass defines the criterion that determines whether the
        buffer has exceeded its limit (number of exchanges, number of
        tokens, etc.)
        """
        raise NotImplementedError

    def clear(self) -> None:
        """
        Empties the sliding window entirely and persists the (now empty)
        state to disk.
        """
        self.history.clear()

    def get_history(self) -> list[dict[str, str]]:
        """
        Returns the sliding window as a list of question/answer dicts
        """
        return list(self.history)


class ConversationBuffer(Buffer):
    """
    Sliding window bounded by number of exchanges (conversations).
    When the history exceeds `n` exchanges, the oldest one is dropped
    (and returned by `add`).
    """

    def _exceeds_limit(self) -> bool:
        return len(self.history) > self.n


class TokenBuffer(Buffer):
    """
    Sliding window bounded by number of tokens.
    When the history text exceeds `n` tokens, the oldest exchange is
    dropped from the front (and returned by `add`).
    """
    def _exceeds_limit(self) -> bool:
        all_text = " ".join(
            e["question"] + " " + e["answer"] for e in self.history
        )
        return estimate_tokens(all_text) > self.n