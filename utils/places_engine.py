import pandas as pd
import numpy as np
import requests 
import json
import math
class PlacesSearchEngine:
    def __init__(self):
        self.otm_url = 'https://api.opentripmap.com/0.1/en/places'
        self.otm_api_key = '5ae2e3f221c38a28845f05b6862cadcee936a16d50308813cb45978b'

    # kinds such as: 
    '''
        fuel,
        sport,
        restaurants,
        churches,
        mosques,
        beaches,
        historic,

        natural
        tourist_facilities,
            banks,
            food,
            transport,
            shops,

        cultural,
            theatres_and_entertainments
            museums
    '''
    # get specific city information like latitude and longitude. 
    def get_city_details(self, city_name):
        url = f'{self.otm_url}/geoname?name={city_name}&apikey={self.otm_api_key}'
        response = requests.request("GET", url)
        data = json.loads(response.text)
        return data

    # get all available places in a specifice location.
    def search_places(self, city_name, kind =''):    
        crds = self.get_city_details(city_name)

        if len(kind):
            kind = '&kinds={}'.format(kind)

        url = '{}/radius?radius=200000&lon={}&lat={}{}&apikey={}'.format(
            self.otm_url,
            crds['lon'],                                                                                            
            crds['lat'],                                                                                            
            kind,                  
            self.otm_api_key)

        response = requests.request("GET", url)

        return json.loads(response.text)
    
    # get all available places in location using the coordinates.
    def search_places_by_coords(self, latitude, longitude, kind =''):    
        if len(kind):
            kind = '&kinds={}'.format(kind)

        url = '{}/radius?radius=200000&lon={}&lat={}{}&apikey={}'.format(
            self.otm_url,
            longitude,                                                                                            
            latitude,                                                                                            
            kind,                  
            self.otm_api_key)

        response = requests.request("GET", url)

        return json.loads(response.text)
    
    def get_top_rated_places(self, latitude, longitude, places_count, kind = ''):
        res_plcs = self.search_places_by_coords(latitude, longitude, kind)['features']
        res_plcs = self.clean_results(res_plcs)
        wanted_items = []
        for idx, item in enumerate(res_plcs):
            wanted_items.append((idx, item['guestrating']))
        wanted_items.sort(key=lambda tup: tup[1],  reverse=True)  # sorts in place
        
        fnl_res = []
        for idx, _ in wanted_items[:places_count]:
            fnl_res.append(res_plcs[idx])   
        return fnl_res
    # get all the information about a group of places in a specific location.
    def get_places_info(self, city_name, kind = ''):
        places_ids = self.search_places(city_name, kind)
        lis = []
#         range_ =  len(places_ids['features'])
        range_ = 3
        for xid in range(0 , range_):
            det = self.get_object_properties(places_ids['features'][xid]['properties']['xid'])
            lis.append(det)
        return lis

    # available information about a place with a specifice object_id.
    def get_object_properties(self, object_id : str): 
        url = '{}/xid/{}?apikey={}'.format(self.otm_url, object_id, self.otm_api_key)
        response = requests.request("GET" ,url)
        return json.loads(response.text)

    # a list of places to be displayed when use search for a specific location.
    def get_place_preview(self, list_of_places : list):
        fnl = []
        for place in list_of_places:
            dict = {
                'xid' : place['xid'],
                'name' : place['name'],
                'rate' : place['rate'],
            }
            try: 
                dict.update({'img_url' : place['image']})
            except: 
                pass
            fnl.append(dict)
        return fnl


    def get_list_of_places(self, city_name, kind = ''):
        row_data = self.get_places_info(city_name , kind)
        res = self.get_place_preview(row_data[:2])
        return res

    def clean_results(self, data):
        res = []
        for item in data:
            res.append({
                'id' : item['properties']['xid'],
                'name' : item['properties']['name'],
                'guestrating' : item['properties']['rate'],
                'kinds' : item['properties']['kinds'],
                'distance' : item['properties']['dist'],
                'coordinate' : {'lat' : item['geometry']['coordinates'][1],
                                'lon' : item['geometry']['coordinates'][0]}
            })
        return res
    
    def get_place_features(self, city_name, kinds):
        data = self.search_places(city_name, kinds)['features']
        res = []
        return self.clean_results(data)

    # get specific city information like latitude and longitude. 
    def get_closest_places(self, latitude, longitude, radius, kind = ''):
        if len(kind):
            kind = '&kinds={}'.format(kind)

        url = '{}/radius?radius={}&lon={}&lat={}{}&apikey={}'.format(
            self.otm_url,
            radius,
            longitude,                                                                                            
            latitude,                                                                                            
            kind,                  
            self.otm_api_key)

        response = requests.request("GET", url)

        return json.loads(response.text)