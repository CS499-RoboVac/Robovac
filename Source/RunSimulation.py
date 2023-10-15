import pygame
import tkinter as tk

import Common.Colors as Colors
import Common.Fonts as Fonts
import Common.Util as Util
import Common.UI as UI
# import FloorPlanDesigner.TopBar as TopBar
import Simulation.SideBar as SideBar


def run():
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

    screen_resolution = canvas.get_size()

    # Title the window
    pygame.display.set_caption(f"Simulation {version}")
    exit = False

    # Create the top bar
    # topbar = TopBar.TopBar(
    #     canvas=canvas,
    #     x_pos=0,
    #     y_pos=0,
    #     width=1,
    #     height=0.075,
    # )
    # drawables.append(topbar)
    # eventables.append(topbar)

    # Create the toolbar
    sideBar = SideBar.SideBar(
        canvas=canvas,
        x_pos=0,
        y_pos=0.071,
        width=0.2,
        height=0.93,
    )
    drawables.append(sideBar)
    eventables.append(sideBar)

    while not exit:
        canvas.fill(Colors.WHITE)
        # draw the drawables
        for drawable in drawables:
            drawable.draw(canvas, screen_resolution)

        for event in pygame.event.get():
            # handle the eventables

            if event.type == pygame.QUIT:
                exit = True
            elif event.type == pygame.VIDEORESIZE:
                screen_resolution = (event.w, event.h)

                screen_resolution_list = list(screen_resolution)

                if screen_resolution_list[0] < 400:
                    screen_resolution = (400, screen_resolution[1])
                if screen_resolution_list[1] < 500:
                    screen_resolution = (screen_resolution[0], 500)

                # screen_resolution = tuple(screen_resolution_list)
                canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)
            for eventable in eventables:
                eventable.handle_events(event)
        pygame.display.update()


if __name__ == "__main__":
    run()
