import pygame
import abc

from Common import Colors
from Common import Fonts


class scalable:
    # Constructor
    def __init__(self, parent, x_pos, y_pos, width, height, scale=True):
        self.parent = parent
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.scale = scale
        if isinstance(self.parent, scalable):
            self.parent_resolution = self.parent.get_resolution()
        else:
            # If the parent is not a scalable, it is the pygame display
            self.parent_resolution = self.parent.get_size()

    # get_width: used to generate a width relative to the parent
    # Use this instead of hardcoding the width of a drawable
    def get_width(self):
        if self.scale:
            return self.width * self.parent_resolution[0]
        else:
            return self.width

    # get_height: used to generate a height relative to the parent
    # Use this instead of hardcoding the height of a drawable
    def get_height(self):
        if self.scale:
            return self.height * self.parent_resolution[1]
        else:
            return self.height

    # get_x: used to generate an x position relative to the parent
    # Use this instead of hardcoding the x position of a drawable
    def get_x(self):
        if self.scale:
            if isinstance(self.parent, scalable):
                return (self.x * self.parent.get_width()) + self.parent.get_x()
            else:
                return self.x * self.parent_resolution[0]
        return self.x

    # get_y: used to generate a y position relative to the parent
    # Use this instead of hardcoding the y position of a drawable
    def get_y(self):
        if self.scale:
            if isinstance(self.parent, scalable):
                return (self.y * self.parent.get_height()) + self.parent.get_y()
            else:
                return self.y * self.parent_resolution[1]
        return self.y

    # get_resolution: used to get the resolution of the drawable
    def get_resolution(self):
        return (self.get_width(), self.get_height())

    # Handle updating the drawable's size when the screen is resized
    def handle_events(self, event):
        if event.type == pygame.VIDEORESIZE:
            # If the parent is a scalable, get the parent's resolution
            if isinstance(self.parent, scalable):
                self.parent_resolution = self.parent.get_resolution()
            else:
                # If the parent is not a scalable, it is the pygame display
                self.parent_resolution = self.parent.get_size()


# A parameterizable button class
class Button(scalable):
    # Constructor
    # x_pos: The x position of the button
    # y_pos: The y position of the button
    # width: The width of the button
    # height: The height of the button
    # text: The text of the button
    # font: The font of the button
    # color: The color of the button
    # hover_color: The color of the button when hovered over
    # click_color: The color of the button when clicked
    # border_thickness: Optional, the thickness of the border
    # rounded: Optional, whether or not the button should be rounded
    # action: The action to perform when the button is pressed
    def __init__(
        self,
        parent,
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
        scale=True,
    ):
        super().__init__(parent, x_pos, y_pos, width, height, scale)
        self.text = font.render(text, True, (0, 0, 0))
        self.color = base_color
        self.base_color = base_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.action = action
        self.border_radius = 0
        self.border_thickness = border_thickness
        self.rounded = rounded
        self.activated = False

    # Draw the button
    # canvas: The canvas to draw the button on
    def draw(self, canvas):
        active_color = self.color

        # Check if the button is being hovered over
        if self.is_hovered(pygame.mouse.get_pos()):
            active_color = self.hover_color
        else:
            active_color = self.color

        # If the button is rounded, set the border radius
        if self.rounded:
            self.border_radius = 5
        else:
            self.border_radius = 0

        # Draw the button
        pygame.draw.rect(
            canvas,
            active_color,
            (self.get_x(), self.get_y(), self.get_width(), self.get_height()),
            border_radius=self.border_radius,
        )

        # If the button has a border, draw it
        if self.border_thickness > 0:
            pygame.draw.rect(
                canvas,
                (0, 0, 0),
                (
                    self.get_x(),
                    self.get_y(),
                    self.get_width(),
                    self.get_height(),
                ),
                self.border_thickness,
                border_radius=self.border_radius,
            )

        # Draw the text
        canvas.blit(
            self.text,
            (
                self.get_x() + (self.get_width() / 2 - self.text.get_width() / 2),
                self.get_y() + (self.get_height() / 2 - self.text.get_height() / 2),
            ),
        )

    # Handle events for the button
    # event: The pygame event to handle
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(event.pos):
                self.color = self.click_color
                self.activated = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.activated:
                self.color = self.hover_color
                self.activated = False
                self.action()
        elif event.type == pygame.MOUSEMOTION:
            if self.is_hovered(event.pos):
                self.color = self.hover_color
            else:
                self.color = self.base_color

    # Check if the button is being hovered over
    # mouse_pos: The position of the mouse
    # @return: True if the button is being hovered over, False otherwise
    def is_hovered(self, mouse_pos):
        return (
            self.get_x() <= mouse_pos[0] <= self.get_x() + self.get_width()
            and self.get_y() <= mouse_pos[1] <= self.get_y() + self.get_height()
        )


