
import requests
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_URL, ASSISTANT_NAME

_history = []
MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}, a helpful personal desktop voice assistant.
Speak naturally and concisely because your answers are read aloud.
You may explain how to perform tasks, but you cannot directly execute
computer commands. Never claim a physical device changed state unless
the control module confirms it. The user is in control of the computer.
"""

def ask_ai(question):
    global _history

    if not GROQ_API_KEY or "PASTE_YOUR_" in GROQ_API_KEY:
        return "Please configure your Groq API key in the .env file."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *_history,
        {"role": "user", "content": question},
    ]

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "temperature": 0.6,
                "max_tokens": 500,
            },
            timeout=30,
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"].strip()

        _history.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ])
        _history = _history[-MAX_HISTORY_MESSAGES:]
        return answer or "I didn't receive a usable answer."
    except requests.RequestException as exc:
        print("AI connection error:", exc)
        return "I couldn't connect to my online AI service."
    except (KeyError, IndexError, ValueError):
        return "I received an unexpected response from the AI service."
