from Common.Util import Vec2
import math
class Rectangle:
    def __init__(self, minCorner: Vec2, maxCorner: Vec2, exclusion: bool):
        self.minCorner = minCorner
        self.maxCorner = maxCorner
        self.exclusion = exclusion

    def BoundingBox(self):
        return (self.minCorner, self.maxCorner)

    def isValid(self,point : Vec2):
        """Checks to see if point is inside of the rectangle, returns inverted result if the rectangle is an exclusion primitive
        point: Vec2
        returns: boolean
        """
        inside = point.x > self.minCorner.x and point.y > self.minCorner.y and point.x < self.maxCorner.x and point.y < self.maxCorner.y
        return inside^self.exclusion # ^ is XOR (inverts result if exclusion is true)

class Circle:
    def __init__(self, center: Vec2, radius : float, exclusion: bool):
        self.center = center
        self.radius = radius
        self.exclusion = exclusion

    def BoundingBox(self): 
        #returns vec2s representing the top left and bottom right corners of the bounds of the shape
        diag = Vec2(self.radius, self.radius)
        return (self.center-diag, self.center+diag)

    def isValid(self,point : Vec2):
        """Checks to see if point is inside of the circle, returns inverted result if the circle is an exclusion primitive
        point: Vec2
        returns: boolean
        """
        inside = (self.center-point).length()<self.radius
        return inside^self.exclusion # ^ is XOR (inverts result if exclusion is true)

def PrimitiveInclusion(shapes,point):
    """function that inputs a list of primitive shapes and a point and returns true if the point in a valid zone for all primitives in the list
    point: Vec2
    shapes: list<shapes>
    return: boolean"""
    return all([primitive.isValid(point) for primitive in shapes])
    
# TODO: make this work with the new robot class, also this will probably need to be changed and or moved to the floorplan class once that exists
def Collision(pos: Vec2, r: float, FloorPlan: dict):
    """function that takes a position and radius, and a floorplan dict, returns True if a collision happens or False if the position is clear
    pos : Vec2 of the vacuum's position,
    r : float radius of the vacuum,
    FloorPlan : dict with entries of the form (int, int): FloorTile"""

    for x in range(math.floor(pos.x - r), math.ceil(pos.x + r) + 1):
        for y in range(math.floor(pos.y - r), math.ceil(pos.y + r) + 1):
            if (
                Vec2(x, y) - pos
            ).length() < r:  # we looped over a square; now we're using the ones within a radius in that square
                if not (x, y) in FloorPlan:
                    return True  # there was a collision
    return False  # no collisions, we can go onwards
