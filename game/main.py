import pygame
import sys
import random
from game.agent import Agent
from sim import BLACK

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 3
# agent_speed = 5

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pandemic Spread Simulation')

screen.fill(BLACK)

agents=[]

random.seed(10)
for i in range(100):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    age = random.randint(1, 100)
    agent = Agent(i,x,y, age, 'S')
    agents.append(agent)

    agent.draw(screen,GREEN)

pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for agent in agents:
        agent.position = agent.calculate_position()
        print(agent.position)
        agent.draw(screen,GREEN)
    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(FPS)

