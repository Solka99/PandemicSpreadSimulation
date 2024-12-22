import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import random
from game.agent import Agent

agents=[]
random.seed(10)
for i in range(100):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    age = random.randint(1, 100)
    agent = Agent(i,x,y, age, 'S',8)
    if i==20:
        agent.health_state='R'
    agents.append(agent)

class PlotManager:
    def __init__(self):
        self.time_steps = []
        self.susceptible_counts = []
        self.exposed_counts = []
        self.infected_counts = []
        self.recovered_counts = []
        self.dead_counts = []

    def update_data(self,frame):
        # susceptible = sum(1 for agent in agents if agent.health_state == 'S')
        susceptible=0
        for agent in agents:
            if agent.health_state == 'S':
                susceptible+=1

        # exposed = sum(1 for agent in agents if agent.health_state == 'E')
        # infected = sum(1 for agent in agents if agent.health_state == 'I')
        # recovered = sum(1 for agent in agents if agent.health_state == 'R')
        # dead = sum(1 for agent in agents if agent.health_state == 'D')
        #
        self.susceptible_counts.append(susceptible)
        # self.exposed_counts.append(exposed)
        # self.infected_counts.append(infected)
        # self.recovered_counts.append(recovered)
        # self.dead_counts.append(dead)

        plt.cla()
        plt.plot(self.susceptible_counts)
        # plt.plot(self.infected_counts)
        # plt.plot(self.recovered_counts)

    # def plot_animation(self,agents):
    #     def update_plot(frame):
    #         self.update_data(frame, agents)
    #         plt.cla()
    #         plt.tight_layout()
    #         plt.plot(self.time_steps, self.susceptible_counts, label="Susceptible", color="green")
    #         plt.plot(self.time_steps, self.infected_counts, label="Infected", color="red")
    #         plt.plot(self.time_steps, self.recovered_counts, label="Recovered", color="blue")
    #         plt.legend(loc="upper right")
    #         plt.xlabel("Time Steps")
    #         plt.ylabel("Count")
    #         plt.title("Agent States Over Time")


    def animation(self):
        ani = FuncAnimation(plt.gcf(),self.update_data,len(agents),interval=500)
        plt.cla()
        plt.show()

    # def run_in_thread(self, agents):
    #     """Uruchamia wykres w osobnym wątku."""
    #     plot_thread = threading.Thread(target=self.update_data, args=(agents,), daemon=True)
    #     plot_thread.start()

plotManager = PlotManager()
plotManager.animation()