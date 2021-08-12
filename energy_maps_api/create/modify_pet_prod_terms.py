try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/PetroleumProduct_Terminals_US_Aug2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/PetroleumProduct_Terminals_US_Aug2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Petroleum product terminals",
            "years": [feature["properties"]["original"]["Data_perio"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "terminal",
            "secondary": "petroleum_product"
        }

    json.dump(file_data, f)