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
from urllib.parse import quote_plus
import threading
from ctypes import POINTER, cast
try:
    # pycaw is optional; we'll use it when available for native Windows volume control
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    _PYCAW_AVAILABLE = True
except Exception:
    _PYCAW_AVAILABLE = False
import shutil
import shutil

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

    def _run_tts(t):
        try:
            if OS == "windows":
                # Use PowerShell with SAPI for Windows TTS
                subprocess.run(["powershell", "-c", f'(New-Object -ComObject SAPI.SpVoice).Speak("{t}")'], capture_output=True)
            elif OS == "darwin":  # macOS
                # macOS TTS using say command
                subprocess.run(["say", t], capture_output=True)
            elif OS == "linux":
                # Linux TTS using espeak (fallback to festival if available)
                try:
                    subprocess.run(["espeak", t], capture_output=True)
                except FileNotFoundError:
                    try:
                        subprocess.run(["festival", "--tts"], input=t.encode(), capture_output=True)
                    except FileNotFoundError:
                        print(f"TTS not available on this Linux system. Text: {t}")
            else:
                print(f"TTS not supported on {OS}. Text: {t}")
        except Exception as e:
            print(f"Error in speaking: {e}")
            print(f"Text was: {t}")  # Fallback to show text

    # Run TTS in background thread so it doesn't block the main loop
    try:
        t = threading.Thread(target=_run_tts, args=(text,), daemon=True)
        t.start()
    except Exception as e:
        print("Failed to start TTS thread:", e)

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


def direct_search(query=None):
    """Open a Google search for the query and try to fetch a short summary.

    This helper safely opens the user's default browser to Google and then
    attempts to fetch a brief summary using DuckDuckGo Instant Answer API
    (no API key required). The DuckDuckGo result is used only as a lightweight
    spoken summary when available.
    """
    # If no query provided, ask the user
    if not query:
        speak("What would you like me to search for on Google?")
        query = listen()
        if not query:
            speak("No search query provided.")
            return

    safe_q = query.strip()
    url = f"https://www.google.com/search?q={quote_plus(safe_q)}"
    try:
        webbrowser.open(url)
        speak(f"Opening Google search for {safe_q}")
        # Try DuckDuckGo instant answer for a short summary
        try:
            ddg_url = (
                "https://api.duckduckgo.com/?format=json&no_html=1&no_redirect=1&q="
                + quote_plus(safe_q)
            )
            r = requests.get(ddg_url, timeout=5)
            if r.status_code == 200:
                body = r.json()
                abstract = body.get("AbstractText") or body.get("Answer") or ""
                if abstract:
                    # Keep it short
                    short = abstract.strip()
                    if len(short) > 400:
                        short = short[:400].rsplit(".", 1)[0] + "."
                    speak(short)
                    log_interaction(query, short, source="ddg")
                    return
                # Fallback to RelatedTopics snippet
                topics = body.get("RelatedTopics") or []
                if topics:
                    # Try to find first text
                    for t in topics:
                        if isinstance(t, dict):
                            text = t.get("Text") or t.get("Result") or None
                            if text:
                                speak(text)
                                log_interaction(query, text, source="ddg_related")
                                return
        except Exception:
            # If DuckDuckGo fails, don't block — we've already opened the browser
            pass

        # If no summary found, at least log the search
        log_interaction(query, f"Search opened: {safe_q}", source="local")
    except Exception as e:
        speak("Sorry, I couldn't open the browser for that search.")
        log_interaction(query, f"Search error: {e}", source="local")

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


def _pycaw_set_master_volume_percent(pct: float) -> bool:
    """Set master volume to pct (0-100) using pycaw. Returns True on success."""
    if not _PYCAW_AVAILABLE:
        return False
    try:
        sessions = AudioUtilities.GetSpeakers()
        interface = sessions.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        scalar = max(0.0, min(1.0, pct / 100.0))
        volume.SetMasterVolumeLevelScalar(scalar, None)
        return True
    except Exception:
        return False


def _pycaw_change_master_volume_by_percent(delta_pct: float) -> bool:
    if not _PYCAW_AVAILABLE:
        return False
    try:
        sessions = AudioUtilities.GetSpeakers()
        interface = sessions.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        cur = volume.GetMasterVolumeLevelScalar()
        new = max(0.0, min(1.0, cur + delta_pct / 100.0))
        volume.SetMasterVolumeLevelScalar(new, None)
        return True
    except Exception:
        return False


