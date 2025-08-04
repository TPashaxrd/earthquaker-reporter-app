import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1401657153860927751/MH_JtnCR7T70DctXfbcIq78oOZahUBh6Tabx1xYMpxlA8ZLGL5k8b5I_m_2MbhVc5bh9"

def send_discord_alert(message: str):
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=5)
        if response.status_code == 204:
            print("[DISCORD] Mesaj gönderildi.")
        else:
            print(f"[DISCORD] Mesaj gönderilemedi! Status code: {response.status_code}")
    except Exception as e:
        print(f"[DISCORD HATA] {e}")
