from typing import List

import pickle
from icecream import ic
import random
import geopandas
from math import floor
from haversine import haversine
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import math
# import networkx as nx
import folium
from search_engine.trip_planner.trip_classes.Trip import Trip
from trip_planning.Planner import Planner, get_distance

axis = [[32.745255, -74.034775], [34.155834, -119.202789], [42.933334, -100.566666], [42.095554, -79.238609],
        [38.846668, -71.948059], [36.392502, -81.534447], [32.745255, -74.034775]]

with open('../testing/samples/berlin_london_istanbul_riyadh_trip_data.pkl', 'rb') as input:
    m_trip = pickle.load(input)

items = m_trip
colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
]


# ic(list(items.values()))

def plot_path(trip,name):
    m = folium.Map(location=[52.529412, 13.125847])
    path = []
    for i,day in enumerate(trip.days):
        path.extend(day.items)

        for j,item in enumerate(day.items):
            folium.Marker(
                location=[item.coordinate['lat'], item.coordinate['lon']],
                icon=folium.Icon(color=colors[i if i < len(colors) else 0]),
                tooltip=f'Day:{i+1},Place:{j+1}, {item.item_type}, {item.name}'
            ).add_to(m)


    folium.PolyLine(locations=[[item.coordinate['lat'],item.coordinate['lon']] for item in path], weight=5).add_to(m)

    m.save(name)
    print('saved')

def plan_itinerary_schedule(items_dict: dict, places_per_day, food_count, is_shopping_last,shop_count,n_days):
    trip = Trip(days=[])
    print('sum of data',sum([len(x) for x in items_dict.values()]))

    if places_per_day > food_count:
        for value in items_dict.values():
            print(value)
            planner = Planner(value, shopping_last=is_shopping_last)
            optimal_route, optimal_cost, path = planner.plan_two_opt(iterations=5)
            full_plan_city = planner.plan_itinerary(places_per_day, food_count,shop_count,n_days=n_days)
            trip.add_bulk_days(full_plan_city)
    else:
        raise ValueError('Need Poi to be more than Food')
    ic(trip.days)
    plot_path(trip,'map.html')

    return trip


if __name__ == '__main__':
    full_itinerary = plan_itinerary_schedule(items, places_per_day=9, food_count=3,shop_count=1, is_shopping_last=False)
    ic(full_itinerary.days)
