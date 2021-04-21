from utils.hotels_engine import HotelSearchEngine as Hotels
from utils.places_engine import PlacesSearchEngine as Places
from trip_classes.Item import Item
from enum import Enum

class Search_Engine:
    def __init__(self):
        self.hotels = Hotels()
        self.places = Places()
    
    class EngineType(Enum):
        HOTELS = 1,
        PLACES = 2,
        
    class HSE_EndPoints(Enum):
        BOOK = 1, #location_name & other booking information 'dict'
        DETAILS = 2, #hotel_id 'int'
        IMAGES = 3,   #hotel_id 'int'
        REVIEWS = 4,  #hotel_id 'int'
        FINDHOTEL = 5,    #hotel_name 'str'
        BESTCHOISE = 6, # location 'str

    class PSE_EndPoints(Enum):
        DETAILS = 1, #place_id : str
        LOCATION = 2, #place_name & wanted_filters
        LISTVIEW = 3, #place_name & wanted_filters
        COORDINATES = 4, #lat & lon : str, kind : str 
        BESTCHOISE = 5, #lat & lon : str, places count : int, kind : str 
        
    class OptionalPlacesKinds(Enum):
        HIS = 'historic',
        CUL = 'cultural',
        NAT = 'natural',
        REL = 'religion',
        SPO = 'sport',
        ARC = 'architecture',
    
    class TirpMode(Enum):
        extended_trip = 1,
        focused_trip = 2,

        
    ### need to specify the calculation mechanism of items count per trip.... -> dist
    def collect_trip_components(self, location : str, num_of_days : int, preferences : list, trip_mode : str):
        if bool(preferences):
            if trip_mode not in self.TirpMode.__members__:
                raise ValueError('You have entered wrong mode!')
            else:
                trip_components = []
                fixed_places = ['fast_food', 'malls', 'marketplaces', 'restaurants', 'cafes'] 
                
                starting_pt = self.hotels.best_hotels_in_country(location) #starting point -> first hotel.
                trip_components.append(Item('hotel', starting_pt['0']))
                
                dist = 0
                suspicion = 0.2
                if trip_mode == 'focused_trip':
                    dist = num_of_days + 0.5
                    
                elif trip_mode == 'extended_trip':
                    dist = num_of_days * 1.5
                    
                for kind in fixed_places:
                    suspicion = suspicion * -1.1
                    dist = dist + suspicion
                    print('collecting', kind, '...')
                    places = self.places.get_top_rated_places(starting_pt['0']['coordinate']['lat'],
                                                               starting_pt['0']['coordinate']['lon'],
                                                               round(dist),
                                                               kind)

                    for place in places:
                        trip_components.append(Item(kind, place))
                   
                for kind in preferences:
                    suspicion = suspicion * -1.1
                    dist = dist + suspicion
                    print('collecting', str(self.OptionalPlacesKinds[kind].value[0]), '...')
                    places = self.places.get_top_rated_places(starting_pt['0']['coordinate']['lat'],
                                                               starting_pt['0']['coordinate']['lon'],
                                                               round(dist),
                                                               self.OptionalPlacesKinds[kind].value[0])

                    for place in places:
                        trip_components.append(Item(str(self.OptionalPlacesKinds[kind].value[0]), place))
                
                
                return set(trip_components)
        else: 
            raise ValueError('cannot collect trip components without specifying kinds!')  
            
    def get(self, engine_type, end_point ,query_params):

        def hotel_search_engine_endpoints_es(end_point, query_params):
            booking_query_params = [
                'location',
                'page_number',
                'adults',
                'check_in_date',
                'check_out_date',
            ]
            if end_point not in self.HSE_EndPoints.__members__:
                raise ValueError('fuck A very specific bad thing happened.')
            else:    
                if end_point == 'DETAILS':
                    if 'id' in query_params:
                        return self.hotels.hotel_details(query_params['id'])
                    else:
                        raise ValueError('A very specific bad thing happened.')
                elif end_point == 'IMAGES':      
                    if 'id' in query_params:
                        return self.hotels.get_hotel_imgs(query_params['id'])
                    else:
                        raise ValueError('A very specific bad thing happened.')
                elif end_point == 'FINDHOTEL':      
                    if 'name' in query_params:
                        return self.hotels.get_hotel_details_by_name(query_params['name'])
                    else:
                        raise ValueError('A very specific bad thing happened.')       
                elif end_point == 'REVIEWS':      
                    if 'id' in query_params and 'page_number' in query_params:
                        return self.hotels.get_hotel_reviews(query_params['id'], query_params['page_number'])
                    else:
                        raise ValueError('A very specific bad thing happened.')
                elif end_point == 'BESTCHOISE':      
                    if 'location' in query_params:
                        return self.hotels.best_hotels_in_country(query_params['location'])
                    else:
                        raise ValueError('A very specific bad thing happened.')    
                elif end_point == 'BOOK':      
                    if all(param in query_params for param in booking_query_params):
                        return self.hotels.search_location(query_params['location'],
                                                      query_params['page_number'],
                                                      query_params['check_in_date'],
                                                      query_params['check_out_date'],
                                                      query_params['adults'],
                                                      sort_order = query_params['sort_order'] if 'sort_order' in query_params else 'PRICE',
                                                      filters = query_params['filters'] if 'filters' in query_params else {}
                                                     )
                    else:
                        raise ValueError('A very specific bad thing happened.')           
        def place_search_engine_endpoints_es(end_point, query_params):
            if end_point not in self.PSE_EndPoints.__members__:
                raise ValueError('Can not Find the Entered Endpoint!, try something else')
            else:    
                if end_point == 'DETAILS':
                    if 'id' in query_params:
                        return self.places.get_object_properties(query_params['id'])
                    else:
                        raise ValueError('A very specific bad thing happened.')
                elif end_point == 'LISTVIEW':      
                        if 'name' in query_params:
                            if 'filter' in query_params:
                                return self.places.get_list_of_places(query_params['name'], query_params['filter'])
                            else:    
                                return self.places.get_list_of_places(query_params['name'], '')
                        else:
                            raise ValueError('A very specific bad thing happened.') 
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
            return hotel_search_engine_endpoints_es(end_point, query_params)

        elif engine_type == 'PLACES':
            print('Places search engine in use!')
            return place_search_engine_endpoints_es(end_point, query_params)
            
        else:
            raise ValueError('Can not Find the Entered Type!, try -> HOTELS or PLACES!') 

