import tkinter as tk
from tkinter import ttk
import requests
import time

def last_deprem():
    def deprem_verilerini_cek():
        try:
            API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
            response = requests.get(API_URL, timeout=10)
            data = response.json()
            depremler = []
            for feature in data["features"]:
                props = feature["properties"]
                zaman = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(props["time"] / 1000))
                yer = props["place"]
                buyukluk = props["mag"]
                derinlik = feature["geometry"]["coordinates"][2]
                depremler.append((zaman, yer, buyukluk, derinlik))
            return depremler
        except Exception as e:
            print("Error:", e)
            return []

    def tabloyu_guncelle():
        depremler = deprem_verilerini_cek()
        for row in tree.get_children():
            tree.delete(row)
        for zaman, yer, buyukluk, derinlik in depremler:
            tree.insert("", "end", values=(zaman, yer, buyukluk, f"{derinlik:.1f} km"))
        status_var.set(f"Showing {len(depremler)} earthquakes from last 24 hours worldwide.")

    def otomatik_guncelle():
        tabloyu_guncelle()
        window.after(300000, otomatik_guncelle)

    window = tk.Toplevel()
    window.title("🌍 Earthquake Detective | Global Earthquake Map")
    window.geometry("900x550")
    window.configure(bg="#121212")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#1e1e1e",
                    foreground="white",
                    rowheight=28,
                    fieldbackground="#1e1e1e",
                    font=('Segoe UI', 10))
    style.configure("Treeview.Heading",
                    background="#333333",
                    foreground="white",
                    font=('Segoe UI', 12, 'bold'))
    style.map('Treeview', background=[('selected', '#4CAF50')])

    tree = ttk.Treeview(window, columns=("Time", "Location", "Magnitude", "Depth"), show="headings")
    tree.heading("Time", text="Time (UTC)")
    tree.heading("Location", text="Location")
    tree.heading("Magnitude", text="Magnitude (Mw)")
    tree.heading("Depth", text="Depth")
    tree.column("Time", width=190, anchor='center')
    tree.column("Location", width=480, anchor='w')
    tree.column("Magnitude", width=110, anchor='center')
    tree.column("Depth", width=100, anchor='center')
    tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    refresh_button = tk.Button(window,
                               text="🔄 Refresh Now",
                               command=tabloyu_guncelle,
                               font=('Segoe UI', 12, 'bold'),
                               bg="#4CAF50", fg="white",
                               activebackground="#388E3C",
                               activeforeground="white",
                               relief="flat",
                               padx=18,
                               pady=9,
                               cursor="hand2")
    refresh_button.pack(pady=(0, 10))

    status_var = tk.StringVar()
    status_label = tk.Label(window, textvariable=status_var, fg="white", bg="#121212", font=('Segoe UI', 10, 'italic'))
    status_label.pack()

    tabloyu_guncelle()
    otomatik_guncelle()