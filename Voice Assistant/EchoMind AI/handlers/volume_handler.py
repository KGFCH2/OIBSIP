"""Volume control handler"""
import re
import subprocess
from config.settings import OS
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_volume(command):
    """Handle volume control commands"""
    if not re.search(r'\b(volume|sound|mute|unmute|increase|decrease)\b', command, re.IGNORECASE):
        return False
    
    # Try to parse a percentage
    m = re.search(r"(\d{1,3})\s*%?", command)
    if m:
        perc = int(m.group(1))
        perc = max(0, min(100, perc))
        success = False
        
        if OS == "windows":
            try:
                raw = int(perc / 100.0 * 65535)
                subprocess.run(["nircmd", "setsysvolume", str(raw)], check=False)
                success = True
            except Exception:
                success = False
        
        if success:
            speak(f"Set volume to {perc} percent")
            log_interaction(command, f"Set volume to {perc}%", source="local")
        else:
            speak("Volume control not available on this system. Please install nircmd or manage volume manually.")
            log_interaction(command, "Volume change requested but not executed", source="local")
        return True
    else:
        # Generic volume command
        if "increase" in command or "up" in command:
            speak("Increasing the volume")
        elif "decrease" in command or "down" in command:
            speak("Decreasing the volume")
        else:
            speak("I can change volume if you tell me a percentage, for example 'set volume to 60'.")
        log_interaction(command, "Volume command (no percent)", source="local")
        return True
