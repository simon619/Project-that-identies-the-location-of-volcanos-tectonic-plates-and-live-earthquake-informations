import requests
import json
import folium
import csv
from datetime import date, timedelta


with open('Raw Data//volcano_location_data.json') as f:
    volcano_data = json.load(f)


lon, lat = 0, 0
mapa = folium.Map(location=[lat, lon], tiles="Cartodb Positron", zoom_start=2)

for i in range(len(volcano_data)):
    lat, lng, pop_up = volcano_data[i]['lat'], volcano_data[i]['lng'], volcano_data[i]['vn']
    marker = folium.map.Marker([lat, lng], icon=folium.Icon(color='red', icon='triangle'), popup=folium.map.Popup(pop_up))
    mapa.add_child(marker)


with open('Raw Data//tectonicplates.csv', 'r') as csv_file:
    tectonic_plates_data = csv.reader(csv_file)

    for line in tectonic_plates_data:
        # print(line[1], line[2])
        plate, lat, lng = line[0], float(line[1]), float(line[2])
        marker = folium.Circle(radius=5, location=(lat, lng), color='green', fill=True, popup=plate)
        mapa.add_child(marker)

time_today = date.today()
time_yesterday = date.today() - timedelta(days=1)
csv_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={time_yesterday}&endtime{time_today}"
eq_list = list(csv.DictReader(requests.get(csv_url).text.splitlines()))
print(eq_list)

for i in range(len(eq_list)):
    pop_up = f"Magnitude: {eq_list[i]['mag']}, Type: {eq_list[i]['magType']}, Depth: {eq_list[i]['depth']}, Time: {eq_list[i]['time']}"
    lat, lng = float(eq_list[i]['latitude']), float(eq_list[i]['longitude'])
    rad = 100000 * float(eq_list[i]['mag'])
    marker = folium.Circle(radius=rad, location=(lat, lng), color='yellow', fill=False, popup=pop_up)
    mapa.add_child(marker)



mapa.save("map.html")

#
# marker = folium.Circle([lat, lng], icon=folium.Icon(icon_color='#000000', icon='ban-circle', prefix='fa'), popup=plate)
