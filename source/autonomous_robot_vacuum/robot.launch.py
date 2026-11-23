"""
AUTONOMOUS ROBOT VACUUM
File: robot.launch.py

Starts robot hardware and sensor nodes.
ROS 2 Jazzy
VJaYa Robotics
"""

from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description():

    package_path = Path(
        get_package_share_directory(
            'autonomous_robot_vacuum'
        )
    )

    config_path = package_path / 'config'
    description_path = package_path / 'description'

    urdf_path = description_path / 'robot.urdf'

    with open(urdf_path, 'r', encoding='utf-8') as file:
        robot_description = file.read()

    return LaunchDescription([

        # Robot model

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': False
            }]
        ),

        # Motor controller

        Node(
            package='autonomous_robot_vacuum',
            executable='motor_control',
            name='motor_controller',
            output='screen'
        ),

        # Wheel encoder

        Node(
            package='autonomous_robot_vacuum',
            executable='encoder',
            name='encoder_controller',
            output='screen'
        ),

        # LiDAR filter

        Node(
            package='autonomous_robot_vacuum',
            executable='lidar',
            name='lidar_controller',
            output='screen'
        ),

        # IMU filter

        Node(
            package='autonomous_robot_vacuum',
            executable='imu',
            name='imu_controller',
            output='screen'
        ),

        # Ultrasonic sensors

        Node(
            package='autonomous_robot_vacuum',
            executable='ultrasonic',
            name='ultrasonic_controller',
            parameters=[
                str(config_path / 'ultrasonic.yaml')
            ],
            output='screen'
        ),

        # Bumper switches

        Node(
            package='autonomous_robot_vacuum',
            executable='bumper',
            name='bumper_controller',
            parameters=[
                str(config_path / 'bumper.yaml')
            ],
            output='screen'
        ),

        # Emergency safety controller

        Node(
            package='autonomous_robot_vacuum',
            executable='safety_controller',
            name='safety_controller',
            output='screen'
        ),

        # Navigation velocity safety gate

        Node(
            package='autonomous_robot_vacuum',
            executable='velocity_controller',
            name='velocity_controller',
            output='screen'
        ),

        # Odometry transform

        Node(
            package='autonomous_robot_vacuum',
            executable='odometry',
            name='odometry_tf_publisher',
            output='screen'
        ),

    ])