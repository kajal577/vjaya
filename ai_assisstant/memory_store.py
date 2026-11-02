
import json
import os
from config import MEMORY_FILE

def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

def remember(key, value):
    data = _load()
    data[key.strip()] = value.strip()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return f"I'll remember that {key} is {value}."

def recall(key=None):
    data = _load()
    if key:
        matches = {
            k: v for k, v in data.items()
            if key.lower() in k.lower()
        }
        if not matches:
            return "I don't have that saved in my memory."
        return "; ".join(f"{k}: {v}" for k, v in matches.items())

    if not data:
        return "My personal memory is empty."
    return "; ".join(f"{k}: {v}" for k, v in data.items())

def forget(key):
    data = _load()
    matches = [k for k in data if key.lower() in k.lower()]
    for k in matches:
        del data[k]
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return "Memory deleted." if matches else "I couldn't find that memory."
