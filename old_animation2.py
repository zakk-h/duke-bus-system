# heatmap_animation.py

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.animation as animation
from BusModeling import simulate_for_params  # Assuming your original code is in a file named "duke_bus_simulation.py"

def animate_heatmap(i):
    plt.clf()
    bus_numbers = list(range(1, i + 2))  # Increasing the number of buses for each frame
    wait_times = np.linspace(0.5, 10, 20)  
    results_with_output = simulate_for_params(wait_times, bus_numbers)

    # Extracting results for graphing
    X, Y, Z = [], [], []
    for (wait_time, bus_num), avg_wait in results_with_output.items():
        X.append(wait_time)
        Y.append(bus_num)
        Z.append(avg_wait)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    # Convert the results to a DataFrame for heatmap
    df = pd.DataFrame({
        'Wait Time at Stop': X,
        'Number of Buses': Y,
        'Average Wait Time (Uniform Distribution)': Z
    })

    # Create a pivot table for the heatmap
    heatmap_data = df.pivot_table(index='Number of Buses', columns='Wait Time at Stop', values='Average Wait Time (Uniform Distribution)')

    # Plot the heatmap
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='viridis', linewidths=.5)
    plt.title('Effects of Wait Time at Stop and Number of Buses on Average Wait Time (Uniform Distribution)')

fig = plt.figure(figsize=(12, 8))
ani = animation.FuncAnimation(fig, animate_heatmap, frames=10, repeat=True)
plt.show()
