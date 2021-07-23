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


# quick and dirty version
client = MongoClient('mongodb+srv://dev:lB1MU5zzBb8MOmIn@cluster0.gjutf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['energy_maps_db']
collection_infrastructure = db['infrastructure']

files = []
for dirname, dirnames, filenames in os.walk('../../data/json'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

files.remove('../../data/json/.DS_Store')
# pp.pprint(files)

for file in files:
    with open(file, 'r') as f:
        try:
            file_data = json.loads(f.read())
            print(file_data.keys())
            collection_infrastructure.insert_many(file_data['features'])
        except: 
            print('failed file:' + file)


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


