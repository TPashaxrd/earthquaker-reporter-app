import tkinter as tk
import threading
import winsound
import pyttsx3

alert_window = None

def sesli_okuma(metin):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 120)
    engine.say(metin)
    engine.runAndWait()

def show_alert(yer, buyukluk):
    global alert_window
    if alert_window is not None and alert_window.winfo_exists():
        return

    alert_window = tk.Tk()
    alert_window.title("Earthquake Alert")
    alert_window.attributes("-fullscreen", True)
    alert_window.configure(bg="#0D0D0D") 

    label = tk.Label(
        alert_window,
        text="🌍 HAVE EARTHQUAKE RIGHT NOW!",
        font=("Ubuntu Mono", 60, "bold"),
        fg="#FF0000",
        bg="#0D0D0D"
    )
    label.pack(pady=60)

    info_label = tk.Label(
        alert_window,
        text=f"Location: {yer} Size: {buyukluk}",
        font=("Segoe UI", 40),
        fg="white",
        bg="#0D0D0D"
    )
    info_label.pack(pady=20)

    def hide_alert():
        global alert_window
        if alert_window is not None:
            alert_window.destroy()
            alert_window = None

    def on_enter(e):
        btn_hide.configure(bg="#FF4C4C", fg="white")

    def on_leave(e):
        btn_hide.configure(bg="white", fg="#FF4C4C")

    btn_hide = tk.Button(
        alert_window,
        text="EARTHQUAKE THE END 🧠",
        font=("Segoe UI", 30, "bold"),
        bg="white",
        fg="#FF4C4C",
        activebackground="#FF1C1C",
        activeforeground="white",
        padx=40,
        pady=10,
        command=hide_alert
    )
    btn_hide.pack(pady=50)
    btn_hide.bind("<Enter>", on_enter)
    btn_hide.bind("<Leave>", on_leave)

    def play_siren():
        freq1 = 1000
        freq2 = 1500
        dur = 500
        for _ in range(10):
            winsound.Beep(freq1, dur)
            winsound.Beep(freq2, dur)

    threading.Thread(target=play_siren, daemon=True).start()
    threading.Thread(target=sesli_okuma, args=(f"Deprem tespit edildi! Konum: {yer}, Büyüklük: {buyukluk}",), daemon=True).start()

    alert_window.mainloop()

show_alert("İstanbul", "5.6")