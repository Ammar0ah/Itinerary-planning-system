import pickle

from search_engine.search_engine import SearchEngine

search_engine = SearchEngine()

trip = search_engine.collect_trip_components(['istanbul'], 6, ['REL', 'HIS', 'ARC'], 'focused_trip',
                                             True, True)
#
# with open('samples/istanbul_dubai_madrid_trip_data.pkl', 'wb') as output:
#     pickle.dump(list(trip), output, pickle.HIGHEST_PROTOCOL)

# trip = search_engine.collect_trip_components(['milan'], 3, ['HIS', 'CUL', ], 'extended_trip', False, True)
#
# with open('samples/milan_trip_data.pkl', 'wb') as output:
#     pickle.dump(list(trip), output, pickle.HIGHEST_PROTOCOL)

# with open('samples/milan_trip_data.pkl', 'rb') as input:
#     l_trip = pickle.load(input)

# booking_dict = {
#     'location' : 'new yourk',
#     'page_number' : 1,
#     'check_in_date' : "2021-07-06",
#     'check_out_date' : "2021-07-20",
#     'adults' : 1,
#     'sort_order' : 'GUEST_RATING'
# }
# res1 = search_engine.get('HOTELS', 'BOOK', booking_dict)
# print(res1)

# res6 = search_engine.get('PLACES', 'LOCATION', {'name': 'london'})
# print(res6[:32])
print(trip)