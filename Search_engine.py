from utils.hotels_engine import HotelSearchEngine as Hotels
from utils.places_engine import PlacesSearchEngine as Places
from enum import Enum

class Search_Engine:
    def __init__(self):
        self.hotels = Hotels()
        self.places = Places()
    
    class engine_types(Enum):
        HOTELS = 1,
        PLACES = 2,
        
    class hse_end_points(Enum):
        BOOK = 1, #location_name & other booking information 'dict'
        DETAILS = 2, #hotel_id 'int'
        IMAGES = 3,   #hotel_id 'int'
        REVIEWS = 4,  #hotel_id 'int'
        HOTEL = 5,    #hotel_name 'str'

    class pse_end_points(Enum):
        DETAILS = 1, #place_id : str
        LOCATION = 2, #place_name & wanted_filters
        LISTVIEW = 3, #place_name & wanted_filters
        
    def get(self, engine_type, end_point ,query_params):

        def hotel_search_engine_endpoint(end_point, query_params):
            booking_query_params = [
                'location',
                'page_number',
                'adults',
                'check_in_date',
                'check_out_date',
            ]
            if end_point not in self.hse_end_points.__members__:
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
                elif end_point == 'HOTEL':      
                    if 'name' in query_params:
                        return self.hotels.get_hotel_details_by_name(query_params['name'])
                    else:
                        raise ValueError('A very specific bad thing happened.')       
                elif end_point == 'REVIEWS':      
                    if 'id' in query_params and 'page_number' in query_params:
                        return self.hotels.get_hotel_reviews(query_params['id'], query_params['page_number'])
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
        def place_search_engine_endpoint(end_point, query_params):
            if end_point not in self.pse_end_points.__members__:
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

        if engine_type == 'HOTELS':
            print('Hotels search engine in use!')
            return hotel_search_engine_endpoint(end_point, query_params)

        elif engine_type == 'PLACES':
            print('Places search engine in use!')
            return place_search_engine_endpoint(end_point, query_params)

