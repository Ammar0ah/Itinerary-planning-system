import pandas as pd
import numpy as np
import requests 
import json
import math

otm_url = 'https://api.opentripmap.com/0.1/en/places'
otm_api_key = '5ae2e3f221c38a28845f05b6862cadcee936a16d50308813cb45978b'

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
def get_city_details(city_name):
    url = f'{otm_url}/geoname?name={city_name}&apikey={otm_api_key}'
    response = requests.request("GET", url)
    data = json.loads(response.text)
    return data

# get all available places in a specifice location.
def search_places(city_name, kind =''):    
    crds = get_city_details(city_name)
    
    if len(kind):
        kind = '&kinds={}'.format(kind)
        
    url = '{}/radius?radius=1000&lon={}&lat={}{}&apikey={}'.format(
        otm_url,
        crds['lon'],                                                                                            
        crds['lat'],                                                                                            
        kind,                  
        otm_api_key)
    
    response = requests.request("GET", url)
    
    return json.loads(response.text)

# get all the information about a group of places in a specific location.
def get_places_info(city_name, kind = ''):
    places_ids = search_places(city_name, kind)
    lis = []
    for xid in range(0 , len(places_ids['features'])):
        det = get_object_properties(places_ids['features'][xid]['properties']['xid'])
        lis.append(det)
    return lis

# available information about a place with a specifice object_id.
def get_object_properties(object_id : str): 
    url = '{}/xid/{}?apikey={}'.format(otm_url, object_id, otm_api_key)
    response = requests.request("GET" ,url)
    return json.loads(response.text)

# a list of places to be displayed when use search for a specific location.
def get_place_preview(list_of_places : list):
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


def get_list_of_places(city_name, kind = ''):
    row_data = get_places_info(city_name , kind)
    res = get_place_preview(row_data)
    return res

def get_place_features(city_name):
    data = search_places(city_name)['features']
    res = []
    for item in data:
        res.append({
            'id' : item['properties']['xid'],
            'name' : item['properties']['name'],
            'rate' : item['properties']['rate'],
            'kinds' : item['properties']['kinds'],
        })
    return res