def _pycaw_get_master_volume_percent() -> float | None:
    if not _PYCAW_AVAILABLE:
        return None
    try:
        sessions = AudioUtilities.GetSpeakers()
        interface = sessions.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        cur = volume.GetMasterVolumeLevelScalar()
        return float(cur * 100.0)
    except Exception:
        return None

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
        elif any(word in command for word in ["volume", "sound", "mute", "unmute", "increase", "decrease", "up", "down", "set volume", "set volume to", "set volume up", "set volume down"]):
            # Parse intents: absolute set (to X%), relative change (by X%) or simple up/down
            # Examples supported: "set volume to 60", "increase volume by 20", "decrease volume 10", "volume up"
            # Find numeric percentage if present
            m = re.search(r"(\d{1,3})\s*%?", command)
            perc = None
            if m:
                try:
                    perc = int(m.group(1))
                    perc = max(0, min(100, perc))
                except Exception:
                    perc = None

            # Detect increase vs decrease vs set
            is_increase = any(tok in command for tok in ("increase", "up")) and "by" in command
            is_decrease = any(tok in command for tok in ("decrease", "down")) and "by" in command
            is_set = any(phrase in command for phrase in ("set volume to", "set volume")) or (perc is not None and ("to" in command or "set" in command))

            # Helper to speak and log result
            def _ack(msg):
                speak(msg)
                log_interaction(command, msg, source="local")

            # Try nircmd on Windows if available
            nircmd = None
            if OS == "windows":
                nircmd = shutil.which("nircmd") or shutil.which("nircmd.exe")

            try:
                if nircmd and OS == "windows":
                    # nircmd uses 0-65535 volume scale
                    scale = 65535
                    if is_set and perc is not None:
                        raw = int(perc / 100.0 * scale)
                        subprocess.run([nircmd, "setsysvolume", str(raw)], check=False)
                        _ack(f"Set volume to {perc} percent")
                    elif (is_increase or ("increase" in command and "by" in command)) and perc is not None:
                        delta = int(perc / 100.0 * scale)
                        subprocess.run([nircmd, "changesysvolume", str(delta)], check=False)
                        _ack(f"Increased volume by {perc} percent")
                    elif (is_decrease or ("decrease" in command and "by" in command)) and perc is not None:
                        delta = int(perc / 100.0 * scale)
                        # changesysvolume accepts negative values to decrease
                        subprocess.run([nircmd, "changesysvolume", str(-delta)], check=False)
                        _ack(f"Decreased volume by {perc} percent")
                    else:
                        # No numeric provided: default +/- 10%
                        default_delta = int(0.1 * scale)
                        if any(tok in command for tok in ("increase", "up")):
                            subprocess.run([nircmd, "changesysvolume", str(default_delta)], check=False)
                            _ack("Increased volume")
                        elif any(tok in command for tok in ("decrease", "down")):
                            subprocess.run([nircmd, "changesysvolume", str(-default_delta)], check=False)
                            _ack("Decreased volume")
                        else:
                            _ack("I can set the volume if you tell me a percentage, for example 'set volume to 60' or 'increase volume by 10'.")
                else:
                    # nircmd not available: instruct user how to enable or provide fallback
                    if perc is not None and is_set:
                        _ack(f"I can't change system volume from here. Please install nircmd (https://www.nirsoft.net/utils/nircmd.html) to enable setting the volume to {perc} percent automatically.")
                    elif perc is not None and (is_increase or is_decrease):
                        _ack(f"I can't change system volume from here. Please install nircmd to enable changing volume by {perc} percent automatically.")
                    else:
                        _ack("Volume control not available on this system. To enable programmatic volume control on Windows, install nircmd and add it to your PATH.")
            except Exception as e:
                print("Volume change error:", e)
                speak("Sorry, I couldn't change the volume right now.")
        
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
                    # Best-effort streaming: speak chunks as they arrive.
                    try:
                        for chunk in gemini_client.stream_generate(command):
                            if chunk:
                                print("[stream chunk]", chunk)
                                speak(chunk)
                        log_interaction(command, "(streamed response)", source="gemini_stream")
                    except Exception as e:
                        print("Streaming error:", e)
                        speak("Sorry, there was an error with streaming response.")
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