from random import choice

from game.agent import Agent

def change_to_infected_logic(agent):
    # tutaj dodać logikę matematyczną

    if agent.health_state == 'E':
        answer = choice(['yes', 'no'])
        if answer == 'yes':
            agent.change_health_state('I')

def change_to_recovered_logic(agent):
    # tutaj dodać logikę matematyczną

    if agent.health_state == 'I':
        answer = choice(['yes', 'no'])
        if answer == 'yes':
            agent.change_health_state('R')

def change_to_dead_logic(agent):
    # tutaj dodać logikę matematyczną

    if agent.health_state == 'I':
        answer = choice(['yes', 'no'])
        if answer == 'yes':
            agent.change_health_state('D')




