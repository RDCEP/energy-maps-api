try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/PowerPlants_US_2014Aug_R.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/PowerPlants_US_2014Aug_R.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "total_cap",
            "legend": feature["properties"]["original"]["PrimaryFue"] + " power plants",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": ""
        }

        feature["properties"]["type"] = {
            "primary": "power_plant",
            "secondary": feature["properties"]["original"]["PrimaryFue"].lower()
        }

    json.dump(file_data, f, indent=2)