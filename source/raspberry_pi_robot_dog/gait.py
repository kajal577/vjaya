"""Slow alternating crawl gait. Start with the dog supported off the ground."""
import math
import time
import config

class GaitController:
    def __init__(self, legs): self.legs = legs; self.running = False

    def walk(self, direction=1, turn=0.0, duration=1.0):
        self.running = True
        start = time.monotonic()
        step_time = config.WALK_STEP_SECONDS
        while self.running and time.monotonic() - start < duration:
            t = (time.monotonic() - start) / step_time * 2.0 * math.pi
            for index, name in enumerate(('front_left','front_right','rear_left','rear_right')):
                phase = t + (math.pi if index in (1, 2) else 0.0)
                swing = math.sin(phase) * config.WALK_SWING_DEG * direction
                lift = max(0.0, math.cos(phase)) * config.KNEE_BEND_DEG
                hip = 90 + (turn * 12 if index in (0, 2) else -turn * 12)
                # Mirror shoulder/knee direction on right side; tune for mechanical linkage.
                mirror = -1 if index in (1, 3) else 1
                shoulder = 90 + mirror * swing
                knee = 90 + mirror * lift
                self.legs.set_leg(name, hip, shoulder, knee, smooth=False)
            time.sleep(0.04)
        self.running = False

    def stop(self): self.running = False
