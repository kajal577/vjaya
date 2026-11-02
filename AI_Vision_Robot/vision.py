
import cv2

from config import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MIN_FACE_WIDTH,
    MAX_FACE_WIDTH,
    CENTER_TOLERANCE,
)


class FaceVision:
    def __init__(self):
        model_path = (
            cv2.data.haarcascades
            + "haarcascade_frontalface_default.xml"
        )

        self.detector = cv2.CascadeClassifier(model_path)

        if self.detector.empty():
            raise RuntimeError("Could not load face detector")

    def process(self, frame):
        frame = cv2.resize(
            frame, (FRAME_WIDTH, FRAME_HEIGHT)
        )

        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50)
        )

        if len(faces) == 0:
            cv2.putText(
                frame, "NO FACE - STOP",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 0, 255), 2
            )
            return frame, "STOP"

        # Follow the largest detected face.
        x, y, w, h = max(
            faces, key=lambda face: face[2] * face[3]
        )

        center_x = x + w // 2
        image_center = FRAME_WIDTH // 2

        cv2.rectangle(
            frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2
        )
        cv2.line(
            frame,
            (image_center, 0),
            (image_center, FRAME_HEIGHT),
            (255, 0, 0), 1
        )

        # First align the robot with the face.
        if center_x < image_center - CENTER_TOLERANCE:
            command = "LEFT"
        elif center_x > image_center + CENTER_TOLERANCE:
            command = "RIGHT"

        # Then control approximate distance using face size.
        elif w < MIN_FACE_WIDTH:
            command = "FWD"
        elif w > MAX_FACE_WIDTH:
            command = "BACK"
        else:
            command = "STOP"

        cv2.putText(
            frame,
            f"FACE: {w}px | CMD: {command}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2
        )

        return frame, command
