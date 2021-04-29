from Item import Item
import pickle
from icecream import ic
import random2

from math import floor
from haversine import haversine

Days = list([])

with open('../samples/milan_trip_data.pkl', 'rb') as inp:
    m_trip = pickle.load(inp)

items = list(m_trip)
cities_names = []


class Planner:
    optimal_route = []
    optimal_cost = 0

    def __init__(self, items):
        self.graph = []
        for i in range(len(items)):
            cities_names.append(f"{items[i].item_id}, Type:{items[i].item_type}")
            self.graph.append([])
            for j in range(len(items)):
                self.graph[i].append(floor(self.get_distance(items[i], items[j]) * 1000) / 1000)

    def get_distance(self, item1: Item, item2: Item):
        cord1 = item1.coordinate
        cord2 = item2.coordinate
        tuple1 = (cord1['lat'], cord1['lon'])
        tuple2 = (cord2['lat'], cord2['lon'])
        return haversine(tuple1, tuple2)

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
            cost = 0
            for i in range(1, len(path) - 1):
                cost += self.get_distance(path[i], path[i - 1])
                total_costs.append((cost, best_route))
        total_costs = sorted(total_costs, key=lambda x: x[0])
        self.optimal_cost, self.optimal_route = total_costs[0]
        return self.optimal_route, self.optimal_cost


route = list(range(len(items)))

planner = Planner(items)
optimal_route, optimal_cost = planner.plan_two_opt(iterations=6)

ic(optimal_route)
ic(optimal_cost)
