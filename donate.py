import tkinter as tk
from tkinter import messagebox
import webbrowser

def donates():
    def copy_to_clipboard(text, label):
        root.clipboard_clear()
        root.clipboard_append(text)
        label.config(text="✅ Copied!", fg="#4CAF50")
        root.after(2000, lambda: label.config(text="Click to copy", fg="#888"))

    def open_url(url):
        webbrowser.open(url)

    root = tk.Tk()
    root.title("💎 Support & Credits")
    root.geometry("500x600")
    root.configure(bg="#1a1a1a")
    root.resizable(False, False)

    bg_color = "#1a1a1a"
    card_bg = "#2a2a2a"
    accent_color = "#4CAF50"
    text_color = "#ffffff"
    subtitle_color = "#cccccc"
    link_color = "#64B5F6"
    
    font_title = ("Segoe UI", 24, "bold")
    font_subtitle = ("Segoe UI", 16, "bold")
    font_text = ("Segoe UI", 12)
    font_link = ("Segoe UI", 12, "underline")
    font_small = ("Segoe UI", 10)
    font_mono = ("Consolas", 11, "bold")

    main_frame = tk.Frame(root, bg=bg_color)
    main_frame.pack(fill='both', expand=True, padx=30, pady=30)

    header_frame = tk.Frame(main_frame, bg=bg_color)
    header_frame.pack(fill='x', pady=20)

    title = tk.Label(
        header_frame, 
        text="💎 Support & Credits", 
        fg=accent_color, 
        bg=bg_color, 
        font=font_title
    )
    title.pack(pady=10)

    creator = tk.Label(
        header_frame, 
        text="Made with ❤️ by Toprak", 
        fg=text_color, 
        bg=bg_color, 
        font=font_subtitle
    )
    creator.pack(pady=5)

    version = tk.Label(
        header_frame, 
        text="Earthquake Reporter v2.0", 
        fg=subtitle_color, 
        bg=bg_color, 
        font=font_small
    )
    version.pack()

    btc_card = tk.Frame(main_frame, bg=card_bg, relief="flat", bd=1)
    btc_card.pack(fill='x', pady=15)

    btc_header = tk.Frame(btc_card, bg=card_bg, padx=20, pady=15)
    btc_header.pack(fill='x')

    btc_icon = tk.Label(
        btc_header,
        text="₿",
        font=("Segoe UI", 24, "bold"),
        fg="#F7931A",
        bg=card_bg
    )
    btc_icon.pack(side=tk.LEFT, padx=10)

    btc_title_frame = tk.Frame(btc_header, bg=card_bg)
    btc_title_frame.pack(side=tk.LEFT, fill='y')

    btc_label = tk.Label(
        btc_title_frame, 
        text="Bitcoin (BTC)", 
        fg=text_color, 
        bg=card_bg, 
        font=font_subtitle,
        anchor="w"
    )
    btc_label.pack(anchor="w")

    btc_subtitle = tk.Label(
        btc_title_frame,
        text="Support with cryptocurrency",
        fg=subtitle_color,
        bg=card_bg,
        font=font_small,
        anchor="w"
    )
    btc_subtitle.pack(anchor="w")

    btc_content = tk.Frame(btc_card, bg=card_bg, padx=20, pady=15)
    btc_content.pack(fill='x')

    btc_addr = "bc1qwsqaqz08atxlh38uqp5z0wmd24xq85lvzchr5h"
    btc_text = tk.Label(
        btc_content, 
        text=btc_addr, 
        fg=link_color, 
        bg="#3a3a3a", 
        font=font_mono,
        cursor="hand2",
        padx=15,
        pady=10,
        relief="flat",
        bd=0
    )
    btc_text.pack(fill='x', pady=5)

    btc_copy_label = tk.Label(
        btc_content, 
        text="Click to copy", 
        fg="#888", 
        bg=card_bg, 
        font=font_small
    )
    btc_copy_label.pack()

    btc_text.bind("<Button-1>", lambda e: copy_to_clipboard(btc_addr, btc_copy_label))
    btc_text.bind("<Enter>", lambda e: btc_text.config(bg="#4a4a4a"))
    btc_text.bind("<Leave>", lambda e: btc_text.config(bg="#3a3a3a"))

    iban_card = tk.Frame(main_frame, bg=card_bg, relief="flat", bd=1)
    iban_card.pack(fill='x', pady=15)

    iban_header = tk.Frame(iban_card, bg=card_bg, padx=20, pady=15)
    iban_header.pack(fill='x')

    iban_icon = tk.Label(
        iban_header,
        text="🏦",
        font=("Segoe UI", 24, "bold"),
        fg="#2196F3",
        bg=card_bg
    )
    iban_icon.pack(side=tk.LEFT, padx=10)

    iban_title_frame = tk.Frame(iban_header, bg=card_bg)
    iban_title_frame.pack(side=tk.LEFT, fill='y')

    iban_label = tk.Label(
        iban_title_frame, 
        text="Bank Transfer (IBAN)", 
        fg=text_color, 
        bg=card_bg, 
        font=font_subtitle,
        anchor="w"
    )
    iban_label.pack(anchor="w")

    iban_subtitle = tk.Label(
        iban_title_frame,
        text="Traditional bank transfer",
        fg=subtitle_color,
        bg=card_bg,
        font=font_small,
        anchor="w"
    )
    iban_subtitle.pack(anchor="w")

    iban_content = tk.Frame(iban_card, bg=card_bg, padx=20, pady=15)
    iban_content.pack(fill='x')

    iban_num = "TR 00 00"
    iban_text = tk.Label(
        iban_content, 
        text=iban_num, 
        fg=link_color, 
        bg="#3a3a3a", 
        font=font_mono,
        cursor="hand2",
        padx=15,
        pady=10,
        relief="flat",
        bd=0
    )
    iban_text.pack(fill='x', pady=5)

    iban_copy_label = tk.Label(
        iban_content, 
        text="Click to copy", 
        fg="#888", 
        bg=card_bg, 
        font=font_small
    )
    iban_copy_label.pack()

    iban_text.bind("<Button-1>", lambda e: copy_to_clipboard(iban_num, iban_copy_label))
    iban_text.bind("<Enter>", lambda e: iban_text.config(bg="#4a4a4a"))
    iban_text.bind("<Leave>", lambda e: iban_text.config(bg="#3a3a3a"))

    social_card = tk.Frame(main_frame, bg=card_bg, relief="flat", bd=1)
    social_card.pack(fill='x', pady=15)

    social_header = tk.Frame(social_card, bg=card_bg, padx=20, pady=15)
    social_header.pack(fill='x')

    social_icon = tk.Label(
        social_header,
        text="🌐",
        font=("Segoe UI", 24, "bold"),
        fg="#9C27B0",
        bg=card_bg
    )
    social_icon.pack(side=tk.LEFT, padx=10)

    social_title_frame = tk.Frame(social_header, bg=card_bg)
    social_title_frame.pack(side=tk.LEFT, fill='y')

    social_label = tk.Label(
        social_title_frame, 
        text="Connect & Follow", 
        fg=text_color, 
        bg=card_bg, 
        font=font_subtitle,
        anchor="w"
    )
    social_label.pack(anchor="w")

    social_subtitle = tk.Label(
        social_title_frame,
        text="Stay updated with latest developments",
        fg=subtitle_color,
        bg=card_bg,
        font=font_small,
        anchor="w"
    )
    social_subtitle.pack(anchor="w")

    social_content = tk.Frame(social_card, bg=card_bg, padx=20, pady=15)
    social_content.pack(fill='x')

    def make_social_link(text, url, icon, color):
        link_frame = tk.Frame(social_content, bg=card_bg)
        link_frame.pack(fill='x', pady=5)
        
        link_btn = tk.Button(
            link_frame,
            text=f"{icon} {text}",
            fg=text_color,
            bg="#3a3a3a",
            font=font_link,
            cursor="hand2",
            bd=0,
            relief="flat",
            padx=15,
            pady=10,
            anchor="w",
            command=lambda: open_url(url)
        )
        link_btn.pack(fill='x')
        
        link_btn.bind("<Enter>", lambda e: link_btn.config(bg="#4a4a4a", fg=color))
        link_btn.bind("<Leave>", lambda e: link_btn.config(bg="#3a3a3a", fg=text_color))
        
        return link_btn

    github = make_social_link("GitHub", "https://github.com/TPashaxrd", "🐙", "#6f42c1")
    linkedin = make_social_link("LinkedIn", "https://linkedin.com/in/", "💼", "#0077b5")

    footer_frame = tk.Frame(main_frame, bg=bg_color)
    footer_frame.pack(fill='x', pady=20)

    footer_text = tk.Label(
        footer_frame,
        text="Thank you for supporting this project! 🙏",
        fg=subtitle_color,
        bg=bg_color,
        font=font_text
    )
    footer_text.pack()

    footer_subtext = tk.Label(
        footer_frame,
        text="Your support helps improve earthquake safety worldwide",
        fg="#666",
        bg=bg_color,
        font=font_small
    )
    footer_subtext.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    donates()