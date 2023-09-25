# The main toolbar on the top of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util, Furniture
import pygame


class TopBar(UI.ToolBar):
    # Constructor
    def __init__(
        self,
        canvas,
        x_pos,
        y_pos,
        width,
        height,
        bg_color=Colors.DARK_GRAY,
        scale=True,
    ):
        super().__init__(canvas, x_pos, y_pos, width, height, bg_color, scale)
        self.add_ui_elements()

    def append_drawable_eventable(self, element):
        self.drawables.append(element)
        self.eventables.append(element)

    def add_ui_elements(self):
        pass
