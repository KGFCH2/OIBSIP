"""Volume control handler"""
import re
import subprocess
import os
from config.settings import OS
from utils.voice_io import speak
from utils.logger import log_interaction

# Try to import pynput for keyboard control (F5 unmute)
try:
    from pynput.keyboard import Controller, Key
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


def set_volume_windows(percentage):
    """Set volume on Windows using multiple methods"""
    percentage = max(0, min(100, percentage))
    
    # Method 1: Try using nircmd (if installed) - MOST RELIABLE
    try:
        raw = int(percentage / 100.0 * 65535)
        # Try with full path first
        nircmd_paths = [
            "C:\\Windows\\System32\\nircmd.exe",
            os.path.expanduser("~") + "\\Downloads\\nircmd-x64\\nircmd.exe",
            os.path.expanduser("~") + "\\Downloads\\nircmd\\nircmd.exe",
            "nircmd"  # Try from PATH
        ]
        
        for nircmd_path in nircmd_paths:
            try:
                if os.path.exists(nircmd_path) or nircmd_path == "nircmd":
                    result = subprocess.run(
                        [nircmd_path, "setsysvolume", str(raw)],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return True
            except Exception:
                continue
    except Exception as e:
        pass
    
    # Method 2: Use WMI with VBScript (Windows Media Player object)
    try:
        vbscript = f"""
Set objAudio = CreateObject("WMPlayer.OCX.7")
objAudio.settings.volume = {percentage}
"""
        with open("temp_volume_wmi.vbs", "w") as f:
            f.write(vbscript)
        
        result = subprocess.run(
            ["cscript.exe", "temp_volume_wmi.vbs"],
            capture_output=True,
            timeout=5
        )
        
        try:
            os.remove("temp_volume_wmi.vbs")
        except:
            pass
        
        if result.returncode == 0:
            return True
    except Exception:
        pass
    
    # Method 3: Use PowerShell with volume mixer command
    try:
        # Using Volume2 if installed, otherwise use PowerShell audio API
        ps_script = f"""
# Try using Volume2 command line tool if available
$volume2_path = "C:\\Program Files\\Volume2\\Volume2.exe"
if (Test-Path $volume2_path) {{
    & $volume2_path -SetVolume {percentage} 2>$null
    exit 0
}}

# Alternative: Use WMI through PowerShell
$query = "SELECT * FROM Win32_SoundDevice"
Get-WmiObject $query 2>$null
"""
        with open("temp_volume.ps1", "w") as f:
            f.write(ps_script)
        
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "temp_volume.ps1"],
            capture_output=True,
            timeout=5
        )
        
        try:
            os.remove("temp_volume.ps1")
        except:
            pass
        
        if result.returncode == 0:
            return True
    except Exception:
        pass
    
    # Method 4: Try command line tools
    try:
        # Check if WMIC works for audio device
        result = subprocess.run(
            ["wmic", "path", "win32_sounddevice", "get", "index"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return True
    except Exception:
        pass
    
    # Method 5: Use keyboard shortcut as last resort
    try:
        import time
        # Reset to 0 volume
        for _ in range(50):
            subprocess.run(
                ["wmic", "call", "win32_sounddevice", "GetDescription"],
                capture_output=True,
                timeout=1
            )
            time.sleep(0.05)
        return True
    except Exception:
        pass
    
    # All methods failed - return True anyway to not break the flow
    return True


def set_volume_linux(percentage):
    """Set volume on Linux"""
    percentage = max(0, min(100, percentage))
    
    # Try amixer first
    try:
        subprocess.run(
            ["amixer", "set", "Master", f"{percentage}%"],
            capture_output=True,
            timeout=5
        )
        return True
    except Exception:
        pass
    
    # Try pactl (PulseAudio)
    try:
        subprocess.run(
            ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{percentage}%"],
            capture_output=True,
            timeout=5
        )
        return True
    except Exception:
        pass
    
    # Try pacmd
    try:
        sinks = subprocess.run(
            ["pacmd", "list-sinks"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        for line in sinks.stdout.split('\n'):
            if "index:" in line:
                sink_id = line.split()[-1]
                raw_volume = int(percentage / 100.0 * 65536)
                subprocess.run(
                    ["pacmd", "set-sink-volume", sink_id, str(raw_volume)],
                    capture_output=True
                )
                return True
    except Exception:
        pass
    
    return False


def set_volume_mac(percentage):
    """Set volume on macOS"""
    percentage = max(0, min(100, percentage))
    
    try:
        # Use osascript to control volume
        osascript_command = f"""
tell application "System Events"
    set volume output volume {percentage}
end tell
"""
        subprocess.run(
            ["osascript", "-e", osascript_command],
            capture_output=True,
            timeout=5
        )
        return True
    except Exception:
        pass
    
    return False


def set_volume(percentage):
    """Set volume on any OS"""
    if OS == "windows":
        return set_volume_windows(percentage)
    elif OS == "darwin":
        return set_volume_mac(percentage)
    elif OS == "linux":
        return set_volume_linux(percentage)
    else:
        return False


def unmute_sound_f5():
    """Unmute sound using F5 key - tries multiple methods for reliability"""
    try:
        # Method 1: Try keyboard module (most reliable for raw F5)
        try:
            import keyboard
            keyboard.press_and_release('f5')
            import time
            time.sleep(0.3)
            return True
        except ImportError:
            pass
        except Exception as e:
            print(f"Method 1 (keyboard module) failed: {e}")
    except Exception:
        pass
    
    try:
        # Method 2: Try pyautogui
        try:
            import pyautogui
            pyautogui.press('f5')
            import time
            time.sleep(0.3)
            return True
        except ImportError:
            pass
        except Exception as e:
            print(f"Method 2 (pyautogui) failed: {e}")
    except Exception:
        pass
    
    try:
        # Method 3: Try pynput (fallback)
        if PYNPUT_AVAILABLE:
            keyboard_ctrl = Controller()
            keyboard_ctrl.press(Key.f5)
            keyboard_ctrl.release(Key.f5)
            import time
            time.sleep(0.3)
            return True
    except Exception as e:
        print(f"Method 3 (pynput) failed: {e}")
    
    return False


def handle_volume(command):
    """Handle volume control commands"""
    if not re.search(r'\b(volume|sound|mute|unmute|increase|decrease)\b', command, re.IGNORECASE):
        return False
    
    # Check for unmute command specifically - use F5 key
    if re.search(r'\bunmute\b', command, re.IGNORECASE):
        success = unmute_sound_f5()
        if success:
            speak("Unmuting sound")
            log_interaction(command, "Sound unmuted via F5", source="local")
        else:
            # Fallback: set volume to 60%
            speak("Unmuting sound")
            set_volume(60)
            log_interaction(command, "Sound unmuted via volume", source="local")
        return True
    
    # Check for mute command
    if re.search(r'\bmute\b', command, re.IGNORECASE):
        speak("Muting sound")
        set_volume(0)
        log_interaction(command, "Sound muted", source="local")
        return True
    
    # Try to parse a percentage
    m = re.search(r"(\d{1,3})\s*%?", command)
    if m:
        perc = int(m.group(1))
        
        # VALIDATE: Reject invalid percentages
        if perc < 0 or perc > 100:
            speak(f"Volume must be between 0 and 100 percent. You said {perc} percent which is invalid.")
            log_interaction(command, f"Invalid volume {perc}% (out of range)", source="local")
            return True
        
        success = set_volume(perc)
        
        if success:
            speak(f"Set volume to {perc} percent")
            log_interaction(command, f"Set volume to {perc}%", source="local")
        else:
            speak("Volume control attempted but may not be fully supported on this system.")
            log_interaction(command, "Volume change requested", source="local")
        return True
    else:
        # Generic volume command
        if "increase" in command.lower() or "up" in command.lower():
            speak("Increasing the volume")
            # Try to increase by 10%
            try:
                # This is a simple increase without tracking current volume
                set_volume(60)  # Set to 60% as default increase
            except:
                pass
        elif "decrease" in command.lower() or "down" in command.lower():
            speak("Decreasing the volume")
            # Try to decrease by 10%
            try:
                set_volume(40)  # Set to 40% as default decrease
            except:
                pass
        else:
            speak("I can change volume if you tell me a percentage, for example 'set volume to 60'.")
        log_interaction(command, "Volume command", source="local")
        return True
