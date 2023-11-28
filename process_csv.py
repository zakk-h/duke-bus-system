import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil import parser

# Load the CSV data into a DataFrame
df = pd.read_csv('vehicle_data.csv', names=['timestamp', 'vehicle_id', 'passenger_load'])

def custom_date_parser(date_str):
    # Replace invalid month and year with default values
    date_str = date_str.replace('/0/', '/1/').replace('00 ', '2000 ')
    try:
        return pd.to_datetime(date_str, format='%d/%m/%Y %I:%M %p', errors='raise')
    except ValueError:
        # Handle the exception if the date is still incorrect
        return pd.NaT  # Return 'Not a Time' for invalid timestamps

df['timestamp'] = df['timestamp'].apply(custom_date_parser)

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%I:%M:%S %p', errors='coerce')

# Drop rows where timestamp could not be parsed (if any)
df.dropna(subset=['timestamp'], inplace=True)


# Group the data by 'vehicle_id'
grouped = df.groupby('vehicle_id')

# Plotting
fig, ax = plt.subplots()

for name, group in grouped:
    ax.plot(group['timestamp'], group['passenger_load'], label=name)

ax.legend(title='Vehicle ID')
plt.xlabel('Time')
plt.ylabel('Passenger Load (%)')
plt.title('Passenger Load Over Time for Each Bus')
plt.xticks(rotation=45)  # Rotate the x-axis labels to avoid overlap
plt.tight_layout()  # Adjust the plot to ensure everything fits without overlapping
plt.show()

# Drop rows where timestamp could not be parsed
df.dropna(subset=['timestamp'], inplace=True)

# Sort the DataFrame based on the 'timestamp' column
df.sort_values('timestamp', inplace=True)

# Group the data by 'timestamp' and sum the 'passenger_load'
total_load_per_time = df.groupby('timestamp')['passenger_load'].sum()

# Plotting
plt.figure(figsize=(10, 6))
total_load_per_time.plot()
plt.xlabel('Time')
plt.ylabel('Total Passenger Load (%)')
plt.title('Total Passenger Load Over Time Across All Buses')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Calculate the 30-minute moving average
moving_avg = total_load_per_time.rolling('30T').mean()  # '30T' is 30 minutes

# Plotting
plt.figure(figsize=(10, 6))
moving_avg.plot()
plt.xlabel('Time')
plt.ylabel('30-Minute Moving Average of Passenger Load (%)')
plt.title('30-Minute Moving Average of Total Passenger Load Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()