try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/SPR_Aug2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/SPR_Aug2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["Capacity"],
            "legend": "Strategic petroleum reserves",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "spr"
        }

    json.dump(file_data, f)