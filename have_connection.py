import socket
import sys

def have_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

if not have_connection():
    print("[INTERNET] No internet connection detected. Please check your connection.")
    sys.exit() 

print("[INTERNET] Successyfull Connection!")