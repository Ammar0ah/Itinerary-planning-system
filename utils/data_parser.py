import pandas as pd 
import json


def get_clean_rate(df):
    try:
        res = [] 
        for row in df['guestReviews']:
            if type(row) is dict:
                res.append(json.loads(json.dumps(row))['rating'])
            elif type(row) is float:
                res.append('')
        return res
    except: 
        return {}
    
def get_clean_address(df):
    try:
        res = []
        for row in df['address']:
            if type(row) is dict:
                res.append(json.loads(json.dumps(row))['locality'])
            elif type(row) is float:
                res.append('unknown')
        return res   
    except: 
        return {}

def get_clean_street(df):
    try:
        res = []
        for row in df['address']:
            if type(row) is dict:
                res.append(json.loads(json.dumps(row))['locality'])
            elif type(row) is float:
                res.append('unknown')
        return res 
    except: 
        return {}

def get_clean_offer(df):
    try:
        res = []
        for row in df['deals']:
            if type(row) is dict:
                res.append(json.loads(json.dumps(row))['specialDeal'][0])
            elif type(row) is float:
                res.append('unknown')
        return res  
    except: 
        return {}

def get_clean_url(df):
    try:
        res = []
        for row in df['optimizedThumbUrls']:
            if type(row) is dict:
                res.append(json.loads(json.dumps(row))['srpDesktop'])
            elif type(row) is float:
                res.append('unknown')
        return res 
    except: 
        return {}
    

def split_price_plan(df):
    try:
        price = []
        features = []
        for row in df['ratePlan']:
            if type(row) is dict:
                price.append({'old_price' :json.loads(json.dumps(row))['price']['exactCurrent'],
                               'new_price' : json.loads(json.dumps(row))['price']['current'],
                               })
                features.append({
                              'paymentPreference' : json.loads(json.dumps(row))['features']['paymentPreference'],
                              'noCCRequired': json.loads(json.dumps(row))['features']['noCCRequired']
                }
                )
            elif type(row) is float:
                price.append('')
                features.append('')
        return price, features
    except: 
        return {}

def get_json_file(df):
    result = df.to_json(orient="index")
    return json.loads(result)



# parsing hotel details....

def split_hotel_overview(jsn):
    try:
        json_data = json.loads(jsn)['data']['body']['overview']['overviewSections']
        res = {}
        for idx in range(0, len(json_data)):
            res.update(
               { json_data[idx]['type'] : json_data[idx]['content']}) 
        return res
    except: 
        return {}

def split_rooms_features(jsn):
    try:
        res = []
        json_data = json.loads(jsn)['data']['body']['propertyDescription']['roomTypeNames']
        for  room in json_data:
            if len(room) > 3:
                res.append(room)
        return {'ROOMS' : res}
    except: 
        return {}

def split_features(jsn):
    try:
        room_features = []
        json_data = json.loads(jsn)['data']['body']['amenities']
        for item in json_data[1]['listItems']:
            for ele in item['listItems']:
                room_features.append(ele)
        return{'ROOM_FEATURES' : room_features,
               'HOTEL_FEATURES' : json_data[0]['listItems']}
    except: 
        return {}

def hygiene(jsn):
    try:
        json_data = json.loads(jsn)['data']['body']['hygieneAndCleanliness']['title']
        return{'HYGIENE' : json_data}
    except: 
        return {}

def policies(jsn):
    try:
        json_data = json.loads(jsn)['data']['body']['smallPrint']['policies'][0]
        return{'POLICIES' : json_data}
    except: 
        return {}

def dining(jsn):
    json_data = json.loads(jsn)['data']['body']['specialFeatures']['sections']
    res = {}
    for idx in range(0, len(json_data)):
        res.update({json_data[idx]['heading'] : json_data[idx]['freeText']})
    return res

def coordinates(jsn):
    json_data = json.loads(jsn)['data']['body']['pdpHeader']['hotelLocation']['coordinates']
    return {'longitude' : json_data['longitude'],
            'latitude' : json_data['latitude'],
           }


def pets_and_net(jsn):
    try:
        json_data = json.loads(jsn)['data']['body']['atAGlance']['travellingOrInternet']
        return{'PETS' : json_data['travelling']['pets'],
              'INTERNET' : json_data['internet']}
    except: 
        return {}

def map_url(jsn):
    try:
        json_data = json_data = json.loads(jsn)['data']['body']['propertyDescription']['mapWidget']['staticMapUrl']
        return{'MAP_URL' : json_data}
    except: 
        return {}

def get_description(jsn):
    try:
        name = json.loads(jsn)['data']['body']['propertyDescription']['name']
        rate = json.loads(jsn)['data']['body']['propertyDescription']['starRating']
        price = json.loads(jsn)['data']['body']['propertyDescription']['featuredPrice']['currentPrice']['plain']
        return {'NAME' : name,
               'STAR_RATE': rate,
                'PRICE' : price}
    except: 
        return {}
    
    
def get_check_in_required(jsn):
     try:
        json_data = json.loads(jsn)['data']['body']['atAGlance']['keyFacts']['requiredAtCheckIn']
        return {'CHECKIN_REQUIRED' : json_data}
     except: 
        return {}

def parse_details(jsn):
    res = split_hotel_overview(jsn)
    res.update(get_description(jsn))
    res.update(coordinates(jsn))
    res.update(split_rooms_features(jsn))
    res.update(split_features(jsn))
    res.update(hygiene(jsn))
    res.update(dining(jsn))
    res.update(policies(jsn))
    res.update(pets_and_net(jsn))
    res.update(map_url(jsn))
    res.update(get_check_in_required(jsn))
    return res


def clean_results(df):
    df['price'], df['features'] = split_price_plan(df)

    df['guestrating'] = get_clean_rate(df)   

    df['street'] = get_clean_street(df)  
    
    df['imgURL'] = get_clean_url(df)
    
    df.address = get_clean_address(df)   
    
    return df[['id', 'name', 'starRating', 'guestrating','address', 'street',
        'price', 'features', 'imgURL', 'coordinate', 'deals']]
