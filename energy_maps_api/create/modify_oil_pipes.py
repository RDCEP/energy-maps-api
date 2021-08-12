try:
    import simplejson as json
except ImportError:
    import json


with open('../../data/original_data/CrudeOil_Pipelines_US_Nov2014.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/CrudeOil_Pipelines_US_Nov2014.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Oil pipelines",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
        }

        feature["properties"]["type"] = {
            "primary": "pipeline",
            "secondary": "oil"
        }

    json.dump(file_data, f)