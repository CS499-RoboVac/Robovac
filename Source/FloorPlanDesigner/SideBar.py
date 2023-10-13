# The main toolbar on the top of the FloorPlanDesigner

from Common import Colors, UI
import Common.Furniture as Furniture
import pygame


class SideBar(UI.ToolBar):
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

    # Create a new chest with the given dimensions
    def add_chest(self, width=15, height=15):
        chest = Furniture.Chest(
            parent=self,
            x_pos=0.1,
            y_pos=0.6,
            width=width,
            height=height,
            width_scale=0.8,
        )
        self.append_drawable_eventable(chest)


    def add_ui_elements(self):
        # Add the input boxes to the toolbar
        chest_width = UI.InputBox(
            parent=self,
            x_pos=0.066,
            y_pos=0.15,
            width=0.40,
            height=0.05,
            number_only=True,
        )
        self.append_drawable_eventable(chest_width)

        chest_height = UI.InputBox(
            parent=self,
            x_pos=0.532,
            y_pos=0.15,
            width=0.40,
            height=0.05,
            number_only=True,
        )
        self.append_drawable_eventable(chest_height)

        # Labels for the input boxes
        chest_width_label = UI.TextBox(
            parent=self,
            x_pos=0.066,
            y_pos=0.125,
            width=0.40,
            height=0.05,
            text="Chest Width (inches)",
            text_color=Colors.WHITE,
            background_color=Colors.DARK_GRAY,
            font=pygame.font.SysFont("Arial", 12),
        )
        self.append_drawable_eventable(chest_width_label)

        chest_height_label = UI.TextBox(
            parent=self,
            x_pos=0.532,
            y_pos=0.125,
            width=0.40,
            height=0.05,
            text="Chest Height (inches)",
            text_color=Colors.WHITE,
            background_color=Colors.DARK_GRAY,
            font=pygame.font.SysFont("Arial", 12),
        )
        self.append_drawable_eventable(chest_height_label)

        # Add the buttons to the toolbar
        save_floorplan_button = UI.Button(
            parent=self,
            x_pos=0.066,
            y_pos=0,
            width=0.868,
            height=0.05,
            text="Save Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Save Floorplan"),
        )
        self.append_drawable_eventable(save_floorplan_button)

        load_floorplan_button = UI.Button(
            parent=self,
            x_pos=0.066,
            y_pos=0.05,
            width=0.40,
            height=0.05,
            text="Load Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Load Floorplan"),
        )
        self.append_drawable_eventable(load_floorplan_button)

        new_floorplan_button = UI.Button(
            parent=self,
            x_pos=0.532,
            y_pos=0.05,
            width=0.40,
            height=0.05,
            text="Create New Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Create New Floorplan"),
        )
        self.append_drawable_eventable(new_floorplan_button)

        add_chest_button = UI.Button(
            parent=self,
            x_pos=0.066,
            y_pos=0.10,
            width=0.40,
            height=0.05,
            text="Add Chest",
            border_thickness=2,
            rounded=True,
            action= lambda: self.add_chest( int(chest_width.text), int(chest_height.text) ),
        )
        self.append_drawable_eventable(add_chest_button)
