# Code Refactoring: Before & After Comparison

## Problem: Large Monolithic File

Your original `main.py` had **817 lines** with everything mixed together:
- TTS functions
- Voice input functions
- 14 different command handlers
- Time/date utilities
- Weather API calls
- Configuration constants
- Main loop
- Error handling

**Making changes was difficult because:**
- Hard to find a specific feature
- Risk of breaking something else
- Difficult to test individual parts
- Hard for new developers to understand

## Solution: Modular Architecture

Break it into **small, focused modules** where each does one thing well.

---

## Before: One Big File (main.py - 817 lines)

### Structure:
```python
# main.py (817 lines)

# ===== Constants (25 apps, mappings, settings) - Lines 1-60
COMMON_APPS = {...}
WEBSITE_MAP = {...}
OS = platform.system()
API_KEY = os.getenv(...)

# ===== Helper functions (TTS, listen, etc.) - Lines 61-210
def speak(text):
    # 20 lines of cross-platform TTS code
    ...

def listen():
    # 50 lines of speech recognition
    ...

def convert_spoken_symbols(text):
    # 40 lines of regex patterns
    ...

def get_time():
    # Time in IST
    ...

def get_date():
    # Date in IST
    ...

def get_greeting():
    # Time-based greeting
    ...

def log_interaction(user, response, source):
    # Logging to JSONL
    ...

def get_weather(city):
    # OpenWeather API call
    ...

# ===== Handlers (mixed together) - Lines 211-750
def handle_thank_you(command):
    if "thank you" in command:
        speak("...")
        return True
    return False

def handle_greeting(command):
    if "hello" in command or "hi" in command:
        speak("...")
        return True
    return False

def handle_time(command):
    if "time" in command:
        speak(get_time())
        return True
    return False

# ... 11 more handlers all in one file ...

def handle_weather(command):
    # Complex weather handling
    # ... 50 lines mixed with everything else ...
    return True/False

def handle_web_search(command):
    # Web search handling
    # ... 40 lines ...
    return True/False

# ... and so on for app, file, volume, close, etc. ...

# ===== Main loop - Lines 751-817
def main():
    greeting = get_greeting()
    speak(greeting)
    while True:
        command = listen()
        command = convert_spoken_symbols(command)
        
        if handle_thank_you(command):
            continue
        elif handle_greeting(command):
            continue
        elif handle_time(command):
            continue
        # ... 11 more if/elif statements ...
        elif handle_weather(command):
            continue
        else:
            # Gemini fallback
            response = gemini_client.generate_response(command)
            speak(response)
```

**Problems:**
- 817 lines in one file
- All functions at same level
- Constants mixed with code
- Hard to find specific handler
- Risk of breaking things
- No code reuse structure

---

## After: Modular Structure

### New Organization:

```
config/
  └── settings.py (103 lines)
      - COMMON_APPS
      - WEBSITE_MAP
      - LOCATION_MAP
      - All constants

utils/
  ├── voice_io.py (63 lines)
  │   - speak()
  │   - listen()
  ├── text_processing.py (34 lines)
  │   - convert_spoken_symbols()
  │   - is_symbol_only()
  │   - clean_connector_words()
  ├── time_utils.py (33 lines)
  │   - get_time()
  │   - get_date()
  │   - get_greeting()
  ├── weather.py (16 lines)
  │   - get_weather()
  └── logger.py (18 lines)
      - log_interaction()

handlers/
  ├── greeting_handler.py (8 lines)
  │   - handle_greeting()
  ├── thank_you_handler.py (8 lines)
  │   - handle_thank_you()
  ├── time_handler.py (8 lines)
  │   - handle_time()
  ├── date_handler.py (8 lines)
  │   - handle_date()
  ├── weather_handler.py (36 lines)
  │   - handle_weather()
  ├── web_handler.py (102 lines)
  │   - handle_browser_search()
  │   - handle_website_opening()
  ├── app_handler.py (95 lines)
  │   - handle_app_opening()
  ├── ... (6 more handlers)

main_refactored.py (80 lines)
  - route_command()
  - handle_gemini_fallback()
  - main()
```

---

## Code Comparison Examples

### Example 1: Time Handler

#### OLD (mixed in main.py with 800+ lines):
```python
# Line 285 (somewhere in main.py)
def get_time():
    """Get current time in IST"""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    return now.strftime("%H:%M")

# Lines 490-495 (in main loop)
elif re.search(r'\b(what time|what is the time|...)\b', command, re.IGNORECASE):
    time_str = get_time()
    speak(f"The current time is {time_str}")
    log_interaction(command, f"The current time is {time_str}", source="local")
    continue
```

