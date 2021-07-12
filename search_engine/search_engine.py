from search_engine.utils.hotels_engine import HotelSearchEngine as Hotels
from search_engine.utils.places_engine import PlacesSearchEngine as Places
from search_engine.trip_planner.trip_classes.Item import Item
from enum import Enum


class SearchEngine:
    def __init__(self):
        self.hotels = Hotels()
        self.places = Places()

    class EngineType(Enum):
        HOTELS = 1,
        PLACES = 2,

    class HSEEndPoints(Enum):
        BOOK = 1,  # location_name & other booking information 'dict'
        DETAILS = 2,  # hotel_id 'int'
        IMAGES = 3,  # hotel_id 'int'
        REVIEWS = 4,  # hotel_id 'int'
        FINDHOTEL = 5,  # hotel_name 'str'
        BESTCHOISE = 6,  # location 'str
        RECOMMEND = 7,   # hotel_id

    class PSEEndPoints(Enum):
        DETAILS = 1,  # place_id : str
        LOCATION = 2,  # place_name & wanted_filters
        LISTVIEW = 3,  # place_name & wanted_filters
        COORDINATES = 4,  # lat & lon : str, kind : str
        BESTCHOISE = 5,  # lat & lon : str, places count : int, kind : str

    class OptionalPlacesKinds(Enum):
        HIS = 'historic',
        CUL = 'cultural',
        NAT = 'natural',
        REL = 'religion',
        SPO = 'sport',
        ARC = 'architecture',

    class TripMode(Enum):
        extended_trip = 1,
        focused_trip = 2,

    def _collect_trip_components(self, locations: list, trip_mode: str, food_importance: int,
                                 shop_importance: int, days_count: int, places_per_day: int,
                                 places_preferences: dict):
        def _calc_places_count():
            places_count = places_per_day * days_count
            result = {}
            for place in places_preferences.keys():
                result[place] = round((places_preferences[place] / sum(places_preferences.values())) * places_count)
            return result

        if bool(places_preferences):
            if trip_mode not in self.TripMode.__members__:
                raise ValueError('You have entered wrong mode!')
            else:
                trip_components = []

                print('start collecting trip data..')

                preferences = _calc_places_count()
                print(preferences)

                for location in locations:
                    shops_count = round((shop_importance * days_count) / len(locations))
                    foods_count = round((food_importance * days_count) / len(locations))

                    print(f'collecting best hotels in {location}..')

                    starting_pt = self.hotels.best_hotels_in_country(location)  # starting point -> first hotel.
                    trip_components.append(Item('hotel', starting_pt['0']))

                    if food_importance > 0:
                        print(f'collecting food palces in {location}..')
                        places = self.places.get_top_rated_places(starting_pt['0']['coordinate']['lat'],
                                                                  starting_pt['0']['coordinate']['lon'],
                                                                  foods_count,
                                                                  'foods', '3')
                        for place in places:
                            trip_components.append(Item('food', place))
                    if shop_importance > 0:
                        print(f'collecting shopping places in {location}..')
                        places = self.places.get_top_rated_places(starting_pt['0']['coordinate']['lat'],
                                                                  starting_pt['0']['coordinate']['lon'],
                                                                  shops_count,
                                                                  'shops', '3')
                        for place in places:
                            trip_components.append(Item('shop', place))
                    print('collecting Point of Interest Places...')
                    for place_type in preferences.keys():

                        places = self.places.get_top_rated_places(starting_pt['0']['coordinate']['lat'],
                                                                  starting_pt['0']['coordinate']['lon'],
                                                                  int(preferences[place_type] / len(locations)),
                                                                  self.OptionalPlacesKinds[place_type].value[0],
                                                                  '3')

                        for place in places:
                            trip_components.append(Item(str(self.OptionalPlacesKinds[place_type].value[0]), place))
            return trip_components
        else:
            raise ValueError('cannot collect trip components without specifying kinds!')

    def _build_plan(self, data: list, constraints: dict):
        pass  # add code here!   #ammar

    def plan_trip(self, constraints: dict):
        trip_data = self._collect_trip_components(locations=constraints['locations'],
                                                  trip_mode=constraints['trip_mode'],
                                                  food_importance=constraints['food_importance'],
                                                  shop_importance=constraints['shop_importance'],
                                                  days_count=constraints['days_count'],
                                                  places_preferences=constraints['places_preferences'],
                                                  places_per_day=constraints['places_per_day'],
                                                  )
        self._build_plan(trip_data, constraints)
        return trip_data
        # add code here -> return planned trip as json file! ammar

    def get(self, engine_type, end_point, query_params):

        def hotel_search_engine_endpoints_es():
            booking_query_params = [
                'location',
                'page_number',
                'adults',
                'check_in_date',
                'check_out_date',
            ]
            if end_point not in self.HSEEndPoints.__members__:
                raise ValueError('Can not Find the Entered Endpoint!, try something else')
            else:
                if end_point == 'DETAILS':
                    if 'id' in query_params:
                        return self.hotels.hotel_details(query_params['id'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'IMAGES':
                    if 'id' in query_params:
                        return self.hotels.get_hotel_imgs(query_params['id'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'FINDHOTEL':
                    if 'name' in query_params:
                        return self.hotels.get_hotel_details_by_name(query_params['name'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'RECOMMEND':
                    if 'id' in query_params:
                        hotel_details = self.hotels.hotel_details(query_params['id'])
                        hotel_features = hotel_details['HOTEL_FEATURE'] + hotel_details['HOTEL_FREEBIES'] + hotel_details['ROOMS']
                        # add code here --> return list of recommended hotel names   #adnan
                        names = ['Hyatt Regency Istanbul Ataköy']
                        recommended_hotels = []
                        for name in names:
                            recommended_hotels.append(self.hotels.get_hotel_details_by_name(name))
                        return recommended_hotels
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'REVIEWS':
                    if 'id' in query_params and 'page_number' in query_params:
                        return self.hotels.get_hotel_reviews(query_params['id'], query_params['page_number'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'BESTCHOISE':
                    if 'location' in query_params:
                        return self.hotels.best_hotels_in_country(query_params['location'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'BOOK':
                    if all(param in query_params for param in booking_query_params):
                        return self.hotels.search_location(query_params['location'],
                                                           query_params['page_number'],
                                                           query_params['check_in_date'],
                                                           query_params['check_out_date'],
                                                           query_params['adults'],
                                                           sort_order=query_params[
                                                               'sort_order'] if 'sort_order' in query_params else 'PRICE',
                                                           filters=query_params[
                                                               'filters'] if 'filters' in query_params else {}
                                                           )
                    else:
                        raise ValueError('There is something missed in the query_params!')

        def place_search_engine_endpoints_es():
            if end_point not in self.PSEEndPoints.__members__:
                raise ValueError('Can not Find the Entered Endpoint!, try something else')
            else:
                if end_point == 'DETAILS':
                    if 'id' in query_params:
                        return self.places.get_object_properties(query_params['id'])
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'LISTVIEW':
                    if 'name' in query_params:
                        if 'filter' in query_params:
                            return self.places.get_list_of_places(query_params['name'], query_params['filter'])
                        else:
                            return self.places.get_list_of_places(query_params['name'], '')
                    else:
                        raise ValueError('There is something missed in the query_params!')
                elif end_point == 'LOCATION':
                    if 'name' in query_params:
                        if 'filter' in query_params:
                            return self.places.get_place_features(query_params['name'], query_params['filter'])
                        else:
                            return self.places.get_place_features(query_params['name'], '')
                    else:
                        raise ValueError('A very specific bad thing happened.')

                elif end_point == 'COORDINATES':
                    if 'lat' in query_params and 'lon' in query_params:
                        if 'filter' in query_params:
                            return self.places.search_places_by_coords(query_params['lat'],
                                                                       query_params['lon'],
                                                                       query_params['filter'])
                        else:
                            return self.places.search_places_by_coords(query_params['lat'],
                                                                       query_params['lon'],
                                                                       '')
                    else:
                        raise ValueError('There is something wrong with the coordinates!')
                elif end_point == 'BESTCHOISE':
                    if 'lat' in query_params and 'lon' in query_params and 'count' in query_params:
                        if 'filter' in query_params:
                            return self.places.get_top_rated_places(query_params['lat'],
                                                                    query_params['lon'],
                                                                    query_params['count'],
                                                                    query_params['filter'])
                        else:
                            return self.places.get_top_rated_places(query_params['lat'],
                                                                    query_params['lon'],
                                                                    query_params['count'],
                                                                    '')
                    else:
                        raise ValueError('There is something wrong with the coordinates!')

        if engine_type == 'HOTELS':
            print('Hotels search engine in use!')
            return hotel_search_engine_endpoints_es()

        elif engine_type == 'PLACES':
            print('Places search engine in use!')
            return place_search_engine_endpoints_es()

        else:
            raise ValueError('Can not Find the Entered Type!, try -> HOTELS or PLACES!')
