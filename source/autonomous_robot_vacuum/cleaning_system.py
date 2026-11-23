
"""
AUTONOMOUS ROBOT VACUUM
File: cleaning_system.py

Vacuum suction and cleaning brush controller.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

try:
    from gpiozero import OutputDevice
except ImportError:
    OutputDevice = None


class CleaningSystem(Node):

    def __init__(self):
        super().__init__('cleaning_system')

        # GPIO configuration
        self.declare_parameter('vacuum_gpio', -1)
        self.declare_parameter('brush_gpio', -1)

        # Active-high by default.
        # Set according to your relay or driver hardware.
        self.declare_parameter('active_high', True)

        self.vacuum_gpio = int(
            self.get_parameter('vacuum_gpio').value
        )

        self.brush_gpio = int(
            self.get_parameter('brush_gpio').value
        )

        self.active_high = bool(
            self.get_parameter('active_high').value
        )

        self.vacuum = None
        self.brush = None

        self.vacuum_enabled = False
        self.brush_enabled = False

        self.setup_hardware()

        self.vacuum_subscription = self.create_subscription(
            Bool,
            '/cleaning/vacuum',
            self.vacuum_callback,
            10
        )

        self.brush_subscription = self.create_subscription(
            Bool,
            '/cleaning/brush',
            self.brush_callback,
            10
        )

        self.get_logger().info(
            'Cleaning System Started'
        )

    # ======================================
    # INITIALIZE HARDWARE
    # ======================================

    def setup_hardware(self):

        if OutputDevice is None:
            self.get_logger().warning(
                'gpiozero is unavailable. '
                'Cleaning hardware disabled.'
            )
            return

        if self.vacuum_gpio < 0 or self.brush_gpio < 0:
            self.get_logger().warning(
                'Cleaning GPIO pins not configured. '
                'Vacuum and brush remain disabled.'
            )
            return

        if self.vacuum_gpio == self.brush_gpio:
            self.get_logger().error(
                'Vacuum and brush GPIO pins must be different.'
            )
            return

        try:
            self.vacuum = OutputDevice(
                self.vacuum_gpio,
                active_high=self.active_high,
                initial_value=False
            )

            self.brush = OutputDevice(
                self.brush_gpio,
                active_high=self.active_high,
                initial_value=False
            )

            self.get_logger().info(
                'Cleaning hardware initialized.'
            )

        except Exception as error:

            self.get_logger().error(
                f'Cleaning hardware initialization failed: {error}'
            )

            self.stop_cleaning()

    # ======================================
    # VACUUM CONTROL
    # ======================================

    def vacuum_callback(self, msg):

        if self.vacuum is None:
            return

        try:
            if msg.data:
                self.vacuum.on()
                self.vacuum_enabled = True

                self.get_logger().info(
                    'Vacuum suction ON'
                )

            else:
                self.vacuum.off()
                self.vacuum_enabled = False

                self.get_logger().info(
                    'Vacuum suction OFF'
                )

        except Exception as error:

            self.get_logger().error(
                f'Vacuum control error: {error}'
            )

            self.stop_cleaning()

    # ======================================
    # BRUSH CONTROL
    # ======================================

    def brush_callback(self, msg):

        if self.brush is None:
            return

        try:
            if msg.data:
                self.brush.on()
                self.brush_enabled = True

                self.get_logger().info(
                    'Cleaning brush ON'
                )

            else:
                self.brush.off()
                self.brush_enabled = False

                self.get_logger().info(
                    'Cleaning brush OFF'
                )

        except Exception as error:

            self.get_logger().error(
                f'Brush control error: {error}'
            )

            self.stop_cleaning()

    # ======================================
    # STOP ALL CLEANING SYSTEMS
    # ======================================

    def stop_cleaning(self):

        try:
            if self.vacuum is not None:
                self.vacuum.off()

            if self.brush is not None:
                self.brush.off()

        except Exception as error:

            self.get_logger().error(
                f'Cleaning shutdown error: {error}'
            )

        self.vacuum_enabled = False
        self.brush_enabled = False

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.stop_cleaning()

        if self.vacuum is not None:
            self.vacuum.close()

        if self.brush is not None:
            self.brush.close()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    cleaning_node = CleaningSystem()

    try:
        rclpy.spin(cleaning_node)

    except KeyboardInterrupt:
        pass

    finally:
        cleaning_node.stop_cleaning()
        cleaning_node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
