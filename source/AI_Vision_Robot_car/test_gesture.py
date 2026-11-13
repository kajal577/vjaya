
import cv2
from vision import HandGestureDetector

camera = cv2.VideoCapture(0)
detector = HandGestureDetector()

if not camera.isOpened():
    print("Camera not detected!")
    detector.close()
    exit()

print("Hand gesture recognition started!")
print("Show your hand in front of the camera.")
print("Press Q to quit.")

try:
    while True:
        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        fingers = detector.detect(frame)

        if fingers is None:
            message = "NO HAND DETECTED"
        else:
            message = f"FINGERS DETECTED: {fingers}"

        cv2.putText(
            frame,
            message,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("AI VISION ROBOT - HAND DETECTION", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera.release()
    detector.close()
    cv2.destroyAllWindows()
