try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/biodiesel.json', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/biodiesel.json', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Biodiesel",
            "years": [feature["properties"]["original"]["Data_Perio"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "biodiesel",
            "secondary": None
        }

    json.dump(file_data, f)