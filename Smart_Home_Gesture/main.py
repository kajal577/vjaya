
import cv2

from config import CAMERA_INDEX, GESTURE_STABLE_FRAMES
from bluetooth_link import BluetoothLink
from vision import HandGestureDetector


# Finger count -> Arduino Bluetooth command
GESTURE_COMMANDS = {
    0: ("0", "ALL OFF"),
    1: ("1", "LIGHT ON"),
    2: ("2", "LIGHT OFF"),
    3: ("3", "FAN ON"),
    4: ("4", "FAN OFF"),
    5: ("5", "LIGHT + FAN ON"),
}


def main():
    bluetooth = BluetoothLink()
    detector = HandGestureDetector()
    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        detector.close()
        return

    try:
        bluetooth.connect()

        stable_gesture = None
        previous_gesture = None
        gesture_frames = 0

        print("SMART HOME GESTURE AUTOMATION STARTED")
        print("Show your hand to control appliances.")
        print("Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("Webcam frame not available.")
                break

            frame = cv2.flip(frame, 1)
            finger_count = detector.detect(frame)

            if finger_count is None:
                stable_gesture = None
                gesture_frames = 0
                display_text = "No hand detected"
            else:
                display_text = f"Fingers: {finger_count}"

                if finger_count == previous_gesture:
                    gesture_frames += 1
                else:
                    previous_gesture = finger_count
                    gesture_frames = 1

                if gesture_frames >= GESTURE_STABLE_FRAMES:
                    if stable_gesture != finger_count:
                        stable_gesture = finger_count

                        command, appliance_status = GESTURE_COMMANDS[
                            finger_count
                        ]

                        bluetooth.send_command(command)
                        print(
                            f"Gesture {finger_count}: "
                            f"{appliance_status} | Sent: {command}"
                        )

                    display_text = GESTURE_COMMANDS[
                        finger_count
                    ][1]

            cv2.putText(
                frame,
                display_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow("Smart Home Gesture Automation", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as error:
        print("Error:", error)

    finally:
        # Turn appliances OFF when the program closes
        try:
            bluetooth.send_command("0")
            bluetooth.close()
        except Exception:
            pass

        camera.release()
        detector.close()
        cv2.destroyAllWindows()
        print("Program closed. Appliances commanded OFF.")


if __name__ == "__main__":
    main()
