try:
    import simplejson as json
except ImportError:
    import json

with open('../../data/original_data/TX_CAPCOG_wells.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/TX_CAPCOG_wells.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["AQUIFER"],
            "legend": "TX CAPCOG wells",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "Texas Capital Area Council of Governments wells",
            "name": "tx_capcog_wells"
        }

    json.dump(file_data, f)