from Day import Day
from Item import Item
from Trip import Trip
from itertools import permutations
import pickle
from icecream import ic
from math import floor
from sys import maxsize

Days = list([])

with open('../samples/milan_trip_data.pkl', 'rb') as inp:
    m_trip = pickle.load(inp)

items = list(m_trip)[:10]


def get_distance(item1: Item, item2: Item):
    cord1 = item1.coordinate
    cord2 = item2.coordinate
    return abs(cord1['lat'] - cord2['lat']) + abs(cord1['lon'] - cord2['lon'])


graph = []

for i in range(len(items)):
    graph.append([])
    for j in range(len(items)):
        graph[i].append(floor(get_distance(items[i], items[j]) * 1000) / 1000)

ic(graph)


def plan_trip(s):
    vertices = []
    for k in range(len(graph)):
        if k != s:
            vertices.append(k)

    weights = []
    perms = list(permutations(vertices))
    min_path = maxsize

    for i in perms:
        k = s
        current_weight = 0
        for j in i:
            current_weight += graph[k][j]
            k = j
        current_weight += graph[k][s]

        min_path = min(current_weight, min_path)
        weights.append(min_path)

    return min_path, weights, perms


s = 0
min_weight, weights, perms = plan_trip(s)
min_path = weights.index(min_weight)
min_path = list(perms[min_path])
min_path.insert(0, s)
min_path.append(s)
for i in range(len(min_path)):
    min_path[i] += 1

ic(min_path, min_weight)
