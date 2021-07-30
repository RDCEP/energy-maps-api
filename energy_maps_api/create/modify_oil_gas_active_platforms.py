try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/Oil_Gas_Active_Platforms.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/Oil_Gas_Active_Platforms.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Oil/gas active platforms",
            "years": [feature["properties"]["INSTALL"],feature["properties"]["REMOVAL"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "oil_gas_active_platforms"
        }

    json.dump(file_data, f, indent=2)