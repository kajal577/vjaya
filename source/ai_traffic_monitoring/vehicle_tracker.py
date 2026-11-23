
import math
from config import TRACK_MAX_DISTANCE, TRACK_MAX_DISAPPEARED


class VehicleTracker:

    def __init__(self):

        self.next_id = 1
        self.tracks = {}

    def centroid(self, bbox):

        x1, y1, x2, y2 = bbox

        return (
            (x1 + x2) // 2,
            (y1 + y2) // 2
        )

    def update(self, detections):

        current = []

        for detection in detections:

            detection["centroid"] = self.centroid(
                detection["bbox"]
            )

            current.append(detection)

        used_ids = set()

        for detection in current:

            cx, cy = detection["centroid"]

            best_id = None
            best_distance = TRACK_MAX_DISTANCE

            for track_id, track in self.tracks.items():

                if track_id in used_ids:
                    continue

                tx, ty = track["centroid"]

                distance = math.hypot(
                    cx - tx,
                    cy - ty
                )

                if distance < best_distance:
                    best_distance = distance
                    best_id = track_id

            if best_id is None:

                best_id = self.next_id
                self.next_id += 1

                self.tracks[best_id] = {
                    "centroid": (cx, cy),
                    "disappeared": 0,
                    "vehicle_type": detection.get(
                        "vehicle_type", "unknown"
                    )
                }

            else:

                self.tracks[best_id]["centroid"] = (
                    cx, cy
                )

                self.tracks[best_id]["disappeared"] = 0

            used_ids.add(best_id)

            detection["track_id"] = best_id

        for track_id in list(self.tracks):

            if track_id not in used_ids:

                self.tracks[track_id]["disappeared"] += 1

                if (
                    self.tracks[track_id]["disappeared"]
                    > TRACK_MAX_DISAPPEARED
                ):
                    del self.tracks[track_id]

        return current
