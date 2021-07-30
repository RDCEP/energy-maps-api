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
        feature["properties"]["required"] = {
            "unit": None,
            # visual dimension
            "viz_dim": feature["properties"]["Atm_Dist"] + feature["properties"]["Vac_Dist"] + feature["properties"]["Cat_Crack"] + feature["properties"]["Visbreak"] + feature["properties"]["Cat_Reform"] + feature["properties"]["Desulfur"] + feature["properties"]["Coking"] + feature["properties"]["Hydro_Crac"] + feature["properties"]["Alky_Iso"],
            "legend": "Petroleum refineries",
            "years": []
        }

        feature["properties"]["optional"] = {
            "description": "",
            "name": "petroleum_refineries"
        }

    json.dump(file_data, f)