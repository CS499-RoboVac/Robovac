#
#   floorTile.py
#   Author: Ryan Corob (rac0026@uah.edu)
#   Date Created: 08 September 2023
#   This file contains the class for the map's Floor Tiles.
#   These objects will be held my a Map dictionary, which holds
#       an x and y coordinate alongside this class
#

class floorTile():
    def __init__(self):
        self.dirtiness = 0.0
        self.carpetType = 0
        self.parentRoomName = 'Default Room'
        
    def clean(self, efficiency):
        #TO BE IMPLEMENTED
        1