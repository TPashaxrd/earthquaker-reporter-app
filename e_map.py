import requests
import folium
from datetime import datetime, timezone, timedelta
import webview
import tempfile
import time
import threading

class EMap:
    def __init__(self):
        self.last_update = None
        self.update_interval = 300
        self.is_live = False
        
    def get_earthquake_data(self):
        """Get earthquake data from multiple sources for better coverage"""
        earthquakes = []
        
        try:
            usgs_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
            response = requests.get(usgs_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for feature in data['features']:
                    coords = feature['geometry']['coordinates']
                    props = feature['properties']
                    
                    time_value = props.get('time')
                    if isinstance(time_value, str):
                        try:
                            time_value = int(time_value)
                        except (ValueError, TypeError):
                            time_value = int(time.time() * 1000) 
                    
                    earthquake = {
                        'latitude': coords[1],
                        'longitude': coords[0],
                        'magnitude': props.get('mag'),
                        'place': props.get('place', 'Unknown location'),
                        'time': time_value,
                        'depth': coords[2],
                        'type': props.get('type', 'earthquake'),
                        'alert': props.get('alert'),
                        'tsunami': props.get('tsunami', 0),
                        'felt': props.get('felt'),
                        'cdi': props.get('cdi'),
                        'mmi': props.get('mmi'),
                        'source': 'USGS'
                    }
                    earthquakes.append(earthquake)
            
            try:
                emsc_url = "https://www.seismicportal.eu/fdsnws/event/1/query?format=json&limit=100&orderby=time-desc"
                emsc_response = requests.get(emsc_url, timeout=10)
                if emsc_response.status_code == 200:
                    emsc_data = emsc_response.json()
                    for event in emsc_data.get('features', []):
                        coords = event['geometry']['coordinates']
                        props = event['properties']
                        
                        time_value = props.get('time')
                        if isinstance(time_value, str):
                            try:
                                time_value = int(time_value)
                            except (ValueError, TypeError):
                                time_value = int(time.time() * 1000) 
                        
                        existing = any(
                            abs(eq['latitude'] - coords[1]) < 0.1 and 
                            abs(eq['longitude'] - coords[0]) < 0.1 and 
                            abs(eq['time'] - time_value) < 60000
                            for eq in earthquakes
                        )
                        
                        if not existing:
                            earthquake = {
                                'latitude': coords[1],
                                'longitude': coords[0],
                                'magnitude': props.get('mag'),
                                'place': props.get('flynn_region', 'Unknown location'),
                                'time': time_value,
                                'depth': coords[2],
                                'type': 'earthquake',
                                'alert': None,
                                'tsunami': 0,
                                'felt': None,
                                'cdi': None,
                                'mmi': None,
                                'source': 'EMSC'
                            }
                            earthquakes.append(earthquake)
            except Exception as e:
                print(f"EMSC API error: {e}")
                
        except Exception as e:
            print(f"Error fetching earthquake data: {e}")
            return []
        
        valid_earthquakes = [eq for eq in earthquakes if isinstance(eq['time'], (int, float)) and eq['time'] > 0]
        
        valid_earthquakes.sort(key=lambda x: x['time'], reverse=True)
        
        unique_earthquakes = []
        seen = set()
        for eq in valid_earthquakes:
            key = (round(eq['latitude'], 2), round(eq['longitude'], 2), eq['time'] // 60000)  
            if key not in seen:
                seen.add(key)
                unique_earthquakes.append(eq)
        
        return unique_earthquakes[:100]

    def get_magnitude_color(self, mag, alert=None):
        """Get color based on magnitude and alert level"""
        if alert == 'red':
            return '#ff0000' 
        elif alert == 'orange':
            return '#ff6600' 
        elif alert == 'yellow':
            return '#ffcc00' 
        elif mag is None:
            return '#666666'
        elif mag >= 6.0:
            return '#ff4c4c'
        elif mag >= 4.5:
            return '#ffa726'
        else:
            return '#66bb6a'

    def get_magnitude_size(self, mag):
        """Get marker size based on magnitude"""
        if mag is None:
            return 5
        elif mag >= 6.0:
            return 12 + mag * 2
        elif mag >= 4.5:
            return 8 + mag * 1.5
        else:
            return 6 + mag

    def format_time(self, timestamp):
        """Format timestamp to readable time"""
        if timestamp and isinstance(timestamp, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
                now = datetime.now(timezone.utc)
                diff = now - dt
                
                if diff.total_seconds() < 3600:
                    minutes = int(diff.total_seconds() / 60)
                    return f"{minutes} minutes ago"
                elif diff.total_seconds() < 86400:
                    hours = int(diff.total_seconds() / 3600)
                    return f"{hours} hours ago"
                else:
                    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
            except (ValueError, OSError):
                return "Unknown"
        return "Unknown"

    def create_popup_content(self, eq):
        """Create enhanced popup content with detailed information"""
        mag_class = "magnitude-low"
        if eq['magnitude']:
            if eq['magnitude'] >= 6.0:
                mag_class = "magnitude-high"
            elif eq['magnitude'] >= 4.5:
                mag_class = "magnitude-medium"
        
        alert_icon = ""
        if eq['alert']:
            alert_icons = {'red': '🔴', 'orange': '🟠', 'yellow': '🟡', 'green': '🟢'}
            alert_icon = alert_icons.get(eq['alert'], '')
        
        tsunami_warning = "🌊 TSUNAMI WARNING" if eq['tsunami'] == 1 else ""
        
        popup_html = f"""
        <div class="custom-popup">
            <div class="popup-header">
                🌍 Earthquake Alert {alert_icon}
            </div>
            <div class="popup-content">
                <div class="popup-item">
                    <div class="popup-label">📍 Location</div>
                    <div class="popup-value">{eq['place']}</div>
                </div>
                <div class="popup-item">
                    <div class="popup-label">📏 Magnitude</div>
                    <div class="popup-value {mag_class}">{eq['magnitude'] if eq['magnitude'] else 'N/A'}</div>
                </div>
                <div class="popup-item">
                    <div class="popup-label">⬇️ Depth</div>
                    <div class="popup-value">{eq['depth']:.1f} km</div>
                </div>
                <div class="popup-item">
                    <div class="popup-label">⏰ Time</div>
                    <div class="popup-value">{self.format_time(eq['time'])}</div>
                </div>
                <div class="popup-item">
                    <div class="popup-label">📡 Source</div>
                    <div class="popup-value">{eq['source']}</div>
                </div>
                {f'<div class="popup-item"><div class="popup-label">🌊 Tsunami</div><div class="popup-value tsunami-warning">{tsunami_warning}</div></div>' if eq['tsunami'] == 1 else ''}
                {f'<div class="popup-item"><div class="popup-label">👥 Felt Reports</div><div class="popup-value">{eq["felt"]} people</div></div>' if eq['felt'] else ''}
            </div>
        </div>
        """
        return popup_html

    def show_map(self):
        """Display the earthquake map with live data"""
        earthquakes = self.get_earthquake_data()
        
        if not earthquakes:
            print("No earthquake data available")
            return
        
        m = folium.Map(
            location=[0, 0], 
            zoom_start=2,
            tiles='CartoDB dark_matter',
            prefer_canvas=True
        )

        custom_css = """
        <style>
        .custom-popup {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            border: 2px solid #ff4c4c;
            border-radius: 12px;
            padding: 0;
            margin: 0;
            box-shadow: 0 4px 20px rgba(255, 76, 76, 0.3);
        }
        .popup-header {
            background: linear-gradient(135deg, #ff4c4c, #e63b3b);
            color: white;
            padding: 12px 16px;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
            font-size: 14px;
            text-align: center;
            border-bottom: 1px solid #ff4c4c;
        }
        .popup-content {
            padding: 16px;
            color: #ffffff;
            background: #1a1a1a;
            border-radius: 0 0 10px 10px;
        }
        .popup-item {
            margin: 8px 0;
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }
        .popup-item:last-child {
            border-bottom: none;
        }
        .popup-label {
            color: #ff4c4c;
            font-weight: bold;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .popup-value {
            color: #ffffff;
            font-size: 13px;
            margin-top: 4px;
        }
        .magnitude-high {
            color: #ff4c4c;
            font-weight: bold;
        }
        .magnitude-medium {
            color: #ffa726;
            font-weight: bold;
        }
        .magnitude-low {
            color: #66bb6a;
            font-weight: bold;
        }
        .tsunami-warning {
            color: #ff4c4c;
            font-weight: bold;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.5; }
        }
        </style>
        """

        m.get_root().header.add_child(folium.Element(custom_css))

        for eq in earthquakes:
            color = self.get_magnitude_color(eq['magnitude'], eq['alert'])
            size = self.get_magnitude_size(eq['magnitude'])
            
            folium.CircleMarker(
                location=[eq['latitude'], eq['longitude']],
                radius=size,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                weight=2,
                popup=folium.Popup(self.create_popup_content(eq), max_width=350),
                tooltip=f"Magnitude: {eq['magnitude'] if eq['magnitude'] else 'N/A'} - {eq['place']}"
            ).add_to(m)

        legend_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 250px; height: 180px; 
                    background-color: rgba(26, 26, 26, 0.95);
                    border: 2px solid #ff4c4c; border-radius: 10px; 
                    padding: 15px; font-size: 12px; color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    z-index: 1000;">
        <div style="text-align: center; font-weight: bold; margin-bottom: 15px; color: #ff4c4c;">
        🌍 Live Earthquake Map
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #ff4c4c;">●</span> High (≥6.0) / Red Alert
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #ffa726;">●</span> Medium (4.5-5.9) / Orange Alert
        </div>
        <div style="margin: 8px 0;">
            <span style="color: #66bb6a;">●</span> Low (<4.5) / Green Alert
        </div>
        <div style="margin: 8px 0; font-size: 10px; color: #888;">
        Last updated: {datetime.now().strftime('%H:%M:%S')}
        </div>
        <div style="margin: 8px 0; font-size: 10px; color: #888;">
        Data: USGS + EMSC
        </div>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        m.save(tmp_file.name)

        webview.create_window(
            "🌍 Earthquake Detective - Live Earthquake Map", 
            tmp_file.name, 
            width=1400, 
            height=900,
            resizable=True,
            min_size=(800, 600)
        )
        webview.start()