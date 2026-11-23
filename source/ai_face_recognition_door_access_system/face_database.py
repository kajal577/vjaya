import cv2
import json

from pathlib import Path


class FaceDatabase:

    def __init__(self, faces_dir):

        self.faces_dir = Path(faces_dir)
        self.faces_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.metadata_file = self.faces_dir / "users.json"

        if not self.metadata_file.exists():
            self.metadata_file.write_text(
                "{}",
                encoding="utf-8"
            )

    def get_users(self):

        try:
            return json.loads(
                self.metadata_file.read_text(
                    encoding="utf-8"
                )
            )
        except (json.JSONDecodeError, OSError):
            return {}

    def register_user(self, user_id, name, face_images):

        if not user_id.isdigit():
            raise ValueError("User ID must contain digits only.")

        if not name.strip():
            raise ValueError("User name cannot be empty.")

        if len(face_images) < 10:
            raise ValueError(
                "At least 10 face images are required."
            )

        users = self.get_users()

        if user_id in users:
            raise ValueError("User ID already exists.")

        user_folder = self.faces_dir / user_id
        user_folder.mkdir(exist_ok=True)

        saved_count = 0

        for index, image in enumerate(face_images):

            if image is None or image.size == 0:
                continue

            file_path = user_folder / f"{index}.jpg"

            if cv2.imwrite(str(file_path), image):
                saved_count += 1

        if saved_count < 10:
            raise RuntimeError(
                "Could not save enough face images."
            )

        users[user_id] = {
            "name": name.strip(),
            "enabled": True
        }

        self.metadata_file.write_text(
            json.dumps(users, indent=4),
            encoding="utf-8"
        )

        return saved_count

    def load_training_data(self):

        users = self.get_users()

        images = []
        labels = []

        for user_id, details in users.items():

            if not details.get("enabled", False):
                continue

            user_folder = self.faces_dir / user_id

            if not user_folder.exists():
                continue

            for image_path in user_folder.glob("*.jpg"):

                image = cv2.imread(
                    str(image_path),
                    cv2.IMREAD_GRAYSCALE
                )

                if image is not None:
                    image = cv2.resize(image, (200, 200))

                    images.append(image)
                    labels.append(int(user_id))

        return images, labels

    def get_user_name(self, user_id):

        users = self.get_users()

        user = users.get(str(user_id))

        if user and user.get("enabled", False):
            return user["name"]

        return None