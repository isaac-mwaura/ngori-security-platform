import json
import os
from typing import Any, Dict, List
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqRouter:
    def __init__(self):
        self.keys: List[str] = [
            key for key in (
                os.getenv("GROQ_API_KEY_1"),
                os.getenv("GROQ_API_KEY_2"),
                os.getenv("GROQ_API_KEY_3"),
                os.getenv("GROQ_API_KEY_4"),
            ) if key
        ]
        self.current_key_index = 0
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    def available(self) -> int:
        return len(self.keys)

    def get_next_key(self):
        if not self.keys:
            return None
        key = self.keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        return key

    def complete_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: int = 1200,
    ) -> Dict[str, Any]:
        if not self.keys:
            return {"error": "No GROQ_API_KEY_1..4 configured"}

        errors = []
        for _ in range(len(self.keys)):
            key = self.get_next_key()
            try:
                client = Groq(api_key=key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"},
                )
                content = response.choices[0].message.content
                if not content:
                    raise ValueError("Empty Groq response")
                return json.loads(content)
            except Exception as exc:
                errors.append(str(exc))

        return {
            "error": "All configured Groq keys failed",
            "details": errors,
        }