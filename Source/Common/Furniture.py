# Furniture obstructions that the robot will run into
from typing import Any
import Common.Colors as Colors


# Chest object. This is a furniture object that the robot cannot pass through
class Chest:
    # Constructor
    # x_pos: x position of the chest
    # y_pos: y position of the chest
    # width: width of the chest in inches
    # height: height of the chest in inches
    def __init__(self, x_pos, y_pos, width, height):
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.type = "chest"

    # Draw the chest on the canvas
    # canvas: the canvas to draw the chest on
    def draw(self, canvas, position_override=None):
        if position_override:
            draw_x = position_override[0]
            draw_y = position_override[1]
        else:
            draw_x = self.x
            draw_y = self.y

    # Change the position of the chest
    # x_pos: the new x position of the chest
    # y_pos: the new y position of the chest
    def change_position(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
