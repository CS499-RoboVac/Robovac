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


# A parameterizable text input box class
class InputBox:
    def __init__(
        self,
        x_pos,
        y_pos,
        width,
        height,
        background_color_inactive=Colors.LIGHT_GRAY,
        background_color_active=Colors.WHITE,
        border_color_inactive=Colors.BLACK,
        border_color_active=Colors.BLACK,
        font=Fonts.text_box_font,
        text="",
        number_only=False,
    ):
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.border_color_inactive = border_color_inactive
        self.border_color_active = border_color_active
        self.border_color = border_color_inactive
        self.background_color_inactive = background_color_inactive
        self.background_color_active = background_color_active
        self.background_color = background_color_inactive
        self.font = font
        self.text = text
        self.number_only = number_only
        self.txt_surface = font.render(text, True, self.border_color)
        self.active = False
        self.key_pressed = False
        self.key_repeat_timer = 0
        self.held_key = None

        # Calculate the maximum number of characters that can fit in the text box
        self.max_chars = max(int(width / self.font.size("a")[0]) - 3, 1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.border_color = (
                self.border_color_active if self.active else self.border_color_inactive
            )
            self.background_color = (
                self.background_color_active
                if self.active
                else self.background_color_inactive
            )

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_chars and (
                        not self.number_only
                        or (self.number_only and event.unicode.isdigit())
                    ):
                        self.text += event.unicode

                # handle key being held down
                self.key_pressed = True
                self.key_repeat_timer = 0
                self.held_key = (event.key, event.unicode)

                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.border_color)

        # Keep removing characters until backspace is released
        if event.type == pygame.KEYUP:
            self.key_pressed = False

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    # Helper function to handle key being held down
    def handle_key_held(self):
        if self.key_pressed:
            self.key_repeat_timer += 1
            if self.key_repeat_timer > 400:
                self.key_repeat_timer = 350

                if self.held_key[0] != pygame.K_BACKSPACE:
                    if len(self.text) < self.max_chars and (
                        not self.number_only
                        or (self.number_only and self.held_key[1].isdigit())
                    ):
                        self.text += self.held_key[1]
                else:
                    self.text = self.text[:-1]
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.border_color)

    def draw(self, screen):
        # Handle key being held down
        self.handle_key_held()

        # Draw the background of the input box.
        pygame.draw.rect(screen, self.background_color, self.rect, 0)
        # Draw the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

    # Get the text box's text
    # @return: The text box's text
    def get_text(self):
        return self.text

    # Get the text box's text as an integer if it is a number
    # @return: The text box's text as an integer if it is a number, None otherwise
    def get_text_as_int(self):
        try:
            return int(self.text)
        except ValueError:
            return None

    # Set the text box's text
    # @param text: The text to set the text box's text to
    def set_text(self, text):
        self.text = text
        self.txt_surface = self.font.render(self.text, True, self.border_color)
