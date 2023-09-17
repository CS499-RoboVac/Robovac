import pygame
import tkinter as tk

import Common.Colors as Colors
import Common.Fonts as Fonts
import Common.UI as UI
import FloorPlanDesigner.MainToolbar as MainToolbar


version = "0.0.1"

# Get the screen size to make the canvas an appropriate size
tkRoot = tk.Tk()

# How much of the screen should the canvas take up on start?
start_size = 0.6
screen_resolution = (tkRoot.winfo_screenwidth() * start_size, tkRoot.winfo_screenheight() * start_size)

# Initialize pygame
pygame.init()

# Create the Canvas
canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)

# Title the window
pygame.display.set_caption(f"Floor Plan Designer {version}")
exit = False

# Create the toolbar
toolbar = MainToolbar.MainToolbar(canvas, screen_resolution)


while not exit:
	canvas.fill(Colors.WHITE)
	toolbar.draw()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True
		elif event.type == pygame.VIDEORESIZE:
			screen_resolution = (event.w, event.h)
			canvas = pygame.display.set_mode(screen_resolution, pygame.RESIZABLE)
	pygame.display.update()
