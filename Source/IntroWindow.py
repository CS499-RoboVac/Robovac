# This intro window is the first window that the user sees when they open the program.
# It will give the user the option to open the Floor Plan Designer, the Simulator, or the view previus runs window.
# It uses the same UI elements as the other windows.

import pygame
import tkinter as tk

import Common.Colors as Colors
import Common.Fonts as Fonts
import Common.Util as Util
import Common.UI as UI

import RunFloorPlanDesigner as RunFloorPlanDesigner

import IntroWindow.Toolbar as Toolbar

from subprocess import Popen

version = "0.0.1"

# Get the screen size to make the canvas an appropriate size
tkRoot = tk.Tk()

# Drawables
drawables = []

# Eventables
eventables = []


def append_drawable_eventable(element):
    drawables.append(element)
    eventables.append(element)


# How much of the screen should the canvas take up on start?
start_size = 0.4
screen_resolution = (
    tkRoot.winfo_screenheight() * start_size,
    tkRoot.winfo_screenheight() * start_size,
)

# Initialize pygame
pygame.init()

# Create the Canvas
canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)

screen_resolution = canvas.get_size()


# Title the window
pygame.display.set_caption(f"RoboSim {version}")
exit = False


# Open the windows in a new process with popen
buttonFunctions = {
    "open_floorplan_designer": lambda: Util.open_floorplan_designer(),
    "open_simulator": lambda: print("Open Simulator"),
    "open_view_previous_runs": lambda: print("Open View Previous Runs"),
}


# Add the toolbar
toolbar = Toolbar.Toolbar(
    canvas,
    x_pos=0,
    y_pos=0,
    width=1,
    height=1,
    bg_color=Colors.DARK_GRAY,
    scale=True,
    buttonFunctions=buttonFunctions,
)
append_drawable_eventable(toolbar)


# Main loop
while not exit:
    canvas.fill(Colors.WHITE)
    # draw the drawables
    for drawable in drawables:
        drawable.draw(canvas, screen_resolution)

    for event in pygame.event.get():
        # handle the eventables
        for eventable in eventables:
            eventable.handle_events(event)

        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.VIDEORESIZE:
            screen_resolution = (event.w, event.h)
            canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)
    pygame.display.update()
