import Util.py
import floorTile
import Robot


class Simulation:
    def __init__(self, floor: dict, ai, robot: Robot):
        """
        floor: dict of (int, int):floorTile representing the floorplan
        ai: any object with a method that matches the update(bool) -> (float, float) signature. Outputs should both be in the range [-1, 1].
        robot: the Robot object
        """
        self.AI = ai
        self.FloorPlan = floor
        if robot.validate() and not Collision(robot.pos, robot.diameter / 2, floor):
            self.robot = robot
        else:
            raise ValueError("Robot not valid, or collides with terrain")

        self.ElapsedTime = 0
        self.IsColliding = False
        self.SimSpeed = 1
        self.DefaultHertz = 60

    def update(dT):
        """dT, in seconds, is the real time since the last Update call"""
        self.robot.doCleaning(self.FloorPlan, dT)
        # these values are in the [-1, 1] range, representing fraction of the robot's maximum ability
        speed, dTheta = self.AI.update(self.IsColliding)
        self.robot.facing += dTheta * self.robot.maxTurn * dT * self.SimSpeed
        ProspectivePosition = (
            self.robot.pos + speed * self.robot.maxSpeed * dT * self.SimSpeed
        )
        self.IsColliding = Collision(
            ProspectivePosition, self.robot.diameter / 2, self.FloorPlan
        )
        if not self.IsColliding:
            # the robot's motion is valid
            self.robot.pos = ProspectivePosition
