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
    # Constructor
    # @param x_pos: The x position of the whisker
    # @param y_pos: The y position of the whisker
    # @param diameter: The diameter of the whisker
    def __init__(self, x_pos, y_pos, diameter):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.diameter = diameter


class Robot:
    # Constructor
    # @param x_pos: The x position of the robot
    # @param y_pos: The y position of the robot
    # @param diameter: The diameter of the robot in inches
    # @param whisker_length: The length of the whiskers on the robot
    # @param vaccum_width: The width of the vaccum on the robot
    def __init__(
        self,
        x_pos,
        y_pos,
        diameter=12.8,
        whisker_length=13.5,
        vaccum_width=5.8,
    ):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.diameter = diameter
        self.whisker_length = whisker_length
        self.whiskers = []
        self.vaccum_width = vaccum_width
        self.is_valid = True

        # Create the whiskers
        self.whiskers.append(
            Whisker(
                x_pos + self.diameter / 2,
                y_pos + self.diameter / 2,
                self.whisker_length,
            )
        )
        self.whiskers.append(
            Whisker(
                x_pos - self.diameter / 2,
                y_pos + self.diameter / 2,
                self.whisker_length,
            )
        )

    # Validate the robot
    # @return: True if the robot is valid, False otherwise
    def validate(self):
        # Is the vaccum width larger than the robot's diameter?
        if self.vaccum_width > self.diameter:
            self.is_valid = False
            return False

        # Are the centers of the whiskers outside of the robot?
        for whisker in self.whiskers:
            dx = abs(whisker.x_pos - self.x_pos)
            dy = abs(whisker.y_pos - self.y_pos)
            radius = self.diameter / 2
            if dx + dy <= radius:
                break
            if dx > radius or dy > radius:
                self.is_valid = False
                return False
            if dx * dx + dy * dy <= radius * radius:
                break
            self.is_valid = False
            return False

    # Update the size of the robot
    # @param diameter: The new diameter of the robot
    # @return: True if the robot is valid, False otherwise
    def update_size(self, diameter):
        self.diameter = diameter
        return self.validate()

    # Update the whisker length
    # @param whisker_length: The new whisker length
    def update_whisker_length(self, whisker_length):
        self.whisker_length = whisker_length
        self.whiskers[0].diameter = whisker_length
        self.whiskers[1].diameter = whisker_length

    # Update the vaccum width
    # @param vaccum_width: The new vaccum width
    # @return: True if the robot is valid, False otherwise
    def update_vaccum_width(self, vaccum_width):
        self.vaccum_width = vaccum_width
        return self.validate()