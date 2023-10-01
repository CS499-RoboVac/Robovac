#
#   fileIO.py
#   Author: Ryan Corob (rac0026@uah.edu)
#   Date Created: 10 September 2023
#   This file contains the structure for importing/exporting map layouts.
#

import floorTile
import json


def NewBlankFloor(SideLength):
    floorPlan = dict()
    for x in range(0, SideLength):
        for y in range(0, SideLength):
            floorPlan[(x, y)] = floorTile.floorTile()
    return floorPlan

def exportFloorPlan(floorPlan, fileName):
    with open(fileName, "w") as fid:
        for k, v in floorPlan.items():
            fid.write(f"{k[0]} {k[1]} {v.dirtiness} {v.carpetType} {v.parentRoomName}\n")#parentRoomName being at the end is important; when I split these I'm going to use "everything after the Nth entry" as name so spaces work

def importFloorPlan(fileName):
    floorPlan = dict()
    with open(fileName, 'r') as fid:
        for line in fid.readlines():
            k1, k2, dirt, carp, name = line.split(" ", 4)# split 4 times, peeling the 4 initial items off and leaving ewveryhting else as "name"
            floorPlan[(int(k1), int(k2))] = floorTile.floorTile(dirtiness=float(dirt), carpetType=int(carp), parentRoomName=name.strip())
    return floorPlan
