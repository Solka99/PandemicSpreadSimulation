import pygame.math
import random
class Agent:
    def __init__(self, id, x, y, age, health_state):
        self.id = id
        self.x = x
        self.y = y
        self.position = (x, y)
        self.direction = self.choose_random_direction()
        self.age = age
        self.health_state = health_state

    def choose_random_direction(self):
        random_direction = random.randint(0, 360)
        return random_direction

