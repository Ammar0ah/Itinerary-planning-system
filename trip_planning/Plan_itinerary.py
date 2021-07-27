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
from collections import Counter

from queue import PriorityQueue
from search_engine.trip_planner.trip_classes.Trip import Trip
from trip_planning.Planner import Planner, get_distance

axis = [[32.745255, -74.034775], [34.155834, -119.202789], [42.933334, -100.566666], [42.095554, -79.238609],
        [38.846668, -71.948059], [36.392502, -81.534447], [32.745255, -74.034775]]

with open('../testing/samples/berlin_london_istanbul_riyadh_trip_data.pkl', 'rb') as input:
    m_trip = pickle.load(input)

items = m_trip


# ic(list(items.values()))

def plot_path(path):
    x_axes = [item.coordinate['lat'] for item in path]
    y_axes = [item.coordinate['lon'] for item in path]
    plt.plot(x_axes, y_axes, 'o--')

    plt.plot(x_axes[0], y_axes[0], 'go--', linewidth=2, markersize=12, color="r")
    plt.plot(x_axes[-1], y_axes[-1], 'go--', linewidth=2, linestyle="dashed", markersize=12, color='r')
    x = np.arange(39, 42, 0.5)
    # y = np.arange(0,3, 0.2)
    plt.xticks(x)
    # plt.yticks(y)
    for i, x in enumerate(x_axes):
        plt.annotate(str(i) + path[i].item_type, (x_axes[i], y_axes[i]))
    plt.show()


def plan_itinerary_schedule(items_dict: dict, places_per_day, food_count, is_shopping_last):
    trip = Trip(days=[])
    if places_per_day > food_count:
        for value in items_dict.values():
            planner = Planner(value, shopping_last=is_shopping_last)
            optimal_route, optimal_cost, path = planner.plan_two_opt(iterations=5)
            ic(path)
            full_plan_city = planner.plan_itinerary(places_per_day, food_count)
            trip.add_bulk_days(full_plan_city)
    else:
        raise ValueError('Need Poi to be more than Food')
    return trip


if __name__ == '__main__':
    full_itinerary = plan_itinerary_schedule(items, places_per_day=9, food_count=3, is_shopping_last=False)
    ic(full_itinerary.days)
