try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/PowerPlants_US_2014Aug_R.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/PowerPlants_US_2014Aug_R.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["total_cap"],
            "legend": feature["properties"]["PrimaryFue"] + " power plants",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": feature["properties"]["primary_fu"] +"_power_plants"
        }

    json.dump(file_data, f)