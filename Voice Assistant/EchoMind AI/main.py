import speech_recognition as sr
import subprocess
import datetime
import webbrowser
import requests
import os
import platform
import json
import re
import time
from dotenv import load_dotenv
import pytz
import gemini_client
from realtime_poc.poc import LocalTTS

# Load environment variables
load_dotenv()

# Detect operating system
OS = platform.system().lower()

# Initialize the recognizer
recognizer = sr.Recognizer()

# OpenWeather API key from environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")
# Gemini API key for calling the Gemini API (streaming LLM). Keep this in your
# local .env or environment variables and never commit it.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Warn at startup but do not print the key
    print("Warning: GEMINI_API_KEY not set. Gemini features will be disabled until you set this environment variable.")

# Common apps dictionary (Windows-focused, can be extended for other OS)
COMMON_APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "paint": "mspaint",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "ppt": "powerpnt",
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "browser": "chrome",  # default browser
    "file explorer": "explorer",
    "explorer": "explorer",
    "command prompt": "cmd",
    "cmd": "cmd",
    "powershell": "powershell",
    "settings": "start ms-settings:",
    "control panel": "control",
    "task manager": "taskmgr",
    "camera": "start microsoft.windows.camera:",  # UWP app
    "photos": "start microsoft.windows.photos:",  # UWP app
    "store": "start ms-windows-store:",
    "google": "chrome",
    "google chrome": "chrome",
}


