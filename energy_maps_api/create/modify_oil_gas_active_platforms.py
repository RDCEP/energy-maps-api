try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/Oil_Gas_Active_Platforms.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/Oil_Gas_Active_Platforms.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Oil/gas active platforms",
            "years": [feature["properties"]["original"]["INSTALL"],feature["properties"]["original"]["REMOVAL"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "active_platforms",
            "secondary": "oil_gas"
        }

    json.dump(file_data, f)