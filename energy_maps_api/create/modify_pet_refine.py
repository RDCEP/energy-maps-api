try:
    import simplejson as json
except ImportError:
    import json

processes = ['Atm_Dist', 'Vac_Dist', 'Cat_Crack', 'Visbreak',
      'Cat_Reform', 'Desulfur', 'Coking', 'Hydro_Crac', 'Alky_Iso']

with open('../../data/original_data/Petroleum_Refineries_US_2015.geojson', 'r') as f:
    file_data = json.loads(f.read())

with open('../../data/new_data/Petroleum_Refineries_US_2015.geojson', 'w') as f:
    for feature in file_data["features"]:
        feature["properties"] = { "original" : feature["properties"]}
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["original"]["Atm_Dist"] + feature["properties"]["original"]["Vac_Dist"] + feature["properties"]["original"]["Cat_Crack"] + feature["properties"]["original"]["Visbreak"] + feature["properties"]["original"]["Cat_Reform"] + feature["properties"]["original"]["Desulfur"] + feature["properties"]["original"]["Coking"] + feature["properties"]["original"]["Hydro_Crac"] + feature["properties"]["original"]["Alky_Iso"],
            "legend": "Petroleum refineries",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "petroleum_refineries"
        }

        feature["properties"]["type"] = {
            "primary": "refinery",
            "secondary": "petroleum"
        }

    json.dump(file_data, f)