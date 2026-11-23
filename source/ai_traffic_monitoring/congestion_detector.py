
from config import TRAFFIC_THRESHOLDS


class CongestionDetector:

    def __init__(self):
        self.status = "LOW"

    def detect(self, vehicle_count):

        if vehicle_count >= TRAFFIC_THRESHOLDS["SEVERE"]:
            self.status = "SEVERE"

        elif vehicle_count >= TRAFFIC_THRESHOLDS["HIGH"]:
            self.status = "HIGH"

        elif vehicle_count >= TRAFFIC_THRESHOLDS["MEDIUM"]:
            self.status = "MEDIUM"

        else:
            self.status = "LOW"

        return {
            "status": self.status,
            "vehicle_count": vehicle_count,
            "description": self.get_description()
        }

    def get_description(self):

        descriptions = {
            "LOW": "Traffic is moving freely.",
            "MEDIUM": "Moderate traffic detected.",
            "HIGH": "Heavy traffic detected.",
            "SEVERE": "Severe congestion detected."
        }

        return descriptions[self.status]
