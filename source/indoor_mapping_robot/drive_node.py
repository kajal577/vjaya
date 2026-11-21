#!/usr/bin/env python3
"""ROS 2 /cmd_vel differential drive motor node for L298N + gpiozero."""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from . import config

class DriveNode(Node):
    def __init__(self):
        super().__init__('drive_node')
        self.left_a = DigitalOutputDevice(config.LEFT_IN1)
        self.left_b = DigitalOutputDevice(config.LEFT_IN2)
        self.right_a = DigitalOutputDevice(config.RIGHT_IN1)
        self.right_b = DigitalOutputDevice(config.RIGHT_IN2)
        self.left_pwm = PWMOutputDevice(config.LEFT_EN, frequency=config.PWM_FREQUENCY_HZ)
        self.right_pwm = PWMOutputDevice(config.RIGHT_EN, frequency=config.PWM_FREQUENCY_HZ)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.on_cmd, 10)
        self.timer = self.create_timer(0.25, self.watchdog)
        self.last_cmd = self.get_clock().now()
        self.stop()
        self.get_logger().info('Drive node ready; waiting for /cmd_vel')

    @staticmethod
    def clamp(value, low, high):
        return max(low, min(high, value))

    def set_motor(self, a, b, pwm, speed):
        speed = self.clamp(speed, -1.0, 1.0)
        if speed > 0:
            a.on(); b.off()
        elif speed < 0:
            a.off(); b.on()
        else:
            a.off(); b.off()
        pwm.value = abs(speed)

    def on_cmd(self, msg):
        v = self.clamp(msg.linear.x, -config.MAX_LINEAR_MPS, config.MAX_LINEAR_MPS)
        w = self.clamp(msg.angular.z, -config.MAX_ANGULAR_RPS, config.MAX_ANGULAR_RPS)
        left = v - (w * config.WHEEL_BASE_M / 2.0)
        right = v + (w * config.WHEEL_BASE_M / 2.0)
        peak = max(abs(left), abs(right), config.MAX_LINEAR_MPS)
        left /= peak; right /= peak
        self.set_motor(self.left_a, self.left_b, self.left_pwm, left)
        self.set_motor(self.right_a, self.right_b, self.right_pwm, right)
        self.last_cmd = self.get_clock().now()

    def stop(self):
        self.set_motor(self.left_a, self.left_b, self.left_pwm, 0.0)
        self.set_motor(self.right_a, self.right_b, self.right_pwm, 0.0)

    def watchdog(self):
        if (self.get_clock().now() - self.last_cmd).nanoseconds > 700_000_000:
            self.stop()

    def destroy_node(self):
        self.stop()
        for device in (self.left_a, self.left_b, self.right_a, self.right_b,
                      self.left_pwm, self.right_pwm):
            device.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args); node = DriveNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
