# The main toolbar on the top of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util, Furniture
import pygame


class Toolbar(UI.ToolBar):
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
        buttonFunctions=None,
    ):
        self.buttonFunctions = buttonFunctions
        super().__init__(canvas, x_pos, y_pos, width, height, bg_color, scale)
        self.add_ui_elements()

    def append_drawable_eventable(self, element):
        self.drawables.append(element)
        self.eventables.append(element)

    def add_ui_elements(self):
        # Add Buttons
        open_floorplan_designer = UI.Button(
            parent=self,
            x_pos=0.066,
            y_pos=0.066,
            width=0.868,
            height=0.2,
            text="Open Floorplan Designer",
            border_thickness=2,
            rounded=True,
            action=lambda: self.buttonFunctions["open_floorplan_designer"](),
        )
        self.append_drawable_eventable(open_floorplan_designer)
