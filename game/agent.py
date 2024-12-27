import pygame.math
import random
import pygame.sprite
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)


class Agent:
    def __init__(self, id, x, y, age, health_state,radius,infection_distance):
        self.id = id
        self.x = x
        self.y = y
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.speed = 0.3
        self.age = age
        self.health_state = health_state
        self.color = GREEN
        self.radius = radius
        self.infection_radius = radius + infection_distance

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
        if distance <= 2 * self.radius:
            self.direction.x *= -1
            dot2.direction.x *= -1
            self.direction.y *= -1
            dot2.direction.y *= -1
            self.move()
            dot2.move()
            if self.health_state == 'I' and dot2.health_state == 'S':
                dot2.health_state = 'E'
                dot2.change_color()
            if dot2.health_state == 'I' and self.health_state == 'S':
                self.health_state = 'E'
                self.change_color()

    def check_exposure(self, other):
        if self.health_state == 'I':
            distance = self.position.distance_to(other.position)
            if self.radius < distance <= self.infection_radius:
                other.change_health_state('E')


    def change_health_state(self, state):
        self.health_state = state
        self.change_color()

    def change_color(self):
        match self.health_state:
            case 'S':
                self.color = GREEN
            case 'I':
                self.color = RED
            case 'E':
                self.color = YELLOW
            case 'R':
                self.color = BLUE
            case 'D':
                self.color = GRAY

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

        # Rysowanie strefy infekcji (opcjonalne, można zakomentować)
        # pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.infection_radius, 2)