#Modified from https://github.com/akash-r34/Bus-Schedule-Optimization/blob/main/Web_mining_J_Component.ipynb
#Added support for multiple buses

import os
import csv
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

import time
import csv
from datetime import datetime

############Segment 1
# RIT agency_id: 643

# py -2 agency.py
import requests
# import time
# import argparse

url = "https://transloc-api-1-2.p.rapidapi.com/agencies.json"

querystring = {"callback":"call"}

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "c7a9a279b1msh49ce82192ac5ef8p1830cejsnf6c553ccadea"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

agencies = response.json()
print("List of all agencies:", end="\n\n")
for agency in agencies["data"]:
  print(agency)


#Selected agency
agency_id = 176
route_id = '4008330'

querystring = {"callback":"call", "agencies":agency_id}
response = requests.request("GET", url, headers=headers, params=querystring)
print()
print("Selected agency:")
print()
print(response.text)

############Segment 2
# Get Vehicle Location

# Province Route ID: 4013312
# Evening Campus Route ID: 4013322


import requests

url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"

# Province Route ID: 4013312 ; RIT Agency ID: 643
#querystring = {"routes":"4016624","callback":"call","agencies":"643"} # Evening Campus Shuttle
agency_id = 176
querystring = {"callback":"call", "agencies":agency_id}

# querystring = {"routes":"4013312","callback":"call","agencies":"643"}   # Province

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "c7a9a279b1msh49ce82192ac5ef8p1830cejsnf6c553ccadea"
    }


response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)
# print(response.headers)
json = response.json()
print(json)


# RIT Agency ID: 643
# Get the vehicle Location
location = (json['data']['176'][0]['location'])
print("Location: " + str(location))

lat = location['lat']   # Get vehicle Latitude
print("Latitude: " + str(lat))

lon = location['lng']   # Get vehicle Longitude
print("Longitude: " + str(lon))

#map = plt.imread('Agency location/map.png')
#fig, ax = plt.subplots(figsize = (8,7))
#ax.scatter(lon, lat, zorder=1, alpha= 0.2, c='b', s=10)
#BBox = [-77.6895, -77.6517, 43.0925, 43.0748]
#ax.imshow(map, zorder=0, extent = BBox, aspect= 'equal')

############Segment 3
import requests
import time
import datetime

# ---------------------------------#
def get_routes(agency_id):
    url = "https://transloc-api-1-2.p.rapidapi.com/routes.json"

    # RIT Agency ID: 643
    querystring = {"callback":"call","agencies":agency_id}

    headers = {
        'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
        'x-rapidapi-key': "c7a9a279b1msh49ce82192ac5ef8p1830cejsnf6c553ccadea"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)

    json = response.json()
    # print(json)

    routes = json['data']['176']    # Get the different routes for RIT(643)
    # print("Number of Routes: " + str(len(routes)))


    # Get the data for each route
    route_name = []
    route_id = []
    for route in routes:
        route_name.append(route['long_name'])
        route_id.append(route['route_id'])
    # print(route_name,route_id)

    # Print route_id for each route
    # for route in range(len(routes)):
    #     # print(route_name[route] + ": " + route_id[route])
    return route_name, route_id

# -----------------------------------------------------------------------------#
# Return the current date and time
def get_current_datetime():
    dt = datetime.datetime.today()
    day = dt.day
    mon = dt.month
    yr = dt.year
    hr = dt.hour
    min = dt.minute
    sec = dt.second
    today_datetime = [day, mon, yr, hr, min, sec]
    # today_datetime.extend((day, mon, yr, hr, min, sec))
    return today_datetime

# -----------------------------------------------------------------------------#
#Inserted
def csv_get_current_datetime():
    return datetime.datetime.now()

def write_to_csv(data, filename="vehicle_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for vehicle in data:
            writer.writerow([datetime.datetime.now(), vehicle[0], vehicle[1]])
#
def get_vehicles(route_id,agency_id):
    url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"

    # Province Route ID: 4013312 ; RIT Agency ID: 643
    # querystring = {"routes":"4013312","callback":"call","agencies":"643"}
    querystring = {"routes":route_id,"callback":"call","agencies":agency_id}

    headers = {
        'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
        'x-rapidapi-key': "c7a9a279b1msh49ce82192ac5ef8p1830cejsnf6c553ccadea"
        }


    response = requests.request("GET", url, headers=headers, params=querystring)
    json = response.json()
    
    vehicles_data = []
    if 'data' in json and str(agency_id) in json['data']:
        vehicles = json['data'][str(agency_id)]
        #Support for multipple buses
        for vehicle in vehicles:
            passenger_load = round(vehicle['passenger_load'], 2) * 100
            vehicles_data.append((vehicle['vehicle_id'], passenger_load))
            print(f"Vehicle ID: {vehicle['vehicle_id']} Passenger Load: {passenger_load}%")
    else:
        print("No vehicle data available.")
    return vehicles_data

while True:
    vehicles_data = get_vehicles(route_id, agency_id) 
    write_to_csv(vehicles_data) 
    print(csv_get_current_datetime())
    time.sleep(60)  # Wait for 1 minute before looping again

    
# -----------------------------------------------------------------------------#
def get_available_vehicles(route_id,agency_id,route_name):
    url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"

    # Province Route ID: 4013312 ; RIT Agency ID: 643
    # querystring = {"routes":"4013312","callback":"call","agencies":"643"}
    querystring = {"routes":route_id,"callback":"call","agencies":agency_id}

    headers = {
        'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
        'x-rapidapi-key': "c7a9a279b1msh49ce82192ac5ef8p1830cejsnf6c553ccadea"
        }


    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    # print(response.headers)
    json = response.json()
    # print(json)

    # Get rate limit
    rate_limit = (json['rate_limit'])
    # print("Rate Limit: " + str(rate_limit))

    # Check if the route is active or not. i.e. if data for the route is available.
    route_status = len((json['data']))
    if route_status>0:
        # RIT Agency ID: 643
        # Get the passenger_load for the Bus
        # passenger_load = (json['data']['643'][0]['passenger_load'])
        # passenger_load = round(passenger_load,2) * 100  # Convert to Percentage
        # print(str(route_name) + "Pasenger Load: " + str(passenger_load) + "%")

        passenger_load = (json['data']['176'][0]['passenger_load'])
        passenger_load = round(passenger_load,3) * 100  # Convert to Percentage
        # print(str(route_name) + "Pasenger Load: " + str(passenger_load) + "%")
        return passenger_load, rate_limit
    else:
        passenger_load = 0  # Route Inactive. Hence set passenger_load to 0.
        return passenger_load, rate_limit



# -----------------------------------------------------------------------------#
# Make a list of passenger_load for both active and inactive route/vehicles
def passenger_load_list(route_id_list,agency_id,route_name_list):
    passenger_load_list = []
    for route_id in route_id_list:
        route_name = route_name_list[route_id_list.index(route_id)]
        passenger_load, rate_limit = get_available_vehicles(route_id,agency_id,route_name)
        if passenger_load == None:
            passenger_load_list.append(0)
        else:
            passenger_load_list.append(passenger_load)
        time.sleep(rate_limit*1.1)  # Limit API requests to the rate_limit times 1.1

    # print("passenger_load_list",passenger_load_list)
    return passenger_load_list

#-------------------------

####################################################################Duke Specific Code
agency_id = '176' 
print(get_routes(agency_id))
#We see from the above output that route_id = '4008330' for C1
route_id = '4008330'
print(get_vehicles(route_id, agency_id))
print(get_available_vehicles(route_id, agency_id, "C1"))


###########################Storing

