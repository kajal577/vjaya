"""
AUTONOMOUS ROBOT VACUUM
File: slam.launch.py

Starts SLAM Toolbox mapping.
ROS 2 Jazzy
VJaYa Robotics
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description():

    slam_package = get_package_share_directory(
        'slam_toolbox'
    )

    project_package = get_package_share_directory(
        'autonomous_robot_vacuum'
    )

    slam_launch = Path(
        slam_package
    ) / 'launch' / 'online_async_launch.py'

    slam_config = Path(
        project_package
    ) / 'config' / 'slam_toolbox.yaml'

    return LaunchDescription([

        IncludeLaunchDescription(

            PythonLaunchDescriptionSource(
                str(slam_launch)
            ),

            launch_arguments={
                'slam_params_file': str(slam_config),
                'use_sim_time': 'false'
            }.items()

        )

    ])