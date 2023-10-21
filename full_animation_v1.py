import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from BusModeling import DukeBusSystem  # Commented this out as it's not available in this environment

bus_stop_east = []
bus_stop_west = []

def animate_bus_system(bus_system, rate_of_people=15/60, board_rate=3, unload_rate=3):
    board_rate = board_rate * 5
    unload_rate = unload_rate * 5
    global bus_stop_east, bus_stop_west

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.set_yticks([5])
    ax.set_yticklabels(['Route'])
    ax.set_xlabel('Position along Route')
    ax.set_title("Bus Movement Simulation")

    travel_time = bus_system.time_between_ew * 5  # Convert to animation frames
    stop_time = int((5/7) * travel_time)
    spacing = 100 / bus_system.num_buses

    buses = [{'position': i * spacing, 'direction': 1, 'people': 0, 'waiting_time': 0, 'state': 'moving', 'loading': False} for i in range(bus_system.num_buses)]

    def init():
        return []

    def update(num):
        global bus_stop_east, bus_stop_west

        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 10)
        ax.set_yticks([5])
        ax.set_yticklabels(['Route'])
        ax.set_xlabel('Position along Route')
        ax.set_title("Bus Movement Simulation")

        for bus in buses:
            # Other logic remains unchanged...

            # Boarding new people
            if bus['loading']:
                if bus['position'] >= 95:
                    for _ in range(board_rate):
                        if bus_stop_east and bus['people'] < 100:
                            bus['people'] += 1
                            bus_stop_east.pop(0)
                        if not bus_stop_east or bus['people'] >= 100:
                            bus['waiting_time'] = 0
                            break
                elif bus['position'] <= 5:
                    for _ in range(board_rate):
                        if bus_stop_west and bus['people'] < 100:
                            bus['people'] += 1
                            bus_stop_west.pop(0)
                        if not bus_stop_west or bus['people'] >= 100:
                            bus['waiting_time'] = 0
                            break

            # The rest of the logic remains unchanged...

        # Add new people to the bus stops
        new_people_east = int(rate_of_people * 5)
        new_people_west = int(rate_of_people * 5)
        bus_stop_east += [1] * new_people_east
        bus_stop_west += [1] * new_people_west

        # Draw people at bus stops
        for i in range(len(bus_stop_east)):
            ax.text(95, 7 + 0.2*i, 'o', ha='center', va='center', color='red')

        for i in range(len(bus_stop_west)):
            ax.text(5, 7 + 0.2*i, 'o', ha='center', va='center', color='red')

        # Add overlay text for people count at each bus stop
        ax.text(95, 8.5, f"{len(bus_stop_east)} waiting", ha='center', va='center', fontsize=8, color='black')
        ax.text(5, 8.5, f"{len(bus_stop_west)} waiting", ha='center', va='center', fontsize=8, color='black')

        return []

    ani = animation.FuncAnimation(fig, update, frames=int(bus_system.get_lap_time(bus_system.get_one_way_time()) * 5), init_func=init, blit=True, interval=200)
    plt.show()

duke_actual_system = DukeBusSystem("Actual", time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=5, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, num_stops=2, time_takes_to_wait_for_them=45/60)
animate_bus_system(duke_actual_system)
