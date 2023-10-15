#
#   floorTile.py
#   Author: Ryan Corob (rac0026@uah.edu)
#   Date Created: 08 September 2023
#   This file contains the class for the map's Floor Tiles.
#   These objects will be held by a Map dictionary, which holds
#       an x and y coordinate alongside this class
#


class floorTile:
    def __init__(self, dirtiness=0.0, carpetType=0, parentRoomName="Default Room"):
        self.dirtiness = dirtiness
        self.carpetType = carpetType
        self.parentRoomName = parentRoomName

    def clean(self, efficiency):
        # TO BE IMPLEMENTED
        pass
