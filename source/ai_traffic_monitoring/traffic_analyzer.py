
from collections import Counter
import time


class TrafficAnalyzer:

    def __init__(self):

        self.history = []
        self.last_update = time.time()

    def analyze(self, detections):

        counts = Counter(
            item.get("vehicle_type", "unknown")
            for item in detections
        )

        total = sum(counts.values())

        result = {
            "timestamp": time.time(),
            "vehicles_present": total,
            "cars": counts.get("car", 0),
            "motorcycles": counts.get("motorcycle", 0),
            "buses": counts.get("bus", 0),
            "trucks": counts.get("truck", 0)
        }

        self.history.append(result)

        if len(self.history) > 1000:
            self.history.pop(0)

        return result

    def get_history(self):
        return self.history

    def get_average_traffic(self):

        if not self.history:
            return 0

        values = [
            item["vehicles_present"]
            for item in self.history
        ]

        return round(sum(values) / len(values), 2)
