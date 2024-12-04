import pygame
import sys
import random
from game.agent import Agent

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 60


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
    if i==0:
        agent.health_state='I'
        agent.change_color()
    agents.append(agent)
    agent.draw(screen)

pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for agent in agents:
        agent.move()
        for agent2 in agents[1:]:
            agent.collision_action(agent2)

    for agent in agents:
        agent.draw(screen)


    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(FPS)

