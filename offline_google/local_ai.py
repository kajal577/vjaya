
import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def ask_local_ai(question):
    question = str(question).strip()

    if not question:
        return "Please ask me a question."

    payload = {
        "model": MODEL_NAME,
        "system": (
            "You are MUSKAN, a helpful offline personal AI assistant. "
            "Answer accurately, naturally, and concisely. "
            "Reply in the same language as the user's question, "
            "including English or Hindi. "
            "Explain educational topics simply. "
            "Never pretend to know breaking news or live information "
            "without a current source. "
            "If you are unsure, say so. "
            "Make answers suitable for speaking aloud."
        ),
        "prompt": question,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 300
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = result.get("response", "").strip()

        if not answer:
            return "Sorry, I could not generate an answer."

        return answer

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Cannot reach Ollama. Check that Ollama is running "
            "and qwen2.5:3b is installed."
        ) from error
