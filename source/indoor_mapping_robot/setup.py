from setuptools import setup
package_name = 'indoor_mapping_robot'
setup(name=package_name, version='0.1.0', packages=[package_name],
      data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]),
                 ('share/' + package_name, ['package.xml']),
                 ('share/' + package_name + '/launch', ['launch/robot_bringup.launch.py', 'launch/mapping.launch.py'])],
      install_requires=['setuptools'], zip_safe=True,
      entry_points={'console_scripts': [
          'drive_node = indoor_mapping_robot.drive_node:main',
          'odometry_node = indoor_mapping_robot.odometry_node:main']})
