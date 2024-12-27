import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

class PlotManager:
    def __init__(self):
        self.time_steps = []
        self.susceptible_counts = []
        self.exposed_counts = []
        self.infected_counts = []
        self.recovered_counts = []
        self.dead_counts = []

    def update_data(self,frame,agents):
        susceptible = sum(1 for agent in agents if agent.health_state == 'S')
        exposed = sum(1 for agent in agents if agent.health_state == 'E')
        infected = sum(1 for agent in agents if agent.health_state == 'I')
        recovered = sum(1 for agent in agents if agent.health_state == 'R')
        dead = sum(1 for agent in agents if agent.health_state == 'D')

        self.susceptible_counts.append(susceptible)
        self.exposed_counts.append(exposed)
        self.infected_counts.append(infected)
        self.recovered_counts.append(recovered)
        self.dead_counts.append(dead)

        plt.cla()

        categories = ["Susceptible", "Exposed", "Infected", "Recovered", "Dead"]
        values = [
            self.susceptible_counts[-1], # ostatnia wartośćmw liście to ostatni count
            self.exposed_counts[-1],
            self.infected_counts[-1],
            self.recovered_counts[-1],
            self.dead_counts[-1],
        ]
        plt.ylim(0, 100) # można tu dać zmienną ilości agentów

        plt.bar(categories, values, color=["green", "yellow", "red", "blue", "gray"])
        plt.xlabel("Health States")
        plt.ylabel("Count")
        plt.title("Agent Health State Over Time")
        plt.tight_layout()


    def animation(self, agents):
        def update(frame):
            self.update_data(frame,agents)  # Przekazywanie agents do update_data

        ani = FuncAnimation(plt.gcf(), update,frames=None, interval=500)
        plt.show()

    def run_in_thread(self, agents):
        """Uruchamia wykres w osobnym wątku."""
        plot_thread = threading.Thread(target=self.animation, args=(agents,), daemon=True) # wyłączy się jak wyłączy się główny program
        plot_thread.start()
