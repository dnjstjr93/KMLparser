from fastkml import kml
import json
import os

KML_DIR = './KML/'

JSON_DIR = './JSON/'
if not os.path.isdir(JSON_DIR):
    os.mkdir(JSON_DIR)

# KMLFILE = KML_DIR + "booyeo.kml"
KMLFILE = KML_DIR + "hwasung.kml"

file_name = KMLFILE.split('/')[-1].split('.')[0]
with open(KMLFILE) as f:
    doc = f.read().encode()

INPUT = kml.KML()
OUTPUT = kml.KML()
INPUT.from_string(doc)
FEATURES = list(INPUT.features())
placemark = list(FEATURES[0].features())
coordinates = list(placemark[0].geometry.coords)

umac6_data = dict()
umac6_data["name"] = "UMAC6"
umac6_data["gcs"] = "KETI_MUV"
umac6_data["goto_position"] = ["cancel"]
umac6_data["system_id"] = 6

umac7_data = dict()
umac7_data["name"] = "UMAC7"
umac7_data["gcs"] = "KETI_MUV"
umac7_data["goto_position"] = ["cancel"]
umac7_data["system_id"] = 7

umac8_data = dict()
umac8_data["name"] = "UMAC8"
umac8_data["gcs"] = "KETI_MUV"
umac8_data["goto_position"] = ["cancel"]
umac8_data["system_id"] = 8

for idx in range(1, len(coordinates)):
    lat = coordinates[idx][1]
    lon = coordinates[idx][0]
    alt = coordinates[idx][2]

    temp_alt = coordinates[1][2]

    data = "%.7f:%.7f:%.1f:%.1f" % (lat, lon, 100.0, 10.0)
    if alt == temp_alt:  # alttitude = 50 in QGC
        umac6_data["goto_position"].append(data)
    elif alt == temp_alt + 50:  # alttitude = 100 in QGC
        umac7_data["goto_position"].append(data)
    elif alt == temp_alt + 100:  # alttitude = 150 in QGC
        umac8_data["goto_position"].append(data)

with open(JSON_DIR + file_name + '_UMAC6.json', 'w', encoding='utf-8') as make_file:
    json.dump(umac6_data, make_file, indent="\t")

with open(JSON_DIR + file_name + '_UMAC7.json', 'w', encoding='utf-8') as make_file:
    json.dump(umac7_data, make_file, indent="\t")

with open(JSON_DIR + file_name + '_UMAC8.json', 'w', encoding='utf-8') as make_file:
    json.dump(umac8_data, make_file, indent="\t")
