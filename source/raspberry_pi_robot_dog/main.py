"""Raspberry Pi Robot Dog firmware entry point."""
from servo_driver import ServoDriver
from robot_controller import RobotController

def main():
    driver = ServoDriver()
    robot = RobotController(driver)
    try:
        robot.run()
    except KeyboardInterrupt:
        print('\nStopping robot dog.')
    finally:
        robot.close()

if __name__ == '__main__': main()
