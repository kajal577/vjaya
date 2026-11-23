"""
AUTONOMOUS ROBOT VACUUM
File: main.py

Main project launcher.
ROS 2 Jazzy
VJaYa Robotics
"""

import sys

from launch import LaunchService
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def main():

    package_path = Path(
        get_package_share_directory(
            'autonomous_robot_vacuum'
        )
    )

    robot_launch = (
        package_path
        / 'launch'
        / 'robot.launch.py'
    )

    launch_service = LaunchService(
        argv=sys.argv[1:]
    )

    launch_service.include_launch_description(

        IncludeLaunchDescription(

            PythonLaunchDescriptionSource(
                str(robot_launch)
            )

        )

    )

    return launch_service.run()


if __name__ == '__main__':

    main()