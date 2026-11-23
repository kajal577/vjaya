
# ==========================================
# SIGN LANGUAGE DATA COLLECTION
# ==========================================

import cv2
import csv
import os

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    DATA_DIR
)

from hand_tracker import HandTracker


CSV_PATH = os.path.join(
    DATA_DIR,
    "gestures.csv"
)


def main():

    os.makedirs(DATA_DIR, exist_ok=True)

    label = input(
        "Enter sign label (example HELLO): "
    ).strip().upper().replace(" ", "_")

    if not label:
        print("Label cannot be empty.")
        return

    camera = cv2.VideoCapture(CAMERA_INDEX)

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    tracker = HandTracker()

    file_exists = os.path.exists(CSV_PATH)

    try:

        with open(
            CSV_PATH,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow(
                    ["label"] +
                    [f"f{i}" for i in range(63)]
                )

            count = 0

            while camera.isOpened():

                success, frame = camera.read()

                if not success:
                    print("Camera error.")
                    break

                frame = cv2.flip(frame, 1)

                features, results = (
                    tracker.extract_landmarks(frame)
                )

                tracker.draw_landmarks(
                    frame,
                    results
                )

                cv2.putText(
                    frame,
                    f"Label: {label}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Samples: {count}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "SPACE = Save | Q = Finish",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                cv2.imshow(
                    "Sign Language Data Collection",
                    frame
                )

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                if key == 32 and features is not None:

                    writer.writerow(
                        [label] + features.tolist()
                    )

                    count += 1

                    print(
                        f"Saved sample {count}"
                    )

    finally:

        camera.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
