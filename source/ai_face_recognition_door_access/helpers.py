import cv2
import re


def normalize_face(gray_image, face_coordinates):

    x, y, width, height = face_coordinates

    face = gray_image[
        y:y + height,
        x:x + width
    ]

    if face.size == 0:
        return None

    face = cv2.equalizeHist(face)

    face = cv2.resize(
        face,
        (200, 200)
    )

    return face


def validate_user_name(name):

    name = name.strip()

    if len(name) < 2:
        return False

    return bool(
        re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,49}", name)
    )


def validate_user_id(user_id):

    return user_id.isdigit() and len(user_id) <= 9


def draw_face_box(
    frame,
    coordinates,
    label,
    color=(0, 255, 0)
):

    x, y, width, height = coordinates

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        color,
        2
    )

    cv2.putText(
        frame,
        label,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )

    return frame