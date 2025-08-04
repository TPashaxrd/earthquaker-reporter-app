import tkinter as tk
import threading
import winsound

alert_window = None

def show_alert(yer, buyukluk):
    global alert_window
    if alert_window is not None and alert_window.winfo_exists():
        return

    alert_window = tk.Tk()
    alert_window.title("!!! DEPREM !!!")
    alert_window.attributes("-fullscreen", True)
    alert_window.configure(bg='red')

    label = tk.Label(alert_window, text=f"DEPREM OLDU!\nYer: {yer}\nBüyüklük: {buyukluk}", font=("Arial", 50), fg="white", bg="red")
    label.pack(expand=True)

    def hide_alert():
        global alert_window
        if alert_window is not None:
            alert_window.destroy()
            alert_window = None

    btn_hide = tk.Button(alert_window, text="HEMEN SAKLAN", font=("Arial", 30), bg="white", fg="red", command=hide_alert)
    btn_hide.pack(pady=50)

    def play_siren():
        freq1 = 1000
        freq2 = 1500
        dur = 500
        for _ in range(10):
            winsound.Beep(freq1, dur)
            winsound.Beep(freq2, dur)

    threading.Thread(target=play_siren, daemon=True).start()

    alert_window.mainloop()
