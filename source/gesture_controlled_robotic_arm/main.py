
"""
GESTURE CONTROLLED ROBOTIC ARM
File: main.py

Main application.
Connects camera, hand tracking, gesture control,
and servo controller.
"""

import cv2
import time

from camera import Camera
from hand_tracking import HandTracker
from gesture_control import GestureController
from servo_control import ServoController

from config import EMERGENCY_STOP_KEY


def main():

    camera = Camera()
    hand_tracker = HandTracker()
    gesture_controller = GestureController()
    servo_controller = ServoController()

    camera_started = False
    tracker_started = False
    servo_started = False

    print("--------------------------------")
    print("GESTURE CONTROLLED ROBOTIC ARM")
    print("--------------------------------")
    print("Press Q or ESC to stop.")
    print("Show your hand to control the arm.")

    try:

        # Initialize servo controller
        servo_controller.initialize()
        servo_started = True

        # Start camera
        camera.start()
        camera_started = True

        tracker_started = True

        print("System ready.")

        while True:

            # Capture camera frame
            frame = camera.read()

            if frame is None:
                print("Camera frame unavailable.")
                time.sleep(0.1)
                continue

            # Detect hand
            frame, hand_data = hand_tracker.detect(frame)

            if hand_data is not None:

                # Convert hand movement to servo targets
                targets = gesture_controller.process(
                    hand_data
                )

                if targets is not None:

                    # Move arm gradually
                    servo_controller.move_smoothly(
                        targets
                    )

                    # Display target angles
                    y_position = 60

                    for name, angle in targets.items():

                        text = f"{name}: {angle}"

                        cv2.putText(
                            frame,
                            text,
                            (10, y_position),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.55,
                            (255, 255, 0),
                            2,
                        )

                        y_position += 25

            else:

                # No hand detected:
                # keep the arm at its current position
                cv2.putText(
                    frame,
                    "Arm Holding Position",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

            # Display camera window
            cv2.imshow(
                "Gesture Robotic Arm",
                frame
            )

            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF

            if key == ord(EMERGENCY_STOP_KEY):
                print("Stopping robotic arm.")
                break

            if key == 27:
                print("ESC pressed. Stopping.")
                break

    except KeyboardInterrupt:

        print("Program interrupted.")

    except Exception as error:

        print(f"Error: {error}")

    finally:

        # Stop camera
        if camera_started:
            camera.stop()

        # Release hand tracking
        if tracker_started:
            hand_tracker.close()

        # Release servo driver
        if servo_started:
            servo_controller.cleanup()

        cv2.destroyAllWindows()

        print("Gesture robotic arm stopped.")


if __name__ == "__main__":
    main()