def log_interaction(user: str, response: str, source: str = "local"):
    """Append a JSON line with the interaction to logs/assistant.jsonl"""
    try:
        _dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(_dir, exist_ok=True)
        entry = {"ts": time.time(), "user": user, "response": response, "source": source}
        with open(os.path.join(_dir, "assistant.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

def speak(text):
    """Cross-platform text-to-speech"""
    print(f"Speaking: {text}")  # Debug print
    try:
        if OS == "windows":
            # Use PowerShell with SAPI for Windows TTS
            subprocess.run(["powershell", "-c", f'(New-Object -ComObject SAPI.SpVoice).Speak("{text}")'], capture_output=True)
        elif OS == "darwin":  # macOS
            # macOS TTS using say command
            subprocess.run(["say", text], capture_output=True)
        elif OS == "linux":
            # Linux TTS using espeak (fallback to festival if available)
            try:
                subprocess.run(["espeak", text], capture_output=True)
            except FileNotFoundError:
                try:
                    subprocess.run(["festival", "--tts"], input=text.encode(), capture_output=True)
                except FileNotFoundError:
                    print(f"TTS not available on this Linux system. Text: {text}")
        else:
            print(f"TTS not supported on {OS}. Text: {text}")
    except Exception as e:
        print(f"Error in speaking: {e}")
        print(f"Text was: {text}")  # Fallback to show text

def listen():
    """Function to listen to user's voice command"""
    # Try a couple of times before falling back to typed input
    attempts = 2
    for attempt in range(attempts):
        with sr.Microphone() as source:
            print("Listening...")
            # Short ambient noise calibration to improve recognition in noisy environments
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Use timeout and phrase_time_limit to avoid blocking indefinitely
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                print("Listening timed out waiting for phrase.")
                speak("I didn't hear anything. Could you please repeat?")
                continue

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            # Could not understand audio
            print("Speech not recognized (UnknownValueError)")
            speak("Sorry, I didn't understand that. Could you repeat?")
            # loop to retry
            continue
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Speech service error: {e}")
            speak("Sorry, my speech service is down.")
            break

    # Fallback: allow user to type the question if speech fails
    try:
        typed = input("Type your question (or press Enter to skip): ")
        typed = typed.strip()
        if typed:
            print(f"User typed: {typed}")
            return typed.lower()
    except Exception:
        pass

    return ""

def get_time():
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    return now.strftime("%H:%M")

def get_date():
    """Get current date and day in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    date_str = now.strftime("%Y-%m-%d")
    day_str = now.strftime("%A")
    return f"{date_str}, and it's a {day_str}"

def search_web(query):
    """Search the web for the query"""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching for {query} on Google")
    log_interaction(query, f"Search opened: {query}", source="local")

def get_weather(city):
    """Get weather information for a city"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius."
        else:
            return "Sorry, I couldn't find weather information for that city."
    except Exception as e:
        return "Sorry, there was an error fetching the weather."

def get_greeting():
    """Get time-based greeting in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    hour = now.hour
    if 5 <= hour < 12:
        return "Good morning! I am EchoMind AI, your voice assistant. How can I help you?"
    elif 12 <= hour < 17:
        return "Good afternoon! I am EchoMind AI, your voice assistant. How can I help you?"
    elif 17 <= hour < 22:
        return "Good evening! I am EchoMind AI, your voice assistant. How can I help you?"
    else:
        return "Good night! I am EchoMind AI, your voice assistant. It is time to rest."

def main():
    greeting = get_greeting()
    speak(greeting)
    while True:
        command = listen()
        if not command:
            continue
        
        # Greeting commands
        if any(word in command for word in ["hello", "hi", "hey", "greetings"]):
            speak("Hello! How can I help you?")
        
        # Time commands
        elif any(phrase in command for phrase in ["time", "what time", "what is the time", "what's the time", "current time", "tell me the time"]):
            time_str = get_time()
            speak(f"The current time is {time_str}")
        
        # Date commands
        elif any(phrase in command for phrase in ["date", "what date", "what is the date", "what's the date", "today's date", "what day is it", "what is the day", "tell me the date", "current date", "current day"]):
            date_info = get_date()
            speak(f"Today's date is {date_info}")
        
        # Weather commands
        elif any(word in command for word in ["weather", "forecast", "temperature"]):
            speak("Which city would you like the weather for?")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
                log_interaction(command, weather_info, source="local")
        
        # Open app commands
        elif any(word in command for word in ["open", "launch", "start"]):
            app = None
            # Try to extract app name from command
            command_lower = command.lower()
            for prefix in ["open ", "launch ", "start "]:
                if command_lower.startswith(prefix):
                    app = command[len(prefix):].strip()
                    break
            if not app:
                speak("Which app would you like to open?")
                app = listen()
            if app:
                app_lower = app.lower().strip()
                # Clean the app name
                app_clean = app_lower.replace("microsoft ", "").replace("ms ", "").replace(" app", "").strip()
                # Map simple names like 'google' -> 'chrome'
                if app_clean in ("google", "google chrome"):
                    app_clean = "chrome"
                # Check if it's a common app
                if app_clean in COMMON_APPS:
                    launch_cmd = COMMON_APPS[app_clean]
                    try:
                        if OS == "windows":
                            if launch_cmd.startswith("start "):
                                # For UWP apps
                                subprocess.run(["cmd", "/c", launch_cmd], shell=True)
                            else:
                                subprocess.run(["cmd", "/c", "start", launch_cmd], shell=True)
                        elif OS == "darwin":  # macOS
                            subprocess.run(["open", "-a", launch_cmd], capture_output=True)
                        elif OS == "linux":
                            subprocess.run(["xdg-open", launch_cmd], capture_output=True)
                        else:
                            print(f"App launching not supported on {OS}")
                        speak(f"Opening {app}")
                        log_interaction(command, f"Opening {app}", source="local")
                    except Exception as e:
                        speak("Sorry, I couldn't open that app.")
                else:
                    # Try to launch directly
                    try:
                        if OS == "windows":
                            subprocess.run(["cmd", "/c", "start", app_clean], shell=True)
                        elif OS == "darwin":  # macOS
                            subprocess.run(["open", "-a", app_clean], capture_output=True)
                        elif OS == "linux":
                            subprocess.run(["xdg-open", app_clean], capture_output=True)
                        else:
                            print(f"App launching not supported on {OS}")
                        speak(f"Opening {app}")
                        log_interaction(command, f"Opening {app}", source="local")
                    except Exception as e:
                        speak("Sorry, I couldn't open that app.")
        
        # Personal questions
        elif any(phrase in command for phrase in ["how are you", "how do you do"]):
            speak("I'm doing well, thank you! How can I assist you?")
            log_interaction(command, "I'm doing well, thank you! How can I assist you?", source="local")
        
        elif any(phrase in command for phrase in ["your name", "who are you", "what are you"]):
            speak("I am EchoMind AI, your voice assistant.")
            log_interaction(command, "I am EchoMind AI, your voice assistant.", source="local")

        # Volume control (basic, best-effort)
        elif any(word in command for word in ["volume", "sound", "mute", "unmute", "increase", "decrease"]):
            # Try to parse a percentage
            m = re.search(r"(\d{1,3})\s*%?", command)
            if m:
                perc = int(m.group(1))
                perc = max(0, min(100, perc))
                # Best-effort: try nircmd if installed (common Windows utility)
                success = False
                if OS == "windows":
                    try:
                        # nircmd expects 0-65535
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
            else:
                # generic volume command
                if "increase" in command or "up" in command:
                    speak("Increasing the volume")
                elif "decrease" in command or "down" in command:
                    speak("Decreasing the volume")
                else:
                    speak("I can change volume if you tell me a percentage, for example 'set volume to 60'.")
                log_interaction(command, "Volume command (no percent)", source="local")
        
        # Exit commands
        elif any(word in command for word in ["exit", "quit", "stop", "bye", "goodbye"]):
            speak("Goodbye!")
            break
        
        # Fallback
        else:
            # Route unknown commands to Gemini (or to the stub in gemini_client).
            try:
                # If streaming is enabled, speak chunks as they arrive using queued TTS
                stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
                if stream_flag:
                    tts = LocalTTS()
                    try:
                        for chunk in gemini_client.stream_generate(command):
                            if chunk:
                                print("[stream chunk]", chunk)
                                tts.speak_async(chunk)
                        # Wait for queued speech to finish
                        try:
                            tts.queue.join()
                        except Exception:
                            pass
                    finally:
                        tts.shutdown()
                    log_interaction(command, "(streamed response)", source="gemini_stream")
                else:
                    # Blocking helper
                    response = gemini_client.generate_response(command)
                    if response:
                        speak(response)
                        log_interaction(command, response, source="gemini")
                    else:
                        speak("Sorry, I couldn't generate a response.")
                        log_interaction(command, "No response returned", source="gemini")
            except Exception as e:
                print(f"Gemini integration error: {e}")
                speak("Sorry, I couldn't process that right now.")
                log_interaction(command, f"Gemini error: {e}", source="gemini")

if __name__ == "__main__":
    main()