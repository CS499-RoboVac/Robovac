# Utility functions

# Scale a single value with a min and max
# @param portion_of_screen: How much of the screen should the button take up?
# @param min: The minimum value the button can be
# @scale_value: The value to scale
# @param max: Optional, the maximum value the button can be
# @return: The scaled value
def scale_value(portion_of_screen, minimum_res, scale_value, maximum_res=None):
    scaled_value = scale_value * portion_of_screen
    if maximum_res is not None:
        scaled_value = min(scaled_value, maximum_res)
    if maximum_res is not None:
        return max(min(scaled_value, maximum_res), minimum_res)
    else:
        return max(scaled_value, minimum_res)
    