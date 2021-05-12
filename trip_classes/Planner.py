from numpy.matlib import rand

from Item import Item
import pickle
from icecream import ic
import random2

from math import floor
from haversine import haversine
import numpy as np

from matplotlib import pyplot as plt
import math
import networkx as nx

from queue import PriorityQueue
from Day import Day

with open('../samples/dubai_trip_data.pkl', 'rb') as inp:
    m_trip = pickle.load(inp)

items = list(m_trip)
cities_names = []


def get_distance(item1: Item, item2: Item):
    cord1 = item1.coordinate
    cord2 = item2.coordinate
    tuple1 = (cord1['lat'], cord1['lon'])
    tuple2 = (cord2['lat'], cord2['lon'])
    return haversine(tuple1, tuple2)


class Planner:
    optimal_route = []
    optimal_cost = 0
    constraints = {
        'malls': 1,
        'restaurants': 2,
        'cafes': 3,
        'fast_food': 4,
        'architecture': 5,
        'cultural': 6,
        'sport': 7,
        'natural': 8,
        'marketplaces': 9,
        'hotel': 1000
    }

    def __init__(self, items):
        self.graph = []
        self.G = nx.Graph()
        self.P = nx.Graph()
        for i in range(len(items)):
            cities_names.append(f"{items[i].item_id}, Type:{items[i].item_type}")
            self.graph.append([])
            for j in range(len(items)):
                self.graph[i].append(floor(get_distance(items[i], items[j]) * 1000) / 1000)

    def delta(self, n1, n2, n3, n4):
        return self.graph[n1][n3] + self.graph[n2][n4] - self.graph[n1][n2] - self.graph[n3][n4]

    def plan_two_opt(self, iterations=5):
        i = 0
        total_costs = []
        while i < iterations:
            i += 1
            initial_route = [0] + random2.sample(range(1, len(cities_names)), len(cities_names) - 1)

            best_route = initial_route
            improved = True
            while improved:
                improved = False

                for i in range(1, len(self.graph) - 2):
                    for j in range(i + 1, len(self.graph)):
                        if j - i == 1:
                            continue
                        if self.delta(best_route[i - 1], best_route[i], best_route[j - 1], best_route[j]) < 0:
                            best_route[i:j] = best_route[j - 1:i - 1:-1]
                            improved = True
            path = [items[i] for i in best_route]
            [self.G.add_edge(items[i - 1], items[i]) for i in best_route]
            cost = 0
            for i in range(1, len(path) - 1):
                cost += get_distance(path[i], path[i - 1])

                total_costs.append((cost, best_route))
        total_costs = sorted(total_costs, key=lambda x: x[0])
        self.optimal_cost, self.optimal_route = total_costs[0]
        return self.optimal_route, self.optimal_cost, path

    def get_region_boundary(self, item):
        R = 6378.1  # Radius of the Earth
        brng = 1.57  # Bearing is 90 degrees converted to radians.
        d = 50  # Distance in km
        lat1, lon1 = math.radians(item.coordinate['lat']), math.radians(item.coordinate['lon'])
        # lat1 = math.radians(52.20472)  # Current lat point converted to radians
        # lon1 = math.radians(0.14056)  # Current long point converted to radians

        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                         math.cos(lat1) * math.sin(d / R) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                                 math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = floor(math.degrees(lat2) * 1000) / 1000
        lon2 = floor(math.degrees(lon2) * 1000) / 1000
        return lat2, lon2


def get_sublists(original_list, number_of_sub_list_wanted):
    sublists = list()
    for sub_list_count in range(number_of_sub_list_wanted):
        sublists.append(original_list[sub_list_count::number_of_sub_list_wanted])
    return sublists


if __name__ == '__main__':
    planner = Planner(items)
    optimal_route, optimal_cost, path = planner.plan_two_opt(iterations=1)
    ic(optimal_cost)

    # nx.draw(planner.G, node_color=['red'] * (len(path)), with_labels=True)
    # plt.show()
    range = []
    sub_region = []
    cpath = path.copy()
    while cpath:
        src = cpath[0]
        for p in path:
            if p in cpath:
                dist = get_distance(src, p)
                if dist < 50:
                    range.append((p, dist))
                    cpath.remove(p)
        sub_region.append(range)
        range = []
    days = []
    for sub in sub_region:
        a = []
        if len(sub) > 4:
            for s in sub:
                a.append(s)
                if len(a) >= 5:
                    days.append(Day(len(days), a))
                    a = []
        else:
            days.append(Day(len(days), sub))
    ic(days)
