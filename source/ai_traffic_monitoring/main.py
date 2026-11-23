
import cv2
import time
import logging
import threading

from config import DISPLAY_WINDOW

from camera import TrafficCamera
from vehicle_detector import VehicleDetector
from vehicle_classifier import VehicleClassifier
from vehicle_tracker import VehicleTracker
from vehicle_counter import VehicleCounter
from traffic_analyzer import TrafficAnalyzer
from congestion_detector import CongestionDetector
from database import TrafficDatabase
from dashboard import TrafficDashboard


# ================================================
# LOGGING
# ================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("AI_TRAFFIC")


# ================================================
# MAIN APPLICATION
# ================================================

class TrafficMonitoringSystem:

    def __init__(self):

        self.camera = None
        self.detector = None
        self.classifier = VehicleClassifier()
        self.tracker = VehicleTracker()
        self.counter = VehicleCounter()
        self.analyzer = TrafficAnalyzer()
        self.congestion = CongestionDetector()
        self.database = None
        self.dashboard = TrafficDashboard()

        self.running = False
        self.last_database_save = 0

    # ============================================
    # INITIALIZE SYSTEM
    # ============================================

    def initialize(self):

        logger.info("Starting AI Traffic Monitoring System")

        self.camera = TrafficCamera()

        if not self.camera.start():
            raise RuntimeError("Camera initialization failed")

        self.detector = VehicleDetector()

        self.database = TrafficDatabase()

        dashboard_thread = threading.Thread(
            target=self.dashboard.start,
            daemon=True
        )

        dashboard_thread.start()

        self.running = True

        logger.info("All modules initialized")

    # ============================================
    # DRAW DETECTIONS
    # ============================================

    def draw_detections(self, frame, detections):

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            vehicle_type = detection["vehicle_type"]

            track_id = detection.get("track_id", 0)

            confidence = detection["confidence"]

            label = (
                f"{vehicle_type.upper()} "
                f"ID:{track_id} "
                f"{confidence:.2f}"
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (98, 230, 197),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (98, 230, 197),
                2
            )

        return frame

    # ============================================
    # PROCESS FRAME
    # ============================================

    def process_frame(self, frame):

        # Run Hailo inference
        detections = self.detector.infer(frame)

        # Identify vehicle types
        detections = self.classifier.classify_all(
            detections
        )

        # Track detected vehicles
        detections = self.tracker.update(
            detections
        )

        # Count vehicles crossing the line
        count_statistics = self.counter.update(
            detections,
            frame.shape[0]
        )

        # Analyze currently visible traffic
        statistics = self.analyzer.analyze(
            detections
        )

        # Estimate congestion from current detections
        congestion = self.congestion.detect(
            statistics["vehicles_present"]
        )

        # Add cumulative counts
        statistics["counted_total"] = (
            count_statistics["total"]
        )

        statistics["counted_by_type"] = (
            count_statistics["by_type"]
        )

        statistics["congestion"] = congestion["status"]

        statistics["description"] = (
            congestion["description"]
        )

        # Draw counting line
        frame = self.counter.draw_line(frame)

        # Draw vehicle boxes and tracking IDs
        frame = self.draw_detections(
            frame, detections
        )

        # Display information
        cv2.putText(
            frame,
            f"Visible vehicles: {statistics['vehicles_present']}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Congestion: {congestion['status']}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        # Update dashboard
        self.dashboard.update(
            frame,
            statistics
        )

        # Save statistics every five seconds
        now = time.time()

        if now - self.last_database_save >= 5:

            self.database.save_statistics(
                statistics,
                congestion["status"]
            )

            self.last_database_save = now

        return frame

    # ============================================
    # RUN SYSTEM
    # ============================================

    def run(self):

        self.initialize()

        logger.info("Traffic monitoring is running")

        try:

            while self.running:

                frame = self.camera.get_frame()

                if frame is None:
                    time.sleep(0.05)
                    continue

                result = self.process_frame(frame)

                if DISPLAY_WINDOW:

                    cv2.imshow(
                        "AI Traffic Monitoring System",
                        result
                    )

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

        except KeyboardInterrupt:

            logger.info("Keyboard interruption received")

        except Exception:

            logger.exception("Application error")

        finally:

            self.shutdown()

    # ============================================
    # SHUTDOWN
    # ============================================

    def shutdown(self):

        logger.info("Shutting down system")

        self.running = False

        if self.camera:
            self.camera.release()

        if self.detector:
            self.detector.release()

        if self.database:
            self.database.close()

        cv2.destroyAllWindows()

        logger.info("System stopped")


# ================================================
# APPLICATION ENTRY POINT
# ================================================

if __name__ == "__main__":

    system = TrafficMonitoringSystem()

    system.run()
