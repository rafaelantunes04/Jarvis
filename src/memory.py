from collections import deque
from typing import Deque, Dict, List
from mem0 import Memory as Mem0Memory

from src.config import MEMORY_CONFIG, SLIDING_WINDOW_SIZE, SLIDING_WINDOW_MAX_TOKENS, USER_ID
from src.json_store import JsonSlidingWindowStore

"""
Every class/function below handles the short-term (sliding window) and
long-term (mem0) conversation memory used by the chat assistant.
"""


def exceeds_context_limit(text: str, token_limit: int = SLIDING_WINDOW_MAX_TOKENS) -> bool:
    """
    (Helper)
    Estimates whether a given text exceeds the allowed token limit

    (Used by Memory to decide when to flush to long-term memory)
    """
    total_characters = len(text)

    estimated_tokens = total_characters // 2.5

    return estimated_tokens > token_limit



class Memory:
    """
    (Chatbot memory)
    Class used to keep the last N question/answer exchanges in memory
    """

    def __init__(self, n: int = SLIDING_WINDOW_SIZE, max_tokens: int = SLIDING_WINDOW_MAX_TOKENS):
        if n < 1: raise ValueError("n must be >= 1")

        if max_tokens < 2000: raise ValueError("max_tokens must be >= 2000")

        # Basic vars
        self.n = n
        self.max_tokens = max_tokens
        self.json = JsonSlidingWindowStore()


        # Memory object vars
        self.history: Deque[Dict[str, str]] = deque()
        self.long_term_memory = Mem0Memory.from_config(MEMORY_CONFIG)


        # load previous exchanges if they exist
        previous_exchanges = self.json.read()
        for exchange in previous_exchanges:
            self.history.append(
                {"question": exchange["question"], "answer": exchange["answer"]}
            )

        # flush in case the limit is already exceeded
        if exceeds_context_limit(self.get_text(), self.max_tokens):
            self._flush_to_long_term_memory()

    def add(self, question: str, answer: str) -> None:
        """
        Adds a new question/answer exchange to the sliding window
        """

        self.history.append({"question": question, "answer": answer})

        if exceeds_context_limit(self.get_text(), self.max_tokens):
            self._flush_to_long_term_memory()

        self.json.write(self.get_exchanges())

    def _flush_to_long_term_memory(self) -> None:
        """
        Sends the oldest exchanges to long-term memory (mem0) and keeps
        only the last n exchanges in the sliding window
        """

        messages = []
        for exchange in self.history:
            messages.append({"role": "user", "content": exchange["question"]})
            messages.append({"role": "assistant", "content": exchange["answer"]})

        if messages:
            self.long_term_memory.add(messages, user_id=USER_ID)

        # keep only the last n exchanges in the window
        last_ones = list(self.history)[-self.n:]
        self.history = deque(last_ones)

    def get_text(self) -> str:
        """
        Returns the sliding window formatted as plain text
        """

        blocks: List[str] = []
        for exchange in self.history:
            blocks.append(
                f"User: {exchange['question']}\nAssistant: {exchange['answer']}"
            )
        return "\n\n".join(blocks)

    def get_exchanges(self) -> List[Dict[str, str]]:
        """
        Returns the sliding window as a list of question/answer dicts
        """
        return list(self.history)


memory = Memory()