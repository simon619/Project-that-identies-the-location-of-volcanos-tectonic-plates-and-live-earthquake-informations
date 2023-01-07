import requests
import json
import folium
import csv
from datetime import date, timedelta


class Earth:

    def __init__(self):
        self.volcano_data = None
        self.eq_list = []
        self.earth_map = folium.Map(location=[0, 0], tiles="Cartodb Positron", zoom_start=2)

    def read_data(self):
        with open('Raw Data//volcano_location_data.json') as f:
            self.volcano_data = json.load(f)

        time_today = date.today()
        time_yesterday = date.today() - timedelta(days=1)
        csv_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={time_yesterday}&endtime{time_today}"
        self.eq_list = list(csv.DictReader(requests.get(csv_url).text.splitlines()))

    def earthquake_data(self):
        for i in range(len(self.eq_list)):
            pop_up = f"Magnitude: {self.eq_list[i]['mag']}, Type: {self.eq_list[i]['magType']}, Depth: {self.eq_list[i]['depth']}, Time: {self.eq_list[i]['time']}"
            lat, lng = float(self.eq_list[i]['latitude']), float(self.eq_list[i]['longitude'])
            rad = 100000 * float(self.eq_list[i]['mag'])
            marker = folium.Circle(radius=rad, location=(lat, lng), color='yellow', fill=False, popup=pop_up)
            self.earth_map.add_child(marker)
        print("Earthquake Data Added")

    def tectonic_data(self):
        with open('Raw Data//tectonicplates.csv', 'r') as csv_file:
            tectonic_plates_data = csv.reader(csv_file)

            for line in tectonic_plates_data:
                plate, lat, lng = line[0], float(line[1]), float(line[2])
                marker = folium.Circle(radius=5, location=(lat, lng), color='green', fill=True, popup=plate)
                self.earth_map.add_child(marker)

        print("Tectonic Plate Data Added")

    def volcanic_data(self):
        for i in range(len(self.volcano_data)):
            lat, lng, pop_up = self.volcano_data[i]['lat'], self.volcano_data[i]['lng'], self.volcano_data[i]['vn']
            marker = folium.map.Marker([lat, lng], icon=folium.Icon(color='red', icon='triangle'),
                                       popup=folium.map.Popup(pop_up))
            self.earth_map.add_child(marker)

        print("Volcano Data Added")


if __name__ == '__main__':
    obj = Earth()
    obj.read_data()
    obj.earthquake_data()
    obj.volcanic_data()
    obj.tectonic_data()
    obj.earth_map.save("Output//earth_map.html")
    print("A HTML File Has Been Created")
