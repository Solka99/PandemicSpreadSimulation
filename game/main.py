import pygame
import sys
import random
from game.agent import Agent
from game.infection_spread_logic import change_to_infected_logic, change_to_recovered_logic, change_to_dead_logic
from game.plot import PlotManager
from ui_manager import UIManager

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
VACCINATION_MULTIPLIER = 0.61
INTERVAL = 100  # milliseconds

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pandemic Spread Simulation')

ui_manager = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT)
user_settings = ui_manager.show_menu(screen)
print(f"Ustawienia użytkownika: {user_settings}")

agent_population = user_settings['population']
infection_distance = user_settings['infection_distance']
vaccinated_agents_number = user_settings['vaccinated_agents_number']

screen.fill(BLACK)

agents = []
last_call = pygame.time.get_ticks()


random.seed(10)
vaccinated_counter = vaccinated_agents_number
for i in range(agent_population):
    while True:
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        age = random.randint(1, 100)
        incubation_time = random.randint(3100, 12000)
        recovery_time = random.randint(4500, 15800)
        agent = Agent(i, x, y, age, 'S', True if vaccinated_counter > 0 else False, 8, infection_distance, incubation_time, recovery_time)
        vaccinated_counter -= 1
        if i == 0:
            agent.was_infected = True
            agent.infected_time = pygame.time.get_ticks()
            agent.health_state = 'I'
            agent.change_color()

        no_collision = True
        for a2 in agents:
            distance = agent.position.distance_to(a2.position)
            if distance <= agent.radius + a2.radius:
                no_collision = False
                break

        # Jeśli brak kolizji, dodaj agenta do listy
        if no_collision:
            agents.append(agent)
            break

for agent in agents:
    agent.draw(screen)

pygame.display.update()

plot_manager = PlotManager()
plot_manager.run_in_thread(agents)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = pygame.time.get_ticks()
    if now - last_call >= INTERVAL:  # Wykonuj co 2 sekundy
        for i, agent in enumerate(agents):
            if agent.health_state == 'S' or agent.health_state == 'R' or agent.health_state == 'D':
                continue

            if agent.health_state == 'E':
                if agent.was_exposed and now - agent.exposed_time > agent.incubation_time:
                    agent.health_state = 'I'
                    agent.change_color()
                    agent.was_infected = True
                    agent.infected_time = now

            if agent.health_state == 'I':
                for j, agent2 in enumerate(agents):
                    if j == i:
                        continue
                    if agent2.health_state == 'S':
                        if agent2.get_distance(agent) <= agent2.infection_radius:
                            infection_probability = 1 / ((agent2.get_distance(agent))/10) * (VACCINATION_MULTIPLIER if agent2.vaccinated else 1)
                            random_value = random.random()

                            if random_value < infection_probability:
                                agent2.health_state = 'E'
                                agent2.change_color()
                                agent2.was_exposed = True
                                agent2.exposed_time = now

                if agent.was_infected and now - agent.infected_time > agent.recovered_time:

                    death_probability = 0
                    agent_age = agent.age
                    if 10 <= agent_age <= 39:
                        death_probability = 0.002
                    elif 40 <= agent_age <= 49:
                        death_probability = 0.004
                    elif 50 <= agent_age <= 59:
                        death_probability = 0.013
                    elif 60 <= agent_age <= 69:
                        death_probability = 0.036
                    elif 70 <= agent_age <= 79:
                        death_probability = 0.08
                    elif 80 <= agent_age <= 100:
                        death_probability = 0.15

                    random_value = random.random()

                    if random_value < death_probability:
                        agent.health_state = 'D'
                        agent.change_color()
                    else:
                        agent.health_state = 'R'
                        agent.change_color()

        last_call = now

    for i, agent in enumerate(agents):
        if agent.health_state != 'D':
            agent.move()

        for agent2 in agents[i + 1:]:  # Porównuj tylko unikalne pary
            agent.collision_action(agent2)

    for agent in agents:
        agent.draw(screen)

    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(FPS)
