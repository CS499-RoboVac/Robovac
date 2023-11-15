import random
from enum import Enum
import Common.Robot as Robot
from Common.Util import Vec2

from math import sin, cos, pi, sqrt, atan2


class Turner:
    def __init__(self, goal, speed):
        self.speed = speed
        self.goal = goal
        self.sign = goal / abs(goal)
        self.progress = 0
        self.lastdT = 0

    # return tuple of (DoneTurning, steering)
    def Turn(self, dT):
        self.progress += self.sign * self.lastdT * self.speed
        if abs(self.progress) > abs(self.goal):
            return (True, None)
        self.lastdT = dT
        return (False, (0, self.sign))


class SnakeAI:
    class State(Enum):
        Long = 0
        Turning = 1
        Short = 2

    def __init__(self, robit: Robot):
        self.state = self.State.Turning
        self.robot = robit
        self.TimeShort = 0
        self.turnDir = 1
        self.TurnHelp = Turner(pi/8, self.robot.maxTurn)

    def update(self, isColliding: bool, dT: float):
        """takes in the normal inputs for an AI: bool for if collision occurred on the last frame, and float for what fraction of a second has elapsed since last frame
        returns two values: the percentage of full forwards speed to use, and the percentage of turn speed to use
        """
        if isColliding:
            if self.state == self.State.Long:
                self.turnDir *= -1
            self.TimeShort = 0
            self.state = self.State.Turning
            self.TurnHelp = Turner(pi / 2.1 * self.turnDir, self.robot.maxTurn)
        if self.state == self.State.Long:
            return (1, 0)
        elif self.state == self.State.Turning:
            end, out = self.TurnHelp.Turn(dT)
            if end:
                self.state = [self.State.Short, self.State.Long][self.TimeShort != 0]
                return (0, 0)
            else:
                return out
        elif self.state == self.State.Short:
            self.TimeShort += dT
            if self.TimeShort > self.robot.diameter / self.robot.maxSpeed:
                self.state = self.State.Turning
                self.TurnHelp = Turner(pi / 2.1 * self.turnDir, self.robot.maxTurn)

            return (1, 0)


class BiasedRandomAI:
    def __init__(self, robit: Robot):
        pass

    def update(self, isColliding: bool, dT: float):
        """takes in the normal inputs for an AI: bool for if collision occurred on the last frame, and float for what fraction of a second has elapsed since last frame
        returns two values: the percentage of full forwards speed to use, and the percentage of turn speed to use
        """

        return (random.uniform(-0.5, 1), random.uniform(-0.5, 1))


class RandomBounceAI:
    class State(Enum):
        Going = 0
        Turning = 1

    def __init__(self, robit: Robot):
        self.state = self.State.Going

        self.robot = robit
        self.TurnHelp = None

    def update(self, isColliding: bool, dT: float):
        if self.state == self.State.Going:
            if isColliding:
                self.TurnHelp = Turner(
                    (random.random() - 0.5) * 2 * pi, self.robot.maxTurn
                )
                self.state = self.State.Turning
                return (0, 0)
            else:
                return (1, 0)
        elif self.state == self.State.Turning:
            end, out = self.TurnHelp.Turn(dT)
            if end:
                self.state = self.State.Going

                return (0, 0)
            else:
                return out


class SpiralAI:
    class State(Enum):
        Linear = 0
        Turning = 1
        Spiraling = 2

    def __init__(self, robit: Robot):
        self.state = self.State.Spiraling

        self.robot = robit
        self.TurnHelp = None
        self.SpiralTimer = 0
        self.LinearCountdown = 0
        self.dir = 0

    def GoSpiral(self):
        self.SpiralTimer=0
        self.state = self.State.Spiraling
        self.dir=0

    def update(self, isColliding: bool, dT: float):
        if self.state == self.State.Linear:
            if isColliding:
                self.TurnHelp = Turner(
                    (random.random() - 0.5) * 2 * pi, self.robot.maxTurn
                )
                self.state = self.State.Turning
                return (0, 0)
            if random.random() < 0.01:
                self.GoSpiral()
                return (0, 0)
            return (1, 0)
        elif self.state == self.State.Turning:
            end, out = self.TurnHelp.Turn(dT)
            if end:
                self.state = self.State.Linear
                return (0, 0)
            else:
                return out
        elif self.state == self.State.Spiraling:
            if isColliding:
                self.TurnHelp = Turner(
                    (random.random() - 0.5) * 2 * pi, self.robot.maxTurn
                )
                self.state = self.State.Turning

                return (0, 0)
            
            d = self.robot.diameter
            t = self.SpiralTimer
            
            vel = self.robot.maxSpeed*dT
            # Don't worry about the 628, it's a magic number
            dθ=min((628 * vel/d)/max(self.dir*(d/(2*pi)), 0.001),self.robot.maxTurn)
            self.dir += min(dθ,self.robot.maxTurn)*dT
            self.SpiralTimer += dT

            return (1, min(dθ/(self.robot.maxTurn),1))
