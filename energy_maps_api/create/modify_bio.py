try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/biodiesel.json', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/biodiesel.json', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Biodiesel",
            "years": [feature["properties"]["Data_Perio"]]
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "biodiesel"
        }

    json.dump(file_data, f, indent=2)