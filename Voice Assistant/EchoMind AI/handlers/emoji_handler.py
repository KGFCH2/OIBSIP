"""Emoji mode handler - opens emoji selector using F1 key"""
import re
import subprocess
import time
from pynput.keyboard import Controller, Key
from config.settings import OS
from utils.voice_io import speak
from utils.logger import log_interaction


def open_emoji_windows():
    """Open emoji panel on Windows using Win + . (period) or F1 if configured"""
    try:
        keyboard = Controller()
        
        # Method 1: Try F1 key first (if configured on system)
        try:
            keyboard.press(Key.f1)
            keyboard.release(Key.f1)
            time.sleep(0.5)
            return True
        except Exception:
            pass
        
        # Method 2: Try Windows Key + Period (works on Windows 10+)
        try:
            keyboard.press(Key.cmd)
            keyboard.press(Key.period)
            keyboard.release(Key.period)
            keyboard.release(Key.cmd)
            time.sleep(0.5)
            return True
        except Exception:
            pass
        
        # Method 3: Try Windows Key + Semicolon (alternative)
        try:
            keyboard.press(Key.cmd)
            keyboard.press(';')
            keyboard.release(';')
            keyboard.release(Key.cmd)
            time.sleep(0.5)
            return True
        except Exception:
            pass
        
        # Method 4: Use PowerShell to open emoji panel
        try:
            # PowerShell command to open emoji picker
            ps_command = "explorer ms-settings:easeofaccess-keyboard"
            subprocess.Popen(["powershell", "-Command", ps_command])
            time.sleep(0.5)
            return True
        except Exception:
            pass
        
        return False
    except Exception as e:
        print(f"Error in open_emoji_windows: {e}")
        return False


def open_emoji_linux():
    """Open emoji selector on Linux"""
    try:
        # Try different emoji pickers available on Linux
        emoji_tools = [
            "rofimoji",
            "fuzzel --emoji",
            "dmenu_emoji",
            "xdotool key Super_L+period"
        ]
        
        for tool in emoji_tools:
            try:
                subprocess.Popen(tool, shell=True)
                time.sleep(0.5)
                return True
            except Exception:
                continue
        
        return False
    except Exception:
        return False


def open_emoji_mac():
    """Open emoji picker on macOS using Control + Command + Space"""
    try:
        keyboard = Controller()
        
        # macOS emoji picker: Ctrl + Command + Space
        keyboard.press(Key.ctrl)
        keyboard.press(Key.cmd)
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        keyboard.release(Key.cmd)
        keyboard.release(Key.ctrl)
        
        time.sleep(0.5)
        return True
    except Exception:
        return False


def open_emoji():
    """Open emoji selector on any OS"""
    if OS == "windows":
        return open_emoji_windows()
    elif OS == "darwin":
        return open_emoji_mac()
    elif OS == "linux":
        return open_emoji_linux()
    else:
        return False


def handle_emoji_mode(command):
    """Handle emoji mode/picker commands
    
    Supports:
    - "Open emoji"
    - "Emoji mode"
    - "Show emoji"
    - "Open emoji picker"
    - "Emoji picker"
    """
    if not re.search(r'\b(emoji|emoji picker|emoji mode|emoji selector)\b', command, re.IGNORECASE):
        return False
    
    # Check if it's a request to open/show emoji
    if re.search(r'\b(open|show|display|start|launch)\b', command, re.IGNORECASE):
        success = open_emoji()
        
        if success:
            speak("Opening emoji picker")
            log_interaction(command, "Emoji picker opened", source="local")
        else:
            speak("Tried to open emoji picker but it may not be supported on this system.")
            log_interaction(command, "Emoji picker requested", source="local")
        return True
    else:
        # Generic emoji command
        speak("I can open the emoji picker for you. Just say 'open emoji' or 'show emoji'.")
        log_interaction(command, "Emoji command", source="local")
        return True
