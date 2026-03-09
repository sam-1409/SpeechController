import json
import os
import threading
import time
from datetime import datetime, timedelta

import pyautogui as pg
import pytesseract
from PIL import Image

# file to store reminders
REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "reminders.json")


def _load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_reminders(data):
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def set_reminder(text, when):
    """Schedule a reminder. `when` should be a datetime or string parseable by
    datetime.fromisoformat."""
    if isinstance(when, str):
        when = datetime.fromisoformat(when)
    reminders = _load_reminders()
    reminders.append({"text": text, "when": when.isoformat()})
    _save_reminders(reminders)
    return True


def check_reminders(callback):
    """Starts a background thread that checks reminders every minute. When a
    reminder is due it calls `callback(text)` and removes it."""
    def loop():
        while True:
            now = datetime.now()
            reminders = _load_reminders()
            updated = []
            for r in reminders:
                schedule = datetime.fromisoformat(r["when"])
                if now >= schedule:
                    try:
                        callback(r["text"])
                    except Exception:
                        pass
                else:
                    updated.append(r)
            if len(updated) != len(reminders):
                _save_reminders(updated)
            time.sleep(60)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def read_screen():
    im = pg.screenshot()
    text = pytesseract.image_to_string(im)
    return text


def translate(text, dest_lang="en"):
    from googletrans import Translator

    translator = Translator()
    res = translator.translate(text, dest=dest_lang)
    return res.text


def _is_process_running(name):
    try:
        import psutil
    except ImportError:
        return False
    for proc in psutil.process_iter(attrs=["name"]):
        if proc.info.get("name", "").lower() == name.lower():
            return True
    return False


def _find_executable(name):
    import shutil, os, getpass

    path = shutil.which(name)
    if path:
        return path
    user = getpass.getuser()
    candidates = [
        rf"C:\Program Files\{name}",
        rf"C:\Program Files (x86)\{name}",
        rf"C:\Users\{user}\AppData\Roaming\{name}\{name}.exe",
        rf"C:\Users\{user}\AppData\Local\{name}\{name}.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def play_song(song_name, platform="youtube"):
    import webbrowser
    if platform == "youtube":
        try:
            pg.press('win')
            pg.typewrite(platform)
            pg.press('enter')
            time.sleep(5)
            for i in range(4):
                pg.press('tab')
            pg.typewrite(song_name)
            pg.press('enter')
        except Exception:
            pass
        # query = song_name.replace(" ", "+")
        # url = f"https://www.youtube.com/results?search_query={query}"
        # no native youtube app check available

    elif platform == "spotify":
        query = song_name.replace(" ", "%20")
        spotify_path = _find_executable("spotify.exe")
        if spotify_path:
            if not _is_process_running("spotify.exe"):
                try:
                    import subprocess
                    subprocess.Popen([spotify_path])
                    time.sleep(2)
                except Exception:
                    pass
            url = f"spotify:search:{query}"
        else:
            url = f"https://open.spotify.com/search/{query}"
    else:
        url = None

    # if url:
    #     webbrowser.open(url)
    #     return True
    return False


def media_key(key):
    try:
        pg.press(key)
        return True
    except Exception:
        return False


def volume_up(steps=3):
    for _ in range(steps):
        media_key('volumeup')


def volume_down(steps=3):
    for _ in range(steps):
        media_key('volumedown')


def play_pause():
    media_key('playpause')


def next_track():
    media_key('nexttrack')


def previous_track():
    media_key('prevtrack')

def get_open_windows():
    import win32gui
    import win32con
    import psutil
    
    windows = []
    
    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if exstyle & win32con.WS_EX_TOOLWINDOW:
            return
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER):
            return
        
        class_name = win32gui.GetClassName(hwnd)
        if class_name in ["Progman", "Button", "Shell_TrayWnd", "Windows.UI.Core.CoreWindow"]:
            return
        
        try:
            _, pid = win32gui.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            windows.append({
                "hwnd": hwnd,
                "title": title.strip(),
                "process": proc.name()
            })
        except Exception:
            pass
    
    win32gui.EnumWindows(callback, None)
    return windows


def switch_to_window(hwnd):
    import win32gui
    import win32con
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception:
        return False


def switch_next_app():
    try:
        pg.hotkey('alt', 'tab')
        return True
    except Exception:
        return False


def switch_previous_app():
    try:
        pg.hotkey('shift', 'alt', 'tab')
        return True
    except Exception:
        return False


def switch_to_app_by_name(app_name):
    windows = get_open_windows()
    app_name_lower = app_name.lower()
    for w in windows:
        if w["process"].lower() == app_name_lower or app_name_lower in w["process"].lower():
            return switch_to_window(w["hwnd"])
    for w in windows:
        if app_name_lower in w["title"].lower():
            return switch_to_window(w["hwnd"])
    
    return False
