import random


class BiasedRandomAI:
    def update(self, isColliding: bool, dT : float):
        """ takes in the normal inputs for an AI: bool for if collision occurred on the last frame, and float for what fraction of a second has elapsed since last frame
            returns two values: the percentage of full forwards speed to use, and the percentage of turn speed to use
        """ 
        return (random.uniform(-0.5, 1), random.uniform(-1, 1))
