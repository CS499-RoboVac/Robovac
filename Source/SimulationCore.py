import Util.py
import floorTile
import Robot
class Simulation:
    def __init__(self, floor : dict, ai, robot: Robot):
        """
        floor: dict of (int, int):floorTile representing the floorplan
        ai: any object with a method that matches the update(bool) -> (float, float) signature. Outputs should both be in the range [-1, 1].
        robot: the Robot object
        """
        self.AI = ai
        self.FloorPlan = floor
        if robot.validate() and not Collision(robot.pos, robot.diameter/2, floor):
            self.robot = robot
        else:
            raise ValueError("Robot not valid, or collides with terrain")
        self.ElapsedTime = 0
        self.ISColliding = False
    
    def update():
        speed, dTheta = self.AI.update(self.ISColliding)
        