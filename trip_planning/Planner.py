from copy import deepcopy
from typing import List
from search_engine.trip_planner.trip_classes.Item import Item
import random
from haversine import haversine
import numpy as np

from search_engine.trip_planner.trip_classes.Day import Day
import json
import requests

API_KEY = '5b3ce3597851110001cf624859a9e4cf86a3409abd7387ad2d5cac7a'


def get_distance(item1: Item, item2: Item):
    cord1 = item1.coordinate
    cord2 = item2.coordinate
    tuple1 = (cord1['lat'], cord1['lon'])
    tuple2 = (cord2['lat'], cord2['lon'])
    return haversine(tuple1, tuple2)


class Planner:
    optimal_route = []
    optimal_cost = 0

    def __init__(self, items: List, shopping_last=False):
        self.is_shopping_last = shopping_last
        self.types = [item.item_type for item in items]
        self.coordinates = []
        # print(len(items))
        self.food_types = ['restaurants', 'fast_food', 'food']
        self.market_types = ['shop']
        self.entertainment_types = ['sport', 'natural']

        self.url = 'https://api.openrouteservice.org/v2/matrix/driving-car'
        self.restaurants = [item for item in items if item.item_type in self.food_types]
        # print('res',len(self.restaurants))
        # shopping
        self.market_items = []
        if shopping_last:
            self.items = [item for item in items if item.item_type not in self.food_types + self.market_types]

            self.market_items = [item for item in items if item.item_type in self.market_types]

        else:
            self.items = [item for item in items if item.item_type not in self.food_types]

        self.graph = []
        self.days = []
        self.path = []
        for i in range(len(self.items)):
            self.coordinates.append([self.items[i].coordinate['lon'], self.items[i].coordinate['lat']])
        self.get_distance_matrix()

    # get real world route distances
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

    # 2-opt

    def delta(self, n1, n2, n3, n4):
        return self.graph[n1][n3] + self.graph[n2][n4] - self.graph[n1][n2] - self.graph[n3][n4]

    def cost(self, route):
        graph = np.array(self.graph)
        return graph[np.roll(route, 1), route].sum()

    # plan optimal path on distance
    def plan_two_opt(self, iterations=5):
        iter = 0
        while iter < iterations:
            iter += 1
            initial_route = [0] + random.sample(range(1, len(self.graph)), len(self.graph) - 1)

            best_route = initial_route
            improved = True
            tries = 0
            while improved:
                improved = False
                tries += 1
                if tries > 100:
                    print(tries)
                    break
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

    # make schedule
    def split_trip_on_days(self, path, poi_per_day, n_days):
        places = []
        idx = 0
        for i, place in enumerate(path):
            places.append(place)
            if len(places) >= poi_per_day:
                self.days.append(Day(idx, deepcopy(places)))
                idx +=1
                places = []
        # for items less than 5
        if places:
            self.days.append(Day(idx, places))
            idx+=1
            places = []
        return self.days

    # insert restaurant in the day at index
    def insert_restaurant(self, poi, idx, day):
        distances = []
        if self.restaurants:
            for rest in self.restaurants:
                distances.append(get_distance(poi, rest))
            index = distances.index(min(distances))
            day.insert_item(self.restaurants[index], idx)
            self.restaurants = [self.restaurants[l] for l in range(len(self.restaurants)) if l != index]

    # try to remove duplicates and put restaurants breaks,shopping
    def plan_itinerary(self, places_per_day=5, food_count=3, shop_count=1, n_days=3):
        ### if shopping is not in the last day, consider it as POI
        if self.is_shopping_last:
            self.days = self.split_trip_on_days(self.path, places_per_day, n_days)
        else:
            self.days = self.split_trip_on_days(self.path, places_per_day + shop_count, n_days)

        for i, day in enumerate(self.days):
            days_items = day.items

            # inserting restaurants
            if food_count == 1:
                self.insert_restaurant(days_items[0], 0, day)
            elif food_count == 2:
                self.insert_restaurant(days_items[0], 0, day)
                self.insert_restaurant(days_items[-1], len(days_items), day)
            else:
                self.insert_restaurant(days_items[0], 0, day)
                self.insert_restaurant(days_items[len(days_items) // 2], (len(days_items) // 2) + 1, day)
                self.insert_restaurant(days_items[-1], len(days_items), day)
            # ensure that hotel at first
            for k in range(0, len(days_items)):
                if 'hotel' == days_items[k].item_type and k != 0:
                    day.swap_items(0, k)

        # insert shopping
        if self.is_shopping_last:
            self.days.append(Day(len(self.days), self.market_items))
        return self.days
