"""Interactive command controller for the Raspberry Pi Robot Dog."""
import time
from gait import GaitController
from leg_control import LegController
from obstacle_detection import ObstacleDetector

class RobotController:
    def __init__(self, driver):
        self.driver = driver
        self.legs = LegController(driver)
        self.gait = GaitController(self.legs)
        self.obstacle = ObstacleDetector()

    def run(self):
        self.driver.set_neutral()
        print('\nROBOT DOG COMMANDS: stand | sit | forward | backward | left | right | stop | distance | quit')
        while True:
            command = input('dog> ').strip().lower()
            if command in ('quit', 'q', 'exit'): break
            if command == 'stand': self.legs.stand()
            elif command == 'sit': self.legs.sit()
            elif command == 'stop': self.gait.stop(); self.legs.stop_pose()
            elif command == 'distance': print(f'Distance: {self.obstacle.distance_cm():.1f} cm')
            elif command in ('forward', 'backward', 'left', 'right'):
                if command == 'forward' and self.obstacle.blocked():
                    print('Obstacle detected; movement blocked.'); continue
                direction = -1 if command == 'backward' else 1
                turn = -1 if command == 'left' else (1 if command == 'right' else 0)
                print('Walking for 2 seconds; type stop after the gait returns to prompt.')
                self.gait.walk(direction=direction, turn=turn, duration=2.0)
            else: print('Unknown command.')

    def close(self):
        self.gait.stop(); self.obstacle.close()
        self.driver.close()
