from typing import List

from Item import Item
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
from Day import Day


from Planner import Planner, get_distance

axis = [[32.745255, -74.034775], [34.155834, -119.202789], [42.933334, -100.566666], [42.095554, -79.238609],
        [38.846668, -71.948059], [36.392502, -81.534447], [32.745255, -74.034775]]

with open('../../../testing/samples/istanbul_trip_data.pkl', 'rb') as input:
    m_trip = pickle.load(input)

items = list(m_trip)
print(items)
# print(len(items))

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

if __name__ == '__main__':
    planner = Planner(items)
    optimal_route, optimal_cost, path = planner.plan_two_opt(iterations=1)
    print(path)

    full_plan = planner.plan_itinerary()
    path_full =[]
    for d in full_plan:
        for t in d.items:
            path_full.append(t)
    ic(path_full)


    plot_path(path_full)
