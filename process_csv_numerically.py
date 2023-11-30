import pandas as pd
import matplotlib.pyplot as plt
from BusModeling import DukeBusSystem
# Data from 11/28: https://docs.google.com/spreadsheets/d/1alFjRYx7_sqpGHysy1RGm4835o5iT6imzKh0xQltEo0/edit?usp=sharing

# Load the CSV data into a DataFrame using pandas
df = pd.read_csv('vehicle_data.csv', names=['datetime', 'vehicle_id', 'passenger_load'])

# Combine date and time fromg string format into pandas datatime object
df['datetime'] = pd.to_datetime(df['datetime'])

# Sort data by the date and time. This should already be the case.
df.sort_values('datetime', inplace=True)

# Stores (in 1D) the total passenger load percent across all buses and all time recorded.
total_passenger_percent = df['passenger_load'].sum()
#(total_passenger_load) #70923 (%)
# This is a massive number and is not saying x% divided by the capacity of a single bus is the number of students.
# Instead, this needs to be normalized by the average time periods the student is on the bus. This CSV has data from once a minute.

# To do this, we will use our simulation and models from BusModeling.py
duke_actual_system = DukeBusSystem("Actual", time_between_ew=5.5, time_stop_along_route=20/60, let_off_people=20/60, pull_up_to_stop=20/60, wait_at_stop_for_people=4.2, num_buses=4, num_people_running=3, num_people_on_bus=40, print_output=False, capacity = round(1.2*(112+66*3)/4,0), num_stops=2, time_takes_to_wait_for_them=45/60)
duke_actual_system.simulate()

time_on_bus_minutes = duke_actual_system.get_average_time_person_on_bus()
time_on_bus_csv_periods = time_on_bus_minutes # They are 1-to-1

real_passenger_percent_total = total_passenger_percent/time_on_bus_csv_periods

factor = 1.2 # Capacity may not line up precisely with 100%, and we adjust for that here.
bus_capacity_for_100 = duke_actual_system.capacity/factor 
print(f"Bus Capacity (to have Transloc display 100%, average across bus sizes): {round(bus_capacity_for_100)}")

num_people_uses_over_csv = real_passenger_percent_total/100*bus_capacity_for_100

print(f"Number of C1 uses over the time period: {round(num_people_uses_over_csv)}")
print(f"The total time on the bus of all passengers over this time period is approximately {round(num_people_uses_over_csv*time_on_bus_csv_periods/60)} hours")

duke_class_of_2027 = 1743
print(f"Ratio of number of uses to first-year students: {round(num_people_uses_over_csv/duke_class_of_2027,2)}")
print(f"Ratio of number of uses/2 (round trip) to first-year students: {round((num_people_uses_over_csv/2)/duke_class_of_2027,2)}")
