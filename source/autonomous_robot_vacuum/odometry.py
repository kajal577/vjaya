
"""
AUTONOMOUS ROBOT VACUUM
File: odometry.py

Publishes odom -> base_link TF transform
using wheel odometry from encoder.py.

Raspberry Pi 5 + ROS 2 Jazzy
VJaYa Robotics
"""

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

from tf2_ros import TransformBroadcaster


class OdometryTFPublisher(Node):

    def __init__(self):

        super().__init__('odometry_tf_publisher')

        # ==================================
        # PARAMETERS
        # ==================================

        self.declare_parameter('odom_topic', '/wheel/odometry')
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_link')

        self.odom_frame = str(
            self.get_parameter('odom_frame').value
        )

        self.base_frame = str(
            self.get_parameter('base_frame').value
        )

        # ==================================
        # TF BROADCASTER
        # ==================================

        self.tf_broadcaster = TransformBroadcaster(self)

        # ==================================
        # ODOMETRY SUBSCRIBER
        # ==================================

        odom_topic = str(
            self.get_parameter('odom_topic').value
        )

        self.odom_subscriber = self.create_subscription(
            Odometry,
            odom_topic,
            self.odometry_callback,
            10
        )

        self.get_logger().info(
            'Odometry TF Publisher Started'
        )

        self.get_logger().info(
            f'Listening to: {odom_topic}'
        )

    # ======================================
    # ODOMETRY CALLBACK
    # ======================================

    def odometry_callback(self, msg):

        transform = TransformStamped()

        # Timestamp

        transform.header.stamp = (
            msg.header.stamp
            if msg.header.stamp.sec != 0
            or msg.header.stamp.nanosec != 0
            else self.get_clock().now().to_msg()
        )

        # Coordinate frames

        transform.header.frame_id = self.odom_frame
        transform.child_frame_id = self.base_frame

        # Position

        transform.transform.translation.x = (
            msg.pose.pose.position.x
        )

        transform.transform.translation.y = (
            msg.pose.pose.position.y
        )

        transform.transform.translation.z = (
            msg.pose.pose.position.z
        )

        # Orientation

        q = msg.pose.pose.orientation

        norm = math.sqrt(
            q.x * q.x
            + q.y * q.y
            + q.z * q.z
            + q.w * q.w
        )

        if norm < 1e-9:

            self.get_logger().error(
                'Invalid odometry orientation quaternion.'
            )
            return

        transform.transform.rotation.x = q.x / norm
        transform.transform.rotation.y = q.y / norm
        transform.transform.rotation.z = q.z / norm
        transform.transform.rotation.w = q.w / norm

        # Publish TF

        self.tf_broadcaster.sendTransform(transform)


# ==========================================
# MAIN FUNCTION
# ==========================================

def main(args=None):

    rclpy.init(args=args)

    node = OdometryTFPublisher()

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
