import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from BusModeling import DukeBusSystem
#Change from v3. This version evenly spaces buses with respect to a lap, and not just one-way East to West campus. This is obviously way more efficient, though the buses get off of this alignment due to leaving whenever there are no more people to load.

bus_stop_east = []
bus_stop_west = []

def animate_bus_system(bus_system, time_between_ew=6, rate_of_people=15/60, board_rate=3, unload_rate=3):
    board_rate = board_rate*5
    unload_rate = unload_rate*5
    global bus_stop_east, bus_stop_west

    fig, ax = plt.subplots(figsize=(10, 6
                                    ))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.set_yticks([5])
    ax.set_yticklabels(['Route'])
    ax.set_xlabel('Position along Route')
    ax.set_title("Bus Movement Simulation")

    travel_time = bus_system.time_between_ew * 5  # Convert to animation frames
    stop_time = int((5/time_between_ew) * travel_time)
    spacing = 200 / bus_system.num_buses

    buses = []
    for i in range(bus_system.num_buses):
        position_percentage = (i + 0.5) / bus_system.num_buses  # Add 0.5 to offset and avoid starting at 0%
        position = position_percentage * 100  # Convert percentage to position
        direction = 1 if i % 2 == 0 else -1  # Alternate the direction of each bus
        buses.append({
            'position': position,
            'direction': direction,
            'people': 0,
            'waiting_time': 0,
            'state': 'moving',
            'loading': False
        })

    #buses = [{'position': i * spacing, 'direction': 1, 'people': 0, 'waiting_time': 0, 'state': 'moving', 'loading': False} for i in range(bus_system.num_buses)]

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
            if bus['state'] == 'moving':
                bus['position'] += bus['direction']
                if (bus['position'] >= 95 and bus['direction'] == 1) or (bus['position'] <= 5 and bus['direction'] == -1):
                    bus['state'] = 'stopped'
                    bus['waiting_time'] = stop_time
            
            elif bus['state'] == 'stopped':
                if bus['waiting_time'] > 0:
                    # Unloading people at the opposite side
                    if bus['position'] >= 95 and not bus['loading']:
                        for _ in range(unload_rate):
                            if bus['people'] > 0:
                                bus['people'] -= 1
                            else:
                                bus['loading'] = True

                    elif bus['position'] <= 5 and not bus['loading']:
                        for _ in range(unload_rate):
                            if bus['people'] > 0:
                                bus['people'] -= 1
                            else:
                                bus['loading'] = True

                     # Boarding new people
                    if bus['loading']:
                        if bus['position'] >= 95:
                            for _ in range(board_rate):
                                if bus_stop_east and bus['people'] < 100:
                                    bus['people'] += 1
                                    bus_stop_east.pop(0)
                                elif bus['people'] == 100 or not bus_stop_east:  # Bus is full or no people left
                                    bus['direction'] *= -1
                                    bus['state'] = 'moving'
                                    bus['loading'] = False
                                    break  # Exit the boarding loop
                        elif bus['position'] <= 5:
                            for _ in range(board_rate):
                                if bus_stop_west and bus['people'] < 100:
                                    bus['people'] += 1
                                    bus_stop_west.pop(0)
                                elif bus['people'] == 100 or not bus_stop_west:  # Bus is full or no people left
                                    bus['direction'] *= -1
                                    bus['state'] = 'moving'
                                    bus['loading'] = False
                                    break  # Exit the boarding loop
                    
                    bus['waiting_time'] -= 1
                    if bus['waiting_time'] == 0:
                        bus['direction'] *= -1
                        bus['state'] = 'moving'
                        bus['loading'] = False

            ax.text(bus['position'], 5, 'Bus\n' + str(bus['people']), ha='center', va='center', bbox=dict(facecolor='blue', alpha=0.5))
            
            # Add overlay text for bus passenger count
            ax.text(bus['position'], 3, f"{bus['people']} passengers", ha='center', va='center', fontsize=8, color='black')

        # Add new people to the bus stops
        new_people_east = int(rate_of_people * 5)
        new_people_west = int(rate_of_people * 5)
        bus_stop_east += [1] * new_people_east
        bus_stop_west += [1] * new_people_west

        # Draw people at bus stops
        for i in range(len(bus_stop_east)):
            ax.text(95, time_between_ew + 0.2*i, 'o', ha='center', va='center', color='red')

        for i in range(len(bus_stop_west)):
            ax.text(5, time_between_ew + 0.2*i, 'o', ha='center', va='center', color='red')

        # Add overlay text for people count at each bus stop
        ax.text(95, 8.5, f"{len(bus_stop_east)} waiting", ha='center', va='center', fontsize=8, color='black')
        ax.text(5, 8.5, f"{len(bus_stop_west)} waiting", ha='center', va='center', fontsize=8, color='black')

        return []

    ani = animation.FuncAnimation(fig, update, frames=int(bus_system.get_lap_time(bus_system.get_one_way_time()) * 5), init_func=init, blit=True, interval=200)
    plt.show()

duke_actual_system = DukeBusSystem("Actual", time_between_ew=6, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=5, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, num_stops=2, time_takes_to_wait_for_them=45/60)
animate_bus_system(duke_actual_system)
