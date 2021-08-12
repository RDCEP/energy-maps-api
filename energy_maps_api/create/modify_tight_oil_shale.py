try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/TightOil_ShaleGas_US_Aug2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/TightOil_ShaleGas_US_Aug2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "Area_sq_mi",
            "legend": "Tight Oil/Shale Gas",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": ""
        }

        feature["properties"]["type"] = {
            "primary": feature["properties"]["original"]["Lithology"].lower().replace(" ", "_").replace("&", "").replace("__", "_"),
            "secondary": "gas"
        }

    json.dump(file_data, f)