
"""
AUTONOMOUS ROBOT VACUUM
File: motor_control.py

Differential drive motor controller.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

try:
    from gpiozero import Motor
except ImportError:
    Motor = None


class MotorController(Node):

    def __init__(self):
        super().__init__('motor_controller')

        # Robot configuration
        self.declare_parameter('wheel_radius', 0.035)
        self.declare_parameter('wheel_separation', 0.22)

        self.declare_parameter('max_speed', 0.30)

        # BCM GPIO pin configuration
        # Set these according to your motor driver.
        self.declare_parameter('left_forward_pin', -1)
        self.declare_parameter('left_backward_pin', -1)

        self.declare_parameter('right_forward_pin', -1)
        self.declare_parameter('right_backward_pin', -1)

        self.wheel_radius = float(
            self.get_parameter('wheel_radius').value
        )

        self.wheel_separation = float(
            self.get_parameter('wheel_separation').value
        )

        self.max_speed = float(
            self.get_parameter('max_speed').value
        )

        self.left_motor = None
        self.right_motor = None

        self.hardware_ready = False

        self.setup_motors()

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.velocity_callback,
            10
        )

        self.get_logger().info(
            'Motor Controller Started'
        )

    # ======================================
    # MOTOR INITIALIZATION
    # ======================================

    def setup_motors(self):

        pins = [
            int(self.get_parameter('left_forward_pin').value),
            int(self.get_parameter('left_backward_pin').value),
            int(self.get_parameter('right_forward_pin').value),
            int(self.get_parameter('right_backward_pin').value)
        ]

        if any(pin < 0 for pin in pins):
            self.get_logger().warning(
                'Motor GPIO pins are not configured. '
                'Motors remain disabled.'
            )
            return

        if len(set(pins)) != 4:
            self.get_logger().error(
                'Motor GPIO pins must be different.'
            )
            return

        if Motor is None:
            self.get_logger().error(
                'gpiozero is not installed.'
            )
            return

        try:
            self.left_motor = Motor(
                forward=pins[0],
                backward=pins[1]
            )

            self.right_motor = Motor(
                forward=pins[2],
                backward=pins[3]
            )

            self.hardware_ready = True

            self.stop_motors()

            self.get_logger().info(
                'Motor hardware initialized.'
            )

        except Exception as error:

            self.get_logger().error(
                f'Motor initialization failed: {error}'
            )

            self.stop_motors()

    # ======================================
    # INDIVIDUAL MOTOR CONTROL
    # ======================================

    def set_left_motor(self, speed):

        if not self.hardware_ready:
            return

        speed = max(-1.0, min(1.0, speed))

        self.left_motor.value = speed

    def set_right_motor(self, speed):

        if not self.hardware_ready:
            return

        speed = max(-1.0, min(1.0, speed))

        self.right_motor.value = speed

    # ======================================
    # STOP MOTORS
    # ======================================

    def stop_motors(self):

        try:
            if self.left_motor is not None:
                self.left_motor.stop()

            if self.right_motor is not None:
                self.right_motor.stop()

        except Exception as error:
            self.get_logger().error(
                f'Motor stop error: {error}'
            )

    # ======================================
    # ROS 2 VELOCITY CALLBACK
    # ======================================

    def velocity_callback(self, msg):

        if not self.hardware_ready:
            self.stop_motors()
            return

        linear_velocity = msg.linear.x
        angular_velocity = msg.angular.z

        # Differential drive kinematics

        left_velocity = (
            linear_velocity -
            (angular_velocity * self.wheel_separation / 2.0)
        )

        right_velocity = (
            linear_velocity +
            (angular_velocity * self.wheel_separation / 2.0)
        )

        # Convert wheel velocity to motor speed

        left_speed = left_velocity / self.max_speed
        right_speed = right_velocity / self.max_speed

        # Normalize both speeds together
        # to preserve the turning ratio.

        maximum = max(
            abs(left_speed),
            abs(right_speed),
            1.0
        )

        left_speed /= maximum
        right_speed /= maximum

        self.set_left_motor(left_speed)
        self.set_right_motor(right_speed)

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.stop_motors()

        if self.left_motor is not None:
            self.left_motor.close()

        if self.right_motor is not None:
            self.right_motor.close()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    controller = MotorController()

    try:
        rclpy.spin(controller)

    except KeyboardInterrupt:
        pass

    finally:
        controller.stop_motors()
        controller.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
