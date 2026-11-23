
from collections import defaultdict

from config import COUNTING_LINE_POSITION


class VehicleCounter:

    def __init__(self):

        self.counted_ids = set()

        self.counts = defaultdict(int)

        self.total = 0

        self.previous_positions = {}

    def update(self, detections, frame_height):

        line_y = int(
            frame_height * COUNTING_LINE_POSITION
        )

        for detection in detections:

            track_id = detection.get("track_id")

            if track_id is None:
                continue

            _, cy = detection["centroid"]

            previous_y = self.previous_positions.get(
                track_id
            )

            self.previous_positions[track_id] = cy

            if track_id in self.counted_ids:
                continue

            if previous_y is None:
                continue

            crossed = (
                (previous_y < line_y <= cy)
                or
                (previous_y > line_y >= cy)
            )

            if crossed:

                vehicle_type = detection.get(
                    "vehicle_type", "unknown"
                )

                self.counted_ids.add(track_id)

                self.counts[vehicle_type] += 1
                self.total += 1

        return self.get_statistics()

    def get_statistics(self):

        return {
            "total": self.total,
            "by_type": dict(self.counts)
        }

    def draw_line(self, frame):

        import cv2

        line_y = int(
            frame.shape[0] * COUNTING_LINE_POSITION
        )

        cv2.line(
            frame,
            (0, line_y),
            (frame.shape[1], line_y),
            (0, 255, 0),
            2
        )

        return frame
