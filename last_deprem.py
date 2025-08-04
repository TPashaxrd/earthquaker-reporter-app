import tkinter as tk
from tkinter import ttk
import threading
import requests
import time

def last_deprem():
    def deprem_verilerini_cek():
        try:
            API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
            response = requests.get(API_URL)
            data = response.json()
            depremler = []
            for feature in data["features"]:
                yer = feature["properties"]["place"]
                buyukluk = feature["properties"]["mag"]
                zaman = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(feature["properties"]["time"] / 1000))
                depremler.append((zaman, yer, buyukluk))
            return depremler
        except Exception as e:
            print("Hata:", e)
            return []

    def tabloyu_guncelle():
        for row in tree.get_children():
            tree.delete(row)
        depremler = deprem_verilerini_cek()
        for zaman, yer, buyukluk in depremler:
            tree.insert("", "end", values=(zaman, yer, buyukluk))

    pencere = tk.Toplevel() 
    pencere.title("🌍 Earthquake Detective | Earthquakes Map")
    pencere.geometry("800x500")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", rowheight=25, font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

    tree = ttk.Treeview(pencere, columns=("Time", "Location", "Size"), show="headings")
    tree.heading("Time", text="Time (UTC)")
    tree.heading("Location", text="Location")
    tree.heading("Size", text="Mw")
    tree.pack(fill=tk.BOTH, expand=True)

    yenile_buton = tk.Button(pencere, text="🔄 Yenile", command=tabloyu_guncelle, font=('Arial', 12), bg="#4CAF50", fg="white")
    yenile_buton.pack(pady=10)

    tabloyu_guncelle()
