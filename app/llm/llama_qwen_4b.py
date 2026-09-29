import requests


class LlamaEngine:
    """Client for the local llama.cpp server."""

    SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

    def __init__(self, timeout=120):
        self.timeout = timeout

    def is_available(self):
        """Check whether llama-server is running."""
        try:
            response = requests.get(
                "http://127.0.0.1:8080/health",
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def clean_text(self, text: str) -> str:
        """
        Clean and prepare text for natural text-to-speech.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        prompt = f"""
Clean this text for natural text-to-speech.

Rules:
- Fix grammar and punctuation.
- Correct obvious spelling and typing mistakes.
- Make the wording natural to speak aloud.
- Preserve the original meaning.
- Do not add information.
- Do not explain your changes.
- Return only the final text.

Text:
{text}
"""

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 200
        }

        response = requests.post(
            self.SERVER_URL,
            json=payload,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()