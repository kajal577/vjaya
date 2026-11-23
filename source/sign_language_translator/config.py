
# ==========================================
# SIGN LANGUAGE TRANSLATOR
# Raspberry Pi 5 Configuration
# ==========================================

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Project folders
DATA_DIR = "data"

# AI model files
MODEL_PATH = "models/gesture_model.joblib"
LABELS_PATH = "models/labels.json"

# AI recognition settings
MIN_CONFIDENCE = 0.65

# Training settings
SAMPLES_PER_CLASS = 200

# Speech settings
SPEECH_COOLDOWN_SECONDS = 1.5
