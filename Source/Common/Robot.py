from Common.Util import Vec2
import math
import numpy as np
import cv2
# This class will represent the robot in the simulation
# It will only handle information about the robot, not the actual drawing of the robot
# that will be handled by the RobotDrawer class

# the robot is a circle with two "Whiskers"
# the whiskers are two circles that are attached to the robot
# The whiskers center points cannot be outside of the robot's circle
# The robot also has a vaccum that is a rectangle that is under the robot
# The vaccum's width cannot be larger than the robot's diameter


def Within(pos: Vec2, arr) -> bool:
    s = arr.shape
    return (
        (type(pos.x) == int and type(pos.y) == int)
        and (0 <= pos.x and pos.x < s[0])
        and (0 <= pos.y and pos.y < s[1])
    )


# The whiskers have a diameter, and a position relative to the robot they are attached to
class Whisker:
    def __init__(self, pos: Vec2, diameter: float, eff: float):
        """
        Constructor
        pos: Vec2, the position of the whisker relative to the center
        diameter: float, the diameter of the whisker
        """
        self.pos = pos
        self.diameter = diameter
        self.efficiency = eff


class Robot:
    """
    Constructor
    pos: Vec2, the position of the robot
    facing: float, the angle the robot is facing, in radians
    diameter: float, The diameter of the robot in centimeters
    maxSpeed: float, value in cm/s
    maxTurn: float, value in rad/s, the unit's maximum rotation speed around its own center
    whisker_length: float, The length of the whiskers on the robot (cm)
    vaccum_width: float, The width of the vaccum on the robot (cm)
    """

    def __init__(
        self,
        pos: Vec2 = Vec2(0, 0),
        facing: float = 0,
        diameter: float = 12.8,
        maxSpeed: float = 50,
        maxTurn: float = 2 * math.pi / 3,
        whisker_length: float = 13.5,
        vaccum_width: float = 5.8,
        efficiency=0.5,
        whisker_eff=0.5,
    ):
        self.pos = pos
        self.facing = facing
        self.diameter = diameter
        self.maxSpeed = maxSpeed
        self.maxTurn = maxTurn
        self.whisker_length = whisker_length
        self.vaccum_width = vaccum_width
        self.is_valid = True
        self.efficiency = efficiency
        self.whiskers = [
            Whisker(
                Vec2(self.diameter / 3, self.diameter / 3),
                self.whisker_length,
                whisker_eff,
            ),
            Whisker(
                Vec2(-self.diameter / 3, self.diameter / 3),
                self.whisker_length,
                whisker_eff,
            ),
        ]

    def validate(self):
        """
        Check if the robot is valid
        return: True if the robot is valid, False otherwise
        """
        # Is the vaccum width larger than the robot's diameter?
        if self.vaccum_width > self.diameter:
            self.is_valid = False
            return False

        # Are the centers of the whiskers outside of the robot?
        for whisker in self.whiskers:
            radius = self.diameter / 2
            if whisker.pos.length() <= radius:
                continue
            else:
                self.is_valid = False
                return False

        self.is_valid = True
        return True

    # Update the size of the robot
    # diameter: The new diameter of the robot
    # @return: True if the robot is valid, False otherwise
    def update_size(self, diameter):
        self.diameter = diameter
        return self.validate()

    # Update the whisker length
    # whisker_length: The new whisker length
    def update_whisker_length(self, whisker_length):
        self.whisker_length = whisker_length
        self.whiskers[0].diameter = whisker_length
        self.whiskers[1].diameter = whisker_length

    # Update the vaccum width
    # vaccum_width: The new vaccum width
    # @return: True if the robot is valid, False otherwise
    def update_vaccum_width(self, vaccum_width):
        self.vaccum_width = vaccum_width
        return self.validate()

    def doCleaning(
        self, dirt, dT
    ):  # NOTE we are assuming small movement relative to timestep
        # circles:
        for whisker in self.whiskers:
            p = self.pos + whisker.pos.turn(self.facing)
            for x in range(
                math.floor(-whisker.diameter / 2), math.ceil(whisker.diameter / 2) + 1
            ):
                for y in range(
                    math.floor(-whisker.diameter / 2),
                    math.ceil(whisker.diameter / 2) + 1,
                ):
                    if Within(
                        Vec2(math.floor(p.y) + y, math.floor(p.x) + x), dirt
                    ) and (x * x + y * y <= whisker.diameter * whisker.diameter / 4):
                        dirt[math.floor(p.y) + y, math.floor(p.x) + x] *= (
                            1 - whisker.efficiency * dT
                        )
        RV = Vec2(self.diameter / 2, 0).turn(self.facing)

        for point in self.bresenham_line(
            self.pos.x + RV.x,
            self.pos.y + RV.y,
            self.pos.x - (RV.x),
            self.pos.y - (RV.y),
        ):
            if Within(Vec2(point[1], point[0]), dirt):
                dirt[point[1], point[0]] *= 1 - self.efficiency * dT

    def bresenham_line(self, x1, y1, x2, y2):
        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end (x, y) points
        """

        # Setup initial conditions
        x1, y1 = int(round(x1)), int(round(y1))
        x2, y2 = int(round(x2)), int(round(y2))
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        return points

    def __str__(self) -> str:
        return (
            f"Robot(pos={self.pos}, \n"
            f"facing={self.facing}, diameter={self.diameter},\n"
            f"maxSpeed={self.maxSpeed}, maxTurn={self.maxTurn},\n"
            f"whisker_length={self.whisker_length}, vaccum_width={self.vaccum_width},\n"
            f"is_valid={self.is_valid}, whiskers={self.whiskers}"
        )
