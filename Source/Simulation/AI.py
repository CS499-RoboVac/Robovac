import random
import Robot


class SnakeAI:
    class State(Enum):
        Long = 0
        Turning = 1
        Short = 2

    def __init__(self, robit: Robot):
        self.state = Long
        self.robot = robit
        self.TimeTurning = 0
        self.TimeShort = 0
        self.turnDir = 1

    def update(self, isColliding: bool, dT: float):
        """takes in the normal inputs for an AI: bool for if collision occurred on the last frame, and float for what fraction of a second has elapsed since last frame
        returns two values: the percentage of full forwards speed to use, and the percentage of turn speed to use
        """
        if isColliding:
            if self.state == Long:
                self.turnDir *= -1
                self.TimeShort = 0
            self.state = Turning
            self.TimeTurning = -math.pi / (
                2 * self.robot.maxTurn
            )  # set the countdown for one quarter turn
        if self.state == Long:
            return (1, 0)
        elif self.state == Turning:
            self.TimeTurning += dT
            if self.TimeTurning > 0:
                self.state = [Short, Long](self.TimeShort != 0)
            return (0, turnDir)
        elif self.state == Short:
            self.TimeShort += dT
            if self.TimeShort > self.robot.diameter / self.robot.maxSpeed:
                self.state = Turning
                self.TimeTurning -= math.pi / (2 * self.robot.maxTurn)
            return (1, 0)


class BiasedRandomAI:
    def update(self, isColliding: bool, dT: float):
        """takes in the normal inputs for an AI: bool for if collision occurred on the last frame, and float for what fraction of a second has elapsed since last frame
        returns two values: the percentage of full forwards speed to use, and the percentage of turn speed to use
        """
        return (random.uniform(-0.5, 1), random.uniform(-1, 1))
