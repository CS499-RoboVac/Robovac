# Furniture obstructions that the robot will run into
from typing import Any
from Common.Util import Vec2
import Common.Colors as Colors


# Chest object. This is a furniture object that the robot cannot pass through
class Chest:
    
    def __init__(self, position: Vec2, size: Vec2):
        """
        Constructor
        position: Vec2, the position of the chest
        size: Vec2, the size of the chest
        """
        self.position = position
        self.size = size
        self.color = Colors.CHEST
    # Draw the chest on the canvas
    # canvas: the canvas to draw the chest on
    def draw(self):
        pass

    def change_position(self, position: Vec2):
        """
        Change the position of the chest
        position: Vec2, the new position of the chest
        """
        self.position = position
