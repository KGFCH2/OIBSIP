# EchoMind AI - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   USER INPUT (Voice/Text)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    main_refactored.py                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  listen() - Get voice input                            ││
│  │  convert_spoken_symbols() - "question mark" → "?"      ││
│  │  is_symbol_only() - Skip "?" or "!"                    ││
│  └─────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────┘
                         │
                    Processed
                    Command
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              route_command(command)                          │
│  Checks 14 handlers in priority order:                     │
│                                                             │
│  1. Thank You        ──►  handle_thank_you()              │
│  2. Greeting         ──►  handle_greeting()               │
│  3. Time             ──►  handle_time()                   │
│  4. Date             ──►  handle_date()                   │
│  5. Simple Weather   ──►  handle_simple_city_weather()    │
│  6. Weather          ──►  handle_weather()                │
│  7. Browser Search   ──►  handle_browser_search()         │
│  8. Website          ──►  handle_website_opening()        │
│  9. File             ──►  handle_file_opening()           │
│ 10. App              ──►  handle_app_opening()            │
│ 11. Personal         ──►  handle_personal_questions()     │
│ 12. Volume           ──►  handle_volume()                 │
│ 13. Close App        ──►  handle_app_closing()            │
│ 14. Exit             ──►  handle_exit()                   │
│                                                             │
│ First match wins!                                           │
│ Returns: "handled", "exit", or "not_handled"              │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │          │
            handled/exit    not_handled
                    │          │
                    ▼          ▼
        ┌──────────────────┐  ┌─────────────────────────────┐
        │   Log Response   │  │  handle_gemini_fallback()   │
        │   & Return       │  │  ┌─────────────────────────┐│
        │                  │  │  │ Gemini API Processing   ││
        │                  │  │  │ (Streaming or Blocking) ││
        │                  │  │  └─────────────────────────┘│
        └──────────────────┘  └────────────┬────────────────┘
                    │                      │
                    │                  Log Response
                    │                      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  speak(response)     │
                    │  TTS to user         │
                    └──────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Continue Loop /     │
                    │  or Exit             │
                    └──────────────────────┘
```

## Module Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    main_refactored.py                        │
│  (Orchestration - 80 lines)                                 │
└────────────────┬───────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────────┐ ┌────────┐ ┌─────────────────┐
│  config/   │ │ utils/ │ │  handlers/      │
│ settings.py│ │ (6)    │ │  (14)           │
│            │ │        │ │                 │
│ Constants: │ │ voice_ │ │ greeting_h      │
│ - APPS     │ │ io     │ │ thank_you_h     │
│ - WEBSITES │ │ text_  │ │ time_h          │
│ - PATHS    │ │ process│ │ date_h          │
│ - KEYS     │ │ time_  │ │ weather_h       │
│            │ │ utils  │ │ simple_w_h      │
│            │ │ weather│ │ web_h           │
│            │ │ logger │ │ file_h          │
│            │ │        │ │ app_h           │
│            │ │        │ │ personal_h      │
│            │ │        │ │ volume_h        │
│            │ │        │ │ close_app_h     │
│            │ │        │ │ exit_h          │
└────────────┘ └────────┘ └─────────────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
              Imported by
              all handlers
                   │
                   ▼
      ┌────────────────────────┐
      │  External Libraries    │
      ├────────────────────────┤
      │ speech_recognition     │
      │ requests (weather)     │
      │ pytz (timezone)        │
      │ python-dotenv          │
      │ google-generativeai    │
      └────────────────────────┘
```

## Handler Execution Flow

