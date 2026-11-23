
"""
AUTONOMOUS ROBOT VACUUM
File: bumper.py

Front and rear bumper collision detection.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, String

try:
    from gpiozero import Button
except ImportError:
    Button = None


class BumperController(Node):

    def __init__(self):

        super().__init__('bumper_controller')

        # ==================================
        # GPIO CONFIGURATION
        # ==================================

        self.declare_parameter('front_bumper_pin', -1)
        self.declare_parameter('rear_bumper_pin', -1)

        self.declare_parameter('pull_up', True)
        self.declare_parameter('debounce_time', 0.05)

        self.front_bumper = None
        self.rear_bumper = None

        self.front_pressed = False
        self.rear_pressed = False

        # ==================================
        # ROS 2 PUBLISHERS
        # ==================================

        self.front_publisher = self.create_publisher(
            Bool,
            '/bumper/front',
            10
        )

        self.rear_publisher = self.create_publisher(
            Bool,
            '/bumper/rear',
            10
        )

        self.emergency_publisher = self.create_publisher(
            Bool,
            '/bumper/emergency',
            10
        )

        self.event_publisher = self.create_publisher(
            String,
            '/bumper/event',
            10
        )

        # ==================================
        # INITIALIZE GPIO
        # ==================================

        self.setup_bumpers()

        # ==================================
        # PUBLISH TIMER
        # ==================================

        self.timer = self.create_timer(
            0.05,
            self.publish_status
        )

        self.get_logger().info(
            'Bumper Controller Started'
        )

    # ======================================
    # INITIALIZE BUMPERS
    # ======================================

    def setup_bumpers(self):

        front_pin = int(
            self.get_parameter('front_bumper_pin').value
        )

        rear_pin = int(
            self.get_parameter('rear_bumper_pin').value
        )

        if front_pin < 0 and rear_pin < 0:

            self.get_logger().warning(
                'Bumper GPIO pins not configured.'
            )
            return

        if Button is None:

            self.get_logger().error(
                'gpiozero Button is unavailable.'
            )
            return

        if (
            front_pin >= 0
            and rear_pin >= 0
            and front_pin == rear_pin
        ):

            self.get_logger().error(
                'Front and rear bumper pins must be different.'
            )
            return

        pull_up = bool(
            self.get_parameter('pull_up').value
        )

        debounce_time = float(
            self.get_parameter('debounce_time').value
        )

        try:

            if front_pin >= 0:

                self.front_bumper = Button(
                    front_pin,
                    pull_up=pull_up,
                    bounce_time=debounce_time
                )

                self.front_bumper.when_pressed = (
                    self.on_front_pressed
                )

                self.front_bumper.when_released = (
                    self.on_front_released
                )

            if rear_pin >= 0:

                self.rear_bumper = Button(
                    rear_pin,
                    pull_up=pull_up,
                    bounce_time=debounce_time
                )

                self.rear_bumper.when_pressed = (
                    self.on_rear_pressed
                )

                self.rear_bumper.when_released = (
                    self.on_rear_released
                )

            self.get_logger().info(
                'Bumper switches initialized.'
            )

        except Exception as error:

            self.get_logger().error(
                f'Bumper initialization failed: {error}'
            )

            self.close_bumpers()

    # ======================================
    # FRONT BUMPER CALLBACKS
    # ======================================

    def on_front_pressed(self):

        self.front_pressed = True

        self.get_logger().warning(
            'FRONT COLLISION DETECTED!'
        )

        self.publish_event(
            'FRONT_COLLISION'
        )

    def on_front_released(self):

        self.front_pressed = False

        self.get_logger().info(
            'Front bumper released.'
        )

    # ======================================
    # REAR BUMPER CALLBACKS
    # ======================================

    def on_rear_pressed(self):

        self.rear_pressed = True

        self.get_logger().warning(
            'REAR COLLISION DETECTED!'
        )

        self.publish_event(
            'REAR_COLLISION'
        )

    def on_rear_released(self):

        self.rear_pressed = False

        self.get_logger().info(
            'Rear bumper released.'
        )

    # ======================================
    # PUBLISH COLLISION EVENT
    # ======================================

    def publish_event(self, event_name):

        msg = String()

        msg.data = event_name

        self.event_publisher.publish(msg)

    # ======================================
    # PUBLISH BUMPER STATUS
    # ======================================

    def publish_status(self):

        front_msg = Bool()
        front_msg.data = self.front_pressed

        rear_msg = Bool()
        rear_msg.data = self.rear_pressed

        emergency_msg = Bool()
        emergency_msg.data = (
            self.front_pressed or self.rear_pressed
        )

        self.front_publisher.publish(front_msg)
        self.rear_publisher.publish(rear_msg)

        self.emergency_publisher.publish(
            emergency_msg
        )

    # ======================================
    # CLOSE GPIO
    # ======================================

    def close_bumpers(self):

        if self.front_bumper is not None:

            self.front_bumper.close()
            self.front_bumper = None

        if self.rear_bumper is not None:

            self.rear_bumper.close()
            self.rear_bumper = None

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().info(
            'Stopping Bumper Controller'
        )

        self.close_bumpers()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    node = BumperController()

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
