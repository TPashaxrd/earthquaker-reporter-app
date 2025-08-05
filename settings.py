import tkinter as tk
from tkinter import ttk

class HoverButton(ttk.Button):
    def __init__(self, master=None, **kw):
        style_name = kw.pop('style', 'TButton')
        super().__init__(master=master, style=style_name, **kw)

        self.default_style = style_name
        self.hover_style = style_name + ".Hover"
        self['cursor'] = 'hand2'

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(style=self.hover_style)

    def on_leave(self, event):
        self.configure(style=self.default_style)

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None

    def show(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#333333", foreground="#eeeeee",
                         relief='solid', borderwidth=1,
                         font=("Segoe UI", 10, "normal"),
                         padx=8, pady=4)
        label.pack()

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class SettingsWindow:
    def __init__(self, master, alarm_active, alarm_threshold, on_change):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("⚙️ Earthquake Detector - Settings")
        self.window.geometry("420x380")
        self.window.resizable(False, False)
        self.set_position_top_left()
        self.window.attributes('-topmost', True)
        self.window.configure(bg="#121212")

        self.on_change = on_change
        self.language = 'en'
        self.is_dark_theme = True

        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")

        self.style.configure("TLabel", background="#121212", foreground="#ddd", font=("Segoe UI", 12))
        self.style.configure("TCheckbutton", background="#121212", foreground="#ddd", font=("Segoe UI", 12))
        self.style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#eee", font=("Segoe UI", 12))
        self.style.configure("TFrame", background="#121212")

        self.style.configure("Main.TFrame", background="#1e1e1e", relief="flat")

        self.style.configure("Custom.TButton",
                             background="#1abc9c",
                             foreground="#121212",
                             font=("Segoe UI", 12, "bold"),
                             padding=10,
                             borderwidth=0,
                             relief="flat")
        self.style.map("Custom.TButton",
                       background=[('active', '#16a085')],
                       foreground=[('disabled', '#7f8c8d')])
        self.style.configure("Custom.TButton.Hover",
                             background="#16a085",
                             foreground="#fff")

        self.container = ttk.Frame(self.window, style="Main.TFrame")
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=380, height=320)

        self.lbl_title = ttk.Label(self.container, text="⚙️ Settings", font=("Segoe UI", 20, "bold"))
        self.lbl_title.pack(anchor='w', padx=20, pady=(20, 15))

        self.alarm_active_var = tk.BooleanVar(value=alarm_active)
        self.chk_alarm = ttk.Checkbutton(self.container, text="🔔 Enable Alarm", variable=self.alarm_active_var,
                                         command=self.settings_changed)
        self.chk_alarm.pack(anchor='w', padx=25, pady=15)

        frame_threshold = ttk.Frame(self.container, style="Main.TFrame")
        frame_threshold.pack(anchor='w', fill='x', padx=25, pady=10)

        self.lbl_threshold = ttk.Label(frame_threshold, text="📏 Alarm Threshold (Magnitude):")
        self.lbl_threshold.pack(side='left', padx=(0,10))

        self.alarm_threshold_var = tk.StringVar(value=str(alarm_threshold))
        self.ent_threshold = ttk.Entry(frame_threshold, textvariable=self.alarm_threshold_var, width=10)
        self.ent_threshold.pack(side='left')
        self.ent_threshold.bind("<FocusIn>", self.show_tooltip)
        self.ent_threshold.bind("<FocusOut>", self.hide_tooltip)
        self.alarm_threshold_var.trace_add("write", lambda *args: self.validate_threshold())

        self.tooltip = Tooltip(self.ent_threshold, "Enter a number (e.g., 5.0)")

        self.lbl_preview = ttk.Label(self.container, text=f"Current Threshold: {alarm_threshold:.1f}", font=("Segoe UI", 10), foreground="#aaa")
        self.lbl_preview.pack(anchor='w', padx=25, pady=(5, 15))

        self.language_var = tk.StringVar(value='English')
        lang_menu = ttk.OptionMenu(self.container, self.language_var, 'English', 'English', 'Türkçe', command=self.change_language)
        lang_menu.pack(anchor='w', padx=25, pady=10, fill='x')

        self.theme_var = tk.BooleanVar(value=self.is_dark_theme)
        self.chk_theme = ttk.Checkbutton(self.container, text="🌙 Dark Theme", variable=self.theme_var, command=self.toggle_theme)
        self.chk_theme.pack(anchor='w', padx=25, pady=10)

        self.btn_close = HoverButton(self.container, text="Close", command=self.window.destroy, style="Custom.TButton", width=18)
        self.btn_close.pack(anchor='w', padx=25, pady=(20, 10))

        self.apply_language()
        self.toggle_theme()

    def set_position_top_left(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = 20
        y = 40
        self.window.geometry(f"+{x}+{y}")

    def show_tooltip(self, event=None):
        self.tooltip.show()

    def hide_tooltip(self, event=None):
        self.tooltip.hide()

    def validate_threshold(self):
        try:
            val = float(self.alarm_threshold_var.get())
            if val < 0:
                raise ValueError
            self.ent_threshold.configure(foreground="#eee")
            self.lbl_preview.configure(text=f"Current Threshold: {val:.1f}")
            self.settings_changed()
        except:
            self.ent_threshold.configure(foreground="#e74c3c")
            self.lbl_preview.configure(text="Invalid Threshold!")

    def settings_changed(self):
        try:
            active = self.alarm_active_var.get()
            threshold = float(self.alarm_threshold_var.get())
            if threshold >= 0:
                self.on_change(active, threshold)
        except:
            pass

    def change_language(self, choice):
        self.language = 'tr' if choice == 'Türkçe' else 'en'
        self.apply_language()

    def apply_language(self):
        if self.language == 'en':
            self.window.title("⚙️ Earthquake Detector - Settings")
            self.lbl_title.config(text="⚙️ Settings")
            self.chk_alarm.config(text="🔔 Enable Alarm")
            self.lbl_threshold.config(text="📏 Alarm Threshold (Magnitude):")
            self.chk_theme.config(text="🌙 Dark Theme")
            self.btn_close.config(text="Close")
        else:
            self.window.title("⚙️ Deprem Dedektörü - Ayarlar")
            self.lbl_title.config(text="⚙️ Ayarlar")
            self.chk_alarm.config(text="🔔 Alarmı Aktif Et")
            self.lbl_threshold.config(text="📏 Alarm Eşiği (Büyüklük):")
            self.chk_theme.config(text="🌙 Koyu Tema")
            self.btn_close.config(text="Kapat")

    def toggle_theme(self):
        self.is_dark_theme = self.theme_var.get()
        if self.is_dark_theme:
            self.window.configure(bg="#121212")
            self.style.configure("TLabel", background="#121212", foreground="#ddd")
            self.style.configure("TCheckbutton", background="#121212", foreground="#ddd")
            self.style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#eee")
            self.style.configure("TFrame", background="#121212")
            self.style.configure("Main.TFrame", background="#1e1e1e")
        else:
            self.window.configure(bg="#f9f9f9")
            self.style.configure("TLabel", background="#f9f9f9", foreground="#222")
            self.style.configure("TCheckbutton", background="#f9f9f9", foreground="#222")
            self.style.configure("TEntry", fieldbackground="#fff", foreground="#222")
            self.style.configure("TFrame", background="#f9f9f9")
            self.style.configure("Main.TFrame", background="#e6e6e6")

if __name__ == "__main__":
    def on_change(active, threshold):
        print(f"Alarm Enabled: {active}, Threshold: {threshold}")

    root = tk.Tk()
    root.withdraw()
    SettingsWindow(root, True, 5.0, on_change)
    root.mainloop()