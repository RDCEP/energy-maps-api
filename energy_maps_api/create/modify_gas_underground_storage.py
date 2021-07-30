try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/NaturalGas_UndergroundStorage_US_July2014.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/NaturalGas_UndergroundStorage_US_July2014.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["WorkingGas"],
            "legend": "Gas underground storage",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "gas_underground_storage"
        }

    json.dump(file_data, f, indent=2)