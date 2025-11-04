"""Application handler"""
import re
import subprocess
import time
import os
from config.settings import OS, COMMON_APPS
from utils.voice_io import speak, listen
from utils.text_processing import clean_connector_words
from utils.logger import log_interaction

def handle_app_opening(command):
    """Handle application opening commands"""
    if not re.search(r'\b(open|launch|start)\b', command, re.IGNORECASE):
        return False
    
    app = None
    remaining_text = None
    command_lower = command.lower()
    
    # Extract app name from command
    for prefix in ["open ", "launch ", "start "]:
        if command_lower.startswith(prefix):
            remainder = command[len(prefix):].strip()
            app_words = remainder.split()
            
            if len(app_words) >= 2:
                first_word = app_words[0].lower()
                if "microsoft" in first_word or first_word == "ms":
                    app = " ".join(app_words[:2])
                    remaining_text = " ".join(app_words[2:]) if len(app_words) > 2 else None
                elif first_word in COMMON_APPS:
                    app = first_word
                    remaining_text = " ".join(app_words[1:]) if len(app_words) > 1 else None
                else:
                    app = first_word
                    remaining_text = " ".join(app_words[1:]) if len(app_words) > 1 else None
            else:
                app = remainder
                remaining_text = None
            break
    
    # Clean up connector words from remaining text
    if remaining_text:
        remaining_text = clean_connector_words(remaining_text)
    
    if not app:
        speak("Which app would you like to open?")
        app = listen()
    
    if app:
        app_lower = app.lower().strip()
        app_clean = app_lower.replace("microsoft ", "").replace("ms ", "").replace(" app", "").strip()
        
        if app_clean in ("google", "google chrome"):
            app_clean = "chrome"
        
        # Check if it's a common app
        if app_clean in COMMON_APPS:
            launch_cmd = COMMON_APPS[app_clean]
            try:
                if OS == "windows":
                    if launch_cmd.startswith("start "):
                        subprocess.run(["cmd", "/c", launch_cmd], shell=True)
                    else:
                        subprocess.run(["cmd", "/c", "start", launch_cmd], shell=True)
                elif OS == "darwin":
                    subprocess.run(["open", "-a", launch_cmd], capture_output=True)
                elif OS == "linux":
                    subprocess.run(["xdg-open", launch_cmd], capture_output=True)
                
                speak(f"Opening {app}")
                log_interaction(command, f"Opening {app}", source="local")
                
                # If there's remaining text, process it with Gemini
                if remaining_text and remaining_text.strip():
                    _process_remaining_text(remaining_text)
                return True
            except Exception as e:
                speak("Sorry, I couldn't open that app.")
                return False
        else:
            # Try to launch directly
            try:
                if OS == "windows":
                    subprocess.run(["cmd", "/c", "start", app_clean], shell=True)
                elif OS == "darwin":
                    subprocess.run(["open", "-a", app_clean], capture_output=True)
                elif OS == "linux":
                    subprocess.run(["xdg-open", app_clean], capture_output=True)
                
                speak(f"Opening {app}")
                log_interaction(command, f"Opening {app}", source="local")
                
                # If there's remaining text, process it with Gemini
                if remaining_text and remaining_text.strip():
                    _process_remaining_text(remaining_text)
                return True
            except Exception as e:
                speak("Sorry, I couldn't open that app.")
                return False
    
    return False

def _process_remaining_text(text):
    """Helper function to process remaining text with Gemini"""
    import gemini_client
    
    time.sleep(1)  # Give the app time to launch
    speak(f"Now, {text}")
    stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
    
    if stream_flag:
        try:
            for chunk in gemini_client.stream_generate(text):
                if chunk:
                    print("[stream chunk]", chunk)
                    speak(chunk)
            log_interaction(text, "(streamed response)", source="gemini_stream")
        except Exception as e:
            print("Streaming error:", e)
            speak("Sorry, there was an error with the response.")
    else:
        response = gemini_client.generate_response(text)
        if response:
            speak(response)
            log_interaction(text, response, source="gemini")
        else:
            speak("Sorry, I couldn't generate a response.")
