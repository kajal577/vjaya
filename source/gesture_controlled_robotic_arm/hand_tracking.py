
"""
GESTURE CONTROLLED ROBOTIC ARM
File: hand_tracking.py

Detects hand landmarks using MediaPipe.
"""

import cv2
import mediapipe as mp

from config import (
    HAND_DETECTION_CONFIDENCE,
    HAND_TRACKING_CONFIDENCE,
)


class HandTracker:
    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=HAND_TRACKING_CONFIDENCE,
        )

        print("Hand tracking initialized.")

    def detect(self, frame):
        """
        Detect hand landmarks.

        Returns:
            frame: Frame with landmarks drawn.
            hand_data: Dictionary containing hand coordinates.
                       None if no hand is detected.
        """

        if frame is None:
            return frame, None

        # Convert BGR image to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        rgb_frame.flags.writeable = False

        results = self.hands.process(rgb_frame)

        rgb_frame.flags.writeable = True

        hand_data = None

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            # Draw hand landmarks
            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )

            landmarks = []

            for landmark in hand_landmarks.landmark:

                landmarks.append({
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z,
                })

            # Wrist landmark: index 0
            wrist = landmarks[0]

            # Middle finger tip: index 12
            middle_finger_tip = landmarks[12]

            hand_data = {
                "landmarks": landmarks,
                "wrist_x": wrist["x"],
                "wrist_y": wrist["y"],
                "wrist_z": wrist["z"],
                "middle_tip_x": middle_finger_tip["x"],
                "middle_tip_y": middle_finger_tip["y"],
            }

            # Display tracking status
            cv2.putText(
                frame,
                "Hand Detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

        else:

            cv2.putText(
                frame,
                "Show Your Hand",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        return frame, hand_data

    def close(self):
        """Release MediaPipe resources."""

        self.hands.close()

        print("Hand tracker closed.")
