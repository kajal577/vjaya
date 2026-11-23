import cv2
import numpy as np

from config import FACE_MATCH_THRESHOLD


class FaceRecognizer:

    def __init__(self):
        if not hasattr(cv2, "face"):
            raise RuntimeError(
                "OpenCV face module missing. "
                "Install opencv-contrib-python or the "
                "compatible Raspberry Pi contrib package."
            )

        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.trained = False

    def train(self, face_images, labels):

        if len(face_images) == 0:
            raise ValueError("No registered face images found.")

        self.model.train(
            face_images,
            np.array(labels, dtype=np.int32)
        )

        self.trained = True

    def save_model(self, path):
        if not self.trained:
            raise RuntimeError("Model has not been trained.")

        self.model.write(str(path))

    def load_model(self, path):
        self.model.read(str(path))
        self.trained = True

    def recognize(self, face_image):

        if not self.trained:
            return None, None

        label, confidence = self.model.predict(face_image)

        # LBPH confidence is a distance:
        # lower values indicate a closer match.
        if confidence <= FACE_MATCH_THRESHOLD * 100:
            return int(label), float(confidence)

        return None, float(confidence)