try:
    from energy_maps_api.main import EnergyMapsAPI
except ImportError:
    print('app not loading properly')
from energy_maps_api.constants import MONGO, URI
import os
from pymongo import MongoClient, mongo_client
try:
    import simplejson as json
except ImportError:
    import json
import pprint as pp


client = MongoClient(URI)
db = client[MONGO['database']]
collection_infrastructure = db['infrastructure']

# quick and dirty version

files = []
for dirname, dirnames, filenames in os.walk('../../data/json'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

UNICODE_ERRORS = [
    '../../data/json/.DS_Store',
    '../../data/json/wind-map/.DS_Store',
    '../../data/json/wind-map/windmap-output/.DS_Store'
]

for path in UNICODE_ERRORS:
    files.remove(path)

FAILING_FILES = [
    '../../data/json/states-10m.json',
    '../../data/json/wind-map/ws-clipped-merged-simplify20.json',
    '../../data/json/states-output/nation.json',
    '../../data/json/states-output/states-no-overlap.json'
]

for file in FAILING_FILES:
    with open(file, 'r') as f:
        file_data = json.loads(f.read())
        print(file, file_data.keys())

# The following 2 "failing files" upload successfully when you do them
# this way rather than iterativley with the rest. The first two
# indeces of FAILING_FILES won't go through manually either though.
with open(FAILING_FILES[2], 'r') as f:
    file_data = json.loads(f.read())
    print(file_data.keys())
    collection_infrastructure.insert_many(file_data['geometries'])

with open(FAILING_FILES[3], 'r') as f:
    file_data = json.loads(f.read())
    print(file_data.keys())
    collection_infrastructure.insert_many(file_data['geometries'])

for path in FAILING_FILES:
    files.remove(path)

for file in files:
    with open(file, 'r') as f:
        file_data = json.loads(f.read())
        print('Attempted file: ' + file)
        print (file_data.keys())

        if file_data.keys() == "dict_keys(['type', 'crs', 'features'])" or "dict_keys(['type', 'name', 'crs', 'features'])" or "dict_keys(['type', 'name', 'features'])" or "dict_keys(['type', 'features'])":
            collection_infrastructure.insert_many(file_data['features'])
            print('Successful file: ' + file)
        if file_data.keys() == "dict_keys(['type', 'arcs', 'transform', 'objects'])":
            collection_infrastructure.insert_many(file_data['objects'])
            print('Successful file: ' + file)
        if file_data.keys() == "dict_keys(['type', 'geometries'])":
            collection_infrastructure.insert_many(file_data['geometries'])
            print('Successful file: ' + file)

# This method had things failing seemingly arbitrarily.
        # try:
        #     print('successful file: ' + file)
        #     print(file_data.keys())
        #     collection_infrastructure.insert_many(file_data['features'])
        # except: 
        #     collection_infrastructure.insert_many(file_data['objects'])
        #     print('OBJECTS FILE: ' + file, file_data.keys())
        # finally:
        #      print('GEOMETRIES FILE: ' + file, file_data.keys())
        #      collection_infrastructure.insert_many(file_data['geometries'])

client.close()

# with open('../../data/json/test_file.geojson', 'r') as f:
#     file_data = json.load(f)

# collection_infrastructure.insert_one(file_data)
# client.close()

# api = EnergyMapsAPI()

# read a file and convert to dict
# with open('../../data/json/test_file.geojson', 'r') as f:
#     file_data = json.load(f)
# pp.pprint(file_data)

# modify the schema 

# with open('../../data/json/test_file.geojson', 'w') as f:
#     json.dump(file_data, f)

# upload to single massive collection
# create index upon collection instantiation
# index should update automatically


