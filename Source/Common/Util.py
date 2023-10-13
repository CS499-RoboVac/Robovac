# Utility functions
from subprocess import Popen

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
    
def open_floorplan_designer():
    Popen(
        ["python", "Source/RunFloorPlanDesigner.py"]
    )
    # close the current window
    exit()

def open_intro_window(close_current=True):
    Popen(
        ["python", "Source/IntroWindow.py"]
    )
    # close the current window
    if close_current:
        exit()
