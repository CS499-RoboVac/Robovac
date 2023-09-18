# The main toolbar on the left of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util
import pygame


class MainToolbar:
    # @param canvas: The canvas to draw the toolbar on
    # @param screen_resolution: The resolution of the screen
    def __init__(self, canvas, screen_resolution):
        self.canvas = canvas
        self.screen_resolution = screen_resolution

        # Lists of ui elements
        self.buttons = []
        self.text_boxes = []

        # Add the text boxes to the toolbar
        test_text_box = UI.InputBox(
            x_pos=10,
            y_pos=100,
            width=210,
            height=30,
            number_only=True,
        )
        self.text_boxes.append(test_text_box)

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
        # Draw the toolbar
        pygame.draw.rect(
            self.canvas,
            Colors.DARK_GRAY,
            (
                0,
                0,
                230,
                self.screen_resolution[1],
            ),
        )

        # Draw the buttons
        for button in self.buttons:
            button.draw(self.canvas)

        # Draw the text boxes
        for text_box in self.text_boxes:
            text_box.draw(self.canvas)

    # Handle events for components in the toolbar
    # @param event: The event to handle
    def handle_events(self, event):
        for text_box in self.text_boxes:
            text_box.handle_event(event)
