import json

with open('volcano_location_raw_json_data.json') as f:
    purified_volcano_data = json.load(f)

with open('volcano_location_data.json', 'w') as file:
    json.dump(purified_volcano_data, file, indent=2)
#



