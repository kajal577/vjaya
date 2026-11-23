
# AUTONOMOUS ROBOT VACUUM
## VJaYa Robotics

An autonomous robot vacuum cleaner built using Raspberry Pi 5, Ubuntu 24.04 and ROS 2 Jazzy.

### Features
- Autonomous room mapping using LiDAR
- SLAM-based environment mapping
- Autonomous navigation using Nav2
- Obstacle detection and avoidance
- Differential drive motor control
- Wheel encoder feedback
- IMU integration
- Automatic vacuum and brush control

### Hardware Requirements
1. Raspberry Pi 5
2. 2D LiDAR sensor
3. Differential drive chassis
4. Two DC geared motors with encoders
5. Motor driver
6. IMU sensor
7. Ultrasonic sensors
8. Bumper switches
9. Vacuum motor
10. Cleaning brush motor
11. Battery and power management system

### Software Requirements
- Ubuntu 24.04 (64-bit)
- ROS 2 Jazzy
- SLAM Toolbox
- Nav2
- Python 3
- Colcon

### Installation

Update Ubuntu:

```bash
sudo apt update
sudo apt upgrade -y
```

Install ROS 2 Jazzy:

```bash
sudo apt install ros-jazzy-desktop
```

Install navigation and mapping:

```bash
sudo apt install ros-jazzy-navigation2
sudo apt install ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-slam-toolbox
```

### Build Instructions

Navigate to the workspace:

```bash
cd ~/AUTONOMOUS_ROBOT_VACUUM
```

Build:

```bash
colcon build
```

Source workspace:

```bash
source install/setup.bash
```

### Safety
- Test motor control with wheels lifted.
- Use a suitable protected battery and motor driver.
- Keep the vacuum motor power circuit separate from Raspberry Pi GPIO.
- Include an emergency stop.
- Never operate the robot unattended during initial testing.

### Developed By
VJaYa Robotics
