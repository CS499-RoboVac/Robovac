# The main toolbar on the top of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util, Furniture
import pygame

class TopBar(UI.ToolBar):

    def add_ui_elements():
        # Add the input boxes to the toolbar
        chest_width = UI.InputBox(
            x_pos=10,
            y_pos=110,
            width=100,
            height=30,
            number_only=True,
        )
        super().eventables.append(chest_width)
        super().drawables.append(chest_width)

        chest_height = UI.InputBox(
            x_pos=120, y_pos=110, width=100, height=30, number_only=True
        )
        super().eventables.append(chest_height)
        super().drawables.append(chest_height)

        # Labels for the input boxes
        chest_width_label = UI.TextBox(
            x_pos=10,
            y_pos=85,
            width=100,
            height=25,
            text="Chest Width (inches)",
            text_color=Colors.WHITE,
            background_color=Colors.DARK_GRAY,
            font=pygame.font.SysFont("Arial", 12),
        )
        super().drawables.append(chest_width_label)
        super().eventables.append(chest_width_label)

        chest_height_label = UI.TextBox(
            x_pos=120,
            y_pos=85,
            width=100,
            height=25,
            text="Chest Height (inches)",
            text_color=Colors.WHITE,
            background_color=Colors.DARK_GRAY,
            font=pygame.font.SysFont("Arial", 12),
        )
        self.text_boxes.append(chest_height_label)

        # Add the buttons to the toolbar
        save_floorplan_button = UI.Button(
            x_pos=10,
            y_pos=50,
            width=100,
            height=30,
            text="Save Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Save Floorplan"),
        )
        self.buttons.append(save_floorplan_button)

        load_floorplan_button = UI.Button(
            x_pos=120,
            y_pos=50,
            width=100,
            height=30,
            text="Load Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Load Floorplan"),
        )
        self.buttons.append(load_floorplan_button)

        new_floorplan_button = UI.Button(
            x_pos=10,
            y_pos=10,
            width=210,
            height=30,
            text="Create New Floorplan",
            border_thickness=2,
            rounded=True,
            action=lambda: print("Create New Floorplan"),
        )
        self.buttons.append(new_floorplan_button)

    add_ui_elements()
