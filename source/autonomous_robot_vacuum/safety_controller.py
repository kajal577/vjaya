
"""
AUTONOMOUS ROBOT VACUUM
File: safety_controller.py

Emergency stop and obstacle safety controller.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import Bool


class SafetyController(Node):

    def __init__(self):

        super().__init__('safety_controller')

        # ==================================
        # PARAMETERS
        # ==================================

        self.declare_parameter('stop_distance', 0.25)
        self.declare_parameter('sensor_timeout', 1.0)

        self.stop_distance = float(
            self.get_parameter('stop_distance').value
        )

        self.sensor_timeout = float(
            self.get_parameter('sensor_timeout').value
        )

        # ==================================
        # SENSOR STATUS
        # ==================================

        self.front_bumper_pressed = False
        self.rear_bumper_pressed = False

        self.front_distance = None
        self.rear_distance = None

        self.front_sensor_time = None
        self.rear_sensor_time = None

        self.front_sensor_received = False
        self.rear_sensor_received = False

        # ==================================
        # SUBSCRIBERS
        # ==================================

        self.create_subscription(
            Bool,
            '/bumper/front',
            self.front_bumper_callback,
            10
        )

        self.create_subscription(
            Bool,
            '/bumper/rear',
            self.rear_bumper_callback,
            10
        )

        self.create_subscription(
            Range,
            '/ultrasonic/front',
            self.front_range_callback,
            10
        )

        self.create_subscription(
            Range,
            '/ultrasonic/rear',
            self.rear_range_callback,
            10
        )

        # ==================================
        # PUBLISHER
        # ==================================

        self.velocity_publisher = self.create_publisher(
            Twist,
            '/safety/cmd_vel',
            10
        )

        self.emergency_publisher = self.create_publisher(
            Bool,
            '/safety/emergency',
            10
        )

        # ==================================
        # TIMER
        # ==================================

        self.timer = self.create_timer(
            0.05,
            self.check_safety
        )

        self.get_logger().info(
            'Safety Controller Started'
        )

    # ======================================
    # BUMPER CALLBACKS
    # ======================================

    def front_bumper_callback(self, msg):

        self.front_bumper_pressed = msg.data

    def rear_bumper_callback(self, msg):

        self.rear_bumper_pressed = msg.data

    # ======================================
    # ULTRASONIC CALLBACKS
    # ======================================

    def front_range_callback(self, msg):

        self.front_sensor_received = True
        self.front_sensor_time = self.get_clock().now()

        if math.isfinite(msg.range):

            self.front_distance = msg.range

        else:

            self.front_distance = None

    def rear_range_callback(self, msg):

        self.rear_sensor_received = True
        self.rear_sensor_time = self.get_clock().now()

        if math.isfinite(msg.range):

            self.rear_distance = msg.range

        else:

            self.rear_distance = None

    # ======================================
    # SENSOR TIMEOUT CHECK
    # ======================================

    def sensor_is_stale(self, received, timestamp):

        if not received or timestamp is None:

            return True

        elapsed = (
            self.get_clock().now() - timestamp
        ).nanoseconds / 1e9

        return elapsed > self.sensor_timeout

    # ======================================
    # OBSTACLE CHECK
    # ======================================

    def obstacle_detected(self, distance):

        if distance is None:
            return True

        return distance <= self.stop_distance

    # ======================================
    # SAFETY CHECK
    # ======================================

    def check_safety(self):

        front_stale = self.sensor_is_stale(
            self.front_sensor_received,
            self.front_sensor_time
        )

        rear_stale = self.sensor_is_stale(
            self.rear_sensor_received,
            self.rear_sensor_time
        )

        emergency = False

        # Bumper collision

        if self.front_bumper_pressed:
            emergency = True

        if self.rear_bumper_pressed:
            emergency = True

        # Sensor timeout or invalid reading

        if front_stale or rear_stale:
            emergency = True

        # Obstacle distance

        if self.obstacle_detected(self.front_distance):
            emergency = True

        if self.obstacle_detected(self.rear_distance):
            emergency = True

        # ==================================
        # PUBLISH SAFETY STATUS
        # ==================================

        emergency_msg = Bool()
        emergency_msg.data = emergency

        self.emergency_publisher.publish(
            emergency_msg
        )

        # ==================================
        # STOP ROBOT
        # ==================================

        if emergency:

            stop_command = Twist()

            self.velocity_publisher.publish(
                stop_command
            )

        else:

            # No movement command is generated here.
            # The navigation velocity must pass through
            # the safety command multiplexer.

            pass

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().info(
            'Stopping Safety Controller'
        )

        stop_command = Twist()

        self.velocity_publisher.publish(
            stop_command
        )

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    node = SafetyController()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        node.destroy_node()

        if rclpy.ok():

            rclpy.shutdown()


if __name__ == '__main__':

    main()
