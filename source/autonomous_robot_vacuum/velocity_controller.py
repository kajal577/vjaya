
"""
AUTONOMOUS ROBOT VACUUM
File: velocity_controller.py

Navigation velocity safety gate.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool


class VelocityController(Node):

    def __init__(self):

        super().__init__('velocity_controller')

        # ==================================
        # PARAMETERS
        # ==================================

        self.declare_parameter('command_timeout', 0.5)

        self.command_timeout = float(
            self.get_parameter('command_timeout').value
        )

        # ==================================
        # STATE
        # ==================================

        self.emergency_active = True

        self.last_command = None
        self.last_command_time = None

        # ==================================
        # SUBSCRIBERS
        # ==================================

        self.create_subscription(
            Twist,
            '/cmd_vel_nav',
            self.navigation_callback,
            10
        )

        self.create_subscription(
            Bool,
            '/safety/emergency',
            self.emergency_callback,
            10
        )

        # ==================================
        # PUBLISHER
        # ==================================

        self.motor_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # ==================================
        # WATCHDOG TIMER
        # ==================================

        self.timer = self.create_timer(
            0.05,
            self.watchdog
        )

        self.get_logger().info(
            'Velocity Safety Gate Started'
        )

    # ======================================
    # NAVIGATION COMMAND
    # ======================================

    def navigation_callback(self, msg):

        self.last_command = msg
        self.last_command_time = self.get_clock().now()

        if self.emergency_active:

            self.publish_stop()
            return

        self.motor_publisher.publish(msg)

    # ======================================
    # EMERGENCY STATUS
    # ======================================

    def emergency_callback(self, msg):

        previous_state = self.emergency_active

        self.emergency_active = msg.data

        if self.emergency_active:

            self.publish_stop()

            if not previous_state:

                self.get_logger().warning(
                    'EMERGENCY ACTIVE - MOTORS STOPPED'
                )

        elif previous_state:

            self.get_logger().info(
                'Emergency cleared. Waiting for new navigation command.'
            )

    # ======================================
    # PUBLISH STOP
    # ======================================

    def publish_stop(self):

        stop_command = Twist()

        self.motor_publisher.publish(
            stop_command
        )

    # ======================================
    # COMMAND WATCHDOG
    # ======================================

    def watchdog(self):

        if self.emergency_active:

            self.publish_stop()
            return

        if self.last_command_time is None:

            self.publish_stop()
            return

        elapsed = (
            self.get_clock().now()
            - self.last_command_time
        ).nanoseconds / 1e9

        if elapsed > self.command_timeout:

            self.publish_stop()

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().warning(
            'Stopping Velocity Controller'
        )

        self.publish_stop()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    node = VelocityController()

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
