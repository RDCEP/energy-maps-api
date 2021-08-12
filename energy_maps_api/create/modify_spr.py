try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/SPR_Aug2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/SPR_Aug2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "Capacity",
            "legend": "Strategic petroleum reserves",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "spr"
        }

        feature["properties"]["type"] = {
            "primary": "strategic_reserve",
            "secondary": "petroleum"
        }

    json.dump(file_data, f)