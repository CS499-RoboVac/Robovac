import random


class BiasedRandomAI:
    def update(self, isColliding: bool):
        return (random.uniform(-0.5, 1), random.uniform(-1, 1))