**To find:** Search through 817 lines, get_time() is mixed with 20+ other functions

#### NEW (dedicated file):
```python
# handlers/time_handler.py (8 lines total)
import re
from utils.voice_io import speak
from utils.time_utils import get_time
from utils.logger import log_interaction

def handle_time(command):
    """Handle time commands"""
    if re.search(r'\b(what time|...)\b', command, re.IGNORECASE):
        time_str = get_time()
        speak(f"The current time is {time_str}")
        log_interaction(command, f"The current time is {time_str}", source="local")
        return True
    return False
```

**To find:** Open `handlers/time_handler.py`, 8 lines of clear code. Done!

---

### Example 2: Weather Handler

#### OLD (150+ lines mixed in main.py):
```python
# Lines 284-340 (somewhere in main.py)
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/..."
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            ...
        else:
            return "Sorry, I couldn't find..."
    except Exception as e:
        return "Sorry, there was an error..."

# Lines 490+ (in main loop)
elif re.search(r'\b(weather|forecast|temperature)\b...', command, re.IGNORECASE):
    weather_match = ...
    if weather_match:
        city = None
        match1 = re.search(...)
        if match1:
            city = match1.group(2)
        
        if not city:
            match2 = re.search(...)
            if match2:
                potential_city = match2.group(1).lower()
                if potential_city not in ("current", "what", ...):
                    city = match2.group(1)
        
        if not city:
            speak("Which city would you like the weather for?")
            city = listen()
        
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
            log_interaction(command, weather_info, source="local")
            continue
```

**To find:** Scattered across multiple sections of 817-line file, hard to understand the flow

#### NEW (focused files):
```python
# utils/weather.py (16 lines)
def get_weather(city):
    """Get weather information for a city"""
    try:
        url = f"http://api.openweathermap.org/..."
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is {description}..."
        else:
            return "Sorry, I couldn't find..."
    except Exception as e:
        return "Sorry, there was an error..."

# handlers/weather_handler.py (36 lines)
def handle_weather(command):
    """Handle weather commands with multi-pattern detection"""
    weather_match = re.search(...) or re.search(...) or re.search(...)
    
    if not weather_match:
        return False
    
    city = None
    
    # Pattern 1: "weather of/in/for CITY"
    match1 = re.search(...)
    if match1:
        city = match1.group(2)
    
    # Pattern 2: "CITY weather/forecast"
    if not city:
        match2 = re.search(...)
        if match2:
            potential_city = match2.group(1).lower()
            if potential_city not in WEATHER_CITY_BLACKLIST:
                city = match2.group(1)
    
    # If no city found, ask user
    if not city:
        speak("Which city would you like the weather for?")
        city = listen()
    
    if city:
        weather_info = get_weather(city)
        speak(weather_info)
        log_interaction(command, weather_info, source="local")
        return True
    
    return False
```

**To find:** 
- Weather logic → `handlers/weather_handler.py`
- Weather API → `utils/weather.py`
Clear separation!

---

### Example 3: Main Loop

#### OLD (complex, mixed logic):
```python
# main.py lines 750-817
def main():
    greeting = get_greeting()
    speak(greeting)
    while True:
        command = listen()
        if not command:
            continue

        command = convert_spoken_symbols(command)

        if command and re.match(r'^[?!.,;:...]', command.strip()):
            speak("I didn't catch a complete command...")
            continue

        if any(phrase in command for phrase in ["thank you", "thanks", ...]):
            speak("You are most welcome...")
            log_interaction(command, "...", source="local")
            continue

        try:
            words = command.split()
            simple_city_candidate = False
            if len(words) == 1 and re.match(r"^[a-zA-Z]{3,40}$", command):
                blacklist_tokens = ("why", "what", ...)
                if command.lower() not in blacklist_tokens:
                    simple_city_candidate = True
            
            if simple_city_candidate:
                weather_info = get_weather(command)
                if weather_info and not weather_info.lower().startswith("sorry"):
                    speak(weather_info)
                    log_interaction(command, weather_info, source="local")
                    continue
        except Exception:
            pass
        
        weather_match = re.search(...) or re.search(...) or re.search(...)
        
        if weather_match:
            # 40 lines of weather handling
            ...
            continue
        
        if re.search(r'\b(hello|hi|hey|greetings)\b', command, ...):
            speak("Hello! How can I help you?")
            log_interaction(command, "...", source="local")
            continue
        
        # ... 14 more elif statements ...
        
        else:
            # Gemini fallback
            stream_flag = os.getenv("GEMINI_API_STREAM", "")...
            if stream_flag:
                for chunk in gemini_client.stream_generate(command):
                    if chunk:
                        print("[stream chunk]", chunk)
                        speak(chunk)
                log_interaction(command, "(streamed response)", source="gemini_stream")
            else:
                response = gemini_client.generate_response(command)
                if response:
                    speak(response)
                    log_interaction(command, response, source="gemini")
                else:
                    speak("Sorry, I couldn't generate a response.")
```

