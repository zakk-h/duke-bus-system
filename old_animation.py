import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from BusModeling import DukeBusSystem, Student, visualize_probabilities

# Create DukeBusSystem instances
duke_actual_system = DukeBusSystem("Actual", time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=5, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, num_stops=2, time_takes_to_wait_for_them=45/60)
duke_optimized_system = DukeBusSystem("Optimized", time_between_ew=7, time_stop_along_route=20/60, let_off_people=30/60, pull_up_to_stop=15/60, wait_at_stop_for_people=45/60, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=True, num_stops=2, time_takes_to_wait_for_them=45/60)

# Initial setup for the animation
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(5, 21)
ax.set_ylim(0, 1)
ax.set_xlabel('Time Allocated for Bus (minutes)')
ax.set_ylabel('Probability of Being Late')
ax.set_title('Probability of Being Late vs Time Allocated for Bus')
ax.grid(True)
line1, = ax.plot([], [], lw=3, label=f'Duke System {duke_actual_system.id}')
line2, = ax.plot([], [], lw=3, label=f'Duke System {duke_optimized_system.id}')
ax.legend()

times = np.arange(5, 21.25, 0.25)

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

def update(frame):
    t = times[:frame]
    probabilities1 = [Student(time).probability_of_being_late(duke_actual_system, want_output=False) for time in t]
    probabilities2 = [Student(time).probability_of_being_late(duke_optimized_system, want_output=False) for time in t]
    line1.set_data(t, probabilities1)
    line2.set_data(t, probabilities2)
    return line1, line2

ani = FuncAnimation(fig, update, frames=len(times), init_func=init, blit=True)
plt.show()
