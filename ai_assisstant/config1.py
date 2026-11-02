
import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = "MUSKAN"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MQTT_HOST = os.getenv("MQTT_HOST", "")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# Never run arbitrary AI-generated terminal commands.
ALLOW_PC_CONTROL = True
MEMORY_FILE = "memory.json"
