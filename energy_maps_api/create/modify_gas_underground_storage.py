try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/NaturalGas_UndergroundStorage_US_July2014.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/NaturalGas_UndergroundStorage_US_July2014.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "WorkingGas",
            "legend": "Gas underground storage",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "underground_storage",
            "secondary": "gas"
        }

    json.dump(file_data, f)