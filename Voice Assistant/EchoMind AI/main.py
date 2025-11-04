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

# CRITICAL: Load environment variables BEFORE importing gemini_client
# so that gemini_client can read GEMINI_API_ENDPOINT, GEMINI_API_KEY, etc.
load_dotenv()

import gemini_client

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
    # Strip Markdown formatting (asterisks, bold markers) before speaking
    clean_text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "")
    print(f"Speaking: {clean_text}")  # Debug print
    try:
        if OS == "windows":
            # Use PowerShell with SAPI for Windows TTS
            subprocess.run(["powershell", "-c", f'(New-Object -ComObject SAPI.SpVoice).Speak("{clean_text}")'], capture_output=True)
        elif OS == "darwin":  # macOS
            # macOS TTS using say command
            subprocess.run(["say", clean_text], capture_output=True)
        elif OS == "linux":
            # Linux TTS using espeak (fallback to festival if available)
            try:
                subprocess.run(["espeak", clean_text], capture_output=True)
            except FileNotFoundError:
                try:
                    subprocess.run(["festival", "--tts"], input=clean_text.encode(), capture_output=True)
                except FileNotFoundError:
                    print(f"TTS not available on this Linux system. Text: {clean_text}")
        else:
            print(f"TTS not supported on {OS}. Text: {clean_text}")
    except Exception as e:
        print(f"Error in speaking: {e}")
        print(f"Text was: {clean_text}")  # Fallback to show text

