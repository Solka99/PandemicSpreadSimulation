import pygame
import sys
import random
from game.agent import Agent
from game.plot import PlotManager
from ui_manager import UIManager
from game.infection_spread_logic import handle_infection

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INTERVAL = 100  # milliseconds

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pandemic Spread Simulation')
clock = pygame.time.Clock()


def initialize_agents(settings):
    agents = []
    vaccinated_counter = settings['vaccinated_agents_number']
    random.seed(10)

    for i in range(settings['population']):
        while True:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            age = random.randint(1, 100)
            incubation_time = random.randint(3100, 12000)
            recovery_time = random.randint(4500, 15800)

            agent = Agent(i, x, y, age, 'S', vaccinated_counter > 0, 8, settings['infection_distance'], incubation_time,
                          recovery_time)
            vaccinated_counter -= 1

            if i == 0:  # Pierwszy agent jest początkowo zainfekowany
                agent.was_infected = True
                agent.infected_time = pygame.time.get_ticks()
                agent.health_state = 'I'
                agent.change_color()

            if not has_collision(agent, agents):
                agents.append(agent)
                break

    return agents


def has_collision(new_agent, existing_agents):
    for agent in existing_agents:
        if new_agent.position.distance_to(agent.position) <= new_agent.radius + agent.radius:
            return True
    return False


def main():
    ui_manager = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    user_settings = ui_manager.show_menu(screen)
    print(f"Ustawienia użytkownika: {user_settings}")

    agents = initialize_agents(user_settings)

    plot_manager = PlotManager()
    plot_manager.run_in_thread(agents)

    last_call = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()

        if now - last_call >= INTERVAL:
            handle_infection(agents, now, user_settings)
            last_call = now

        update_agents(agents)

        render(screen, agents)
        clock.tick(FPS)


def update_agents(agents):
    for i, agent in enumerate(agents):
        if agent.health_state != 'D':
            agent.move()
        for agent2 in agents[i + 1:]:
            agent.collision_action(agent2)


def render(screen, agents):
    screen.fill(BLACK)
    for agent in agents:
        agent.draw(screen)
    pygame.display.update()


if __name__ == "__main__":
    main()
