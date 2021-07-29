try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/LNG_ImpExp_Terminals_US_2013.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/LNG_ImpExp_Terminals_US_2013.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "Storage_Ca", 
            "function": feature["properties"]["Function"],
            "legend": "Import/Export Terminals",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "imp_exp_terminals"
        }

    json.dump(file_data, f)