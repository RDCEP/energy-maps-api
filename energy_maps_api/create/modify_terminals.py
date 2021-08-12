try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/LNG_ImpExp_Terminals_US_2013.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/LNG_ImpExp_Terminals_US_2013.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "Storage_Ca",
            "legend": feature["properties"]["original"]["Function"].capitalize() + " terminals",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": ""
        }

        feature["properties"]["type"] = {
            "primary": "terminal",
            "secondary": feature["properties"]["original"]["Function"].lower().replace(" ", "_")
        }

    json.dump(file_data, f)