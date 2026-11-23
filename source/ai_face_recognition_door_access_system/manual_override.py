from gpiozero import Button

from config import MANUAL_OVERRIDE_PIN


class ManualOverride:

    def __init__(self, door_lock, callback=None):

        self.door_lock = door_lock
        self.callback = callback

        self.button = Button(
            MANUAL_OVERRIDE_PIN,
            pull_up=True,
            bounce_time=0.1
        )

        self.button.when_pressed = self.handle_press

        print("[OVERRIDE] Manual button initialized.")

    def handle_press(self):

        print("[OVERRIDE] Manual unlock activated.")

        self.door_lock.unlock()

        if self.callback:
            self.callback()

    def cleanup(self):

        self.button.close()