
# ==========================================
# HAND TRACKER
# MediaPipe Hand Landmark Detection
# ==========================================

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def extract_landmarks(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None, results

        hand = results.multi_hand_landmarks[0]

        points = np.array(
            [
                [point.x, point.y, point.z]
                for point in hand.landmark
            ],
            dtype=np.float32
        )

        # Make coordinates relative to the wrist
        points = points - points[0]

        # Normalize hand size
        scale = np.max(
            np.linalg.norm(points[:, :2], axis=1)
        )

        if scale > 0:
            points = points / scale

        # 21 landmarks x 3 coordinates = 63 features
        features = points.flatten()

        return features, results

    def draw_landmarks(self, frame, results):

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

    def close(self):

        self.hands.close()
