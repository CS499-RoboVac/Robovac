# This class will represent the robot in the simulation
# It will only handle information about the robot, not the actual drawing of the robot
# that will be handled by the RobotDrawer class

# the robot is a circle with two "Whiskers"
# the whiskers are two circles that are attached to the robot
# The whiskers center points cannot be outside of the robot's circle
# The robot also has a vaccum that is a rectangle that is under the robot
# The vaccum's width cannot be larger than the robot's diameter
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem

# The whiskers have a diameter, and a position relative to the robot they are attached to
class Whisker(QGraphicsItem): 
    # Constructor
    # x_pos: The x position of the whisker
    # y_pos: The y position of the whisker
    # diameter: The diameter of the whisker
    def __init__(self, x_pos, y_pos, diameter):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.diameter = diameter

    def boundingRect(self):
        return QRectF(self.x_pos, self.y_pos, self.diameter, self.diameter)

    def paint(self, painter, option, widget):
        painter.setBrush(Qt.blue)
        painter.drawEllipse(self.boundingRect())


class Robot(QGraphicsItem):
    # Constructor
    # x_pos: The x position of the robot
    # y_pos: The y position of the robot
    # diameter: The diameter of the robot in inches
    # whisker_length: The length of the whiskers on the robot
    # vaccum_width: The width of the vaccum on the robot
    def __init__(
        self,
        x_pos=0,
        y_pos=0,
        diameter=12.8,
        whisker_length=13.5,
        vaccum_width=5.8,
    ):
        super().__init__()
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
    def boundingRect(self):
        return QRectF(self.x_pos - self.diameter / 2, self.y_pos - self.diameter / 2, self.diameter, self.diameter)

    def paint(self, painter, option, widget):
        painter.setBrush(Qt.red)
        painter.drawEllipse(self.boundingRect())

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
