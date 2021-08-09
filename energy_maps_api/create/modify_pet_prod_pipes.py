try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/PetroleumProduct_Pipelines_US_Nov2014.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/PetroleumProduct_Pipelines_US_Nov2014.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": None,
            "legend": "Petroleum product pipelines",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "petroleum_product_pipelines"
        }

    json.dump(file_data, f)