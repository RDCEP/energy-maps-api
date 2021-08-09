try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/TightOil_ShaleGas_US_Aug2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/TightOil_ShaleGas_US_Aug2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["Area_sq_mi"],
            "legend": "Tight Oil/Shale Gas",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "tight_oil_shale_gas"
        }

    json.dump(file_data, f)