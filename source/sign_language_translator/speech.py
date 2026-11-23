
# ==========================================
# TEXT TO SPEECH
# ==========================================

import pyttsx3
import threading


class Speech:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            155
        )

        self.lock = threading.Lock()

    def speak(self, text):

        if not text:
            return

        def speech_worker():

            with self.lock:

                self.engine.say(
                    str(text).replace("_", " ")
                )

                self.engine.runAndWait()

        thread = threading.Thread(
            target=speech_worker,
            daemon=True
        )

        thread.start()
