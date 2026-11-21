"""PCA9685 16-channel PWM servo driver using Adafruit CircuitPython libraries."""
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import config

class ServoDriver:
    def __init__(self):
        self.i2c = board.I2C()
        self.pca = PCA9685(self.i2c, address=config.PCA9685_ADDRESS)
        self.pca.frequency = config.SERVO_PWM_HZ
        self.servos = [servo.Servo(self.pca.channels[i],
                                  min_pulse=config.SERVO_MIN_PULSE_US,
                                  max_pulse=config.SERVO_MAX_PULSE_US)
                       for i in range(16)]

    def set_angle(self, channel, angle):
        if not 0 <= channel <= 15:
            raise ValueError('PCA9685 channel must be 0..15')
        angle = max(config.SERVO_MIN_DEG, min(config.SERVO_MAX_DEG, float(angle)))
        center = config.SERVO_CENTER_DEG[channel]
        offset = angle - 90.0
        actual = center - offset if config.SERVO_REVERSE[channel] else center + offset
        actual = max(config.SERVO_MIN_DEG, min(config.SERVO_MAX_DEG, actual))
        self.servos[channel].angle = actual

    def set_neutral(self):
        for channel in range(12):
            self.set_angle(channel, config.SERVO_CENTER_DEG[channel])

    def disable_all(self):
        for channel in range(16):
            self.pca.channels[channel].duty_cycle = 0

    def close(self):
        self.disable_all()
        self.pca.deinit()
        self.i2c.deinit()
