# The main toolbar on the left of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util, Furniture
import pygame


class LeftBar:
    # canvas: The canvas to draw the toolbar on
    # screen_resolution: The resolution of the screen
    def __init__(self, canvas, screen_resolution):
        self.canvas = canvas
        self.screen_resolution = screen_resolution
        self.height = screen_resolution[1]
        self.width = 230
        self.x_pos = 0
        self.y_pos = 0

        # Lists of ui elements
        self.buttons = []
        self.input_boxes = []
        self.text_boxes = []
        self.furniture = []

        # Add the input boxes to the toolbar
        chest_width = UI.InputBox(
            x_pos=10,
            y_pos=110,
            width=100,
            height=30,
            number_only=True,
        )
        self.input_boxes.append(chest_width)

        chest_height = UI.InputBox(
            x_pos=120, y_pos=110, width=100, height=30, number_only=True
        )
        self.input_boxes.append(chest_height)

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
        self.text_boxes.append(chest_width_label)

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

        # Draw the title
        title = Fonts.title_font.render("Floor Plan Designer", True, Colors.WHITE)
        self.canvas.blit(title, (10, 10))

       
        


    # Function to draw the toolbar
    # Called every frame by the main application loop
    def draw(self, screen_resolution):
        # Update the screen resolution
        self.screen_resolution = screen_resolution
        # Draw the EditBar background
        pygame.draw.rect(
            self.canvas,
            Colors.DARK_GRAY,
            (
                0,
                50,
                230,
                self.screen_resolution[1] - 50,
            ),
        )

        # Draw the buttons
        for button in self.buttons:
            button.draw(self.canvas)

        # Draw the labels
        for text_box in self.text_boxes:
            text_box.draw(self.canvas)

        # Draw the text boxes
        for text_box in self.input_boxes:
            text_box.draw(self.canvas)

        # Draw the furniture
        for furniture in self.furniture:
            furniture.draw(self.canvas)

    # Handle events for components in the toolbar
    # event: The event to handle
    def handle_events(self, event):
        for text_box in self.input_boxes:
            text_box.handle_events(event)
