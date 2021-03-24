import pandas as pd
import numpy as np
import requests 
import json
import math


dojo_url = 'https://hotels4.p.rapidapi.com'

headers = {
    'x-rapidapi-key': "xxxxxxxxx",
    'x-rapidapi-host': "hotels4.p.rapidapi.com"
    }

# get the location id to use it in other queries.
def get_location_ids(loc : str):
    url = "https://hotels4.p.rapidapi.com/locations/search"

    response = requests.request("GET", url, headers=headers, params={"query":loc,"locale":"en_US"})
    return pd.DataFrame.from_dict(json.loads(response.text)['suggestions'][0]['entities'])['destinationId']


# get the location id to use it in other queries.
def get_city_id(loc : str):
    url = "https://hotels4.p.rapidapi.com/locations/search"

    response = requests.request("GET", url, headers=headers, params={"query":loc,"locale":"en_US"})
    jsn_data = json.loads(response.text)
    jsn_data = jsn_data['suggestions'][0]['entities']

    for idx in jsn_data:
        
        if idx['type'] =='CITY':
            return idx['destinationId']
        
# get a list of hotels by using the destination id.
def get_hotels_by_des_id(destination_id, pn, check_in, check_out, adults, sort_order = 'PRICE', filters = {}):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId":destination_id,
                   "pageNumber":"1",
                   "checkIn": check_in,
                   "checkOut": check_out,
                   "pageSize":"10",
                   "adults1": adults,
                   "currency":"USD",
                   "locale":"en_US",
                   "sortOrder": sort_order}
    
    querystring.update(filters)
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    return  response

# get a list of hotels from unparsed json file
def get_search_results(jsn):
    return  pd.DataFrame.from_dict(json.loads(jsn.text)['data']['body']['searchResults']['results'])

# get a list of filters from unparsed json file
def get_search_filters(jsn):
    return  json.loads(jsn.text)['data']['body']['filters']

# get the first hotel from unparsed json file
def get_first_search_results(jsn):
    return  json.loads(jsn.text)['data']['body']['searchResults']['results'][0]

# get hotel information by using its destination_id
def get_hotel_details(destination_id, pn = 1, check_in = "2021-03-12", check_out = "2021-03-20", adults = 1):
    url = "https://hotels4.p.rapidapi.com/properties/get-details"

    querystring = {"id": destination_id ,
                   "locale":"en_US",
                   "currency":"USD",
                   "checkOut":check_out,
                   "adults1":adults,
                   "checkIn":check_in}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

# get hotel profile picture using its id
def get_hotel_prof_img(hotel_id : int):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id":hotel_id}

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)['hotelImages'][1]['baseUrl']
    return res.replace('_{size}','')

# get a list of hotels profile pictures to be displayed when user search for a location.
def get_page_hotels_imgs(df):
    res = []
    for row in df:
        img = handler.get_hotel_prof_img(row)
        res.append(img)
    return res

# get all available images of a specific hotel by using its id.
def get_hotel_imgs(hotel_id):

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    
    response = requests.request("GET", url, headers=headers, params={"id":hotel_id })
    
    json_data = json.loads(response.text)
    imgs= []
    for idx in range(0, len(json_data['hotelImages'])):
        img = json_data['hotelImages'][idx]['baseUrl']
        img = img.replace('_{size}','')
        imgs.append(img)
    return json.dumps(imgs)

# get all available reviews of a specific hotel by using its id.
def get_hotel_reviews(hotel_id : int , pn: int ):
    
    url = "https://hotels4.p.rapidapi.com/reviews/list"

    querystring = {"id":hotel_id ,"page": pn,"loc":"en_US"}

    response = requests.request("GET", url, headers=headers, params = {"id":hotel_id ,"page": pn,"loc":"en_US"})

    json_data = json.loads(response.text)['reviewData']['guestReviewGroups']['guestReviews'][0]['reviews']
    
    res = []
    for review in json_data:
        res.append({'user' : review['recommendedBy'],
                   'rating': review['rating'],
                   'title' : review['title'],
                    'review': review['summary']
        })
        
    return json.dumps(res)

# find hotel information by using its name. 
def get_hotel_id_by_name(name : str):
    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query":name ,"locale":"en_US"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    return json.loads(response.text)['suggestions'][1]['entities'][0]['destinationId']

