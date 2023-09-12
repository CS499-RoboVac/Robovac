#
#   fileIO.py
#   Author: Ryan Corob (rac0026@uah.edu)
#   Date Created: 10 September 2023
#   This file contains the structure for importing/exporting map layouts.
#

import floorTile
import json

map = dict()
for x in range(0, 2000):
    for y in range(0, 800):
        map[(x, y)] = floorTile

def exportFloorPlan(floorPlan, fileName):
    with open(fileName, 'w') as fid:
        json.dump(floorPlan, fid)

exportFloorPlan(map, 'testMap.json')