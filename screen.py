from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import tkinter as tk
import threading
import pyttsx3
import pythoncom
import pygame
import security
from threading import Lock

alert_window = None
mixer_started = False
tts_lock = Lock()

def sesli_okuma(metin):
    pythoncom.CoInitialize()
    with tts_lock: 
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
    global alert_window, mixer_started

    try:
        if alert_window is not None and alert_window.winfo_exists():
            return
    except tk.TclError:
        alert_window = None

    alert_window = tk.Tk()
    alert_window.title("🚨 EARTHQUAKE ALERT SYSTEM")
    alert_window.configure(bg="#0a0a0a")
    alert_window.resizable(False, False)

    ekran_genislik = alert_window.winfo_screenwidth()
    ekran_yukseklik = alert_window.winfo_screenheight()
    alert_window.geometry(f"{ekran_genislik}x{ekran_yukseklik}+0+0")
    alert_window.attributes("-topmost", True)
    alert_window.overrideredirect(True)

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

    main_frame = tk.Frame(alert_window, bg="#0a0a0a")
    main_frame.pack(fill='both', expand=True, padx=50, pady=50)

    header_frame = tk.Frame(main_frame, bg="#0a0a0a", height=120)
    header_frame.pack(fill='x', pady=(0, 40))
    header_frame.pack_propagate(False)

    def pulse_effect():
        try:
            current_color = emergency_label.cget("fg")
            emergency_label.configure(fg="#FF0000" if current_color == "#FF3B3B" else "#FF3B3B")
            alert_window.after(500, pulse_effect)
        except:
            pass

    emergency_label = tk.Label(
        header_frame,
        text="🚨 EMERGENCY ALERT 🚨",
        font=("Segoe UI Black", 72, "bold"),
        fg="#FF3B3B",
        bg="#0a0a0a"
    )
    emergency_label.pack(expand=True)
    pulse_effect()

    info_frame = tk.Frame(main_frame, bg="#1a1a1a", relief="flat", bd=2)
    info_frame.pack(fill='x', pady=(0, 40))

    title_frame = tk.Frame(info_frame, bg="#1a1a1a")
    title_frame.pack(fill='x', padx=30, pady=(25, 15))

    title_label = tk.Label(
        title_frame,
        text="🌍 EARTHQUAKE DETECTED",
        font=("Segoe UI Black", 48, "bold"),
        fg="#FF3B3B",
        bg="#1a1a1a"
    )
    title_label.pack()

    details_frame = tk.Frame(info_frame, bg="#1a1a1a")
    details_frame.pack(fill='x', padx=30, pady=(0, 25))

    location_label = tk.Label(
        details_frame,
        text=f"📍 Location: {yer}",
        font=("Segoe UI", 32, "bold"),
        fg="#ffffff",
        bg="#1a1a1a"
    )
    location_label.pack(pady=(0, 10))

    magnitude_label = tk.Label(
        details_frame,
        text=f"📏 Magnitude: {buyukluk}",
        font=("Segoe UI", 32, "bold"),
        fg="#FFA726",
        bg="#1a1a1a"
    )
    magnitude_label.pack()

    security_frame = tk.Frame(main_frame, bg="#1a1a1a", relief="flat", bd=2)
    security_frame.pack(fill='x', pady=(0, 40))

    security_title = tk.Label(
        security_frame,
        text="🔒 SECURITY LOCK",
        font=("Segoe UI Black", 36, "bold"),
        fg="#FF3B3B",
        bg="#1a1a1a"
    )
    
    security_title.pack(pady=(25, 15))

    message_label = tk.Label(
        security_frame,
        text="Enter your security PIN to unlock the system",
        font=("Segoe UI Semibold", 20),
        fg="#E0E0E0",
        bg="#1a1a1a"
    )
    message_label.pack(pady=(0, 20))

    pin_display_frame = tk.Frame(security_frame, bg="#1a1a1a")
    pin_display_frame.pack(pady=(0, 20))

    pin_display = tk.Label(
        pin_display_frame,
        text="○○○○",
        font=("Consolas", 48, "bold"),
        fg="#FF3B3B",
        bg="#2a2a2a",
        width=8,
        relief="flat",
        bd=0
    )
    pin_display.pack()

    current_pin = ""

    def add_digit(digit):
        nonlocal current_pin
        if len(current_pin) < 4:
            current_pin += str(digit)
            update_pin_display()
            if len(current_pin) == 4:
                verify_pin()

    def clear_pin():
        nonlocal current_pin
        current_pin = ""
        update_pin_display()

    def update_pin_display():
        display_text = "●" * len(current_pin) + "○" * (4 - len(current_pin))
        pin_display.config(text=display_text)

    def verify_pin():
        if security.check_password(current_pin):
            if mixer_started:
                pygame.mixer.music.stop()
            alert_window.destroy()
        else:
            message_label.config(text="❌ INCORRECT PIN - TRY AGAIN", fg="#FF5555")
            clear_pin()

    numpad_frame = tk.Frame(security_frame, bg="#1a1a1a")
    numpad_frame.pack(pady=(0, 25))

    numbers = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['C', '0', 'OK']
    ]

    for i, row in enumerate(numbers):
        row_frame = tk.Frame(numpad_frame, bg="#1a1a1a")
        row_frame.pack(pady=6)
        
        for j, num in enumerate(row):
            if num == 'C':
                btn = tk.Button(
                    row_frame,
                    text="Clear",
                    font=("Segoe UI Black", 24, "bold"),
                    bg="#FF6B6B",
                    fg="white",
                    activebackground="#FF5252",
                    activeforeground="white",
                    width=7,
                    height=3,
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=clear_pin
                )
            elif num == 'OK':
                btn = tk.Button(
                    row_frame,
                    text="Unlock",
                    font=("Segoe UI Black", 24, "bold"),
                    bg="#4CAF50",
                    fg="white",
                    activebackground="#45A049",
                    activeforeground="white",
                    width=7,
                    height=3,
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=verify_pin
                )
            else:
                btn = tk.Button(
                    row_frame,
                    text=num,
                    font=("Segoe UI Black", 24, "bold"),
                    bg="#2a2a2a",
                    fg="white",
                    activebackground="#FF3B3B",
                    activeforeground="white",
                    width=7,
                    height=3,
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                )
                btn.config(command=lambda n=num: add_digit(n))
            
            btn.pack(side=tk.LEFT, padx=6)

    footer_frame = tk.Frame(main_frame, bg="#0a0a0a")
    footer_frame.pack(fill='x', pady=(20, 0))

    warning_label = tk.Label(
        footer_frame,
        text="⚠️  This is a real emergency alert. Please remain calm and follow safety procedures.",
        font=("Segoe UI", 16, "bold"),
        fg="#FFA726",
        bg="#0a0a0a"
    )
    warning_label.pack()

    threading.Thread(target=play_siren, daemon=True).start()
    threading.Thread(
        target=sesli_okuma,
        args=(f"Earthquake is happening. Location: {yer}, Size: {buyukluk}",),
        daemon=True
    ).start()

    alert_window.mainloop()