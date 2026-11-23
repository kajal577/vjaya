
"""
AUTONOMOUS ROBOT VACUUM
File: encoder.py

Wheel encoder monitoring and odometry.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import math
import time
import threading

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion

try:
    from gpiozero import RotaryEncoder
except ImportError:
    RotaryEncoder = None


class EncoderController(Node):

    def __init__(self):
        super().__init__('encoder_controller')

        # Robot parameters
        self.declare_parameter('wheel_radius', 0.035)
        self.declare_parameter('wheel_separation', 0.22)

        self.declare_parameter('ticks_per_revolution', 360)

        self.declare_parameter('left_pin_a', -1)
        self.declare_parameter('left_pin_b', -1)

        self.declare_parameter('right_pin_a', -1)
        self.declare_parameter('right_pin_b', -1)

        self.declare_parameter('publish_rate', 20.0)

        self.wheel_radius = float(
            self.get_parameter('wheel_radius').value
        )

        self.wheel_separation = float(
            self.get_parameter('wheel_separation').value
        )

        self.ticks_per_revolution = int(
            self.get_parameter('ticks_per_revolution').value
        )

        self.publish_rate = float(
            self.get_parameter('publish_rate').value
        )

        self.left_encoder = None
        self.right_encoder = None

        self.hardware_ready = False

        self.left_last_position = 0
        self.right_last_position = 0

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_time = time.monotonic()

        self.lock = threading.Lock()

        self.odom_publisher = self.create_publisher(
            Odometry,
            '/wheel/odometry',
            10
        )

        self.setup_encoders()

        self.timer = self.create_timer(
            1.0 / self.publish_rate,
            self.update_odometry
        )

        self.get_logger().info(
            'Encoder Controller Started'
        )

    # ======================================
    # INITIALIZE ENCODERS
    # ======================================

    def setup_encoders(self):

        pins = [
            int(self.get_parameter('left_pin_a').value),
            int(self.get_parameter('left_pin_b').value),
            int(self.get_parameter('right_pin_a').value),
            int(self.get_parameter('right_pin_b').value)
        ]

        if any(pin < 0 for pin in pins):
            self.get_logger().warning(
                'Encoder GPIO pins not configured.'
            )
            return

        if len(set(pins)) != 4:
            self.get_logger().error(
                'Encoder GPIO pins must be different.'
            )
            return

        if RotaryEncoder is None:
            self.get_logger().error(
                'gpiozero RotaryEncoder is unavailable.'
            )
            return

        try:
            self.left_encoder = RotaryEncoder(
                a=pins[0],
                b=pins[1],
                max_steps=0
            )

            self.right_encoder = RotaryEncoder(
                a=pins[2],
                b=pins[3],
                max_steps=0
            )

            self.left_last_position = (
                self.left_encoder.steps
            )

            self.right_last_position = (
                self.right_encoder.steps
            )

            self.hardware_ready = True

            self.get_logger().info(
                'Wheel encoders initialized.'
            )

        except Exception as error:

            self.get_logger().error(
                f'Encoder initialization failed: {error}'
            )

    # ======================================
    # ANGLE TO QUATERNION
    # ======================================

    @staticmethod
    def create_quaternion(yaw):

        q = Quaternion()

        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)

        return q

    # ======================================
    # UPDATE ODOMETRY
    # ======================================

    def update_odometry(self):

        current_time = time.monotonic()

        dt = current_time - self.last_time

        if dt <= 0:
            return

        self.last_time = current_time

        if not self.hardware_ready:
            return

        with self.lock:

            left_position = self.left_encoder.steps
            right_position = self.right_encoder.steps

            left_ticks = (
                left_position - self.left_last_position
            )

            right_ticks = (
                right_position - self.right_last_position
            )

            self.left_last_position = left_position
            self.right_last_position = right_position

        # Convert encoder ticks into wheel distance

        distance_per_tick = (
            2.0 * math.pi * self.wheel_radius
            / self.ticks_per_revolution
        )

        left_distance = left_ticks * distance_per_tick
        right_distance = right_ticks * distance_per_tick

        # Differential drive odometry

        distance = (
            left_distance + right_distance
        ) / 2.0

        rotation = (
            right_distance - left_distance
        ) / self.wheel_separation

        self.theta += rotation

        self.theta = math.atan2(
            math.sin(self.theta),
            math.cos(self.theta)
        )

        self.x += distance * math.cos(self.theta)
        self.y += distance * math.sin(self.theta)

        linear_velocity = distance / dt
        angular_velocity = rotation / dt

        self.publish_odometry(
            linear_velocity,
            angular_velocity
        )

    # ======================================
    # PUBLISH ROS 2 ODOMETRY
    # ======================================

    def publish_odometry(
        self,
        linear_velocity,
        angular_velocity
    ):

        msg = Odometry()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.0

        msg.pose.pose.orientation = (
            self.create_quaternion(self.theta)
        )

        msg.twist.twist.linear.x = linear_velocity
        msg.twist.twist.angular.z = angular_velocity

        self.odom_publisher.publish(msg)

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.hardware_ready = False

        if self.left_encoder is not None:
            self.left_encoder.close()

        if self.right_encoder is not None:
            self.right_encoder.close()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    encoder_node = EncoderController()

    try:
        rclpy.spin(encoder_node)

    except KeyboardInterrupt:
        pass

    finally:
        encoder_node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
