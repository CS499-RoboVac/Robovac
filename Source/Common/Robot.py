from Common.Util import Vec2
import math

# This class will represent the robot in the simulation
# It will only handle information about the robot, not the actual drawing of the robot
# that will be handled by the RobotDrawer class

# the robot is a circle with two "Whiskers"
# the whiskers are two circles that are attached to the robot
# The whiskers center points cannot be outside of the robot's circle
# The robot also has a vaccum that is a rectangle that is under the robot
# The vaccum's width cannot be larger than the robot's diameter


# The whiskers have a diameter, and a position relative to the robot they are attached to
class Whisker:
    def __init__(self, pos: Vec2, diameter: float):
        """
        Constructor
        pos: Vec2, the position of the whisker relative to the center
        diameter: float, the diameter of the whisker
        """
        self.pos = pos
        self.diameter = diameter


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
        pos: Vec2,
        facing: float = 0,
        diameter: float = 12.8,
        maxSpeed: float = 50,
        maxTurn: float = 2 * math.pi / 3,
        whisker_length: float = 13.5,
        vaccum_width: float = 5.8,
    ):
        self.pos = pos
        self.facing = facing
        self.diameter = diameter
        self.maxSpeed = maxSpeed
        self.maxTurn = maxTurn
        self.whisker_length = whisker_length
        self.vaccum_width = vaccum_width
        self.is_valid = True
        self.whiskers = [
            Whisker(
                pos + Vec2(self.diameter / 2, self.diameter / 2),
                self.whisker_length,
            ),
            Whisker(
                pos + Vec2(-self.diameter / 2, self.diameter / 2),
                self.whisker_length,
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
            delta = whisker.pos - self.pos
            dx = abs(delta.x)
            dy = abs(delta.y)
            radius = self.diameter / 2
            if dx * dx + dy * dy <= radius * radius:
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

    def doCleaning(floor, dT):
        """floor is a dict like normal; the robot should handle its own shape and whisker efficiencies and whatnot"""
        pass  # TODO IMPLEMEMNT LATER

    def __str__(self) -> str:
        return (
            f"Robot(pos={self.pos}, \n"
            f"facing={self.facing}, diameter={self.diameter},\n"
            f"maxSpeed={self.maxSpeed}, maxTurn={self.maxTurn},\n"
            f"whisker_length={self.whisker_length}, vaccum_width={self.vaccum_width},\n"
            f"is_valid={self.is_valid}, whiskers={self.whiskers}"
        )
