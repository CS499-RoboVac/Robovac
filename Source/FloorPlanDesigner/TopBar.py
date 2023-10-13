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

    def open_intro_window(self):
        Util.open_intro_window()

    def add_ui_elements(self):
        # add button to go back to the intro window
        back_button = UI.Button(
            parent=self,
            x_pos=0,
            y_pos=0,
            width=0.1,
            height=0.8,
            text="Back",
            action=lambda: Util.open_intro_window(),
        )
        self.append_drawable_eventable(back_button)
