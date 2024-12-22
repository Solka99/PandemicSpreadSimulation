from random import choice

from game.agent import Agent

def change_to_infected_logic(agent):
    # tutaj dodać logikę matematyczną

    if agent.health_state == 'E':
        answer = choice(['yes', 'no'])
        if answer == 'yes':
            agent.change_health_state('I')





