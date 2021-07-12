import pandas as pd
import numpy as np
import requests
import json
import math
from search_engine.utils import data_parser as dp


class HotelSearchEngine:

    def __init__(self):
        self.headers = {
            'x-rapidapi-key': "1efa92d164msh01d90804f3853d5p17d12djsn8d02050ddb80",
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
        self.dojo_url = 'https://hotels4.p.rapidapi.com'

    # 'raw requests' methods:

    # get the location id to use it in other queries.
    def get_location_ids(self, loc: str):
        url = "https://hotels4.p.rapidapi.com/locations/search"

        response = requests.request("GET", url, headers=self.headers, params={"query": loc, "locale": "en_US"})
        return pd.DataFrame.from_dict(json.loads(response.text)['suggestions'][0]['entities'])['destinationId']

    # get the location id to use it in other queries.
    def get_city_id(self, loc: str):
        url = "https://hotels4.p.rapidapi.com/locations/search"

        response = requests.request("GET", url, headers=self.headers, params={"query": loc, "locale": "en_US"})
        jsn_data = json.loads(response.text)
        jsn_data = jsn_data['suggestions'][0]['entities']

        for idx in jsn_data:

            if idx['type'] == 'CITY':
                return idx['destinationId']

    # get a list of hotels by using the destination id.
    def get_hotels_by_des_id(self, destination_id, pn, check_in, check_out, adults, sort_order='PRICE', filters={}):
        url = "https://hotels4.p.rapidapi.com/properties/list"

        querystring = {"destinationId": destination_id,
                       "pageNumber": "1",
                       "checkIn": check_in,
                       "checkOut": check_out,
                       "pageSize": "10",
                       "adults1": adults,
                       "currency": "USD",
                       "locale": "en_US",
                       "sortOrder": sort_order}

        querystring.update(filters)

        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return response

    # get hotel information by using its destination_id
    def get_hotel_details(self, destination_id, pn=1, check_in="2021-03-12", check_out="2021-03-20", adults=1):
        url = "https://hotels4.p.rapidapi.com/properties/get-details"

        querystring = {"id": destination_id,
                       "locale": "en_US",
                       "currency": "USD",
                       "checkOut": check_out,
                       "adults1": adults,
                       "checkIn": check_in}

        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return response.text

    # parsing methods:

    # get a list of hotels from unparsed json file
    def get_search_results(self, jsn):
        return pd.DataFrame.from_dict(json.loads(jsn.text)['data']['body']['searchResults']['results'])



    def _clean_filters(self, json):
        return {
            'landmarks': json['landmarks']['items'][:10],
            'neighbourhood': json['neighbourhood']['items'][:10],
            'accommodationType': json['accommodationType']['items'][:10],
            'facilities': json['facilities']['items'][:10],
            'accessibility': json['accessibility']['items'][:10],
            'paymentPreference': json['paymentPreference']['items'][:10],
        }
    # get a list of filters from unparsed json file
    def get_search_filters(self, jsn):
        return self._clean_filters(json.loads(jsn.text)['data']['body']['filters'])

    # get the first hotel from unparsed json file
    def get_first_search_results(self, jsn):
        return json.loads(jsn.text)['data']['body']['searchResults']['results'][0]

    # basic end points:

    # general booking end_point -> search for hotels in a specific location.
    def search_location(self, loc, pn, check_in, check_out, adults, sort_order='PRICE', filters={}):
        '''
        sort_order : One of the following is allowed: 
        BEST_SELLER|
        STAR_RATING_HIGHEST_FIRST|
        STAR_RATING_LOWEST_FIRST|
        DISTANCE_FROM_LANDMARK|
        GUEST_RATING|
        PRICE_HIGHEST_FIRST|
        PRICE
        '''
        idx = self.get_city_id(loc)

        res = self.get_hotels_by_des_id(idx, pn, check_in, check_out, adults, sort_order, filters)

        df = self.get_search_results(res)

        df = dp.clean_results(df)

        jsn = self.get_search_filters(res)

        return {'HOTELS': dp.get_json_file(df),
                'FILTERS': jsn}

    #     return df

    # get parsed hotel information by using its destination_id.
    def hotel_details(self, destination_id: int):

        response = self.get_hotel_details(destination_id)

        return dp.parse_details(response)

    # searching for the best hotels in a specific location -> trip planning.
    def best_hotels_in_country(self, country):
        return self.search_location(country,
                                    1,
                                    "2020-01-01",
                                    "2021-01-01", 1,
                                    'STAR_RATING_HIGHEST_FIRST',
                                    {"guestRatingMin": "8"})['HOTELS']

    # find hotel information by using its name.
    def get_hotel_id_by_name(self, name: str):
        url = "https://hotels4.p.rapidapi.com/locations/search"

        querystring = {"query": name, "locale": "en_US"}

        response = requests.request("GET", url, headers=self.headers, params=querystring)

        return json.loads(response.text)['suggestions'][1]['entities'][0]['destinationId']

    def get_hotel_details_by_name(self, name: str):
        idx = self.get_hotel_id_by_name(name)
        res = self.hotel_details(idx)
        return res

    # get all available images of a specific hotel by using its id.
    def get_hotel_imgs(self, hotel_id):

        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

        response = requests.request("GET", url, headers=self.headers, params={"id": hotel_id})

        json_data = json.loads(response.text)
        imgs = []
        for idx in range(0, len(json_data['hotelImages'])):
            img = json_data['hotelImages'][idx]['baseUrl']
            img = img.replace('_{size}', '')
            imgs.append(img)
        return json.dumps(imgs)

    # get all available reviews of a specific hotel by using its id.
    def get_hotel_reviews(self, hotel_id: int, pn: int):

        url = "https://hotels4.p.rapidapi.com/reviews/list"

        querystring = {"id": hotel_id, "page": pn, "loc": "en_US"}

        response = requests.request("GET", url, headers=self.headers,
                                    params={"id": hotel_id, "page": pn, "loc": "en_US"})

        json_data = json.loads(response.text)['reviewData']['guestReviewGroups']['guestReviews'][0]['reviews']

        res = []
        for review in json_data:
            res.append({'user': review['recommendedBy'],
                        'rating': review['rating'],
                        'title': review['title'],
                        'review': review['summary']
                        })

        return json.dumps(res)
