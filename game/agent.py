import pygame.math
import random

class Agent:
    def __init__(self, id, x, y, age,  health_state):
        self.id = id
        self.x = x
        self.y = y
        self.position = (x, y)
        self.movement_vector = self.calculate_movement_vector()
        # self.direction = self.choose_random_direction()
        self.age = age
        self.health_state = health_state

    def choose_random_direction(self):
        random_direction = random.randint(0, 360)
        return random_direction

    def calculate_movement_vector(self):
        direction = self.choose_random_direction()
        vector = pygame.math.Vector2(self.x, self.y).rotate(direction)
        return vector

    def calculate_position(self):
        movement_vector = self.calculate_movement_vector()
        self.x += movement_vector[0]
        self.y += movement_vector[1]
        return self.x, self.y

    def draw(self,screen,color):
        pygame.draw.circle(screen, color, (self.position[0], self.position[1]), 4)
