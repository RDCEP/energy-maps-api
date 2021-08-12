try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/railrdl020.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/railrdl020.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Railroad",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "railroad",
            "secondary": None
        }

    json.dump(file_data, f)