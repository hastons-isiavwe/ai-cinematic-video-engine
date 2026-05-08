import requests


class StoryEngine:

    def expand_prompt(self, prompt):

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )

            result = response.json()
            return result["response"].strip()

        except Exception as e:
            print("⚠️ Ollama failed, using fallback:", e)

            return """
He almost gave up… until something changed.

Nothing was working, and the pressure kept building.

But one decision turned everything around.

Your breakthrough might be closer than you think.
""".strip()