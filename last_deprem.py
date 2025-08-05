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
        status_var.set(f"📊 Showing {len(depremler)} earthquakes from last 24 hours worldwide")

    def otomatik_guncelle():
        tabloyu_guncelle()
        window.after(300000, otomatik_guncelle)

    window = tk.Toplevel()
    window.title("🌍 Global Earthquake Monitor")
    window.geometry("1000x650")
    window.configure(bg="#0f0f0f")
    window.resizable(True, True)

    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("Treeview",
                    background="#1a1a1a",
                    foreground="#ffffff",
                    rowheight=35,
                    fieldbackground="#1a1a1a",
                    font=('Segoe UI', 11),
                    borderwidth=0)
    
    style.configure("Treeview.Heading",
                    background="#2d2d2d",
                    foreground="#ffffff",
                    font=('Segoe UI', 12, 'bold'),
                    borderwidth=0,
                    relief="flat")
    
    style.map('Treeview', 
              background=[('selected', '#1abc9c')],
              foreground=[('selected', '#ffffff')])

    header_frame = tk.Frame(window, bg="#0f0f0f", height=80)
    header_frame.pack(fill='x', padx=20, pady=(20, 0))
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, 
                          text="🌍 Global Earthquake Monitor", 
                          font=('Segoe UI', 24, 'bold'),
                          bg="#0f0f0f", 
                          fg="#1abc9c")
    title_label.pack(side='left', pady=20)
    
    subtitle_label = tk.Label(header_frame, 
                             text="Real-time earthquake data from USGS", 
                             font=('Segoe UI', 12),
                             bg="#0f0f0f", 
                             fg="#888888")
    subtitle_label.pack(side='left', padx=(15, 0), pady=20)

    content_frame = tk.Frame(window, bg="#0f0f0f")
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    tree = ttk.Treeview(content_frame, 
                       columns=("Time", "Location", "Magnitude", "Depth"), 
                       show="headings",
                       height=15)
    
    tree.heading("Time", text="⏰ Time (UTC)")
    tree.heading("Location", text="📍 Location")
    tree.heading("Magnitude", text="📏 Magnitude (Mw)")
    tree.heading("Depth", text="⬇️ Depth")
    
    tree.column("Time", width=200, anchor='center', minwidth=180)
    tree.column("Location", width=520, anchor='w', minwidth=400)
    tree.column("Magnitude", width=120, anchor='center', minwidth=100)
    tree.column("Depth", width=120, anchor='center', minwidth=100)
    
    tree.pack(fill='both', expand=True, pady=(0, 20))

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    control_frame = tk.Frame(window, bg="#0f0f0f")
    control_frame.pack(fill='x', padx=20, pady=(0, 20))

    refresh_button = tk.Button(control_frame,
                               text="🔄 Refresh Data",
                               command=tabloyu_guncelle,
                               font=('Segoe UI', 13, 'bold'),
                               bg="#1abc9c", 
                               fg="white",
                               activebackground="#16a085",
                               activeforeground="white",
                               relief="flat",
                               padx=25,
                               pady=12,
                               cursor="hand2",
                               borderwidth=0)
    refresh_button.pack(side='left')

    status_frame = tk.Frame(window, bg="#0f0f0f")
    status_frame.pack(fill='x', padx=20, pady=(0, 20))

    status_var = tk.StringVar()
    status_label = tk.Label(status_frame, 
                           textvariable=status_var, 
                           fg="#1abc9c", 
                           bg="#0f0f0f", 
                           font=('Segoe UI', 11, 'bold'))
    status_label.pack(side='left')

    info_frame = tk.Frame(window, bg="#1a1a1a", relief="flat", bd=1)
    info_frame.pack(fill='x', padx=20, pady=(0, 20))

    info_text = """ℹ️  Information:
• Data source: USGS (United States Geological Survey)
• Updates automatically every 5 minutes
• Shows earthquakes from the last 24 hours worldwide
• Magnitude scale: Moment magnitude (Mw)
• Depth is measured in kilometers below sea level"""

    info_label = tk.Label(info_frame, 
                         text=info_text,
                         fg="#cccccc", 
                         bg="#1a1a1a", 
                         font=('Segoe UI', 10),
                         justify='left',
                         padx=20,
                         pady=15)
    info_label.pack(anchor='w')

    tabloyu_guncelle()
    otomatik_guncelle()