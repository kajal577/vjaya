
import cv2

from config import (
    SERIAL_PORT,
    BAUD_RATE,
    CAMERA_INDEX,
    ENABLE_MOTORS,
)
from serial_link import RobotSerial
from vision import FaceVision


def main():
    camera = None
    robot = None

    try:
        vision = FaceVision()

        camera = cv2.VideoCapture(CAMERA_INDEX)

        if not camera.isOpened():
            raise RuntimeError("Could not open webcam")

        if ENABLE_MOTORS:
            robot = RobotSerial(SERIAL_PORT, BAUD_RATE)

        print("AI Vision Robot started.")
        print("Press Q to stop and exit.")

        while True:
            ok, frame = camera.read()

            if not ok:
                if robot:
                    robot.send("STOP")
                print("Camera frame failed.")
                break

            frame, command = vision.process(frame)

            if robot:
                robot.send(command)

            cv2.imshow("AI Vision Robot", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Stopping robot...")

    except Exception as error:
        print("ERROR:", error)

    finally:
        if robot:
            try:
                robot.send("STOP")
            finally:
                robot.close()

        if camera:
            camera.release()

        cv2.destroyAllWindows()
        print("Program ended.")


if __name__ == "__main__":
    main()
