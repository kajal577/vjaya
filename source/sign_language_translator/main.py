
# ==========================================
# SIGN LANGUAGE TRANSLATOR
# MAIN APPLICATION
# ==========================================

import os
import time
import cv2

from joblib import load

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    MODEL_PATH,
    MIN_CONFIDENCE,
    SPEECH_COOLDOWN_SECONDS,
    STABLE_FRAMES
)

from hand_tracker import HandTracker
from speech import Speech


def main():

    if not os.path.exists(MODEL_PATH):

        print("AI model not found.")
        print("Run collect_data.py and train_model.py first.")
        return

    model = load(MODEL_PATH)

    tracker = HandTracker()
    speech = Speech()

    camera = cv2.VideoCapture(
        CAMERA_INDEX
    )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    last_spoken = ""
    last_speech_time = 0

    current_label = ""
    stable_count = 0

    try:

        while camera.isOpened():

            success, frame = camera.read()

            if not success:
                print("Camera frame unavailable.")
                break

            frame = cv2.flip(
                frame,
                1
            )

            features, results = (
                tracker.extract_landmarks(frame)
            )

            tracker.draw_landmarks(
                frame,
                results
            )

            label = "Show a hand"
            confidence = 0.0

            if features is not None:

                probabilities = (
                    model.predict_proba(
                        [features]
                    )[0]
                )

                index = probabilities.argmax()

                predicted_label = (
                    model.classes_[index]
                )

                confidence = float(
                    probabilities[index]
                )

                if confidence >= MIN_CONFIDENCE:

                    label = str(
                        predicted_label
                    )

                else:

                    label = "Uncertain"

                # Check if sign remains stable
                if label == current_label:

                    stable_count += 1

                else:

                    current_label = label
                    stable_count = 1

                now = time.time()

                if (
                    label not in (
                        "Uncertain",
                        "Show a hand"
                    )
                    and stable_count >= STABLE_FRAMES
                    and (
                        label != last_spoken
                        or now - last_speech_time
                        >= SPEECH_COOLDOWN_SECONDS
                    )
                ):

                    speech.speak(
                        label.replace("_", " ").lower()
                    )

                    last_spoken = label
                    last_speech_time = now

            else:

                current_label = ""
                stable_count = 0

            # Display recognized sign
            cv2.putText(
                frame,
                f"Sign: {label}",
                (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Confidence: {confidence:.0%}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Q = Quit | S = Speak again",
                (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "VJaYa Sign Language Translator",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if (
                key == ord("s")
                and label not in (
                    "Uncertain",
                    "Show a hand"
                )
            ):

                speech.speak(
                    label.replace("_", " ").lower()
                )

    finally:

        camera.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
