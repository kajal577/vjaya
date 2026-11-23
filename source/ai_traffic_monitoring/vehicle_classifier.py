
from config import VEHICLE_CLASSES


class VehicleClassifier:

    def classify(self, class_id):

        class_id = int(class_id)

        return VEHICLE_CLASSES.get(
            class_id,
            "unknown"
        )

    def classify_all(self, detections):

        for detection in detections:
            detection["vehicle_type"] = self.classify(
                detection["class_id"]
            )

        return detections

    def get_vehicle_types(self):
        return list(VEHICLE_CLASSES.values())
