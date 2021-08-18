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

# Store all data files into array for iteration
files = []
for dirname, dirnames, filenames in os.walk('../../data/new_data'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

for file in files:
    with open(file, 'r') as f:
        file_data = json.loads(f.read())
        # logging to help discern which files are passing
        print('Attempted file: ' + file)
        print (file_data.keys())

        # Update these for new files
        # filter by the appropriate key for each file and log success
        # script will break on its own if there is an error
        if file_data.keys() == "dict_keys(['type', 'crs', 'features'])" or "dict_keys(['type', 'name', 'crs', 'features'])" or "dict_keys(['type', 'name', 'features'])" or "dict_keys(['type', 'features'])":
            collection_infrastructure.insert_many(file_data['features'])
            print('Successful file: ' + file)
        if file_data.keys() == "dict_keys(['type', 'arcs', 'transform', 'objects'])":
            collection_infrastructure.insert_many(file_data['objects'])
            print('Successful file: ' + file)
        if file_data.keys() == "dict_keys(['type', 'geometries'])":
            collection_infrastructure.insert_many(file_data['geometries'])
            print('Successful file: ' + file)


client.close()


