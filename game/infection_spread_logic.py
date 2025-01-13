import random

PIXEL_METER_RATIO = 10
VACCINATION_MULTIPLIER = 0.61
R_0 = 2.5


def handle_infection(agents, current_time, settings):
    for i, agent in enumerate(agents):
        if agent.health_state in ['S', 'R', 'D']:
            continue

        if agent.health_state == 'E' and agent.was_exposed and current_time - agent.exposed_time > agent.incubation_time:
            agent.health_state = 'I'
            agent.change_color()
            agent.was_infected = True
            agent.infected_time = current_time

        if agent.health_state == 'I':
            process_infections(agent, agents, current_time)
            process_recovery_or_death(agent, current_time)


def process_infections(agent, agents, current_time):
    for other_agent in agents:
        if other_agent.health_state == 'S' and agent.get_distance(other_agent) <= agent.infection_radius:
            infection_probability = (
                    (1 / (R_0 + (agent.get_distance(other_agent) / PIXEL_METER_RATIO)))
                    * (VACCINATION_MULTIPLIER if other_agent.vaccinated else 1)
            )
            if random.random() < infection_probability:
                other_agent.health_state = 'E'
                other_agent.change_color()
                other_agent.was_exposed = True
                other_agent.exposed_time = current_time


def process_recovery_or_death(agent, current_time):
    if agent.was_infected and current_time - agent.infected_time > agent.recovered_time:
        death_probability = calculate_death_probability(agent.age)
        if random.random() < death_probability:
            agent.health_state = 'D'
        else:
            agent.health_state = 'R'
        agent.change_color()


def calculate_death_probability(age):
    if 10 <= age <= 39:
        return 0.002
    elif 40 <= age <= 49:
        return 0.004
    elif 50 <= age <= 59:
        return 0.013
    elif 60 <= age <= 69:
        return 0.036
    elif 70 <= age <= 79:
        return 0.08
    elif 80 <= age <= 100:
        return 0.15
    return 0
