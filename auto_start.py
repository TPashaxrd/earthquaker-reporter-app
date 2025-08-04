import os
import sys
import win32com.client

def add_to_startup(script_path=None, shortcut_name="EarthquakeDetector"):
    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])

    startup_dir = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    shortcut_path = os.path.join(startup_dir, f"{shortcut_name}.lnk")

    if os.path.exists(shortcut_path):
        print(f"{shortcut_name} already have autostart.")
        return

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = script_path
    shortcut.save()
    print(f"{shortcut_name} added to AutoStart.")

if __name__ == "__main__":
    add_to_startup("main.pyw")