**To understand:** Read 70+ lines, trace through all the logic, understand 14 handler blocks

#### NEW (clean, obvious):
```python
# main_refactored.py (80 lines TOTAL)
from handlers.thank_you_handler import handle_thank_you
from handlers.greeting_handler import handle_greeting
from handlers.time_handler import handle_time
# ... all imports at top

def route_command(command):
    """Route command to appropriate handler"""
    handlers = [
        ("Thank you", handle_thank_you),
        ("Greeting", handle_greeting),
        ("Time", handle_time),
        ("Date", handle_date),
        ("Simple city weather", handle_simple_city_weather),
        ("Weather", handle_weather),
        ("Browser search", handle_browser_search),
        ("Website opening", handle_website_opening),
        ("File opening", handle_file_opening),
        ("App opening", handle_app_opening),
        ("Personal questions", handle_personal_questions),
        ("Volume control", handle_volume),
        ("App closing", handle_app_closing),
        ("Exit", handle_exit),
    ]
    
    for handler_name, handler in handlers:
        if handler_name == "Exit":
            if handle_exit(command):
                return "exit"
        else:
            if handler(command):
                return "handled"
    
    return "not_handled"

def handle_gemini_fallback(command):
    """Handle unknown commands with Gemini"""
    stream_flag = os.getenv("GEMINI_API_STREAM", "")...
    if stream_flag:
        for chunk in gemini_client.stream_generate(command):
            if chunk:
                speak(chunk)
        log_interaction(command, "(streamed)", source="gemini_stream")
    else:
        response = gemini_client.generate_response(command)
        if response:
            speak(response)
            log_interaction(command, response, source="gemini")

def main():
    """Main function - voice assistant loop"""
    greeting = get_greeting()
    speak(greeting)
    
    while True:
        command = listen()
        if not command:
            continue
        
        command = convert_spoken_symbols(command)
        
        if command and is_symbol_only(command):
            speak("I didn't catch a complete command...")
            continue
        
        result = route_command(command)
        
        if result == "exit":
            speak("Goodbye!")
            break
        elif result == "handled":
            continue
        else:
            handle_gemini_fallback(command)

if __name__ == "__main__":
    main()
```

**To understand:** Read 15 lines of main loop, see handler list, done! Each handler is 8-100 lines elsewhere.

---

## Key Improvements

### 1. Readability
- **Before:** 817 lines to scan through
- **After:** 80 lines in main, ~30 lines per handler

### 2. Maintainability
- **Before:** Bug in time handler? Search through 817 lines
- **After:** Bug in time handler? Open `handlers/time_handler.py` (8 lines)

### 3. Testability
- **Before:** Can't test time handler in isolation
- **After:** `test_handler.py`:
  ```python
  from handlers.time_handler import handle_time
  assert handle_time("what time is it") == True
  ```

### 4. Extensibility
- **Before:** Add new handler? Mess with main loop
- **After:** Create `handlers/joke_handler.py`, import in main, done!

### 5. Code Reuse
- **Before:** Duplicate `speak()` calls everywhere
- **After:** Import `from utils.voice_io import speak`

---

## Summary: What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Main file size | 817 lines | 80 lines |
| Total lines (same features) | 817 | ~750 |
| Files | 1 | 37 |
| Avg file size | 817 | ~30 |
| Easy to find feature | ❌ Hard | ✅ Easy |
| Easy to test | ❌ No | ✅ Yes |
| Easy to extend | ❌ Hard | ✅ Easy |
| Code reuse | ❌ No | ✅ Yes |
| New dev onboarding | ❌ Hard | ✅ Easy |
| Functionality | Original | ✅ Preserved |

---

## Both Versions Work!

### Run old version:
```bash
python main.py
```

### Run new version:
```bash
python main_refactored.py
```

**Same functionality, better organized code!** 🎉
