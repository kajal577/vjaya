from config import DISPLAY_ENABLED


class StatusDisplay:

    def __init__(self):

        self.enabled = DISPLAY_ENABLED

        print("[DISPLAY] Status display initialized.")

        if not self.enabled:
            print("[DISPLAY] Console display mode enabled.")

    def show_message(self, title, message):

        print("\n" + "=" * 35)
        print(title.center(35))
        print("-" * 35)
        print(message)
        print("=" * 35 + "\n")

    def access_granted(self, name):

        self.show_message(
            "ACCESS GRANTED",
            f"Welcome, {name}"
        )

    def access_denied(self):

        self.show_message(
            "ACCESS DENIED",
            "Unknown person"
        )

    def show_locked(self):

        self.show_message(
            "DOOR STATUS",
            "Door is LOCKED"
        )

    def show_unlocked(self):

        self.show_message(
            "DOOR STATUS",
            "Door is UNLOCKED"
        )

    def cleanup(self):
        pass