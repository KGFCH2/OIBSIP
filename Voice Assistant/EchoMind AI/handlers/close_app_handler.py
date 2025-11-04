"""Application closing handler"""
import re
import subprocess
from config.settings import OS, PROCESS_NAMES
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_app_closing(command):
    """Handle application closing commands"""
    if not re.search(r'\b(close|shut|kill|terminate|stop)\b.*\b(camera|chrome|firefox|edge|browser|youtube|notepad|calculator|word|excel)\b', command, re.IGNORECASE):
        return False
    
    command_lower = command.lower()
    
    # Extract the app to close
    app_to_close = None
    for app_key in PROCESS_NAMES:
        if app_key in command_lower:
            app_to_close = app_key
            break
    
    if app_to_close and app_to_close in PROCESS_NAMES:
        try:
            process_list = PROCESS_NAMES[app_to_close]
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
                speak(f"Closing {app_to_close}")
                log_interaction(command, f"Closed {app_to_close}", source="local")
            else:
                speak(f"{app_to_close.capitalize()} is not currently running or could not be closed.")
                log_interaction(command, f"Could not close {app_to_close}", source="local")
            return True
        except Exception as e:
            speak(f"Sorry, I couldn't close {app_to_close}.")
            print(f"Error closing app: {e}")
            return False
    
    return False
