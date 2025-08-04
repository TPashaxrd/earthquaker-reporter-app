import requests
import folium
from datetime import datetime, timezone
import webview
import tempfile

class EMap:
    def show_map(self):
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=50&orderby=time"
        response = requests.get(url).json()

        m = folium.Map(location=[0, 0], zoom_start=2)

        for feature in response['features']:
            coords = feature['geometry']['coordinates']
            properties = feature['properties']
            mag = properties['mag']
            place = properties['place']
            time = datetime.fromtimestamp(properties['time'] / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            popup = f"Yer: {place}<br>Şiddet: {mag}<br>Zaman: {time}"

            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=6 + mag if mag else 5,
                color="crimson",
                fill=True,
                fill_color="crimson",
                popup=popup
            ).add_to(m)

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        m.save(tmp_file.name)

        webview.create_window("🌍 Canlı Deprem Haritası", tmp_file.name, width=1200, height=800)
        webview.start()
