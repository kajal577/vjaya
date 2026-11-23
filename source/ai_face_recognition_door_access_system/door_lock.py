from gpiozero import OutputDevice

from config import (
    LOCK_RELAY_PIN,
    LOCK_RELAY_ACTIVE_LOW
)


class DoorLock:

    def __init__(self):

        self.relay = OutputDevice(
            LOCK_RELAY_PIN,
            active_high=not LOCK_RELAY_ACTIVE_LOW,
            initial_value=False
        )

        self.is_unlocked = False

        print("[LOCK] Door lock initialized.")

    def unlock(self):

        self.relay.on()
        self.is_unlocked = True

        print("[LOCK] DOOR UNLOCKED")

    def lock(self):

        self.relay.off()
        self.is_unlocked = False

        print("[LOCK] DOOR LOCKED")

    def cleanup(self):

        self.lock()
        self.relay.close()

        print("[LOCK] Hardware released.")