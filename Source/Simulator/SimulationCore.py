import Common.Primitives as Primitives
from Common.Robot import Robot
import sys


class Simulation:
    def __init__(self, floor, dirt, ai, robot: Robot):
        """
        floor: our floorplan
        dirt: a 2d array
        ai: any object with a method that matches the update(bool, float) -> (float, float) signature. Outputs should both be in the range [-1, 1].
        robot: the Robot object
        """
        self.ai = ai
        self.floor_plan = floor
        if robot.validate() and not Primitives.Collision(robot.pos, robot.diameter / 2, floor):
            self.robot = robot
        else:
            raise ValueError("Robot not valid, or collides with terrain")

        self.elapsed_time = 0
        self.is_colliding = False
        self.sim_speed = 1
        self.default_tickrate = 60

    def update(self, dT):
        """dT, in seconds, is the simulation time since the last Update call"""
        self.robot.doCleaning(self.floor_plan, dT)
        # these values are in the [-1, 1] range, representing fraction of the robot's maximum ability
        speed, dTheta = self.ai.update(self.is_colliding)
        self.robot.facing += dTheta * self.robot.maxTurn * dT * self.sim_speed
        ProspectivePosition = (
            self.robot.pos + speed * self.robot.maxSpeed * dT * self.sim_speed
        )
        self.is_colliding = Primitives.Collision(
            ProspectivePosition, self.robot.diameter / 2, self.floor_plan
        )
        if not self.is_colliding:
            # the robot's motion is valid
            self.robot.pos = ProspectivePosition
