import pickle

from search_engine.search_engine import SearchEngine

search_engine = SearchEngine()

trip = search_engine.collect_trip_components(['istanbul', 'dubai', 'madrid'], 8, ['REL', 'HIS', 'ARC'], 'focused_trip',
                                             False, False)

with open('samples/istanbul_dubai_madrid_trip_data.pkl', 'wb') as output:
    pickle.dump(list(trip), output, pickle.HIGHEST_PROTOCOL)

# trip = search_engine.collect_trip_components(['milan'], 3, ['HIS', 'CUL', ], 'extended_trip', False, True)
#
# with open('samples/milan_trip_data.pkl', 'wb') as output:
#     pickle.dump(list(trip), output, pickle.HIGHEST_PROTOCOL)

# with open('samples/milan_trip_data.pkl', 'rb') as input:
#     l_trip = pickle.load(input)


# res0 = search_engine.get('HOTELS', 'BESTCHOISE', {'location' : 'new yourk'})
# print(res0)

# res6 = search_engine.get('PLACES', 'LOCATION', {'name' : 'istanbul'})
# print(res6)
