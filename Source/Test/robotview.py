from Common.Robot import Robot



class robotmodel:
    # Constructor
    # x_pos: The x position of the robot
    # y_pos: The y position of the robot
    # diameter: The diameter of the robot in inches
    # whisker_length: The length of the whiskers on the robot
    # vaccum_width: The width of the vaccum on the robot
    def __init__(
        self,
        x_pos=0,
        y_pos=0,
        diameter=12.8,
        whisker_length=13.5,
        vaccum_width=5.8,
    ):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.diameter = diameter
        self.whisker_length = whisker_length
        self.whiskers = []
        self.vaccum_width = vaccum_width
        self.is_valid = True 