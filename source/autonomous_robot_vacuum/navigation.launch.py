"""
AUTONOMOUS ROBOT VACUUM
File: navigation.launch.py

Starts Nav2 autonomous navigation.
ROS 2 Jazzy
VJaYa Robotics
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.actions import SetRemap

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description():

    nav2_package = get_package_share_directory(
        'nav2_bringup'
    )

    project_package = get_package_share_directory(
        'autonomous_robot_vacuum'
    )

    nav2_launch = Path(
        nav2_package
    ) / 'launch' / 'navigation_launch.py'

    nav2_config = Path(
        project_package
    ) / 'config' / 'nav2_params.yaml'

    return LaunchDescription([

        # Navigation velocity safety gate

        Node(
            package='autonomous_robot_vacuum',
            executable='velocity_controller',
            name='velocity_controller',
            output='screen'
        ),

        # Nav2

        GroupAction([

            SetRemap(
                src='/cmd_vel',
                dst='/cmd_vel_nav'
            ),

            IncludeLaunchDescription(

                PythonLaunchDescriptionSource(
                    str(nav2_launch)
                ),

                launch_arguments={
                    'params_file': str(nav2_config),
                    'use_sim_time': 'false',
                    'autostart': 'true'
                }.items()

            )

        ])

    ])