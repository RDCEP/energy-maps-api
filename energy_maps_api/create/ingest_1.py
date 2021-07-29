# from energy_maps_api.constants import MONGO, URI
from pymongo import MongoClient, collection
try:
    import simplejson as json
except ImportError:
    import json
import pprint as pp

# client = MongoClient(URI)
# db = client[MONGO['database']]
# collection_infrastructure = db['infrastructure']

with open('../../data/original_data/test_file.geojson', 'r') as f:
    test_file_data = json.loads(f.read())

with open('../../data/new_data/test_file_output.geojson', 'w') as f:
    for feature in test_file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            "big_tits_key": "tot_prod",
            "legend": "Coal Mines",
            "years": [feature["properties"]["year"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "coal_mine"
        }

    json.dump(test_file_data, f, indent=2)