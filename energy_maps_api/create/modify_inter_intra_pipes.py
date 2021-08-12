try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/NaturalGas_InterIntrastate_Pipelines_US.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/NaturalGas_InterIntrastate_Pipelines_US.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Gas pipelines",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "pipeline",
            "secondary": "gas"
        }

    json.dump(file_data, f, indent=2)