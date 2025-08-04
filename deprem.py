import requests

def get_latest_earthquake():
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        deprem = data["result"][0]
        return {
            "id": deprem["_id"],
            "buyukluk": float(deprem["mag"]),
            "yer": deprem["title"]
        }
    except Exception as e:
        print(f"[DEPREM API HATA] {e}")
        return None