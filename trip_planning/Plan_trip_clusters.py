
from search_engine.trip_planner.trip_classes.Day import Day
from search_engine.trip_planner.trip_classes.Item import Item
import pandas as pd
from sklearn.cluster import KMeans

import pickle
from search_engine.trip_planner.trip_classes.Trip import Trip
from icecream import ic


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import requests
import json

from trip_planning.Plan_itinerary import plot_path,colors

API_KEY = '5b3ce3597851110001cf624859a9e4cf86a3409abd7387ad2d5cac7a'
url = 'https://api.openrouteservice.org/v2/matrix/driving-car'



from haversine import haversine




def get_distance(item1: Item, item2: Item):
    cord1 = item1.coordinate
    cord2 = item2.coordinate
    tuple1 = (cord1['lat'], cord1['lon'])
    tuple2 = (cord2['lat'], cord2['lon'])
    return haversine(tuple1, tuple2)

def create_data_model(p_items):
    coordinates = []

    """Stores the data for the problem."""
    data = {}

    for i in range(len(p_items)):
        coordinates.append([p_items[i].coordinate['lon'],p_items[i].coordinate['lat']])
    body = {'locations': coordinates, 'metrics': ['distance'], 'units': 'km'}
    header = {'Authorization': API_KEY}
    try:
        response = requests.post(url=url, json=body, headers=header)
        if response.status_code == requests.codes.ok:
            data['distance_matrix'] = json.loads(response.text)['distances']
    except ValueError as err:
        print('distance matrix err: ', err)

    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def get_routes(solution, routing, manager):
  """Get vehicle routes from a solution and store them in an array."""
  # Get vehicle routes and store them in a two dimensional array whose
  # i,j entry is the jth location visited by vehicle i along its route.
  routes = []
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
      index = solution.Value(routing.NextVar(index))
      route.append(manager.IndexToNode(index))
    routes.append(route)
  return routes
def plan_itinerary_LP(p_items):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(p_items)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        # print_solution(manager, routing, solution
        path = get_routes(solution,routing,manager)
        return [p_items[i] for i in path[0]]


class ClusterPlanner:
    def __init__(self, items,n_opi):
        self.n_clusters = len(items) // n_opi
        self.clusterer = None
        self.food_types = ['restaurants', 'fast_food', 'food']
        self.items = [item for item in items if item.item_type not in self.food_types]
        self.restaurants = [item for item in items if item.item_type in self.food_types]

        self.data = pd.DataFrame({
            'index': [i for i in range(len(self.items))],
            'lat': [item.coordinate['lat'] for item in self.items],
            'lon': [item.coordinate['lon'] for item in self.items],
            'type': [item.item_type for item in self.items]})

    def cluster_data(self):
        self.clusterer = KMeans(n_clusters=self.n_clusters)
        self.data['label'] = self.clusterer.fit_predict(self.data[['lat', 'lon']].values)

    # insert restaurant in the day at index
    def insert_restaurant(self, poi, idx, day):
        distances = []
        if self.restaurants:
            for rest in self.restaurants:
                distances.append(get_distance(poi, rest))
            index = distances.index(min(distances))
            day.insert_item(self.restaurants[index], idx)
            self.restaurants = [self.restaurants[l] for l in range(len(self.restaurants)) if l != index]

    # plan every cluster in city then return the full plan
    def plan_days(self, i=0, days=[],activities=[]):

        if i == self.n_clusters:
            return days
        places = self.data[self.data['label'] == i]
        p_items = [self.items[int(p['index'])] for l, p in places.iterrows()]
        day_places = p_items
        # plan if items > 3
        if len(p_items) > 3:
            itinerary = plan_itinerary_LP(p_items)[:-1]
            day_places = itinerary
            if len(p_items) > 5:
                day = Day(i,itinerary[:5])
                day_places = itinerary[:5]
                days.append(day)
                day = Day(i, itinerary[5:])
                day_places = itinerary[5:]
                days.append(day)
            else:

                day = Day(i, itinerary)
                days.append(day)
            activities = []

        else:
            activities.append(p_items)
            # day = Day(i, p_items)
            # days.append(day)

        # insert restaurants
        # for j in range(0, len(day_places), 3):
        #     self.insert_restaurant(day_places[j], j, day)

        for k in range(0, len(day_places)):
            if 'hotel' == day_places[k].item_type and k != 0:
                day.swap_items(0, k)

        return self.plan_days(i + 1, days,activities)

# reorganize plan
def plan_itinerary_schedule_clusters(items: dict):
    trip = Trip(days=[])
    for k, city in items.items():
        clusterer = ClusterPlanner(city,4)
        clusterer.cluster_data()
        plan_days = clusterer.plan_days()

    trip.add_bulk_days(plan_days)
    ic('clusters',trip.days)
    plot_path(trip,'map_clusters.html')
    return trip


if __name__ == '__main__':

    with open('../testing/samples/berlin_london_trip_data.pkl', 'rb') as input:
         m_trip = pickle.load(input)

    trip = plan_itinerary_schedule_clusters(m_trip)
    print(trip)

