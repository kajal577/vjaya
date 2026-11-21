"""Pose-level control for a 12-servo quadruped (3 servos per leg)."""
import time
import config

LEG_NAMES = ('front_left', 'front_right', 'rear_left', 'rear_right')

class LegController:
    def __init__(self, driver):
        self.driver = driver
        self.current = {name: [90.0, 90.0, 90.0] for name in LEG_NAMES}

    def set_leg(self, name, hip, shoulder, knee, smooth=False, duration=0.25):
        channels = config.SERVO_CHANNELS[name]
        target = [hip, shoulder, knee]
        if smooth:
            start = self.current[name][:]
            steps = max(1, int(duration / 0.02))
            for step in range(1, steps + 1):
                values = [start[i] + (target[i] - start[i]) * step / steps for i in range(3)]
                for ch, value in zip(channels, values): self.driver.set_angle(ch, value)
                time.sleep(duration / steps)
        else:
            for ch, value in zip(channels, target): self.driver.set_angle(ch, value)
        self.current[name] = target

    def pose(self, hip=90, shoulder=90, knee=90, smooth=True, duration=0.4):
        for name in LEG_NAMES:
            self.set_leg(name, hip, shoulder, knee, smooth=smooth, duration=duration)

    def stand(self):
        # This is a starter neutral pose; tune per frame and linkage.
        self.set_leg('front_left', 90, 78, 112, True, 0.5)
        self.set_leg('front_right', 90, 102, 68, True, 0.5)
        self.set_leg('rear_left', 90, 78, 112, True, 0.5)
        self.set_leg('rear_right', 90, 102, 68, True, 0.5)

    def sit(self):
        self.set_leg('front_left', 90, 70, 135, True, 0.5)
        self.set_leg('front_right', 90, 110, 45, True, 0.5)
        self.set_leg('rear_left',  90, 115, 135, True, 0.5)
        self.set_leg('rear_right', 90, 65, 45, True, 0.5)

    def stop_pose(self):
        self.pose(90, 90, 90, smooth=True, duration=0.3)
