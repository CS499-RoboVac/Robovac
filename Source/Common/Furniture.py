# Furniture obstructions that the robot will run into
from typing import Any
import pygame
from Common.UI import scalable
import Common.Colors as Colors


class Chest(scalable):
    """
    A furniture object that the robot cannot pass through.

    Attributes:
    -----------
    parent : Any
        The parent object of the chest.
    x_pos : float
        The x position of the chest.
    y_pos : float
        The y position of the chest.
    width : float
        The width of the chest in inches.
    height : float
        The height of the chest in inches.
    color : tuple
        The color of the chest.

    Methods:
    --------
    __init__(parent, x_pos, y_pos, width, height, color=Colors.CHEST):
        Initializes a new instance of the Chest class.
    draw(parent, position_override=None):
        Draws the chest on the canvas.
    change_position(x_pos, y_pos):
        Changes the position of the chest.
    """

    def __init__(self, parent: Any, x_pos: float, y_pos: float, width_scale: float, width: float, height: float, color: tuple = Colors.CHEST) -> None:
        """
        Initializes a new instance of the Chest class.

        Parameters:
        -----------
        parent : Any
            The parent object of the chest.
        x_pos : float
            The x position of the chest.
        y_pos : float
            The y position of the chest.
        width_scale : float
            The width of the chest as a percentage of the parent's width.
        width : float
            The width of the chest in inches.
        height : float
            The height of the chest in inches.
        color : tuple, optional
            The color of the chest. Default is Colors.CHEST.
        """
        super().__init__(parent, x_pos, y_pos, width_scale, height)
        self.raw_width = width
        self.raw_height = height
        self.color = color

    def draw(self, parent: Any, position_override: Any = None) -> None:
        """
        Draws the chest on the canvas.

        Parameters:
        -----------
        parent : Any
            The canvas to draw the chest on.
        position_override : Any, optional
            The position to draw the chest at. Default is None.
        """
        width = self.get_width()
        # Scale the height to match the width, as opposed to scaling the height by the size of the parent
        height = width * (self.raw_height / self.raw_width)


        pygame.draw.rect(
            parent,
            self.color,
            (
                self.get_x(),
                self.get_y(),
                width,
                height,
            ),
        )

    def change_position(self, x_pos: int, y_pos: int) -> None:
        """
        Changes the position of the chest.

        Parameters:
        -----------
        x_pos : int
            The new x position of the chest.
        y_pos : int
            The new y position of the chest.
        """
        pass