def listen():
    """Function to listen to user's voice command"""
    # Try a few times before falling back to typed input. Increase timeouts
    # so the assistant waits longer for the user to speak and for long phrases.
    attempts = 3
    # Use a slightly longer ambient calibration in noisy environments
    ambient_duration = 1.5
    listen_timeout = 8           # seconds to wait for phrase to start
    phrase_time_limit = 12       # seconds max length of phrase

    # enable dynamic energy thresholding for better adaption to environment
    try:
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 1.2
    except Exception:
        pass

    for attempt in range(attempts):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                recognizer.adjust_for_ambient_noise(source, duration=ambient_duration)
            except Exception:
                # ignore calibration errors and continue
                pass

            try:
                # Wait up to `listen_timeout` seconds for the phrase to start and
                # accept up to `phrase_time_limit` seconds for the whole phrase.
                audio = recognizer.listen(source, timeout=listen_timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("Listening timed out waiting for phrase.")
                # Be less noisy on repeated timeouts: only speak on the last attempt
                if attempt == attempts - 1:
                    speak("I didn't hear anything. Could you please repeat?")
                continue

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            # Could not understand audio
            print("Speech not recognized (UnknownValueError)")
            # Prompt to repeat; only speak on the final attempt to reduce noise
            if attempt == attempts - 1:
                speak("Sorry, I didn't understand that. Could you repeat?")
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

def convert_spoken_symbols(text):
    """Convert spoken punctuation marks and symbols into their actual characters"""
    # Dictionary mapping spoken words to symbols
    # Note: More specific patterns should come first to avoid partial matches
    symbol_map = {
        # Question mark - handle variations of how it might be spoken
        r'\bquestion mark\b': '?',
        r'\bquestion\s+mark\b': '?',
        r'\bquestion\b$': '?',  # "question" at end of sentence
        # Exclamation variations
        r'\bexclamation mark\b': '!',
        r'\bexclamation point\b': '!',
        r'\bexclamation\b$': '!',  # at end
        # Period variations
        r'\bperiod\b': '.',
        r'\bfull stop\b': '.',
        r'\bdot\b': '.',
        # Other punctuation
        r'\bcomma\b': ',',
        r'\bcolon\b': ':',
        r'\bsemicolon\b': ';',
        r'\bapostrophe\b': "'",
        r'\bquote\b': '"',
        r'\bdouble quote\b': '"',
        r'\bleft paren\b|\bopening paren\b|\bparens\b': '(',
        r'\bright paren\b|\bclosing paren\b': ')',
        r'\bsquare bracket\b|\bleft bracket\b|\bleft square bracket\b': '[',
        r'\bright bracket\b|\bclosing bracket\b|\bright square bracket\b': ']',
        r'\bat sign\b': '@',
        r'\bhash\b|\bhashtag\b|\bpound sign\b': '#',
        r'\bdollar sign\b': '$',
        r'\bpercent\b|\bpercent sign\b': '%',
        r'\bampersand\b|\band sign\b': '&',
        r'\basterisk\b|\bstar\b': '*',
    }
    
    result = text
    for spoken, symbol in symbol_map.items():
        result = re.sub(spoken, symbol, result, flags=re.IGNORECASE)
    
    return result

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

        # Convert spoken symbols to actual punctuation marks (e.g., "question mark" → "?")
        command = convert_spoken_symbols(command)

        # Skip if command is only a symbol (e.g., just "?", "!", ".", etc.)
        if command and re.match(r'^[?!.,;:\'"()\[\]@#$%&*\-/+=~`|\\<>]+$', command.strip()):
            speak("I didn't catch a complete command. Could you please say something more?")
            continue

        # Quick replies: 'thank you' variants
        if any(phrase in command for phrase in ["thank you", "thanks", "thankyou", "thx", "thank"]):
            speak("You are most welcome.... Happy to help you")
            log_interaction(command, "You are most welcome.... Happy to help you", source="local")
            continue

        # If user just says a city name (short, alpha words only) treat it as a weather query.
        # Avoid falsely matching common commands by checking against a small blacklist.
        try:
            words = command.split()
            simple_city_candidate = False
            # STRICT: Only match single-word city names (e.g., "Paris", "Tokyo")
            # OR two-word cities (e.g., "New York") but NOT question phrases
            if len(words) == 1 and re.match(r"^[a-zA-Z]{3,40}$", command):
                # Single word city - check blacklist of common question/command words
                blacklist_tokens = ("why", "what", "when", "where", "how", "do", "did", "does", "don't", "didn't", "tell", "is", "are", "be", "open", "hello", "hi")
                if command.lower() not in blacklist_tokens:
                    simple_city_candidate = True
            
            if simple_city_candidate:
                # Try fetching weather for this candidate; if successful, respond and continue
                weather_info = get_weather(command)
                if weather_info and not weather_info.lower().startswith("sorry"):
                    speak(weather_info)
                    log_interaction(command, weather_info, source="local")
                    continue
        except Exception:
            pass
        
        # Weather commands - check for weather-related keywords OR city names with weather context
        # Patterns: "weather of CITY", "CITY weather", "weather in CITY", "CITY current weather", etc.
        weather_match = re.search(r'\b(weather|forecast|temperature)\b.*\b(in|of|at|for|around)\s+(\w+)\b', command, re.IGNORECASE) or \
                       re.search(r'\b(\w+)\s+(weather|forecast|temperature|current weather)\b', command, re.IGNORECASE) or \
                       re.search(r'\b(weather|forecast|temperature|current weather)\b', command, re.IGNORECASE)
        
        if weather_match:
            # Try to extract city name from the command
            city = None
            
            # Try pattern: "weather of/in/for CITY"
            match1 = re.search(r'\b(weather|forecast|temperature)\b.*\b(?:of|in|at|for|around)\s+(\w+)\b', command, re.IGNORECASE)
            if match1:
                city = match1.group(2)
            
            # Try pattern: "CITY weather/forecast" (but not "current")
            if not city:
                match2 = re.search(r'\b(\w+)\s+(weather|forecast|temperature|current weather)\b', command, re.IGNORECASE)
                if match2:
                    potential_city = match2.group(1).lower()
                    # Don't use "current" as city name
                    if potential_city not in ("current", "what", "tell", "give", "show", "get", "find"):
                        city = match2.group(1)
            
            # If no city found, ask user
            if not city:
                speak("Which city would you like the weather for?")
                city = listen()
            
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
                log_interaction(command, weather_info, source="local")
                continue
        
        # Greeting commands (use word boundaries to avoid matching "hi" in "hrithik")
        if re.search(r'\b(hello|hi|hey|greetings)\b', command, re.IGNORECASE):
            speak("Hello! How can I help you?")
            log_interaction(command, "Hello! How can I help you?", source="local")
            continue
        
        # Time commands (word boundary matching - must NOT match if part of "why" or other words)
        elif re.search(r'\b(what time|what is the time|what\'s the time|current time|tell me the time|time now)\b', command, re.IGNORECASE):
            time_str = get_time()
            speak(f"The current time is {time_str}")
            log_interaction(command, f"The current time is {time_str}", source="local")
            continue
        
        # Date commands (word boundary matching)
        elif re.search(r'\b(date|what date|what is the date|what\'s the date|today\'s date|what day is it|what is the day|tell me the date|current date|current day)\b', command, re.IGNORECASE):
            date_info = get_date()
            speak(f"Today's date is {date_info}")
            log_interaction(command, f"Today's date is {date_info}", source="local")
            continue
        
        # Web search and browser commands (e.g., "open youtube on google", "search hindi songs on google")
        # This must come BEFORE generic "open app" handler to catch website/browser commands
        elif re.search(r'\b(open|search)\b.*\b(on|in)\b.*\b(chrome|firefox|edge|google)\b', command, re.IGNORECASE):
            # Parse: "open/search <query> on/in <browser>"
            # Examples: "open youtube on google", "search hindi songs in firefox"
            command_lower = command.lower()
            
            # Extract browser
            browser = None
            if "chrome" in command_lower or "google" in command_lower:
                browser = "chrome"
                browser_name = "chrome"
            elif "firefox" in command_lower:
                browser = "firefox"
                browser_name = "firefox"
            elif "edge" in command_lower:
                browser = "edge"
                browser_name = "microsoft edge"
            
            # Extract search query - everything between "open/search" and "on/in"
            query = None
            if " on " in command_lower:
                parts = command_lower.split(" on ")
                if len(parts) >= 2:
                    query_part = parts[0]
                    # Remove "open " or "search " prefix
                    if query_part.startswith("open "):
                        query = query_part[5:].strip()
                    elif query_part.startswith("search "):
                        query = query_part[7:].strip()
                    else:
                        query = query_part.strip()
            elif " in " in command_lower:
                parts = command_lower.split(" in ")
                if len(parts) >= 2:
                    query_part = parts[0]
                    # Remove "open " or "search " prefix
                    if query_part.startswith("open "):
                        query = query_part[5:].strip()
                    elif query_part.startswith("search "):
                        query = query_part[7:].strip()
                    else:
                        query = query_part.strip()
            
            if browser and query:
                try:
                    # Check if query is a URL or a search term
                    if query.startswith("http://") or query.startswith("https://") or "." in query:
                        # It's likely a URL (youtube, wikipedia, etc.)
                        url = query if query.startswith("http") else f"https://{query}"
                    else:
                        # It's a search query - use Google search
                        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    
                    # Launch the browser
                    if browser == "chrome":
                        if OS == "windows":
                            subprocess.Popen(["cmd", "/c", f"start chrome {url}"], shell=True)
                        elif OS == "darwin":
                            subprocess.Popen(["open", "-a", "Google Chrome", url])
                        elif OS == "linux":
                            subprocess.Popen(["google-chrome", url])
                    elif browser == "firefox":
                        if OS == "windows":
                            subprocess.Popen(["cmd", "/c", f"start firefox {url}"], shell=True)
                        elif OS == "darwin":
                            subprocess.Popen(["open", "-a", "Firefox", url])
                        elif OS == "linux":
                            subprocess.Popen(["firefox", url])
                    elif browser == "edge":
                        if OS == "windows":
                            subprocess.Popen(["cmd", "/c", f"start msedge {url}"], shell=True)
                        elif OS == "darwin":
                            subprocess.Popen(["open", "-a", "Microsoft Edge", url])
                        elif OS == "linux":
                            subprocess.Popen(["microsoft-edge", url])
                    
                    speak(f"Opening {query} on {browser_name}")
                    log_interaction(command, f"Opened {query} on {browser_name}", source="local")
                except Exception as e:
                    speak("Sorry, I couldn't open that in the browser.")
                    print(f"Browser opening error: {e}")
        
        # Handle website/URL opening with default browser (e.g., "open youtube", "open wikipedia")
        elif re.search(r'\b(open|visit|go to)\b\s+(youtube|wikipedia|reddit|github|facebook|twitter|instagram|gmail|google\.com|stack\s*overflow)', command, re.IGNORECASE):
            command_lower = command.lower()
            website_map = {
                'youtube': 'https://www.youtube.com',
                'wikipedia': 'https://www.wikipedia.com',
                'reddit': 'https://www.reddit.com',
                'github': 'https://www.github.com',
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com',
                'instagram': 'https://www.instagram.com',
                'gmail': 'https://mail.google.com',
                'google': 'https://www.google.com',
                'stackoverflow': 'https://stackoverflow.com',
                'stack overflow': 'https://stackoverflow.com',
            }
            
            # Find which website was mentioned
            website = None
            for site_key in website_map:
                if site_key in command_lower:
                    website = site_key
                    break
            
            if website:
                try:
                    url = website_map[website]
                    if OS == "windows":
                        subprocess.Popen(["cmd", "/c", f"start chrome {url}"], shell=True)
                    elif OS == "darwin":
                        subprocess.Popen(["open", "-a", "Google Chrome", url])
                    elif OS == "linux":
                        subprocess.Popen(["google-chrome", url])
                    speak(f"Opening {website}")
                    log_interaction(command, f"Opened {website}", source="local")
                except Exception as e:
                    speak(f"Sorry, I couldn't open {website}.")
                    print(f"Error: {e}")
        
        # Handle file opening (e.g., "open a pdf", "open a file", "open documents")
        elif re.search(r'\b(open|show)\b.*(pdf|file|document|documents|folder|downloads|pictures|music|videos|explorer)', command, re.IGNORECASE):
            command_lower = command.lower()
            
            # Map file types to common locations
            location_map = {
                'downloads': os.path.expanduser('~\\Downloads'),
                'documents': os.path.expanduser('~\\Documents'),
                'pictures': os.path.expanduser('~\\Pictures'),
                'music': os.path.expanduser('~\\Music'),
                'videos': os.path.expanduser('~\\Videos'),
                'desktop': os.path.expanduser('~\\Desktop'),
            }
            
            # Determine which location to open
            location = None
            for loc_key in location_map:
                if loc_key in command_lower:
                    location = location_map[loc_key]
                    break
            
            # Default to opening file explorer
            if not location:
                if OS == "windows":
                    location = os.path.expanduser('~\\Documents')
                else:
                    location = os.path.expanduser('~')
            
            try:
                if OS == "windows":
                    subprocess.Popen(["explorer", location])
                elif OS == "darwin":
                    subprocess.Popen(["open", location])
                elif OS == "linux":
                    subprocess.Popen(["nautilus", location])
                
                speak(f"Opening file explorer")
                log_interaction(command, "Opened file explorer", source="local")
            except Exception as e:
                speak("Sorry, I couldn't open the file explorer.")
                print(f"Error: {e}")
        
        # Open app commands (word boundary matching) - comes AFTER web/file handling
        elif re.search(r'\b(open|launch|start)\b', command, re.IGNORECASE):
            app = None
            remaining_text = None
            # Try to extract app name from command - only grab the first word (or microsoft/ms + word)
            command_lower = command.lower()
            for prefix in ["open ", "launch ", "start "]:
                if command_lower.startswith(prefix):
                    remainder = command[len(prefix):].strip()
                    app_words = remainder.split()
                    
                    if len(app_words) >= 2:
                        first_word = app_words[0].lower()
                        # Check for multi-word apps (microsoft word, ms excel, etc.)
                        if "microsoft" in first_word or first_word == "ms":
                            app = " ".join(app_words[:2])
                            remaining_text = " ".join(app_words[2:]) if len(app_words) > 2 else None
                        elif first_word in COMMON_APPS:
                            # Single-word app found
                            app = first_word
                            remaining_text = " ".join(app_words[1:]) if len(app_words) > 1 else None
                        else:
                            # Unknown app, just use first word
                            app = first_word
                            remaining_text = " ".join(app_words[1:]) if len(app_words) > 1 else None
                    else:
                        # Single word
                        app = remainder
                        remaining_text = None
                    break
            
            # Clean up connector words from remaining text (and, with, to, inside, etc.)
            if remaining_text:
                connector_words = ["and ", "with ", "to ", "inside ", "then ", "also "]
                for connector in connector_words:
                    if remaining_text.lower().startswith(connector):
                        remaining_text = remaining_text[len(connector):].strip()
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
                        
                        # If there's remaining text (e.g., "write a hindi story"), process it with Gemini
                        if remaining_text and remaining_text.strip():
                            time.sleep(1)  # Give the app time to launch
                            speak(f"Now, {remaining_text}")
                            stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
                            if stream_flag:
                                try:
                                    for chunk in gemini_client.stream_generate(remaining_text):
                                        if chunk:
                                            print("[stream chunk]", chunk)
                                            speak(chunk)
                                    log_interaction(remaining_text, "(streamed response)", source="gemini_stream")
                                except Exception as e:
                                    print("Streaming error:", e)
                                    speak("Sorry, there was an error with the response.")
                            else:
                                response = gemini_client.generate_response(remaining_text)
                                if response:
                                    speak(response)
                                    log_interaction(remaining_text, response, source="gemini")
                                else:
                                    speak("Sorry, I couldn't generate a response.")
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
                        
                        # If there's remaining text, process it with Gemini
                        if remaining_text and remaining_text.strip():
                            time.sleep(1)  # Give the app time to launch
                            speak(f"Now, {remaining_text}")
                            stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
                            if stream_flag:
                                try:
                                    for chunk in gemini_client.stream_generate(remaining_text):
                                        if chunk:
                                            print("[stream chunk]", chunk)
                                            speak(chunk)
                                    log_interaction(remaining_text, "(streamed response)", source="gemini_stream")
                                except Exception as e:
                                    print("Streaming error:", e)
                                    speak("Sorry, there was an error with the response.")
                            else:
                                response = gemini_client.generate_response(remaining_text)
                                if response:
                                    speak(response)
                                    log_interaction(remaining_text, response, source="gemini")
                                else:
                                    speak("Sorry, I couldn't generate a response.")
                    except Exception as e:
                        speak("Sorry, I couldn't open that app.")
        
        # Personal questions (word boundary matching)
        elif re.search(r'\b(how are you|how do you do)\b', command, re.IGNORECASE):
            speak("I'm doing well, thank you! How can I assist you?")
            log_interaction(command, "I'm doing well, thank you! How can I assist you?", source="local")
        
        elif re.search(r'\b(your name|who are you|what are you)\b', command, re.IGNORECASE):
            speak("I am EchoMind AI, your voice assistant.")
            log_interaction(command, "I am EchoMind AI, your voice assistant.", source="local")

        # Volume control (word boundary matching)
        elif re.search(r'\b(volume|sound|mute|unmute|increase|decrease)\b', command, re.IGNORECASE):
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
        
        # Close application commands (e.g., "close camera", "close youtube", "close browser", "close chrome")
        elif re.search(r'\b(close|shut|kill|terminate|stop)\b.*\b(camera|chrome|firefox|edge|browser|youtube|notepad|calculator|word|excel)\b', command, re.IGNORECASE):
            command_lower = command.lower()
            
            # Extract the app to close
            app_to_close = None
            process_names = {
                "camera": ["microsoft.windows.camera", "camera"],
                "chrome": ["chrome.exe", "chrome"],
                "google": ["chrome.exe", "chrome"],
                "firefox": ["firefox.exe", "firefox"],
                "edge": ["msedge.exe", "msedge"],
                "browser": ["chrome.exe", "firefox.exe", "msedge.exe"],  # Close all browsers
                "youtube": ["chrome.exe", "firefox.exe", "msedge.exe"],  # YouTube usually runs in browser
                "notepad": ["notepad.exe"],
                "calculator": ["calc.exe"],
                "word": ["winword.exe"],
                "excel": ["excel.exe"],
                "powerpoint": ["powerpnt.exe"],
                "ppt": ["powerpnt.exe"],
            }
            
            # Find which app was mentioned
            for app_key in process_names:
                if app_key in command_lower:
                    app_to_close = app_key
                    break
            
            if app_to_close and app_to_close in process_names:
                try:
                    process_list = process_names[app_to_close]
                    closed_count = 0
                    
                    if OS == "windows":
                        for proc_name in process_list:
                            try:
                                # Use taskkill to forcefully close the process
                                result = subprocess.run(
                                    ["taskkill", "/IM", proc_name, "/F"],
                                    capture_output=True,
                                    text=True
                                )
                                # taskkill returns 0 if successful, other values if process not found
                                if result.returncode == 0 or "terminated" in result.stdout.lower():
                                    closed_count += 1
                            except Exception as e:
                                print(f"Could not close {proc_name}: {e}")
                    
                    elif OS == "darwin":  # macOS
                        for proc_name in process_list:
                            try:
                                subprocess.run(
                                    ["killall", proc_name],
                                    capture_output=True
                                )
                                closed_count += 1
                            except Exception:
                                pass
                    
                    elif OS == "linux":
                        for proc_name in process_list:
                            try:
                                subprocess.run(
                                    ["killall", proc_name],
                                    capture_output=True
                                )
                                closed_count += 1
                            except Exception:
                                pass
                    
                    if closed_count > 0:
                        speak(f"Closing {app_to_close}")
                        log_interaction(command, f"Closed {app_to_close}", source="local")
                    else:
                        speak(f"{app_to_close.capitalize()} is not currently running or could not be closed.")
                        log_interaction(command, f"Could not close {app_to_close}", source="local")
                
                except Exception as e:
                    speak(f"Sorry, I couldn't close {app_to_close}.")
                    print(f"Error closing app: {e}")
        
        # Exit commands (word boundary matching)
        elif re.search(r'\b(exit|quit|stop|bye|goodbye|terminate)\b', command, re.IGNORECASE):
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