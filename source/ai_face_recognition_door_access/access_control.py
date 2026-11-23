import time

from config import (
    UNLOCK_DURATION,
    ACCESS_COOLDOWN
)


class AccessControl:

    def __init__(
        self,
        door_lock,
        buzzer,
        display,
        logger
    ):

        self.door_lock = door_lock
        self.buzzer = buzzer
        self.display = display
        self.logger = logger

        self.unlock_until = 0
        self.last_access_time = 0

    def grant_access(
        self,
        user_name,
        user_id,
        access_method="FACE"
    ):

        current_time = time.monotonic()

        if (
            access_method == "FACE"
            and current_time - self.last_access_time
            < ACCESS_COOLDOWN
        ):
            return False

        self.door_lock.unlock()

        self.unlock_until = (
            current_time + UNLOCK_DURATION
        )

        self.last_access_time = current_time

        self.display.access_granted(user_name)
        self.buzzer.access_granted()

        self.logger.log_access(
            user_name,
            user_id,
            "GRANTED",
            access_method
        )

        return True

    def deny_access(self):

        self.display.access_denied()
        self.buzzer.access_denied()

        self.logger.log_access(
            "UNKNOWN",
            None,
            "DENIED",
            "FACE"
        )

    def update(self):

        if (
            self.unlock_until
            and time.monotonic() >= self.unlock_until
        ):

            self.door_lock.lock()

            self.display.show_locked()

            self.unlock_until = 0

    def manual_unlock(self):

        self.unlock_until = (
            time.monotonic() + UNLOCK_DURATION
        )

        self.logger.log_access(
            "MANUAL OVERRIDE",
            None,
            "GRANTED",
            "MANUAL"
        )

        self.display.show_unlocked()