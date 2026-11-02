
import json
import threading
from pathlib import Path

import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATHS = {
    "English": BASE_DIR / "models" / "vosk-model-small-en-us-0.15",
    "Hindi": BASE_DIR / "models" / "vosk-model-small-hi-0.22",
}

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

speech_lock = threading.Lock()
models = {}


def load_models():
    for language, path in MODEL_PATHS.items():
        if not path.is_dir():
            print(
                f"WARNING: {language} model not found: {path}",
                flush=True
            )
            continue

        if language not in models:
            print(f"Loading {language} speech model...", flush=True)
            models[language] = Model(str(path))

    if not models:
        raise FileNotFoundError(
            "No Vosk speech models found in the models folder."
        )


def speak(text):
    text = str(text).strip()

    if not text:
        return

    # Print each spoken message only once.
    print(f"MUSKAN: {text}", flush=True)

    is_hindi = any(
        "\u0900" <= character <= "\u097F"
        for character in text
    )

    try:
        with speech_lock:
            if is_hindi:
                for voice in engine.getProperty("voices"):
                    details = (
                        str(voice.name) + " " +
                        str(voice.id) + " " +
                        str(voice.languages)
                    ).lower()

                    if "hindi" in details or "hi-in" in details:
                        engine.setProperty("voice", voice.id)
                        break

            engine.say(text)
            engine.runAndWait()

    except Exception as error:
        print("TTS ERROR:", error, flush=True)


def recognize_audio(audio, model):
    pcm = audio.get_raw_data(
        convert_rate=16000,
        convert_width=2
    )

    kaldi = KaldiRecognizer(model, 16000)
    kaldi.SetWords(True)
    kaldi.AcceptWaveform(pcm)

    result = json.loads(kaldi.FinalResult())
    text = result.get("text", "").strip()
    words = result.get("result", [])

    confidence = (
        sum(word.get("conf", 0.0) for word in words) / len(words)
        if words else 0.0
    )

    return text, confidence


def listen():
    try:
        with sr.Microphone(sample_rate=16000) as source:
            print(
                "Calibrating microphone... Please stay quiet.",
                flush=True
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            print(
                "Listening now. Please ask your question.",
                flush=True
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=12
            )

        candidates = []

        for language, model in models.items():
            text, confidence = recognize_audio(audio, model)

            if text:
                candidates.append((confidence, language, text))

        if not candidates:
            print("No clear speech recognized.", flush=True)
            return ""

        confidence, language, text = max(
            candidates,
            key=lambda item: item[0]
        )

        print(f"Recognized ({language}): {text}", flush=True)
        return text

    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.", flush=True)
        return ""

    except Exception as error:
        print("SPEECH ERROR:", error, flush=True)
        return ""
