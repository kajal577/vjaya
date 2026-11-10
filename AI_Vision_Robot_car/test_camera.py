
import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera not detected!")
    exit()

print("Camera connected successfully!")
print("Press Q to close the camera window.")

while True:
    success, frame = camera.read()

    if not success:
        print("Camera frame not received.")
        break

    cv2.imshow("AI VISION ROBOT - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
