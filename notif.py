from plyer import notification

def start_notification():
    notification.notify(
        title="Earthquake Detector",
        message="🔔 App is running. Be safe...",
        timeout=5,
        app_name="Earthquake Detector',"
    )