
"""
AUTONOMOUS ROBOT VACUUM
File: imu.py

IMU sensor data processing.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu


class IMUController(Node):

    def __init__(self):

        super().__init__('imu_controller')

        # ==================================
        # CONFIGURATION
        # ==================================

        self.declare_parameter(
            'input_topic', '/imu/raw'
        )

        self.declare_parameter(
            'output_topic', '/imu/data'
        )

        self.declare_parameter(
            'frame_id', 'imu_link'
        )

        self.input_topic = (
            self.get_parameter('input_topic').value
        )

        self.output_topic = (
            self.get_parameter('output_topic').value
        )

        self.frame_id = (
            self.get_parameter('frame_id').value
        )

        self.message_count = 0

        # ==================================
        # ROS 2 SUBSCRIBER
        # ==================================

        self.imu_subscription = self.create_subscription(
            Imu,
            self.input_topic,
            self.imu_callback,
            10
        )

        # ==================================
        # ROS 2 PUBLISHER
        # ==================================

        self.imu_publisher = self.create_publisher(
            Imu,
            self.output_topic,
            10
        )

        self.get_logger().info(
            'IMU Controller Started'
        )

        self.get_logger().info(
            f'Input: {self.input_topic}'
        )

        self.get_logger().info(
            f'Output: {self.output_topic}'
        )

    # ======================================
    # PROCESS IMU DATA
    # ======================================

    def imu_callback(self, msg):

        try:

            output = Imu()

            output.header.stamp = (
                self.get_clock().now().to_msg()
            )

            output.header.frame_id = self.frame_id

            # Copy orientation

            output.orientation = msg.orientation

            # Copy angular velocity

            output.angular_velocity = (
                msg.angular_velocity
            )

            # Copy linear acceleration

            output.linear_acceleration = (
                msg.linear_acceleration
            )

            # Copy covariance information

            output.orientation_covariance = (
                list(msg.orientation_covariance)
            )

            output.angular_velocity_covariance = (
                list(msg.angular_velocity_covariance)
            )

            output.linear_acceleration_covariance = (
                list(msg.linear_acceleration_covariance)
            )

            # Validate quaternion

            q = output.orientation

            quaternion_norm = math.sqrt(
                q.x * q.x +
                q.y * q.y +
                q.z * q.z +
                q.w * q.w
            )

            if not math.isfinite(quaternion_norm):
                self.get_logger().warning(
                    'Invalid IMU quaternion received.'
                )
                return

            if quaternion_norm > 0:

                q.x /= quaternion_norm
                q.y /= quaternion_norm
                q.z /= quaternion_norm
                q.w /= quaternion_norm

            # Publish IMU message

            self.imu_publisher.publish(output)

            self.message_count += 1

            if self.message_count % 100 == 0:

                self.get_logger().debug(
                    f'IMU messages processed: '
                    f'{self.message_count}'
                )

        except Exception as error:

            self.get_logger().error(
                f'IMU processing error: {error}'
            )

    # ======================================
    # SHUTDOWN
    # ======================================

    def destroy_node(self):

        self.get_logger().info(
            'Stopping IMU Controller'
        )

        super().destroy_node()


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    imu_node = IMUController()

    try:

        rclpy.spin(imu_node)

    except KeyboardInterrupt:

        pass

    finally:

        imu_node.destroy_node()

        if rclpy.ok():

            rclpy.shutdown()


if __name__ == '__main__':

    main()
