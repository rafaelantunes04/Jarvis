from mem0 import Memory as Mem0Memory

from src.config import MEMORY_CONFIG, USER_ID, SLIDING_WINDOW_SIZE, SLIDING_WINDOW_MAX_TOKENS
from src.memory.buffer import Buffer, ConversationBuffer, TokenBuffer
"""
Every class/function below handles the short-term (sliding window) and
long-term (mem0) conversation memory used by the chat assistant.
"""


class Memory:
    """
    (Chatbot memory)
    Class used to keep the last N question/answer exchanges in memory
    """
    def __init__(self):
        # Memory Spaces
        self.conv_buffer = ConversationBuffer(n=SLIDING_WINDOW_SIZE, json_name="conv_buffer")
        self.token_buffer = TokenBuffer(n=SLIDING_WINDOW_MAX_TOKENS, json_name="token_buffer")
        self.long_term_memory = Mem0Memory.from_config(MEMORY_CONFIG)

        # flush in case the limit is already exceeded
        if self.token_buffer._exceeds_limit():
            self._add_to_long_term_memory(self.token_buffer)
            self.token_buffer.clear()


    def add(self, new_question: str, new_answer: str) -> None:
        """
        Adds a new question/answer exchange to the first buffer, 
        having caution to not overfill both
        """
        self.conv_buffer.add(question=new_question, answer=new_answer)

        if not self.conv_buffer._exceeds_limit():
            self.conv_buffer.update_json()
            return

        switching_conv = self.conv_buffer.pop()

        self.token_buffer.add(switching_conv["question"], switching_conv["answer"])

        if self.token_buffer._exceeds_limit():
            self._add_to_long_term_memory(self.token_buffer)
            self.token_buffer.clear()


        self.conv_buffer.update_json()
        self.token_buffer.update_json()


    def get_history(self) -> list[dict[str, str]]:
        """
        Returns the buffers as a list of role/content dicts
        """
        messages = []

        all_exchanges = self.conv_buffer.get_history()
        all_exchanges.extend(self.token_buffer.get_history())

        for exchange in all_exchanges:
            messages.append({"role": "user", "content": exchange["question"]})
            messages.append({"role": "assistant", "content": exchange["answer"]})

        return messages


    def _add_to_long_term_memory(self, buffer: Buffer) -> None:
        """
        Sends the exchanges to long-term memory (mem0) and clears them
        """
        exchanges = buffer.get_history()

        messages = []
        for exchange in exchanges:
            messages.append({"role": "user", "content": exchange["question"]})
            messages.append({"role": "assistant", "content": exchange["answer"]})

        self.long_term_memory.add(messages=messages, user_id=USER_ID)

    def get_long_term_memory(self, message: str = "", limit: int = 5):
        """
        Retrieves long-term memories from mem0.
        """
        if message:
            result = self.long_term_memory.search(
                query=message, filters={"user_id": USER_ID}, top_k=limit
            )
        else:
            result = self.long_term_memory.get_all(filters={"user_id": USER_ID})

        # mem0 pode devolver uma lista diretamente ou um dict {"results": [...]}
        # dependendo da versão/config; normalizamos aqui
        if isinstance(result, dict):
            return result.get("results", [])
        return result

memory = Memory()