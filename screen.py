from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import tkinter as tk
import threading
import pyttsx3
import security
import pygame

alert_window = None
mixer_started = False

def sesli_okuma(metin):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 120)
    engine.say(metin)
    engine.runAndWait()

def play_siren():
    global mixer_started
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("./Sounds/earthquake-alert.mp3")
        pygame.mixer.music.play(-1)
        mixer_started = True
    except Exception as e:
        print("Ses oynatma hatası:", e)

def show_alert(yer, buyukluk):
    global alert_window
    if alert_window is not None and alert_window.winfo_exists():
        return

    alert_window = tk.Tk()
    alert_window.title("EARTHQUAKE ALERT")
    alert_window.configure(bg="#121212")
    alert_window.resizable(False, False)

    ekran_genislik = alert_window.winfo_screenwidth()
    ekran_yukseklik = alert_window.winfo_screenheight()
    alert_window.geometry(f"{ekran_genislik}x{ekran_yukseklik}+0+0")
    alert_window.attributes("-topmost", True)

    def prevent_move(event=None):
        alert_window.geometry(f"{ekran_genislik}x{ekran_yukseklik}+0+0")
    alert_window.bind("<Configure>", prevent_move)
    alert_window.protocol("WM_DELETE_WINDOW", lambda: None)
    alert_window.bind("<Escape>", lambda e: "break")

    def keep_on_top():
        try:
            alert_window.attributes("-topmost", True)
            alert_window.after(100, keep_on_top)
        except:
            pass
    keep_on_top()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)

    tk.Label(
        alert_window,
        text="🌍 EARTHQUAKE DETECTED!",
        font=("Segoe UI Black", 70, "bold"),
        fg="#FF3B3B",
        bg="#121212"
    ).pack(pady=(80, 30))

    tk.Label(
        alert_window,
        text=f"Location: {yer}  |  Magnitude: {buyukluk}",
        font=("Segoe UI", 36),
        fg="white",
        bg="#121212"
    ).pack(pady=(0, 50))

    message_label = tk.Label(
        alert_window,
        text="Enter PIN to unlock",
        font=("Segoe UI Semibold", 24),
        fg="#E0E0E0",
        bg="#121212"
    )
    message_label.pack(pady=(0, 15))

    password_entry = tk.Entry(
        alert_window,
        show="*",
        font=("Consolas", 28),
        width=16,
        justify="center",
        bg="#1E1E1E",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightcolor="#FF3B3B",
        highlightbackground="#555555",
        selectbackground="#FF3B3B",
        selectforeground="white",
    )
    password_entry.pack(pady=(0, 40))
    password_entry.focus_set()
    password_entry.icursor("end")

    def verify_password():
        pw = password_entry.get().strip()
        if security.check_password(pw):
            if mixer_started:
                pygame.mixer.music.stop()
            alert_window.destroy()
        else:
            message_label.config(text="❌ WRONG PIN", fg="#FF5555")
            password_entry.delete(0, tk.END)

    password_entry.bind("<Return>", lambda e: verify_password())

    btn_hide = tk.Button(
        alert_window,
        text="UNLOCK 🔓",
        font=("Segoe UI", 32, "bold"),
        bg="#FF3B3B",
        fg="white",
        activebackground="#FF1C1C",
        activeforeground="#FFF0F0",
        padx=50,
        pady=15,
        bd=0,
        relief="ridge",
        cursor="hand2",
        command=verify_password
    )
    btn_hide.pack()

    def on_enter(e): btn_hide.configure(bg="#FF1C1C")
    def on_leave(e): btn_hide.configure(bg="#FF3B3B")
    btn_hide.bind("<Enter>", on_enter)
    btn_hide.bind("<Leave>", on_leave)

    threading.Thread(target=play_siren, daemon=True).start()
    threading.Thread(
        target=sesli_okuma,
        args=(f"Earthquakes in happening. Location: {yer}, Size: {buyukluk}",),
        daemon=True
    ).start()

    alert_window.mainloop()