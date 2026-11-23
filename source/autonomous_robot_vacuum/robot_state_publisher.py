
"""
AUTONOMOUS ROBOT VACUUM
File: robot_state_publisher.py

Starts the ROS 2 Robot State Publisher.
Raspberry Pi 5 + ROS 2 Jazzy

VJaYa Robotics
"""

from pathlib import Path

import rclpy
from rclpy.node import Node

from ament_index_python.packages import (
    get_package_share_directory
)

from robot_state_publisher import (
    RobotStatePublisher as RosRobotStatePublisher
)


class RobotModelController(Node):

    def __init__(self):

        super().__init__('robot_model_controller')

        self.declare_parameter(
            'urdf_file',
            ''
        )

        self.declare_parameter(
            'use_sim_time',
            False
        )

        self.get_logger().info(
            'Robot Model Controller Started'
        )

        self.start_robot_model()

    def start_robot_model(self):

        self.get_logger().warning(
            'Robot State Publisher is a separate ROS 2 executable. '
            'Start it through the project launch file using the '
            'robot_state_publisher package.'
        )


def main(args=None):

    rclpy.init(args=args)

    node = RobotModelController()

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
