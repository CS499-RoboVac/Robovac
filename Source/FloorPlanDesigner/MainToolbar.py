# The main toolbar on the left of the FloorPlanDesigner

from Common import Colors, Fonts, UI, Util
import pygame

class MainToolbar:
    # @param canvas: The canvas to draw the toolbar on
    # @param screen_resolution: The resolution of the screen
    def __init__(self, canvas, screen_resolution):
        self.canvas = canvas
        self.screen_resolution = screen_resolution

        # List of buttons
        self.buttons = []

        # Add a button to the toolbar
        testButton = UI.Button(10, 10, 100, 50, "Test", Fonts.button_font, Colors.GRAY, Colors.DARK_GRAY, lambda: print("Test"))
        self.buttons.append(testButton)

        # Draw the title
        title = Fonts.title_font.render("Floor Plan Designer", True, Colors.WHITE)
        self.canvas.blit(title, (10, 10))

    # Function to draw the toolbar
    # Called every frame by the main application loop
    def draw(self):
        # Draw the toolbar
        pygame.draw.rect(self.canvas, Colors.LIGHT_GRAY, (0, 0, Util.scale_value(0.2, 200, self.screen_resolution[0], 400), self.screen_resolution[1]))

        # Draw the buttons
        for button in self.buttons:
            button.draw(self.canvas)

