try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/NaturalGas_ProcessingPlants_US_2014.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/NaturalGas_ProcessingPlants_US_2014.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": "PlantCapac",
            "legend": "Gas processing plants",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "gas_proc_plants"
        }

        feature["properties"]["type"] = {
            "primary": "processing_plant",
            "secondary": "gas"
        }

    json.dump(file_data, f)