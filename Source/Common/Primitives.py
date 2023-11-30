from Common.Util import Vec2
import math


class Rectangle:
    def __init__(
        self,
        minCorner: Vec2,
        maxCorner: Vec2,
        exclusion: bool,
        isTableTop: bool = False,
    ):
        self.minCorner = minCorner
        self.maxCorner = maxCorner
        self.exclusion = exclusion
        self.isTableTop = isTableTop

    def BoundingBox(self):
        return (self.minCorner, self.maxCorner)

    def isInside(self, point: Vec2):
        """Checks to see if point is inside of the rectangle, returns inverted result if the rectangle is an exclusion primitive
        point: Vec2
        returns: boolean
        """
        inside = (
            point.x >= self.minCorner.x
            and point.y >= self.minCorner.y
            and point.x <= self.maxCorner.x
            and point.y <= self.maxCorner.y
        )
        return inside

    def __eq__(self, o):
        if type(0) != type(self):
            return False
        return self.minCorner == o.minCorner and self.maxCorner == o.maxCorner

    def __hash__(self):
        return hash(
            (self.minCorner.x, self.minCorner.y, self.maxCorner.x, self.maxCorner.y)
        )

    def __and__(self, other):
        for pt in [
            self.minCorner,
            self.maxCorner,
            Vec2(self.minCorner.x, self.maxCorner.y),
            Vec2(self.maxCorner.x, self.minCorner.y),
        ]:
            if other.isInside(pt):
                return True
        return False


class Circle:
    def __init__(self, center: Vec2, radius: float, exclusion: bool):
        self.center = center
        self.radius = radius
        self.exclusion = exclusion

    def BoundingBox(self):
        # returns vec2s representing the top left and bottom right corners of the bounds of the shape
        diag = Vec2(self.radius, self.radius)
        return (self.center - diag, self.center + diag)

    def isInside(self, point: Vec2):
        """Checks to see if point is inside of the circle, returns inverted result if the circle is an exclusion primitive
        point: Vec2
        returns: boolean
        """
        inside = (self.center - point).length() < self.radius
        return inside


def PrimitiveInclusion(shapes, point):
    """function that inputs a list of primitive shapes and a point and returns true if the point in a valid zone for all primitives in the list
    point: Vec2
    shapes: list<shapes>
    return: boolean"""

    insideAnyInclusion = False
    outsideEveryExclusion = True
    for primitive in shapes:
        if primitive.isInside(point):
            if primitive.exclusion:
                outsideEveryExclusion = False
                break
            else:
                insideAnyInclusion = True

    return insideAnyInclusion and outsideEveryExclusion


def Collision(pos: Vec2, d: float, shapes: list):
    """function that takes a position and radius, and a floorplan dict, returns True if a collision happens or False if the position is clear
    pos : Vec2 of the vacuum's position,
    r : float radius of the vacuum,
    FloorPlan : dict with entries of the form (int, int): FloorTile"""

    maxDistance = 1  # Maximum distance between collision check points in cm
    n = int((math.pi * d) // maxDistance)
    points = [
        Vec2(
            math.cos((2 * math.pi / n) * i) * (d / 2) + pos.x,
            math.sin((2 * math.pi / n) * i) * (d / 2) + pos.y,
        )
        for i in range(n)
    ]

    return not all([PrimitiveInclusion(shapes, point) for point in points])
