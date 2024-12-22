import pygame
import sys
import random
from game.agent import Agent
from game.infection_spread_logic import change_to_infected_logic, change_to_recovered_logic, change_to_dead_logic

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 60


clock = pygame.time.Clock()

interval = 2000  # czas w milisekundach (np. 2000 ms = 2 sekundy)
last_call = pygame.time.get_ticks()  # Zapisanie czasu początkowego

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pandemic Spread Simulation')

screen.fill(BLACK)

agents=[]


random.seed(10)
for i in range(100):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    age = random.randint(1, 100)
    agent = Agent(i,x,y, age, 'S',8)
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

    now = pygame.time.get_ticks()
    if now - last_call >= interval:  # Wykonuj co 2 sekundy
        for agent in agents:
            change_to_infected_logic(agent)
            # change_to_recovered_logic(agent)
            # change_to_dead_logic(agent)  # muszą mieć osobne odliczanie
        last_call = now

    for i, agent in enumerate(agents):
        agent.move()
        for agent2 in agents[i + 1:]:  # Porównuj tylko unikalne pary
            agent.collision_action(agent2)
            agent.check_exposure(agent2)
    for agent in agents:
        agent.draw(screen)


    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(FPS)

