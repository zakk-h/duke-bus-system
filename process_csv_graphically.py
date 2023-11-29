import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV data into a DataFrame using pandas
df = pd.read_csv('vehicle_data.csv', names=['datetime', 'vehicle_id', 'passenger_load'])

# Combine date and time fromg string format into pandas datatime object
df['datetime'] = pd.to_datetime(df['datetime'])

# Sort data by the date and time. This should already be the case.
df.sort_values('datetime', inplace=True)

plt.figure(figsize=(15, 8))

# Loop through each vehicle_id and plot it on the graph
for vehicle_id, group in df.groupby('vehicle_id'):
    plt.plot(group['datetime'], group['passenger_load'], label=f'Bus {vehicle_id}')

plt.legend()
# Instead of including the date, just use H:M format.
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel('Time')
plt.ylabel('Passenger Load (%)')
plt.title('Passenger Load Over Time for Each Bus')
plt.grid(True)
plt.xticks(rotation=0)  # If including the date, it would be best to rotate the labels on the x axis.
plt.tight_layout()
plt.show()

# Creates a Panda series with each index being the combined percentage of all buses per given time. 
# This percent is still of a single bus, so is likely to exceed 100%
# Additionally, buses already register above 100% for standing passengers, etc.
combined_load = df.groupby('datetime')['passenger_load'].sum()

# Calculate the 1-hour moving average
moving_avg = combined_load.rolling(window='1H').mean()

plt.figure(figsize=(15, 8))

combined_load.plot()

# Plot the moving average starting at minute 61, using the first hours' data for the first point
start_point = combined_load.index[0] + pd.Timedelta(hours=1)
moving_avg[start_point:].plot(label='1-Hour Moving Average')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlabel('Time')
plt.ylabel('Combined Passenger Load (%)')
plt.title('Combined Passenger Load Over Time Across All Buses (with 1HR Moving Average)')
plt.grid(True)
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()
