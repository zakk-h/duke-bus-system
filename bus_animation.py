import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from BusModeling import DukeBusSystem
from matplotlib.widgets import Button

# Global variable to store the mode
is_auto_spawn = True

def toggle_spawning(event):
    global is_auto_spawn, btn  
    is_auto_spawn = not is_auto_spawn
    btn.label.set_text('Auto Spawn: ON' if is_auto_spawn else 'Auto Spawn: OFF')

bus_stop_east = []
bus_stop_west = []

elapsed_frames = 0

def animate_bus_system(bus_system, rate_of_people=15/60, board_rate=3, unload_rate=3):
    global btn
    board_rate = board_rate*5
    unload_rate = unload_rate*5

    fig = plt.figure(figsize=(10, 7))  # Adjust the figure size if needed
    ax = plt.subplot2grid((8, 1), (0, 0), rowspan=7)  # Subplot for the animation

    # Define the position and size of the button [left, bottom, width, height]
    # These values are in figure coordinate (0 to 1)
    button_axes = fig.add_axes([0.75, 0.02, 0.12, 0.04])    
    btn = Button(button_axes, 'Auto Spawn: ON')
    btn.on_clicked(toggle_spawning)

    ax.set_xlim(0, 100)
    ax.set_ylim(1, 500)  # Set the y limit to a fixed range
    ax.set_yticks([5])
    ax.set_yticklabels(['Route'])
    ax.set_xlabel('Position along Route')
    ax.set_title("Bus Movement Simulation")

    travel_time = bus_system.time_between_ew * 5  # Convert to animation frames
    stop_time = int((5/bus_system.time_between_ew) * travel_time)
    spacing = 90 / (bus_system.num_buses - 1)  # Adjust the spacing calculation
    buses = [{
        'position': 5 + i * spacing,  # Start the first bus at position 5 and space out subsequent buses
        'direction': 1 if i % 2 == 0 else -1,  # Alternate direction
        'people': 0,
        'waiting_time': 0,
        'state': 'moving',
        'loading': False
    } for i in range(bus_system.num_buses)]

    def init():
        return []

    def update(num):
        global bus_stop_east, bus_stop_west, is_auto_spawn

        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(1, 500)
        ax.set_yscale("log")
        ax.set_yticks([5])
        ax.set_yticklabels(['Route'])
        ax.set_xlabel('Position along Route')
        ax.set_title("Bus Movement Simulation")

        if is_auto_spawn:
            # Add new people automatically if in auto spawn mode
            new_people_east = int(rate_of_people * 5)
            new_people_west = int(rate_of_people * 5)
            bus_stop_east += [1] * new_people_east
            bus_stop_west += [1] * new_people_west

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
                                if bus_stop_east and bus['people'] < bus_system.capacity:
                                    bus['people'] += 1
                                    bus_stop_east.pop(0)
                                elif bus['people'] == bus_system.capacity or not bus_stop_east:  # Bus is full or no people left
                                    bus['direction'] *= -1
                                    bus['state'] = 'moving'
                                    bus['loading'] = False
                                    break  # Exit the boarding loop
                        elif bus['position'] <= 5:
                            for _ in range(board_rate):
                                if bus_stop_west and bus['people'] < bus_system.capacity:
                                    bus['people'] += 1
                                    bus_stop_west.pop(0)
                                elif bus['people'] == bus_system.capacity or not bus_stop_west:  # Bus is full or no people left
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
            ax.text(bus['position'], 3, f"{bus['people']} passengers", ha='center', va='center', fontsize=8, color='black')

        global elapsed_frames
        elapsed_frames += 1

        # Saying each frame in the animation represents 0.2 seconds in real life
        animation_frame_time = 0.5*bus_system.time_between_ew/9  # in seconds

        # Calculate the real-time elapsed for each frame based on the x-minute travel time
        real_time_per_frame = (bus_system.time_between_ew * 60) / (bus_system.time_between_ew * 5 / animation_frame_time)  # in seconds

        # Calculate the real-time elapsed based on the animation frames
        #real_time_per_frame = (bus_system.time_between_ew * 60) / (bus_system.time_between_ew * 5)  # in seconds
        real_time_elapsed = elapsed_frames * real_time_per_frame  # in seconds

        # Convert the real-time elapsed from seconds to minutes and seconds
        minutes = int(real_time_elapsed // 60)
        seconds = int(real_time_elapsed % 60)

        # Display the timer on the plot
        ax.text(50, 480, f"Elapsed: {minutes:02}:{seconds:02}", ha='center', va='center', fontsize=10, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        # Calculate the total height needed for all the waiting people
        height_east = len(bus_stop_east) * 0.6
        height_west = len(bus_stop_west) * 0.6

        # Start positioning the first person in the list at the front and continue up
        for i, _ in enumerate(bus_stop_east):
            ax.text(95, 10 + height_east - 0.6 * i, 'o', ha='center', va='center', color='red', fontsize=15)

        for i, _ in enumerate(bus_stop_west):
            ax.text(5, 10 + height_west - 0.6 * i, 'o', ha='center', va='center', color='red', fontsize=15)

        ax.text(95, 8.5, f"{len(bus_stop_east)} waiting", ha='center', va='center', fontsize=8, color='black')
        ax.text(5, 8.5, f"{len(bus_stop_west)} waiting", ha='center', va='center', fontsize=8, color='black')

        return []

    ani = animation.FuncAnimation(fig, update, frames=int(bus_system.get_lap_time(bus_system.get_one_way_time()) * 5), init_func=init, blit=True, interval=200)

    def on_click(event):
        global bus_stop_east, bus_stop_west

        if event.xdata is None or event.ydata is None:
            return

        if event.xdata > 50:  # Right side
            num_people = min(int(event.ydata), 500) - len(bus_stop_east)
            bus_stop_east += [1] * max(num_people, 0)
        else:  # Left side
            num_people = min(int(event.ydata), 500) - len(bus_stop_west)
            bus_stop_west += [1] * max(num_people, 0)

    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

# Running the animation
duke_optimized_system = DukeBusSystem("Optimized", time_between_ew=5.5, time_stop_along_route=20/60, let_off_people=20/60, pull_up_to_stop=20/60, wait_at_stop_for_people=45/60, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=False, capacity = round(1.2*(112+60*3)/4,0), num_stops=2, time_takes_to_wait_for_them=45/60)
animate_bus_system(duke_optimized_system)
