
"""
GESTURE CONTROLLED ROBOTIC ARM
File: servo_control.py

PCA9685 servo motor controller.
"""

import time

import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

from config import (
    PCA9685_ADDRESS,
    SERVO_FREQUENCY,
    SERVO_CHANNELS,
    SERVO_LIMITS,
    SERVO_HOME,
    MAX_SERVO_STEP,
)


class ServoController:

    def __init__(self):

        self.i2c = None
        self.pca = None
        self.servos = {}

        self.current_angles = SERVO_HOME.copy()

        self.initialized = False

    def initialize(self):
        """Initialize I2C and PCA9685 servo driver."""

        try:
            self.i2c = busio.I2C(
                board.SCL,
                board.SDA
            )

            self.pca = PCA9685(
                self.i2c,
                address=PCA9685_ADDRESS
            )

            self.pca.frequency = SERVO_FREQUENCY

            # Create servo objects
            for name, channel in SERVO_CHANNELS.items():

                self.servos[name] = servo.Servo(
                    self.pca.channels[channel]
                )

            self.initialized = True

            print("PCA9685 initialized.")
            print("Servo controller ready.")

        except Exception as error:

            self.cleanup()

            raise RuntimeError(
                f"Servo initialization failed: {error}"
            )

    def set_angle(self, name, angle):
        """Set one servo to a target angle."""

        if not self.initialized:
            raise RuntimeError(
                "Servo controller is not initialized."
            )

        if name not in self.servos:
            return

        minimum, maximum = SERVO_LIMITS[name]

        angle = max(
            minimum,
            min(float(angle), maximum)
        )

        self.servos[name].angle = angle

        self.current_angles[name] = angle

    def move_smoothly(self, targets):
        """Move servos gradually toward target angles."""

        if not self.initialized:
            return

        for name, target in targets.items():

            if name not in self.servos:
                continue

            minimum, maximum = SERVO_LIMITS[name]

            target = max(
                minimum,
                min(float(target), maximum)
            )

            current = self.current_angles[name]

            difference = target - current

            while abs(difference) > 0:

                step = min(
                    abs(difference),
                    MAX_SERVO_STEP
                )

                if difference < 0:
                    step = -step

                current += step

                self.set_angle(
                    name,
                    current
                )

                difference = target - current

                time.sleep(0.02)

    def move_home(self):
        """Move the arm to its configured home position."""

        self.move_smoothly(
            SERVO_HOME
        )

    def get_positions(self):
        """Return current servo angles."""

        return self.current_angles.copy()

    def cleanup(self):
        """Release PCA9685 resources."""

        if self.pca is not None:

            self.pca.deinit()
            self.pca = None

        self.initialized = False

        print("Servo controller stopped.")