```
User Says: "Open notepad and write a story"
         │
         ▼
   listen() → "open notepad and write a story"
         │
         ▼
   convert_spoken_symbols() → (no symbols to convert)
         │
         ▼
   is_symbol_only() → False (contains real words)
         │
         ▼
   route_command() checks:
   
   ├─ handle_thank_you() → False
   ├─ handle_greeting() → False
   ├─ handle_time() → False
   ├─ handle_date() → False
   ├─ handle_simple_city_weather() → False
   ├─ handle_weather() → False
   ├─ handle_browser_search() → False
   ├─ handle_website_opening() → False
   ├─ handle_file_opening() → False
   ├─ handle_app_opening() → TRUE! ✓
   │  ├─ Extract app: "notepad"
   │  ├─ Extract remaining: "and write a story"
   │  ├─ Clean connector: "write a story"
   │  ├─ Launch notepad
   │  ├─ speak("Opening notepad")
   │  ├─ Wait 1 second for app to launch
   │  ├─ Call Gemini API with "write a story"
   │  ├─ speak(gemini_response)
   │  └─ log_interaction()
   └─ (returns "handled")
         │
         ▼
   Continue main loop
```

## File Organization Visual

```
EchoMind AI/
│
├── ⚙️  CONFIGURATION
│   └── config/
│       └── settings.py ········· All constants
│
├── 🛠️  UTILITIES (Reusable)
│   └── utils/
│       ├── voice_io.py ········· speak(), listen()
│       ├── text_processing.py ·· Symbols, cleanup
│       ├── time_utils.py ······· Time, date, greeting
│       ├── weather.py ········· Weather API
│       └── logger.py ·········· Logging
│
├── 🎯 HANDLERS (Command processors)
│   └── handlers/
│       ├── greeting_handler.py
│       ├── thank_you_handler.py
│       ├── time_handler.py
│       ├── date_handler.py
│       ├── simple_weather_handler.py
│       ├── weather_handler.py
│       ├── web_handler.py
│       ├── file_handler.py
│       ├── app_handler.py
│       ├── personal_handler.py
│       ├── volume_handler.py
│       ├── close_app_handler.py
│       └── exit_handler.py
│
├── 🚀 ENTRY POINTS
│   ├── main_refactored.py ······ NEW (recommended)
│   └── main.py ················· OLD (still works)
│
├── 🔌 EXTERNAL
│   ├── gemini_client.py ········ Gemini integration
│   └── .env ···················· Environment variables
│
└── 📚 DOCUMENTATION
    ├── MODULAR_ARCHITECTURE.md
    ├── REFACTORING_GUIDE.md
    ├── FILE_REFERENCE.md
    ├── BEFORE_AFTER_COMPARISON.md
    ├── REFACTORING_SUMMARY.md
    └── START_REFACTORING.md
```

## Handler Registration & Priority

```
┌─────────────────────────────────────────────────┐
│  route_command() Handler Priority Chain         │
│  (handlers checked in this order)               │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. ("Thank you", handle_thank_you)             │
│     └─ "thank you", "thanks", "thankful"       │
│                                                 │
│  2. ("Greeting", handle_greeting)               │
│     └─ "hello", "hi", "hey"                    │
│                                                 │
│  3. ("Time", handle_time)                       │
│     └─ "what time is it", "time"               │
│                                                 │
│  4. ("Date", handle_date)                       │
│     └─ "what date", "what day"                 │
│                                                 │
│  5. ("Simple weather", handle_simple_...)       │
│     └─ Single word: "Mumbai", "Paris"          │
│                                                 │
│  6. ("Weather", handle_weather)                 │
│     └─ "weather of X", "X weather"             │
│                                                 │
│  7. ("Browser search", handle_browser...)       │
│     └─ "open youtube on firefox"               │
│                                                 │
│  8. ("Website", handle_website_opening)         │
│     └─ "open youtube"                          │
│                                                 │
│  9. ("File", handle_file_opening)               │
│     └─ "open downloads", "show documents"      │
│                                                 │
│ 10. ("App", handle_app_opening)                 │
│     └─ "open notepad"                          │
│                                                 │
│ 11. ("Personal", handle_personal...)            │
│     └─ "who are you", "how are you"            │
│                                                 │
│ 12. ("Volume", handle_volume)                   │
│     └─ "volume 50%"                            │
│                                                 │
│ 13. ("Close app", handle_app_closing)           │
│     └─ "close chrome"                          │
│                                                 │
│ 14. ("Exit", handle_exit)                       │
│     └─ "bye", "quit", "exit"                   │
│                                                 │
│ → If none match: Gemini API fallback            │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Data Flow Example: "Weather in Mumbai"

```
User Input
    │
    ▼
