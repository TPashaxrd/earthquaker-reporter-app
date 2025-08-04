import pygame
import time
from playsound import playsound
from winotify import Notification

def start_notification():
    toast = Notification(app_id="Earthquake Detector",
                         title="Earthquake Detector",
                         msg="🔔 App is running. Be safe...",
                         duration="short")
    toast.show()

    pygame.mixer.init()
    pygame.mixer.music.load("./Sounds/earthquake-notif.mp3") 
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)