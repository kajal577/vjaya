"""HC-SR04 obstacle distance. ECHO pin requires 3.3 V level conversion."""
from gpiozero import DistanceSensor
import config

class ObstacleDetector:
    def __init__(self):
        self.sensor = DistanceSensor(echo=config.ULTRASONIC_ECHO_BCM,
                                    trigger=config.ULTRASONIC_TRIGGER_BCM,
                                    max_distance=3.0, queue_len=3)
    def distance_cm(self):
        try: return self.sensor.distance * 100.0
        except Exception: return None
    def blocked(self):
        distance = self.distance_cm()
        return distance is not None and distance < config.OBSTACLE_STOP_CM
    def close(self): self.sensor.close()
