import threading
import time
import webbrowser
import pystray
import os
import sys
import win32com.client
from PIL import Image, ImageDraw
import tkinter as tk
import widget
from webhook import send_discord_alert
from deprem import get_latest_earthquake
from screen import show_alert
from settings import SettingsWindow
from dashboard import start_dashboard
from notif import start_notification
from auto_start import add_to_startup as add_startup_func
from have_connection import have_connection
from last_deprem import last_deprem
from e_map import EMap
from donate import donates

def log_earthquake(dep):
    try:
        with open("earthquake_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{dep['id']} | {dep['yer']} | Magnitude: {dep['buyukluk']}\n")
    except Exception as e:
        print(f"[LOG HATA] {e}")

class DepremApp:
    def __init__(self):
        self.SON_DEPREM_ID = None
        self.alarm_active = True
        self.alarm_threshold = 6
        self.settings_window = None
        self.main_window = None
        self.icon = None

        self.root = tk.Tk()
        self.root.withdraw()

        start_notification()
        self.start_tray()
        self.start_widget()
        self.start_dashboard()

        threading.Thread(target=self.kontrol_et, daemon=True).start()

        send_discord_alert("🤖 **Deprem Dedektörü Bot Başladı!**")

        self.root.mainloop()

    def create_image(self):
        image = Image.new('RGB', (64, 64), color='red')
        d = ImageDraw.Draw(image)
        d.rectangle([16, 16, 48, 48], fill='white')
        return image

    def start_tray(self):
        self.icon = pystray.Icon("deprem_dedektoru", self.create_image(), "Earthquake Detector")
        self.icon.menu = pystray.Menu(
            pystray.MenuItem("⚙️ Settings", self.open_settings),
            pystray.MenuItem("📍 Show Map", lambda icon, item: self.root.after(0, lambda: EMap().show_map())),
            pystray.MenuItem("🌍 Last Earthquakes", lambda icon, item: last_deprem()),
            pystray.MenuItem("🔔 Send Test Alert", lambda icon, item: show_alert("Test Alert", 5.0)),
            pystray.MenuItem("📊 Open Dashboard", lambda icon, item: webbrowser.open("http://127.0.0.1:8080/")),
            pystray.MenuItem("🚫 Disturb Mode (Mute Alarms)", lambda icon, item: setattr(self, 'alarm_active', False)),
            pystray.MenuItem("🔄 Restart Application", lambda icon, item: self.root.quit()),
            pystray.MenuItem("❌ Exit Application", lambda icon, item: icon.stop()),
            pystray.MenuItem("💰 Donate", lambda icon, item: donates()),
            
        )
        threading.Thread(target=self.icon.run, daemon=True).start()

    def open_settings(self, icon=None, item=None):
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        def on_settings_change(active, threshold):
            self.alarm_active = active
            self.alarm_threshold = threshold
            print(f"[SETTINGS] Alarm: {'On' if active else 'Off'}, Threshold: {threshold}")

        self.settings_window = SettingsWindow(self.root, self.alarm_active, self.alarm_threshold, on_settings_change).window

    def kontrol_et(self):
        while True:
            deprem = get_latest_earthquake()
            if deprem:
                deprem_id = deprem["id"]
                buyukluk = deprem["buyukluk"]
                yer = deprem["yer"]

                print(f"[CHECK] ID:{deprem_id} - Magnitude:{buyukluk} - Location:{yer}")

                if (self.SON_DEPREM_ID != deprem_id and buyukluk >= self.alarm_threshold and self.alarm_active):
                    self.SON_DEPREM_ID = deprem_id
                    print("[NEW EARTHQUAKE] Triggering alert!")
                    log_earthquake(deprem)
                    threading.Thread(target=show_alert, args=(yer, buyukluk), daemon=True).start()
                    threading.Thread(target=send_discord_alert, args=(f"🚨 EARTHQUAKE! Location: {yer} - Magnitude: {buyukluk}",), daemon=True).start()
            time.sleep(10)

    def start_dashboard(self):
        def dashboard_thread():
            try:
                start_dashboard()
            except Exception as e:
                print(f"[DASHBOARD ERROR] {e}")

        threading.Thread(target=dashboard_thread, daemon=True).start()

    def start_widget(self):
        def widget_thread():
            try:
                widget.DepremWidget()
            except Exception as e:
                print(f"[WIDGET ERROR] {e}")

        threading.Thread(target=widget_thread, daemon=True).start()
    
    
    
def add_to_startup():
    script_path = os.path.abspath(sys.argv[0])
    shortcut_name = "EarthquakeDetector"
    add_startup_func(script_path, shortcut_name)
    print(f"{shortcut_name} added to startup.")

if __name__ == "__main__":
    if not have_connection():
        sys.exit(1)
    else:
        print("[INFO] Internet connection is available.")  
    add_to_startup()
    DepremApp()
    