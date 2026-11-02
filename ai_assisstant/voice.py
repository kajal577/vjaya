
import speech_recognition as sr
import pyttsx3

_recognizer = sr.Recognizer()
_recognizer.pause_threshold = 0.8
_engine = pyttsx3.init()
_engine.setProperty("rate", 175)
_engine.setProperty("volume", 1.0)

def speak(text):
    print(f"MUSKAN: {text}")
    _engine.say(text)
    _engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            _recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = _recognizer.listen(
                source, timeout=6, phrase_time_limit=12
            )
        print("Recognizing speech...")
        return _recognizer.recognize_google(audio).strip()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as exc:
        print("Speech recognition network error:", exc)
        return ""
    except (OSError, AttributeError) as exc:
        print("Microphone error:", exc)
        return ""
