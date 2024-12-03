import pygame.math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)

class Agent:
    def __init__(self, id, x, y, age, health_state):
        self.id = id
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 3
        self.age = age
        self.health_state = health_state

    def choose_random_direction(self):
        random_direction = random.randint(0, 359)
        return random_direction

    def calculate_movement_vector(self):
        direction = self.choose_random_direction()
        vector = pygame.math.Vector2(self.x, self.y).rotate(direction)
        print('Vector: ',vector)
        return vector

    def move(self):
        self.position += self.direction * self.speed
        if self.position.x <= 0:
            self.direction.x *= -1
            self.position.x = 0
        elif self.position.x >= SCREEN_WIDTH:
            self.direction.x *= -1
            self.position.x = SCREEN_WIDTH

        if self.position.y <= 0:
            self.direction.y *= -1
            self.position.y = 0
        elif self.position.y >= SCREEN_HEIGHT:
            self.direction.y *= -1
            self.position.y = SCREEN_HEIGHT

    def draw(self,screen):
        pygame.draw.circle(screen, GREEN, (int(self.position.x), int(self.position.y)), 4)