listen()
"what is the weather in mumbai"
    │
    ▼
convert_spoken_symbols()
"what is the weather in mumbai" (no change)
    │
    ▼
is_symbol_only()
false (has words)
    │
    ▼
route_command()
    │
    ├─ Check 5 handlers (no match)
    │
    ▼
handle_weather()
    │
    ├─ Pattern 1: "weather ... in CITY"
    ├─ Found match!
    ├─ Extract city: "mumbai"
    │
    ▼
get_weather("mumbai")
    │
    ├─ API call to OpenWeather
    ├─ Parse response
    ├─ Format result: "weather in mumbai is..."
    │
    ▼
speak(weather_info)
    │
    ├─ Windows: PowerShell TTS
    ├─ macOS: say command
    ├─ Linux: espeak/festival
    │
    ▼
log_interaction(
    user="what is the weather in mumbai",
    response="weather in mumbai is...",
    source="local"
)
    │
    ▼
logs/assistant.jsonl (appended)
{
  "ts": 1729525600,
  "user": "what is the weather in mumbai",
  "response": "weather in mumbai is...",
  "source": "local"
}
    │
    ▼
Continue loop
```

## Handler Internal Structure

```
┌─────────────────────────────────────────┐
│  handlers/example_handler.py            │
│                                         │
│  def handle_example(command):           │
│      ▼                                  │
│    Check if command matches pattern    │
│      │                                  │
│      ├─ NO → return False               │
│      │                                  │
│      └─ YES                             │
│         │                               │
│         ▼                               │
│      Extract relevant data              │
│         │                               │
│         ▼                               │
│      Process the command                │
│      (API call, calculation, etc.)     │
│         │                               │
│         ▼                               │
│      Call speak(response)               │
│         │                               │
│         ▼                               │
│      Call log_interaction(...)          │
│         │                               │
│         ▼                               │
│      return True  ← Handler matched!   │
│                                         │
└─────────────────────────────────────────┘
```

## Command Classification Tree

```
Command Input
    │
    ├─→ "thank you" / "thanks"
    │   └─ handler: thank_you_handler
    │
    ├─→ "hello" / "hi" / "hey"
    │   └─ handler: greeting_handler
    │
    ├─→ "what time"
    │   └─ handler: time_handler
    │
    ├─→ "what date" / "what day"
    │   └─ handler: date_handler
    │
    ├─→ Single word (city name)
    │   └─ handler: simple_weather_handler
    │
    ├─→ "weather", "forecast", "temperature"
    │   └─ handler: weather_handler
    │
    ├─→ "open/search ... on chrome/firefox"
    │   └─ handler: web_handler (browser_search)
    │
    ├─→ "open youtube/wikipedia/etc"
    │   └─ handler: web_handler (website_opening)
    │
    ├─→ "open downloads/documents/etc"
    │   └─ handler: file_handler
    │
    ├─→ "open app_name"
    │   └─ handler: app_handler
    │
    ├─→ "who are you" / "how are you"
    │   └─ handler: personal_handler
    │
    ├─→ "volume", "mute", "unmute"
    │   └─ handler: volume_handler
    │
    ├─→ "close app_name"
    │   └─ handler: close_app_handler
    │
    ├─→ "exit" / "quit" / "bye"
    │   └─ handler: exit_handler
    │
    └─→ Unknown command
        └─ Gemini API fallback
```

## Summary

```
┌─────────────────────────────────────────────────────────┐
│  Clean, Modular Architecture                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ✓ Single main loop (80 lines)                         │
│  ✓ 14 independent handlers (~30 lines each)            │
│  ✓ 6 reusable utilities (~30 lines each)               │
│  ✓ Centralized configuration (103 lines)               │
│  ✓ Easy to extend (add new handlers)                   │
│  ✓ Easy to maintain (find bugs quickly)                │
│  ✓ Easy to test (unit test each module)                │
│                                                         │
│  Same functionality, better organized code! 🎉         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
