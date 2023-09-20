import pygame
import tkinter as tk

import Common.Colors as Colors
import Common.Fonts as Fonts
import Common.Util as Util
import Common.UI as UI
import FloorPlanDesigner.LeftBar as LeftBar
import FloorPlanDesigner.TopBar as TopBar


version = "0.0.1"

# Get the screen size to make the canvas an appropriate size
tkRoot = tk.Tk()

# Drawables
drawables = []

# Eventables
eventables = []

# How much of the screen should the canvas take up on start?
start_size = 0.6
screen_resolution = (
    tkRoot.winfo_screenwidth() * start_size,
    tkRoot.winfo_screenheight() * start_size,
)

# Initialize pygame
pygame.init()

# Create the Canvas
canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)

# Title the window
pygame.display.set_caption(f"Floor Plan Designer {version}")
exit = False

# Create the toolbar
#leftBar = LeftBar.LeftBar(canvas, screen_resolution)

testToolBar = TopBar.TopBar(
    screen_resolution=screen_resolution,
    x_pos=0,
    y_pos=0,
    width=0.2,
    height=1.0,
    scale=True,
    )
drawables.append(testToolBar)
eventables.append(testToolBar)


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
