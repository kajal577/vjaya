
"""
AUTONOMOUS ROBOT VACUUM
File: lidar.py

LiDAR scan processing and filtering.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan


class LidarController(Node):

    def __init__(self):

        super().__init__('lidar_controller')

        # LiDAR configuration

        self.declare_parameter(
            'input_topic', '/scan_raw'
        )

        self.declare_parameter(
            'output_topic', '/scan'
        )

        self.declare_parameter(
            'min_range', 0.12
        )

        self.declare_parameter(
            'max_range', 8.0
        )

        self.input_topic = (
            self.get_parameter('input_topic').value
        )

        self.output_topic = (
            self.get_parameter('output_topic').value
        )

        self.min_range = float(
            self.get_parameter('min_range').value
        )

        self.max_range = float(
            self.get_parameter('max_range').value
        )

        # Obstacle information

        self.closest_obstacle = float('inf')

        self.scan_count = 0

        # ROS 2 Subscriber

        self.scan_subscription = self.create_subscription(
            LaserScan,
            self.input_topic,
            self.scan_callback,
            10
        )

        # ROS 2 Publisher

        self.scan_publisher = self.create_publisher(
            LaserScan,
            self.output_topic,
            10
        )

        self.get_logger().info(
            'LiDAR Controller Started'
        )

        self.get_logger().info(
            f'Input: {self.input_topic}'
        )

        self.get_logger().info(
            f'Output: {self.output_topic}'
        )

    # ======================================
    # PROCESS LIDAR SCAN
    # ======================================

    def scan_callback(self, msg):

        try:

            filtered_scan = LaserScan()

            # Preserve original scan metadata

            filtered_scan.header = msg.header

            filtered_scan.angle_min = msg.angle_min
            filtered_scan.angle_max = msg.angle_max
            filtered_scan.angle_increment = (
                msg.angle_increment
            )

            filtered_scan.time_increment = (
                msg.time_increment
            )

            filtered_scan.scan_time = msg.scan_time

            filtered_scan.range_min = msg.range_min
            filtered_scan.range_max = msg.range_max

            filtered_scan.intensities = list(
                msg.intensities
            )

            valid_distances = []

            filtered_ranges = []

            # Filter each measurement

            for distance in msg.ranges:

                if not math.isfinite(distance):

                    filtered_ranges.append(float('inf'))
                    continue

                if (
                    distance < self.min_range
                    or distance > self.max_range
                ):

                    filtered_ranges.append(float('inf'))
                    continue

                filtered_ranges.append(distance)

                valid_distances.append(distance)

            filtered_scan.ranges = filtered_ranges

            # Calculate closest obstacle

            if valid_distances:

                self.closest_obstacle = min(
                    valid_distances
                )

            else:

                self.closest_obstacle = float('inf')

            # Publish filtered scan

            self.scan_publisher.publish(
                filtered_scan
            )

            self.scan_count += 1

            if self.scan_count % 100 == 0:

                self.get_logger().debug(
                    f'LiDAR scans processed: '
                    f'{self.scan_count}'
                )

        except Exception as error:

            self.get_logger().error(
                f'LiDAR processing error: {error}'
            )

    # ======================================
    # GET CLOSEST OBSTACLE
    # ======================================

    def get_closest_obstacle(self):

        return self.closest_obstacle

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().info(
            'Stopping LiDAR Controller'
        )

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    lidar_node = LidarController()

    try:

        rclpy.spin(lidar_node)

    except KeyboardInterrupt:

        pass

    finally:

        lidar_node.destroy_node()

        if rclpy.ok():

            rclpy.shutdown()


if __name__ == '__main__':

    main()
