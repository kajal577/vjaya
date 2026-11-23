
"""
GESTURE CONTROLLED ROBOTIC ARM
File: gesture_control.py

Converts hand tracking data into servo commands.
"""

from config import (
    DOF,
    SERVO_LIMITS,
    SERVO_HOME,
)


def clamp(value, minimum, maximum):
    """Keep a value inside the specified range."""

    return max(minimum, min(value, maximum))


def map_value(value, in_min, in_max, out_min, out_max):
    """Convert a value from one range to another."""

    if in_max == in_min:
        return out_min

    result = (
        (value - in_min)
        * (out_max - out_min)
        / (in_max - in_min)
    ) + out_min

    return result


class GestureController:

    def __init__(self):

        self.current_angles = SERVO_HOME.copy()

        print("Gesture controller initialized.")

    def count_fingers(self, landmarks):
        """
        Count extended fingers.

        Assumes the camera image is mirrored.
        """

        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        count = 0

        # Count four fingers
        for tip, pip in zip(finger_tips, finger_pips):

            if landmarks[tip]["y"] < landmarks[pip]["y"]:
                count += 1

        # Count thumb using horizontal position
        thumb_tip = landmarks[4]["x"]
        thumb_ip = landmarks[3]["x"]

        if thumb_tip < thumb_ip:
            count += 1

        return count

    def process(self, hand_data):
        """
        Convert hand coordinates into servo target angles.

        Returns:
            Dictionary containing servo target angles.
        """

        if hand_data is None:
            return None

        landmarks = hand_data["landmarks"]

        # --------------------------
        # BASE
        # --------------------------

        wrist_x = hand_data["wrist_x"]

        base_angle = map_value(
            wrist_x,
            0.15,
            0.85,
            0,
            180
        )

        base_angle = clamp(
            base_angle,
            *SERVO_LIMITS["base"]
        )

        # --------------------------
        # SHOULDER
        # --------------------------

        wrist_y = hand_data["wrist_y"]

        shoulder_angle = map_value(
            wrist_y,
            0.15,
            0.85,
            160,
            20
        )

        shoulder_angle = clamp(
            shoulder_angle,
            *SERVO_LIMITS["shoulder"]
        )

        # --------------------------
        # ELBOW
        # --------------------------

        wrist = landmarks[0]
        middle_tip = landmarks[12]

        dx = middle_tip["x"] - wrist["x"]
        dy = middle_tip["y"] - wrist["y"]

        hand_distance = (dx * dx + dy * dy) ** 0.5

        elbow_angle = map_value(
            hand_distance,
            0.15,
            0.55,
            30,
            150
        )

        elbow_angle = clamp(
            elbow_angle,
            *SERVO_LIMITS["elbow"]
        )

        # --------------------------
        # WRIST
        # --------------------------

        wrist_angle = map_value(
            hand_data["middle_tip_x"],
            0.15,
            0.85,
            0,
            180
        )

        wrist_angle = clamp(
            wrist_angle,
            *SERVO_LIMITS["wrist"]
        )

        # --------------------------
        # GRIPPER
        # --------------------------

        finger_count = self.count_fingers(landmarks)

        if finger_count >= 3:
            gripper_angle = SERVO_LIMITS["gripper"][1]

        else:
            gripper_angle = SERVO_LIMITS["gripper"][0]

        # --------------------------
        # SERVO TARGETS
        # --------------------------

        targets = {
            "base": int(base_angle),
            "shoulder": int(shoulder_angle),
            "elbow": int(elbow_angle),
            "wrist": int(wrist_angle),
        }

        if DOF >= 5:
            targets["gripper"] = int(gripper_angle)

        return targets

    def get_home_position(self):
        """Return the configured home position."""

        return SERVO_HOME.copy()
