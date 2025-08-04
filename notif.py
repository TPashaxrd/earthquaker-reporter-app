from winotify import Notification

def start_notification():
    toast = Notification(app_id="Earthquake Detector",
                         title="Earthquake Detector",
                         msg="🔔 App is running. Be safe...",
                         duration="short")
    toast.show()
