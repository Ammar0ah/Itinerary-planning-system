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

API_KEY = '5b3ce3597851110001cf624859a9e4cf86a3409abd7387ad2d5cac7a'
import json

# with open('../../../testing/samples/milan_trip_data.pkl', 'rb') as input:
#     m_trip = pickle.load(input)
#
# items = list(m_trip)[:15]
cities_names = []
import requests


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
        self.coordinates = []
        self.food_types = ['restaurants', 'fast_food', 'food']
        self.poi_types = ['cultural', 'architecture', 'historic', 'religion']
        self.market_types = ['malls', 'cafes', 'marketplaces', 'shop']
        self.entertainment_types = ['sport', 'natural']
        self.orders = [0, random.choice(self.food_types), random.choice(self.poi_types)]
        self.url = 'https://api.openrouteservice.org/v2/matrix/driving-car'
        self.restaurants = [item for item in items if item.item_type in self.food_types]
        # self.restaurants = []
        self.items = [item for item in items if item.item_type not in self.food_types]
        # self.items = items
        self.breaks = 3
        self.graph = []
        self.days = []
        self.path = []
        for i in range(len(self.items)):
            cities_names.append(f"{self.items[i].item_id}, Type:{self.items[i].item_type}")
            self.coordinates.append([self.items[i].coordinate['lon'], self.items[i].coordinate['lat']])
            # self.graph.append([])
            # for j in range(len(self.items)):
            #     self.graph[i].append(floor(get_distance(self.items[i], self.items[j]) * 1000) / 1000)
        self.get_distance_matrix()

    def get_distance_matrix(self):
        body = {'locations': self.coordinates, 'metrics': ['distance'], 'units': 'km'}
        header = {'Authorization': API_KEY}
        try:
            response = requests.post(url=self.url, json=body, headers=header)
            if response.status_code == requests.codes.ok:
                self.graph = json.loads(response.text)['distances']
        except ValueError as err:
            print('distance matrix err: ', err)

    def get_distance_two_cities(self, city_i, city_j):
        return self.graph[self.optimal_route[city_i]][self.optimal_route[city_j]]

    # scheduling items in day
    def get_constraint(self, current):
        categories = [self.food_types, self.poi_types, self.market_types, self.entertainment_types]
        for type_cat in categories:
            if current in type_cat:
                next_items = [j for j in categories if j == type_cat]
                return next_items[0]  # list in first index

    # 2-opt

    def cost(self, route):
        graph = np.array(self.graph)
        return graph[np.roll(route, 1), route].sum()

    # plan optimal path on distance
    def plan_two_opt(self, iterations=5):
        i = 0
        total_costs = []
        while i < iterations:
            i += 1
            initial_route = [0] + random.sample(range(1, len(cities_names)), len(cities_names) - 1)

            best_route = initial_route
            improved = True
            tries = 0
            while improved:
                improved = False
                tries += 1
                for i in range(1, len(self.graph) - 2):
                    for j in range(i + 1, len(self.graph)):
                        if j - i == 1:
                            continue
                        new_route = best_route[:]
                        new_route[i:j] = best_route[j - 1:i - 1:-1]
                        if self.cost(new_route) < self.cost(best_route):
                            improved = True
                            best_route = new_route
            self.path = [self.items[i] for i in best_route]
            self.optimal_cost = 0
            self.optimal_route = best_route
            for i in range(0, len(best_route)):  # list of path indices
                for j in range(0, len(best_route)):
                    self.optimal_cost += self.get_distance_two_cities(best_route[i], best_route[j])
        return self.optimal_route, self.optimal_cost, self.path

    def split_trip_on_days(self, path):
        places = []
        for i, place in enumerate(path):
            places.append(place)
            if len(places) > 5:
                self.days.append(Day(i // 5, places))
                places = []

        return self.days

    # try to remove duplicates and put restaurants breaks
    def plan_itinerary(self):
        self.days = self.split_trip_on_days(self.path)

        while self.restaurants:
            for i, day in enumerate(self.days):

                days_items = day.items
                food_count = 0
                for k, item in enumerate(days_items):
                    if 'hotel' == item.item_type and k != 0:
                        day.swap_items(0, k)

                    # if k % 3 == 2 and k != 0 and self.restaurants:
                    #     food_count += 1
                    #     if food_count > self.breaks:
                    #         food_count = 0
                    #         continue
                    #     distances = []
                    #     for rest in self.restaurants:
                    #         distances.append(get_distance(item, rest))
                    #     index = distances.index(min(distances))
                    #     day.insert_item(self.restaurants[index], k)
                    #     self.restaurants = [self.restaurants[l] for l in range(len(self.restaurants)) if l != index]
        return self.days
