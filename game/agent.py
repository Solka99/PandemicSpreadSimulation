import pygame.math
import random
import pygame.sprite
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Agent:
    def __init__(self, id, x, y, age, health_state):
        self.id = id
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 0.3
        self.age = age
        self.health_state = health_state
        self.color = GREEN

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

    def collision_action(self,dot2):
        distance = math.sqrt((self.position.x - dot2.position.x) ** 2 + (self.position.y - dot2.position.y) ** 2)
        if distance <= 2 * 8:  # 4 to promień jednej kropki
            self.direction.x *= -1
            dot2.direction.x *= -1
            self.move()
            dot2.move()
            if self.health_state == 'I' and dot2.health_state == 'S':
                dot2.health_state = 'E'
                dot2.change_color()
            if dot2.health_state == 'I' and self.health_state == 'S':
                self.health_state = 'E'
                self.change_color()


    def change_color(self):
        match self.health_state:
            case 'S':
                self.color = GREEN
            case 'I':
                self.color = RED
            case 'E':
                self.color = BLUE

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 8)
