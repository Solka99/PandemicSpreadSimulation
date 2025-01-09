import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from collections import deque


class PlotManager:
    def __init__(self, smoothing_window=5):
        self.time_steps = []
        self.susceptible_counts = []
        self.exposed_counts = []
        self.infected_counts = []
        self.recovered_counts = []
        self.dead_counts = []

        # Kolejki do wygładzania
        self.smoothing_window = smoothing_window
        self.susceptible_queue = deque(maxlen=smoothing_window)
        self.exposed_queue = deque(maxlen=smoothing_window)
        self.infected_queue = deque(maxlen=smoothing_window)
        self.recovered_queue = deque(maxlen=smoothing_window)
        self.dead_queue = deque(maxlen=smoothing_window)

        # Flaga zamknięcia okna
        self.window_closed = False

    def calculate_moving_average(self, queue, new_value):
        """
        Aktualizuje kolejkę i oblicza średnią kroczącą.
        """
        queue.append(new_value)
        return sum(queue) / len(queue)

    def update_data(self, frame, agents):
        # Liczenie agentów w różnych stanach zdrowia
        susceptible = sum(1 for agent in agents if agent.health_state == 'S')
        exposed = sum(1 for agent in agents if agent.health_state == 'E')
        infected = sum(1 for agent in agents if agent.health_state == 'I')
        recovered = sum(1 for agent in agents if agent.health_state == 'R')
        dead = sum(1 for agent in agents if agent.health_state == 'D')

        # Aktualizacja z wygładzaniem
        susceptible_avg = self.calculate_moving_average(self.susceptible_queue, susceptible)
        exposed_avg = self.calculate_moving_average(self.exposed_queue, exposed)
        infected_avg = self.calculate_moving_average(self.infected_queue, infected)
        recovered_avg = self.calculate_moving_average(self.recovered_queue, recovered)
        dead_avg = self.calculate_moving_average(self.dead_queue, dead)

        # Aktualizacja list danych
        self.time_steps.append(frame)
        self.susceptible_counts.append(susceptible_avg)
        self.exposed_counts.append(exposed_avg)
        self.infected_counts.append(infected_avg)
        self.recovered_counts.append(recovered_avg)
        self.dead_counts.append(dead_avg)

    def save_plot(self, agents):
        """
        Rysuje końcowy wykres i zapisuje go jako PNG.
        """
        fig, ax = plt.subplots()

        # Rysowanie wykresu
        ax.plot(self.time_steps, self.susceptible_counts, label="Susceptible", color="green")
        ax.plot(self.time_steps, self.exposed_counts, label="Exposed", color="yellow")
        ax.plot(self.time_steps, self.infected_counts, label="Infected", color="red")
        ax.plot(self.time_steps, self.recovered_counts, label="Recovered", color="blue")
        ax.plot(self.time_steps, self.dead_counts, label="Dead", color="gray")

        # Ustawienia osi i tytułów
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Agent Count")
        ax.set_title("Health States Over Time (Smoothed)")
        ax.legend()
        ax.set_xlim(0, max(self.time_steps) if self.time_steps else 1)
        ax.set_ylim(0, len(agents))

        # Zapis jako PNG
        fig.savefig("simulation_plot.png")
        plt.close(fig)

    def animation(self, agents):
        fig, ax = plt.subplots()

        def update(frame):
            self.update_data(frame, agents)
            ax.clear()

            # Rysowanie wykresu dla każdego stanu zdrowia
            ax.plot(self.time_steps, self.susceptible_counts, label="Susceptible", color="green")
            ax.plot(self.time_steps, self.exposed_counts, label="Exposed", color="yellow")
            ax.plot(self.time_steps, self.infected_counts, label="Infected", color="red")
            ax.plot(self.time_steps, self.recovered_counts, label="Recovered", color="blue")
            ax.plot(self.time_steps, self.dead_counts, label="Dead", color="gray")

            # Ustawienia osi i tytułów
            ax.set_xlabel("Time Steps")
            ax.set_ylabel("Agent Count")
            ax.set_title("Health States Over Time (Smoothed)")
            ax.legend()
            ax.set_xlim(0, max(self.time_steps) if self.time_steps else 1)
            ax.set_ylim(0, len(agents))

        def on_close(event):
            self.window_closed = True
            self.save_plot(agents)

        fig.canvas.mpl_connect("close_event", on_close)

        animation = FuncAnimation(fig, update, frames=None, interval=1000)
        plt.show()

    def run_in_thread(self, agents):
        plot_thread = threading.Thread(target=self.animation, args=(agents,), daemon=True)
        plot_thread.start()
