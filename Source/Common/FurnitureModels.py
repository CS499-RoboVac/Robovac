# Furniture obstructions that the robot will run into
from Common.Util import Vec2
import Common.Colors as Colors


class Furniture:
    """
    Defines a basic furniture object
    """

    def __init__(self, position: Vec2, size: Vec2):
        """
        Constructor
        position: Vec2, the position of the object
        size: Vec2, the size of the object
        """
        self.position = position
        self.size = size

    def change_position(self, position: Vec2):
        """
        Change the position of the object
        position: Vec2, the new position of the object
        """
        self.position = position

    def change_size(self, size: Vec2):
        """
        Change the size of the object
        size: Vec2, the new size of the object
        """
        self.size = size


# Chest object. This is a furniture object that the robot cannot pass through
class Chest(Furniture):
    def __init__(self, position: Vec2, size: Vec2):
        """
        Constructor
        position: Vec2, the position of the chest
        size: Vec2, the size of the chest
        """
        super().__init__(position, size)
        self.color = Colors.CHEST


# Table object. This is a furniture object that the robot can pass "under" as long as it does not collide with the legs
class Table(Furniture):
    def calculate_leg_positions(self):
        """
        Calculate the positions of the legs of the table
        """
        leg_offset = self.leg_diameter / 2

        # top left, top right, bottom left, bottom right
        leg_positions = [
            self.position + Vec2(leg_offset, leg_offset),
            self.position + Vec2(self.size.x, 0) + Vec2(-leg_offset, leg_offset),
            self.position + Vec2(0, self.size.y) + Vec2(leg_offset, -leg_offset),
            self.position + self.size + Vec2(-leg_offset, -leg_offset),
        ]
        return leg_positions

    def __init__(self, position: Vec2, size: Vec2, leg_diameter: float = 3.0):
        """
        Constructor
        position: Vec2, the position of the table
        size: Vec2, the size of the table
        """
        super().__init__(position, size)
        self.leg_diameter = leg_diameter
        self.leg_positions = self.calculate_leg_positions()
        self.color = Colors.TABLE

    def change_position(self, position: Vec2):
        """
        Change the position of the table
        position: Vec2, the new position of the table
        """
        super().change_position(position)
        self.leg_positions = self.calculate_leg_positions()

    def change_size(self, size: Vec2):
        """
        Change the size of the table
        size: Vec2, the new size of the table
        """
        super().change_size(size)
        self.leg_positions = self.calculate_leg_positions()
