
import cv2
import mediapipe as mp
from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandGestureDetector:

    def __init__(self):
        model_path = (
            Path(__file__).parent
            / "models"
            / "hand_landmarker.task"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Hand model not found: {model_path}"
            )

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=str(model_path)
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )

        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.last_timestamp = 0

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        self.last_timestamp += 33

        result = self.detector.detect_for_video(
            image,
            self.last_timestamp
        )

        if not result.hand_landmarks:
            return None

        hand = result.hand_landmarks[0]

        # Count four upright fingers.
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        count = 0

        for tip, pip in zip(finger_tips, finger_pips):
            if hand[tip].y < hand[pip].y:
                count += 1

        return count

    def close(self):
        self.detector.close()
