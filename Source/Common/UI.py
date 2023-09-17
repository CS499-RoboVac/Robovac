import pygame

from Common import Colors
from Common import Fonts


# A parameterizable button class
class Button:
    # Constructor
    # @param x_pos: The x position of the button
    # @param y_pos: The y position of the button
    # @param width: The width of the button
    # @param height: The height of the button
    # @param text: The text of the button
    # @param font: The font of the button
    # @param color: The color of the button
    # @param hover_color: The color of the button when hovered over
    # @param click_color: The color of the button when clicked
    # @param border_thickness: Optional, the thickness of the border
    # @param rounded: Optional, whether or not the button should be rounded
    # @param action: The action to perform when the button is pressed
    def __init__(
        self,
        x_pos,
        y_pos,
        width,
        height,
        text,
        font=Fonts.button_font,
        base_color=Colors.LIGHT_GRAY,
        hover_color=Colors.LIGHT_BLUE,
        click_color=Colors.BLUE,
        border_thickness=0,
        rounded=False,
        action=lambda: print("Button pressed"),
    ):
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.text = font.render(text, True, (0, 0, 0))
        self.color = base_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.action = action
        self.border_radius = 0
        self.border_thickness = border_thickness
        self.rounded = rounded

    # Draw the button
    # @param canvas: The canvas to draw the button on
    def draw(self, canvas):
        active_color = self.color

        # Check if the button is being hovered over
        if self.is_hovered(pygame.mouse.get_pos()):
            active_color = self.hover_color
        else:
            active_color = self.color

        # Check if the button is being clicked
        if self.is_clicked(pygame.mouse.get_pos()) and not self.activated:
            self.activated = True
            self.action()

        # Check if the button is being released
        if self.is_released(pygame.mouse.get_pos()):
            self.activated = False

        # If the button is rounded, set the border radius
        if self.rounded:
            self.border_radius = 5
        else:
            self.border_radius = 0

        # Draw the button
        pygame.draw.rect(
            canvas,
            active_color,
            (self.x, self.y, self.width, self.height),
            border_radius=self.border_radius,
        )

        # If the button has a border, draw it
        if self.border_thickness > 0:
            pygame.draw.rect(
                canvas,
                (0, 0, 0),
                (
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                ),
                self.border_thickness,
                border_radius=self.border_radius,
            )

        # Draw the text
        canvas.blit(
            self.text,
            (
                self.x + (self.width / 2 - self.text.get_width() / 2),
                self.y + (self.height / 2 - self.text.get_height() / 2),
            ),
        )

    # Check if the button is being hovered over
    # @param mouse_pos: The position of the mouse
    # @return: True if the button is being hovered over, False otherwise
    def is_hovered(self, mouse_pos):
        return (
            self.x <= mouse_pos[0] <= self.x + self.width
            and self.y <= mouse_pos[1] <= self.y + self.height
        )

    # Check if the button is being clicked
    # @param mouse_pos: The position of the mouse
    # @return: True if the button is being clicked, False otherwise
    def is_clicked(self, mouse_pos):
        return self.is_hovered(mouse_pos) and pygame.mouse.get_pressed()[0]

    # Check if the button is being clicked
    # @param mouse_pos: The position of the mouse
    # @return: True if the button is being clicked, False otherwise
    def is_released(self, mouse_pos):
        return self.is_hovered(mouse_pos) and not pygame.mouse.get_pressed()[0]
