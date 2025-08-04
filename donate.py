import tkinter as tk
from tkinter import messagebox
import webbrowser

def donates():
    def copy_to_clipboard(text, label):
        root.clipboard_clear()
        root.clipboard_append(text)
        label.config(text="Copied!")
        root.after(1500, lambda: label.config(text="Click to copy"))

    def open_url(url):
        webbrowser.open(url)

    root = tk.Tk()
    root.title("💎 Support & Credits")
    root.geometry("450x500")
    root.configure(bg="#121212")
    root.resizable(False, False)

    fg_color = "white"
    card_bg = "#1e1e1e"
    accent_color = "#4CAF50"
    font_title = ("Segoe UI", 22, "bold")
    font_subtitle = ("Segoe UI", 14, "bold")
    font_text = ("Segoe UI", 12)
    font_link = ("Segoe UI", 12, "underline")

    card = tk.Frame(root, bg=card_bg, padx=25, pady=25)
    card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=460)

    title = tk.Label(card, text="Support & Credits", fg=accent_color, bg=card_bg, font=font_title)
    title.pack(pady=(0, 15))

    creator = tk.Label(card, text="Made with ❤️ by Toprak", fg=fg_color, bg=card_bg, font=font_subtitle)
    creator.pack(pady=(0, 25))

    btc_label = tk.Label(card, text="Bitcoin (BTC) Address:", fg=fg_color, bg=card_bg, font=font_subtitle, anchor="w")
    btc_label.pack(fill="x")
    btc_addr = "bc1qwsqaqz08atxlh38uqp5z0wmd24xq85lvzchr5h"
    btc_text = tk.Label(card, text=btc_addr, fg=accent_color, bg=card_bg, font=font_text, cursor="hand2")
    btc_text.pack(fill="x", pady=(0,10))
    btc_copy_label = tk.Label(card, text="Click to copy", fg="#888", bg=card_bg, font=("Segoe UI", 10))
    btc_copy_label.pack()

    btc_text.bind("<Button-1>", lambda e: copy_to_clipboard(btc_addr, btc_copy_label))

    iban_label = tk.Label(card, text="IBAN:", fg=fg_color, bg=card_bg, font=font_subtitle, anchor="w")
    iban_label.pack(fill="x", pady=(15,0))
    iban_num = "TR 00 00"
    iban_text = tk.Label(card, text=iban_num, fg=accent_color, bg=card_bg, font=font_text, cursor="hand2")
    iban_text.pack(fill="x", pady=(0,10))
    iban_copy_label = tk.Label(card, text="Click to copy", fg="#888", bg=card_bg, font=("Segoe UI", 10))
    iban_copy_label.pack()

    iban_text.bind("<Button-1>", lambda e: copy_to_clipboard(iban_num, iban_copy_label))

    links_frame = tk.Frame(card, bg=card_bg)
    links_frame.pack(pady=20)

    def make_link(text, url):
        lbl = tk.Label(links_frame, text=text, fg=accent_color, bg=card_bg, font=font_link, cursor="hand2")
        lbl.pack(side="left", padx=15)
        lbl.bind("<Enter>", lambda e: lbl.config(fg="#8BC34A"))
        lbl.bind("<Leave>", lambda e: lbl.config(fg=accent_color))
        lbl.bind("<Button-1>", lambda e: open_url(url))
        return lbl

    github = make_link("GitHub", "https://github.com/TPashaxrd")
    linkedin = make_link("LinkedIn", "https://linkedin.com/in/")

    root.mainloop()

if __name__ == "__main__":
    donates()