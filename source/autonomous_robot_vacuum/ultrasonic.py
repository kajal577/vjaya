
"""
AUTONOMOUS ROBOT VACUUM
File: ultrasonic.py

Front and rear ultrasonic obstacle detection.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import time
import threading

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Range

try:
    from gpiozero import DistanceSensor
except ImportError:
    DistanceSensor = None


class UltrasonicController(Node):

    def __init__(self):

        super().__init__('ultrasonic_controller')

        # ==================================
        # CONFIGURATION
        # ==================================

        self.declare_parameter('front_trigger_pin', -1)
        self.declare_parameter('front_echo_pin', -1)

        self.declare_parameter('rear_trigger_pin', -1)
        self.declare_parameter('rear_echo_pin', -1)

        self.declare_parameter('min_range', 0.02)
        self.declare_parameter('max_range', 3.0)

        self.declare_parameter('stop_distance', 0.25)
        self.declare_parameter('update_rate', 5.0)

        self.front_sensor = None
        self.rear_sensor = None

        self.front_distance = float('inf')
        self.rear_distance = float('inf')

        self.sensor_lock = threading.Lock()

        # ==================================
        # ROS 2 PUBLISHERS
        # ==================================

        self.front_publisher = self.create_publisher(
            Range,
            '/ultrasonic/front',
            10
        )

        self.rear_publisher = self.create_publisher(
            Range,
            '/ultrasonic/rear',
            10
        )

        # ==================================
        # INITIALIZE SENSORS
        # ==================================

        self.setup_sensors()

        # ==================================
        # UPDATE TIMER
        # ==================================

        self.update_rate = float(
            self.get_parameter('update_rate').value
        )

        self.timer = self.create_timer(
            1.0 / self.update_rate,
            self.read_sensors
        )

        self.get_logger().info(
            'Ultrasonic Controller Started'
        )

    # ======================================
    # INITIALIZE SENSORS
    # ======================================

    def setup_sensors(self):

        pins = [
            int(self.get_parameter('front_trigger_pin').value),
            int(self.get_parameter('front_echo_pin').value),
            int(self.get_parameter('rear_trigger_pin').value),
            int(self.get_parameter('rear_echo_pin').value)
        ]

        if any(pin < 0 for pin in pins):

            self.get_logger().warning(
                'Ultrasonic GPIO pins not configured.'
            )
            return

        if len(set(pins)) != 4:

            self.get_logger().error(
                'Ultrasonic GPIO pins must be different.'
            )
            return

        if DistanceSensor is None:

            self.get_logger().error(
                'gpiozero DistanceSensor unavailable.'
            )
            return

        try:

            max_distance = float(
                self.get_parameter('max_range').value
            )

            min_distance = float(
                self.get_parameter('min_range').value
            )

            self.front_sensor = DistanceSensor(
                echo=pins[1],
                trigger=pins[0],
                max_distance=max_distance,
                threshold_distance=0.3
            )

            self.rear_sensor = DistanceSensor(
                echo=pins[3],
                trigger=pins[2],
                max_distance=max_distance,
                threshold_distance=0.3
            )

            self.get_logger().info(
                'Ultrasonic sensors initialized.'
            )

        except Exception as error:

            self.get_logger().error(
                f'Sensor initialization failed: {error}'
            )

            self.close_sensors()

    # ======================================
    # READ SENSOR DISTANCE
    # ======================================

    def get_distance(self, sensor):

        if sensor is None:
            return None

        try:

            distance = sensor.distance

            if distance is None:
                return None

            if not 0 <= distance <= float(
                self.get_parameter('max_range').value
            ):
                return None

            return float(distance)

        except Exception as error:

            self.get_logger().warning(
                f'Ultrasonic reading failed: {error}'
            )

            return None

    # ======================================
    # CREATE RANGE MESSAGE
    # ======================================

    def create_range_message(self, distance, frame):

        msg = Range()

        msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        msg.header.frame_id = frame

        msg.radiation_type = Range.ULTRASOUND

        msg.field_of_view = 0.26

        msg.min_range = float(
            self.get_parameter('min_range').value
        )

        msg.max_range = float(
            self.get_parameter('max_range').value
        )

        # NaN represents an invalid measurement.

        if distance is None:
            msg.range = float('nan')
        else:
            msg.range = distance

        return msg

    # ======================================
    # READ BOTH SENSORS
    # ======================================

    def read_sensors(self):

        front = self.get_distance(
            self.front_sensor
        )

        rear = self.get_distance(
            self.rear_sensor
        )

        with self.sensor_lock:

            self.front_distance = (
                front if front is not None
                else float('inf')
            )

            self.rear_distance = (
                rear if rear is not None
                else float('inf')
            )

        # Publish front measurement

        self.front_publisher.publish(
            self.create_range_message(
                front,
                'ultrasonic_front_link'
            )
        )

        # Publish rear measurement

        self.rear_publisher.publish(
            self.create_range_message(
                rear,
                'ultrasonic_rear_link'
            )
        )

    # ======================================
    # GET DISTANCE
    # ======================================

    def get_front_distance(self):

        with self.sensor_lock:
            return self.front_distance

    def get_rear_distance(self):

        with self.sensor_lock:
            return self.rear_distance

    # ======================================
    # CLOSE SENSORS
    # ======================================

    def close_sensors(self):

        if self.front_sensor is not None:
            self.front_sensor.close()
            self.front_sensor = None

        if self.rear_sensor is not None:
            self.rear_sensor.close()
            self.rear_sensor = None

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().info(
            'Stopping Ultrasonic Controller'
        )

        self.close_sensors()

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    ultrasonic_node = UltrasonicController()

    try:

        rclpy.spin(ultrasonic_node)

    except KeyboardInterrupt:

        pass

    finally:

        ultrasonic_node.destroy_node()

        if rclpy.ok():

            rclpy.shutdown()


if __name__ == '__main__':

    main()
