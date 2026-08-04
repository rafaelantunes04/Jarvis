import json
import os

from src.config import SLIDING_WINDOW_PATH

"""
Class to register the sliding window in json
"""

class JsonSlidingWindowStore:
    def __init__(self, json_name: str):
        self.path = SLIDING_WINDOW_PATH + json_name + ".json"

    def read(self) -> list[dict[str, str]]:
        """
        Reads the content in the json and returns an object
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            return []


    def write(self, trocas: list[dict[str, str]]) -> None:
        """
        Updates the json file
        """
        tmp_path = self.path + ".tmp"

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(trocas, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, self.path)