from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='indoor_mapping_robot', executable='drive_node', output='screen'),
        Node(package='indoor_mapping_robot', executable='odometry_node', output='screen'),
    ])
