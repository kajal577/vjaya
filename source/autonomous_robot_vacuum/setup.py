
from setuptools import setup
from glob import glob
import os

package_name = 'autonomous_robot_vacuum'

setup(
    name=package_name,
    version='1.0.0',
    packages=[
        package_name,
        package_name + '.hardware',
        package_name + '.sensors',
        package_name + '.navigation',
    ],
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='VJaYa Robotics',
    maintainer_email='developer@vjayrobotics.com',
    description='Autonomous Robot Vacuum using Raspberry Pi 5 and ROS 2 Jazzy',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = autonomous_robot_vacuum.main:main',
            'motor_control = autonomous_robot_vacuum.hardware.motor_control:main',
            'encoder = autonomous_robot_vacuum.hardware.encoder:main',
            'lidar = autonomous_robot_vacuum.sensors.lidar:main',
            'imu = autonomous_robot_vacuum.sensors.imu:main',
            'navigation = autonomous_robot_vacuum.navigation.navigation:main',
            'slam = autonomous_robot_vacuum.navigation.slam:main',
        ],
    },
)
