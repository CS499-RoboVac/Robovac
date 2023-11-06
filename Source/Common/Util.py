# Utility functions
import math


# Scale a single value with a min and max
# portion_of_screen: How much of the screen should the button take up?
# min: The minimum value the button can be
# @scale_value: The value to scale
# max: Optional, the maximum value the button can be
# @return: The scaled value
def scale_value(portion_of_screen, minimum_res, scale_value, maximum_res=None):
    scaled_value = scale_value * portion_of_screen
    if maximum_res is not None:
        scaled_value = min(scaled_value, maximum_res)
    if maximum_res is not None:
        return max(min(scaled_value, maximum_res), minimum_res)
    else:
        return max(scaled_value, minimum_res)


class Vec2:
    def __init__(self, x, y=None):
        if isinstance(x, (tuple, list, Vec2)):
            if len(x) != 2:
                raise ValueError("Input tuple or list must have exactly 2 elements")
            self.x, self.y = x
        else:
            if y == None:
                raise ValueError(
                    "Vec2() takes 2 values or 1 list/tuple but only 1 was value was given"
                )
            self.x = x
            self.y = y

    # funky way of making the operator stuff smaller
    def selector(self, b, op):
        return (
            Vec2(op(self.x, b.x), op(self.y, b.y))
            if type(b) == Vec2
            else Vec2(op(self.x, b), op(self.y, b))
        )

    def __add__(self, b):
        return self.selector(b, lambda x, y: x + y)

    def __sub__(self, b):
        return self.selector(b, lambda x, y: x - y)

    def __mul__(self, b):
        return self.selector(b, lambda x, y: x * y)

    def __truediv__(self, b):
        return self.selector(b, lambda x, y: x / y)

    def __eq__(self, b):
        return type(b) == Vec2 and self.x == b.x and self.y == b.y

    # Allows for list like indexing, example Vec2(2,3)[0], returns 2
    def __getitem__(self, index):
        return self.y if index else self.x

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"

    def __len__(self):
        return 2

    def __iter__(self):
        return iter((self.x, self.y))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def unit(self):
        return self / math.sqrt(self.x**2 + self.y**2)

    def turn(self, Θ):
        new_x = self.x * math.cos(Θ) - self.y * math.sin(Θ)
        new_y = self.x * math.sin(Θ) + self.y * math.cos(Θ)
        return Vec2(new_x, new_y)
