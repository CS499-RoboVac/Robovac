
import sys
import os

import Common.Primitives as Primitives
from Common.Util import Vec2

from Common.Robot import Robot
import sys


class Simulation:

    def __init__(self, floor, dirt, ai, robot: Robot, tl: Vec2):

        """
        floor: our floorplan
        dirt: a 2d array
        ai: any object with a method that matches the update(bool, float) -> (float, float) signature. Outputs should both be in the range [-1, 1].
        robot: the Robot object
        """
        self.ai = ai
        self.floor_plan = floor

        self.tl = tl
        self.dirt = dirt
        if robot.validate() and not Primitives.Collision(
            robot.pos + tl, robot.diameter / 2, floor

        ):
            self.robot = robot
        else:
            raise RuntimeError("Robot Validation failed")

        self.elapsed_time = 0
        self.max_time = 0
        self.is_colliding = False
        self.default_tickrate = 60

    def update(self, dT):
        """dT, in seconds, is the simulation time since the last Update call"""

        self.robot.doCleaning(self.dirt, dT)
        # these values are in the [-1, 1] range, representing fraction of the robot's maximum ability
        speed, dΘ = self.ai.update(self.is_colliding, dT)
        self.robot.facing += dΘ * self.robot.maxTurn * dT

        ProspectivePosition = self.robot.pos + Vec2(
            0, speed * self.robot.maxSpeed * dT
        ).turn(self.robot.facing)

        self.is_colliding = Primitives.Collision(
            ProspectivePosition + self.tl, self.robot.diameter, self.floor_plan

        )
        if not self.is_colliding:
            # the robot's motion is valid
            self.robot.pos = ProspectivePosition
