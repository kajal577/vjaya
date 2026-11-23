from gpiozero import Buzzer

from config import (
    BUZZER_PIN,
    BUZZER_ENABLED,
    ACCESS_GRANTED_BEEP,
    ACCESS_DENIED_BEEP
)


class AccessBuzzer:

    def __init__(self):

        self.enabled = BUZZER_ENABLED

        self.buzzer = None

        if self.enabled:
            self.buzzer = Buzzer(BUZZER_PIN)

        print("[BUZZER] Initialized.")

    def access_granted(self):

        if self.enabled:
            self.buzzer.on()
            self.buzzer.off()

            print("[BUZZER] Access granted.")

    def access_denied(self):

        if self.enabled:
            self.buzzer.on()

            import time
            time.sleep(ACCESS_DENIED_BEEP)

            self.buzzer.off()

            print("[BUZZER] Access denied.")

    def cleanup(self):

        if self.buzzer:
            self.buzzer.off()
            self.buzzer.close()