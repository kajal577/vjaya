
import cv2
import time

from vision import HandGestureDetector
from robot_control import RobotControl


# Gesture-to-robot mapping
GESTURE_ACTIONS = {
    0: ("STOP", "stop"),
    1: ("FORWARD", "forward"),
    2: ("BACKWARD", "backward"),
    3: ("LEFT", "left"),
    4: ("RIGHT", "right")
}


def main():

    camera = None
    detector = None
    robot = RobotControl()

    try:
        print("AI VISION ROBOT STARTING...")

        # Connect Bluetooth
        robot.connect()
        print("Bluetooth connected!")

        # Start camera
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise RuntimeError("Camera not detected!")

        # Start hand detector
        detector = HandGestureDetector()

        print("Hand gesture control started!")
        print("Press Q to quit.")

        candidate = None
        stable_frames = 0
        active_command = "STOP"
        last_sent_time = 0

        while True:

            success, frame = camera.read()

            if not success:
                print("Camera frame error!")
                break

            frame = cv2.flip(frame, 1)

            fingers = detector.detect(frame)

            current_time = time.monotonic()

            if fingers is None:
                # No hand means immediate STOP
                candidate = None
                stable_frames = 0

                if active_command != "STOP":
                    robot.stop()
                    active_command = "STOP"
                    last_sent_time = current_time

                display_text = "NO HAND - STOP"

            else:
                if fingers == candidate:
                    stable_frames += 1
                else:
                    candidate = fingers
                    stable_frames = 1

                if stable_frames >= 4:

                    action = GESTURE_ACTIONS.get(fingers)

                    if action is not None:

                        display_text = action[0]
                        command = action[1]

                        # Send a new command or refresh movement
                        if (
                            command != active_command
                            or (
                                command != "stop"
                                and current_time - last_sent_time >= 0.35
                            )
                        ):
                            getattr(robot, command)()
                            active_command = command
                            last_sent_time = current_time

                    else:
                        display_text = "STOP"
                        robot.stop()
                        active_command = "STOP"

                else:
                    display_text = "GESTURE DETECTING..."

            cv2.putText(
                frame,
                "AI VISION ROBOT",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                display_text,
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.imshow("AI VISION ROBOT - CONTROL", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as error:
        print("ERROR:", error)

    finally:
        print("Stopping robot...")

        try:
            robot.stop()
        except Exception:
            pass

        if camera is not None:
            camera.release()

        if detector is not None:
            detector.close()

        robot.close()
        cv2.destroyAllWindows()

        print("Robot stopped. Program closed.")


if __name__ == "__main__":
    main()