# A parameterizable text input box class
class InputBox(scalable):
    def __init__(
        self,
        parent,
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
        scale=True,
    ):
        super().__init__(parent, x_pos, y_pos, width, height, scale)
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

    # The maximum number of characters that can be entered into the text box
    def get_max_chars(self):
        # Calculate the maximum number of characters that can fit in the text box
        return max(int(self.get_width() / self.font.size("a")[0]) - 3, 1)

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            rect = pygame.Rect(
                self.get_x(), self.get_y(), self.get_width(), self.get_height()
            )

            if rect.collidepoint(event.pos):
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
                    if len(self.text) < self.get_max_chars() and (
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

        rect = pygame.Rect(
            self.get_x(), self.get_y(), self.get_width(), self.get_height()
        )

        # Draw the background of the input box.
        pygame.draw.rect(screen, self.background_color, rect, 0)
        # Draw the text.
        screen.blit(self.txt_surface, (rect.x + 5, rect.y + 5))
        # Draw the border
        pygame.draw.rect(screen, self.border_color, rect, 2)

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
    # text: The text to set the text box's text to
    def set_text(self, text):
        self.text = text
        self.txt_surface = self.font.render(self.text, True, self.border_color)


# A parameterizable text display box class
class TextBox(scalable):
    def __init__(
        self,
        parent,
        x_pos,
        y_pos,
        width,
        height,
        background_color=Colors.LIGHT_GRAY,
        text_color=Colors.BLACK,
        font=Fonts.text_box_font,
        border_thickness=0,
        text="",
        scale=True,
    ):
        super().__init__(parent, x_pos, y_pos, width, height, scale)
        self.rect = pygame.Rect(
            self.get_x(), self.get_y(), self.get_width(), self.get_height()
        )
        self.text_color = text_color
        self.background_color = background_color
        self.font = font
        self.border_thickness = border_thickness
        self.text = text
        self.txt_surface = font.render(text, True, self.text_color)

    def draw(self, screen):
        self.rect = pygame.Rect(
            self.get_x(), self.get_y(), self.get_width(), self.get_height()
        )
        # Draw the background of the input box.
        pygame.draw.rect(screen, self.background_color, self.rect, 0)
        # Draw the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the border
        if self.border_thickness > 0:
            pygame.draw.rect(screen, self.text_color, self.rect, self.border_thickness)

    # Update the text box's text
    def update_text(self, new_text):
        self.text = new_text
        # Re-render the text
        self.txt_surface = self.font.render(self.text, True, self.text_color)

    # Update the text box's color
    def update_color(self, new_color):
        self.text_color = new_color
        # Re-render the text
        self.txt_surface = self.font.render(self.text, True, self.text_color)

    # Get the text box's text
    # @return: The text box's text
    def get_text(self):
        return self.text


# A toolbar class
# This class has drawables and eventables
# TODO: Add "Button params" to the constructor.
# This will be a list of tuples that contain the parameters for each button.
# It will be optional, and if it is not provided,
# the buttons will use their default parameters, or parameters that are provided on a per-button basis
# If scale is true, width and height will be percentages of the screen resolution
# If scale is false, width and height will be the actual width and height of the toolbar in pixels
class ToolBar(scalable):
    # Constructor
    def __init__(
        self,
        parent,
        x_pos,
        y_pos,
        width,
        height,
        bg_color=Colors.DARK_GRAY,
        scale=True,
    ):
        super().__init__(parent, x_pos, y_pos, width, height, scale)

        self.bg_color = bg_color
        # Drawables and eventables are lists of objects that are drawn and have events handled
        # Their draw and handle_events functions are passed into the main application loop
        # Their draw functions are passed the canvas, and optionally the screen resolution
        # Their handle_events functions are passed the event
        self.drawables = []
        self.eventables = []

    # Handle events for components in the toolbar
    # event: The event to handle
    def handle_events(self, event):
        super().handle_events(event)

        # Handle events for eventables
        for eventable in self.eventables:
            eventable.handle_events(event)

    # Draw the toolbar, and all of its drawables
    def draw(self, canvas, parent):
        # Draw the toolbar background

        pygame.draw.rect(
            canvas,
            self.bg_color,
            (
                self.get_x(),
                self.get_y(),
                self.get_width(),
                self.get_height(),
            ),
        )

        # Draw the drawables
        for drawable in self.drawables:
            try:
                drawable.draw(canvas)
            except AttributeError:
                drawable.draw(canvas, parent)
