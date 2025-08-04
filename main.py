import threading
import time
import pystray
from PIL import Image, ImageDraw
import tkinter as tk

from webhook import send_discord_alert
from deprem import get_latest_earthquake
from screen import show_alert
from settings import SettingsWindow

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

        self.start_tray()
        self.start_widget()

        threading.Thread(target=self.kontrol_et, daemon=True).start()

        send_discord_alert("🤖 **Deprem Dedektörü Bot Başladı!**")

        self.root.mainloop()

    def create_image(self):
        image = Image.new('RGB', (64, 64), color='red')
        d = ImageDraw.Draw(image)
        d.rectangle([16, 16, 48, 48], fill='white')
        return image

    def start_tray(self):
        self.icon = pystray.Icon("deprem_dedektoru", self.create_image(), "Deprem Dedektörü")
        self.icon.menu = pystray.Menu(
            pystray.MenuItem("Ayarlar", self.open_settings),
            pystray.MenuItem("Çıkış", lambda icon, item: icon.stop())
        )
        threading.Thread(target=self.icon.run, daemon=True).start()

    def open_settings(self, icon=None, item=None):
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        def on_settings_change(active, threshold):
            self.alarm_active = active
            self.alarm_threshold = threshold
            print(f"[AYARLAR] Alarm: {'Açık' if active else 'Kapalı'}, Eşik: {threshold}")

        self.settings_window = SettingsWindow(self.root, self.alarm_active, self.alarm_threshold, on_settings_change).window

    def kontrol_et(self):
        while True:
            deprem = get_latest_earthquake()
            if deprem:
                deprem_id = deprem["id"]
                buyukluk = deprem["buyukluk"]
                yer = deprem["yer"]

                print(f"[KONTROL] ID:{deprem_id} - Büyüklük:{buyukluk} - Yer:{yer}")

                if (self.SON_DEPREM_ID != deprem_id and buyukluk >= self.alarm_threshold and self.alarm_active):
                    self.SON_DEPREM_ID = deprem_id
                    print("[YENİ DEPREM] Alarm tetikleniyor!")
                    threading.Thread(target=show_alert, args=(yer, buyukluk), daemon=True).start()
                    threading.Thread(target=send_discord_alert, args=(f"🚨 DEPREM OLDU! Yer: {yer} - Büyüklük: {buyukluk}",), daemon=True).start()
            time.sleep(10)

    def start_widget(self):
        def widget_thread():
            try:
                import widget
                widget.DepremWidget()
            except Exception as e:
                print(f"[WIDGET] HATA: {e}")

        threading.Thread(target=widget_thread, daemon=True).start()


if __name__ == "__main__":
    DepremApp()
