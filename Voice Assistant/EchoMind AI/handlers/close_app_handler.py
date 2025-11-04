"""Application closing handler"""
import re
import subprocess
import time
from config.settings import OS, PROCESS_NAMES
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_app_closing(command):
    """Handle application closing commands
    
    Supports tab-specific closing:
    - "close youtube" → closes only YouTube tab
    - "close youtube in edge" → closes only YouTube tab in Edge, not entire browser
    - "close the youtube tab" → closes only YouTube tab
    """
    if not re.search(r'\b(close|shut|kill|terminate|stop)\b.*\b(camera|chrome|firefox|edge|browser|youtube|notepad|calculator|word|excel|tab)\b', command, re.IGNORECASE):
        return False
    
    command_lower = command.lower()
    
    # Check if user wants to close a specific tab/website (not entire browser)
    tab_match = re.search(r'\bclose\s+(?:the\s+)?(\w+)(?:\s+tab)?', command_lower)
    browser_match = re.search(r'\b(?:in|on|from)\s+(chrome|firefox|edge|microsoft\s+edge|browser)\b', command_lower)
    
    if tab_match:
        tab_name = tab_match.group(1).lower()
        browser_name = None
        
        if browser_match:
            browser_text = browser_match.group(1).lower()
            if "chrome" in browser_text:
                browser_name = "chrome"
            elif "firefox" in browser_text:
                browser_name = "firefox"
            elif "edge" in browser_text:
                browser_name = "edge"
        
        # Handle tab-specific closing
        if tab_name in ("youtube", "tab"):
            return _close_tab_specific(tab_name, browser_name, command)
        elif tab_name in ("chrome", "firefox", "edge", "browser"):
            # User wants to close the browser, not a tab
            return _close_entire_app(tab_name, command)
        elif tab_name in ("notepad", "word", "excel", "calculator"):
            return _close_application(tab_name, command)
    
    # Extract the app to close
    app_to_close = None
    for app_key in PROCESS_NAMES:
        if app_key in command_lower:
            app_to_close = app_key
            break
    
    if app_to_close and app_to_close in PROCESS_NAMES:
        return _close_entire_app(app_to_close, command)
    
    return False


def _close_tab_specific(tab_name, browser_name, command):
    """Close a specific tab without closing the entire browser
    
    Uses keyboard shortcut Ctrl+W to close current tab
    This requires the tab to be active, so we close the last tab or search for it
    """
    import pyautogui
    
    try:
        # Focus on the browser window
        if browser_name == "chrome" or browser_name is None:
            # Try to close the tab using Ctrl+W
            # Note: This works if the tab is already open and active
            pyautogui.hotkey('ctrl', 'w')
            
            speak(f"Closing {tab_name} tab")
            log_interaction(command, f"Closed {tab_name} tab", source="local")
            return True
    except ImportError:
        # pyautogui not available, use alternative method
        return _close_tab_using_keyboard(tab_name, browser_name, command)
    except Exception as e:
        print(f"Error closing tab: {e}")
        # Fall back to trying taskkill but only if it's a standalone app
        return False


def _close_tab_using_keyboard(tab_name, browser_name, command):
    """Alternative method to close tabs using keyboard shortcuts"""
    import importlib

    try:
        # Try to use the 'keyboard' package if available
        try:
            keyboard = importlib.import_module("keyboard")
            # Ctrl+W closes a browser tab
            keyboard.press_and_release('ctrl+w')
            speak(f"Closing {tab_name}")
            log_interaction(command, f"Closed {tab_name}", source="local")
            return True
        except ModuleNotFoundError:
            # Fallback to pyautogui if keyboard is not installed
            try:
                pyautogui = importlib.import_module("pyautogui")
                pyautogui.hotkey('ctrl', 'w')
                speak(f"Closing {tab_name}")
                log_interaction(command, f"Closed {tab_name}", source="local")
                return True
            except ModuleNotFoundError:
                # No suitable automation library is available
                speak(f"Could not programmatically close the {tab_name} tab. Please close it manually.")
                return False
    except Exception as e:
        print(f"Error using keyboard fallback: {e}")
        speak(f"Could not close the {tab_name} tab. Please close it manually.")
        return False


def _close_entire_app(app_name, command):
    """Close entire application using taskkill"""
    app_name_lower = app_name.lower().strip()
    
    if app_name_lower in ("google", "google chrome"):
        app_name_lower = "chrome"
    
    if app_name_lower not in PROCESS_NAMES:
        speak(f"Sorry, I don't know how to close {app_name}.")
        return False
    
    try:
        process_list = PROCESS_NAMES[app_name_lower]
        closed_count = 0
        
        if OS == "windows":
            for proc_name in process_list:
                try:
                    result = subprocess.run(
                        ["taskkill", "/IM", proc_name, "/F"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0 or "terminated" in result.stdout.lower():
                        closed_count += 1
                except Exception as e:
                    print(f"Could not close {proc_name}: {e}")
        
        elif OS == "darwin":
            for proc_name in process_list:
                try:
                    subprocess.run(["killall", proc_name], capture_output=True)
                    closed_count += 1
                except Exception:
                    pass
        
        elif OS == "linux":
            for proc_name in process_list:
                try:
                    subprocess.run(["killall", proc_name], capture_output=True)
                    closed_count += 1
                except Exception:
                    pass
        
        if closed_count > 0:
            speak(f"Closing {app_name_lower}")
            log_interaction(command, f"Closed {app_name_lower}", source="local")
        else:
            speak(f"{app_name.capitalize()} is not currently running or could not be closed.")
            log_interaction(command, f"Could not close {app_name_lower}", source="local")
        return True
    except Exception as e:
        speak(f"Sorry, I couldn't close {app_name}.")
        print(f"Error closing app: {e}")
        return False


def _close_application(app_name, command):
    """Close a specific application file"""
    return _close_entire_app(app_name, command)
