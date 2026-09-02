import os
from dotenv import load_dotenv

load_dotenv()

class GroqRouter:
    def __init__(self):
        self.keys = [
            os.getenv("GROQ_API_KEY_1"),
            os.getenv("GROQ_API_KEY_2"),
            os.getenv("GROQ_API_KEY_3"),
            os.getenv("GROQ_API_KEY_4"),
        ]
        self.current_key_index = 0

    def get_next_key(self):
        """Rotate to the next available key if the current one fails."""
        for i in range(4):
            key = self.keys[(self.current_key_index + i) % 4]
            if key:
                self.current_key_index = (self.current_key_index + i) % 4
                return key
        return None