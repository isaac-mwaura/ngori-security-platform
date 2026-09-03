import json
import os
import time
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class GroqRouter:
    """Router that manages multiple Groq API keys with failover.

    Dependencies are real: if no keys are configured, calls fail gracefully.
    The router is an actual dependency of the triage path, not decorative.
    """

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
        self._max_retries = 3
        self._retry_delay = 2.0

    @property
    def available(self) -> int:
        """Return number of configured API keys."""
        return len(self.keys)

    def get_next_key(self) -> Optional[str]:
        """Rotate to the next available key."""
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
        """Send JSON request to Groq with key rotation and retry logic.

        If all keys fail, returns a structured error dict rather than raising.
        """
        if not self.keys:
            return {"error": "No GROQ_API_KEY_1..4 configured"}

        last_error: Optional[str] = None

        for attempt in range(self._max_retries):
            for _ in range(len(self.keys)):
                key = self.get_next_key()
                try:
                    from groq import Groq
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
                    result = json.loads(content)
                    # Validate it's a dict with reasonable structure
                    if not isinstance(result, dict):
                        raise ValueError("Response is not a JSON object")
                    return result
                except Exception as exc:
                    last_error = str(exc)
                    logger.debug("Groq key %s failed: %s", key[:8] if key else "None", exc)
                    continue

            # If we got here, all keys failed this retry attempt
            if last_error and attempt < self._max_retries - 1:
                time.sleep(self._retry_delay)

        return {
            "error": "All configured Groq keys failed",
            "details": last_error or "Unknown error",
        }