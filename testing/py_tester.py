import pickle

from search_engine.search_engine import SearchEngine

search_engine = SearchEngine()
'''
Build Trips
'''
consts = {
        'locations': ['berlin', 'london','istanbul','riyadh'],  # 1
        'trip_mode': 'extended_trip',  # 2
        'food_importance': 3,  # 3
        'shop_importance': 1,  # 4
        'days_count': 6,  # 5
        'places_per_day': 5,  # 6
        'shop_dis': True,  # 7
        'places_preferences': {'HIS': 5, 'CUL': 10, 'SPO': 2, 'ARC': 10}  # 8
    }
trip = search_engine.plan_trip(constraints=consts)
print(trip)


# with open('samples/berlin_london_istanbul_riyadh_trip_data.pkl', 'wb') as output:
#     pickle.dump(trip, output, pickle.HIGHEST_PROTOCOL)

# with open('samples/milan_trip_data.pkl', 'rb') as input:
#     l_trip = pickle.load(input)
'''
Search Engine Queries
'''
booking_dict = {
    'location' : 'new yourk',
    'page_number' : 1,
    'check_in_date' : "2021-07-22",
    'check_out_date' : "2021-07-27",
    'adults' : 1,
    'sort_order' : 'GUEST_RATING
}

# res1 = search_engine.get('HOTELS', 'BOOK',booking_dict)
# print(res1)

# booking_dict = {
#     'id' : 487455
# }
# #
# res1 = search_engine.get('HOTELS', 'DETAILS',booking_dict)
# print(res1)
#
# res6 = search_engine.get('PLACES', 'LOCATION', {'name': 'england'})
# print(res6)

