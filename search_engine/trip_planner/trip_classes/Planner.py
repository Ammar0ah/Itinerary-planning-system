from copy import deepcopy
from typing import List
# import gmplot
from Item import Item
import pickle
from icecream import ic
import random
# import geopandas
from math import floor
from haversine import haversine
import numpy as np

from matplotlib import pyplot as plt
import math
# import networkx as nx
from collections import Counter

from queue import PriorityQueue
from Day import Day

API_KEY = 'AIzaSyCNvDXCZJSLvw9618045G3856O8x5EqeKw'

# with open('../../../testing/samples/milan_trip_data.pkl', 'rb') as input:
#     m_trip = pickle.load(input)
#
# items = list(m_trip)[:15]
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

    def __init__(self, items: List):
        self.types = [item.item_type for item in items]

        self.food_types = ['restaurants', 'fast_food', 'food']
        self.poi_types = ['cultural', 'architecture', 'historic', 'religion']
        self.market_types = ['malls', 'cafes', 'marketplaces', 'shop']
        self.entertainment_types = ['sport', 'natural']
        self.orders = [0, random.choice(self.food_types), random.choice(self.poi_types)]

        self.restaurants = [item for item in items if item.item_type in self.food_types]

        self.items = [item for item in items if item.item_type not in self.food_types]
        self.breaks = 3
        self.graph = []
        self.days = []
        self.path = []
        for i in range(len(self.items)):
            cities_names.append(f"{self.items[i].item_id}, Type:{self.items[i].item_type}")
            self.graph.append([])
            for j in range(len(self.items)):
                self.graph[i].append(floor(get_distance(self.items[i], self.items[j]) * 1000) / 1000)

    def get_constraint(self, current):
        categories = [self.food_types, self.poi_types, self.market_types, self.entertainment_types]
        for type_cat in categories:
            if current in type_cat:
                next_items = [j for j in categories if j == type_cat]
                return next_items[0]  # list in first index

    def delta(self, n1, n2, n3, n4):
        return self.graph[n1][n3] + self.graph[n2][n4] - self.graph[n1][n2] - self.graph[n3][n4]

    # plan optimal path on distance
    def plan_two_opt(self, iterations=5):
        i = 0
        total_costs = []
        while i < iterations:
            i += 1
            initial_route = [0] + random.sample(range(1, len(cities_names)), len(cities_names) - 1)

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
            path = [self.items[i] for i in best_route]

            cost = 0
            for i in range(1, len(path) - 1):
                cost += get_distance(path[i], path[i - 1])

                total_costs.append((cost, best_route))
        total_costs = sorted(total_costs, key=lambda x: x[0])
        self.optimal_cost, self.optimal_route = total_costs[0]
        self.path = path
        return self.optimal_route, self.optimal_cost, self.path

    def split_trip_on_days(self, path):
        p_range = []
        sub_region = []
        cpath = path.copy()

        orders = [['hotel'], self.food_types, random.choice(self.poi_types), random.choice(self.food_types),
                  random.choice(self.market_types)]
        type_index = 0
        while cpath:
            src = cpath[0]
            order = orders[type_index]
            for p in path:
                if p in cpath:
                    dist = get_distance(src, p)
                    if dist < 50:
                        p_range.append(p)
                        cpath.remove(p)
                    else:
                        if len(orders) > type_index + 1:
                            type_index += 1
            sub_region.append(p_range)
            p_range = []
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
        self.days = days
        return days

    # try to remove duplicates and put restaurants breaks
    def plan_itinerary(self):
        i = 0

        for i in range(200):
            i += 1
            copy_path = deepcopy(self.path)
            for i in range(1, len(copy_path)):
                if copy_path[i].item_type == copy_path[i - 1].item_type:
                    same_type = self.get_constraint(copy_path[i].item_type)

                    distances = []
                    indexes = []
                    for j in range(0, len(copy_path)):
                        if i != j and copy_path[j].item_type not in same_type:
                            indexes.append(j)
                            distances.append(get_distance(copy_path[i], copy_path[j]))
                    index = distances.index(min(distances))
                    index = indexes[index]
                    self.path[i], self.path[index] = self.path[index], self.path[i]

        self.days = self.split_trip_on_days(self.path)
        for i, day in enumerate(self.days):
            days_items = day.items
            food_count = 0
            for k, item in enumerate(days_items):
                if 'hotel' == item.item_type and k != 0:
                    day.swap_items(0, k)

                if k % 2 and k != 0 and self.restaurants:
                    food_count += 1
                    if food_count > self.breaks:
                        food_count = 0
                        continue
                    distances = []
                    for rest in self.restaurants:
                        distances.append(get_distance(item, rest))
                    index = distances.index(min(distances))
                    day.insert_item(self.restaurants[index], k)
                    self.restaurants = [self.restaurants[l] for l in range(len(self.restaurants)) if l != index]
        return self.days
