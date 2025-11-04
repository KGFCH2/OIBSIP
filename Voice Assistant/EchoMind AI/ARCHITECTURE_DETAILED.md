# 🏗️ EchoMind AI - Architecture Diagrams & System Design

## 📊 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                        🎤 USER (Voice Input)                           │
│                                                                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  🎙️ LISTEN (STT)      │
                    │  speech_recognition   │
                    │  Google Cloud API     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  📝 TEXT PROCESSING    │
                    │  • Convert symbols    │
                    │  • Clean text         │
                    │  • Validate input     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  🔀 ROUTE COMMAND      │
                    │  Check handlers       │
                    │  Priority order       │
                    └────────┬───────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ✅ Handler 1      ✅ Handler 2      ❓ No Match?
    Processes        Processes            │
       │                 │                 ▼
       ▼                 ▼           🧠 Gemini AI
                              (Fallback Handler)
          ┌──────────────────┬───────────────────┐
          │                  ▼                   │
          ▼          Generate Response           ▼
                            │
       ┌─────────────────────┴─────────────────────┐
       ▼                                           ▼
    📝 Logging                            🔊 SPEAK (TTS)
    JSON File                             • pyttsx3 (Windows)
    assistant.jsonl                       • say (macOS)
                                          • espeak (Linux)
       │                                           │
       └──────────────────────┬──────────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  👤 USER (Output)  │
                    │  Hears Response    │
                    └────────────────────┘
                              │
                              ▼
                    🔄 Loop back to LISTEN
```

---

## 🔧 Module Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          🎤 ECHOMIND AI CORE                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                     🎯 MAIN ENTRY POINT                          │ │
│  │              main_refactored.py (80 lines)                       │ │
│  │                                                                  │ │
│  │  • Listen for voice commands                                   │ │
│  │  • Route to appropriate handler                               │ │
│  │  • Gemini fallback for unknown commands                       │ │
│  │  • Main event loop                                            │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                        │
│          ┌───────────────────┼───────────────────┐                   │
│          ▼                   ▼                   ▼                   │
│  ┌─────────────────┐ ┌──────────────────┐ ┌──────────────┐         │
│  │ 🎤 UTILITIES    │ │ 🎯 HANDLERS      │ │ ⚙️  CONFIG   │         │
│  │  (utils/)       │ │  (handlers/)     │ │ (config/)    │         │
│  ├─────────────────┤ ├──────────────────┤ ├──────────────┤         │
│  │ voice_io        │ │ • greeting       │ │ settings.py  │         │
│  │ text_proc       │ │ • time           │ │ • COMMON_APP │         │
│  │ time_utils      │ │ • date           │ │ • WEBSITE_MAP│         │
│  │ weather         │ │ • weather        │ │ • LOCATIONS  │         │
│  │ logger          │ │ • web            │ │ • KEYWORDS   │         │
│  └─────────────────┘ │ • file           │ └──────────────┘         │
│         │            │ • app            │         │                 │
│         │            │ • personal       │         │                 │
│         │            │ • volume         │         │                 │
│         │            │ • close_app      │         │                 │
│         │            │ • exit           │         │                 │
│         │            │ • thanks         │         │                 │
│         │            └──────────────────┘         │                 │
│         │                                         │                 │
│         └─────────────────┬───────────────────────┘                 │
│                           ▼                                         │
│              🤖 Gemini AI (gemini_client.py)                       │
│              • Fallback handler                                    │
│              • Unknown command processing                         │
│              • Natural language understanding                     │
│                                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Processing Flow

```
USER SPEAKS:
"What's the weather in London?"
         │
         ▼
    ┌────────────────────────┐
    │ LISTEN (STT)           │
    │ Convert speech to text │
    └─────────┬──────────────┘
              │
    "whats the weather in london"
              │
              ▼
    ┌────────────────────────┐
    │ TEXT PROCESSING        │
    │ • Convert symbols      │
    │ • Validate            │
    └─────────┬──────────────┘
              │
         ┌────┴───────────────────────────┐
         ▼                                ▼
    Handler Matching                  No Match?
    Check each handler                   │
    in order                             ▼
         │                          Gemini AI
         ▼
    Pattern: "weather"
    City: "london"
         │
         ▼
    ┌─────────────────────────────────┐
    │ WEATHER_HANDLER                 │
    │ ✅ Pattern matches!             │
    │                                 │
    │ 1. Extract city name            │
    │ 2. Call OpenWeather API         │
    │ 3. Get weather data             │
    │ 4. Format response              │
    └────────────┬────────────────────┘
                 │
    Response: "It's 15°C in London,
              partly cloudy"
                 │
                 ▼
    ┌─────────────────────────────────┐
    │ TEXT-TO-SPEECH                  │
    │ Convert response to audio       │
    └────────────┬────────────────────┘
                 │
                 ▼
    SPEAK RESPONSE
    User hears: "It's 15°C in London,
                partly cloudy"
                 │
                 ▼
    LOG INTERACTION
    {
      "timestamp": "...",
      "user": "whats the weather in london",
      "response": "It's 15°C in London",
      "handler": "weather_handler",
      "success": true
    }
```

---

## 🎯 Handler Decision Tree

```
                        🎤 COMMAND RECEIVED
                                │
                                ▼
                    ┌───────────────────────┐
                    │ 1. THANK YOU?         │
                    │ "thank you", "thanks" │
                    └─┬─────────────────┬───┘
                      │✅YES             │❌NO
                      │                 ▼
                      │          ┌──────────────────┐
                    Handle       │ 2. GREETING?     │
                    Thank You    │ "hi", "hello"    │
                      │          └─┬────────────┬───┘
                      │            │✅YES        │❌NO
                      │            │            ▼
                      │          Handle    ┌─────────────────┐
                      │          Greeting  │ 3. TIME?        │
                      │            │       │ "what time"     │
                      │            │       └─┬───────────┬───┘
                      │            │         │✅YES       │❌NO
                      │            │         │           ▼
                      │            │       Handle    ┌──────────────┐
                      │            │       Time      │ 4. DATE?     │
                      │            │         │       │ "what date"  │
                      │            │         │       └─┬──────┬─────┘
                      │            │         │         │✅    │❌
                      │            │         │         │     ▼
                      │            │         │       Handle  ...
                      │            │         │       Date
                      │            │         │         │
                      │            │         │         ▼
                      └────────────┴─────────┴────────────────┐
                                                              │
                    Continue through all handlers...         │
                                                              │
                      ┌─────────────────────────────────┐    │
                      │ If NO handler matched:          │    │
                      │ ▼                               │    │
                      │ 🧠 GEMINI AI FALLBACK          │    │
                      │ Generate intelligent response  │    │
                      └─────────────────────────────────┘    │
                                      │                      │
                                      └──────────┬───────────┘
                                                 │
                                    ✅ RESPOND TO USER
                                    🔊 SPEAK & LOG
```

---

## 📦 Data Flow - External APIs

```
┌──────────────────────────────────────────────────────────────────────┐
│                        EchoMind AI Application                       │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                  Internal Processing                          │ │
│  │  • Command routing                                           │ │
│  │  • Text processing                                           │ │
│  │  • Handler execution                                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
    ┌─────────────────────┐ ┌──────────────────┐ ┌────────────────┐
    │ 🌤️ OPENWEATHER API  │ │ 🧠 GEMINI API    │ │ 🎙️ GOOGLE     │
    │ (Optional)          │ │ (Fallback)       │ │ Cloud Speech   │
    │                     │ │                  │ │ (Optional)     │
    │ GET /weather        │ │ POST /generate   │ │                │
    │ ├─ APIKEY           │ │ ├─ APIKEY        │ │ Used by        │
    │ ├─ CITY             │ │ ├─ PROMPT        │ │ STT libraries  │
    │ └─ UNITS            │ │ ├─ STREAM (opt)  │ │                │
    │                     │ │ └─ TEMPERATURE   │ │                │
    │ Returns:            │ │                  │ │ Returns:       │
    │ • Temperature       │ │ Returns:         │ │ • Confidence   │
    │ • Condition         │ │ • Response text  │ │ • Alternatives │
    │ • Humidity          │ │ • Citations      │ │ • Language     │
    │ • Wind speed        │ │ • Streamed text  │ │                │
    │ • Precipitation     │ │ • Safety rating  │ │                │
    └──────┬──────────────┘ └────────┬─────────┘ └────────────────┘
           │                         │
           └──────────────┬──────────┘
                          │
                          ▼
            ┌──────────────────────────────┐
            │ Cache & Process Responses    │
            │ Format for TTS               │
            │ Log to interaction file      │
            └──────────────────────────────┘
```

---

## 🎯 Handler Execution Model

```
┌─────────────────────────────────────────────────────────────┐
│               Handler Execution Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  For each handler in order:                               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                                                     │ │
│  │  1. PATTERN MATCHING                               │ │
│  │     if re.search(pattern, command):                │ │
│  │     ├─ Extract entities (city, app, etc)          │ │
│  │     ├─ Validate extracted data                    │ │
│  │     └─ Continue to step 2                         │ │
│  │                                                     │ │
│  │  2. PROCESS COMMAND                                │ │
│  │     ├─ Call APIs if needed (weather, etc)         │ │
│  │     ├─ Format response                            │ │
│  │     ├─ Error handling & fallback                  │ │
│  │     └─ Continue to step 3                         │ │
│  │                                                     │ │
│  │  3. RESPOND TO USER                                │ │
│  │     ├─ speak(response)  [TTS]                     │ │
│  │     ├─ log_interaction() [Logging]               │ │
│  │     └─ return True                                │ │
│  │                                                     │ │
│  │  4. NEXT ITERATION                                 │ │
│  │     if return False:                              │ │
│  │     └─ Try next handler...                        │ │
│  │                                                     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  If ALL handlers return False:                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  GEMINI FALLBACK                                    │ │
│  │  ├─ Send command to Gemini AI                      │ │
│  │  ├─ Receive AI-generated response                │ │
│  │  ├─ Speak response                                 │ │
│  │  ├─ Log with "gemini" source                       │ │
│  │  └─ Loop back to listen                            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Data Model - Logged Interactions

```
┌────────────────────────────────────────────┐
│ logs/assistant.jsonl (One line per entry) │
├────────────────────────────────────────────┤
│                                            │
│ {                                          │
│   "timestamp": "2025-11-04T10:30:00Z",    │
│   "user_command": "what time is it",      │
│   "command_type": "time_query",           │
│   "handler": "time_handler",              │
│   "response": "It's 10:30 AM",            │
│   "response_time_ms": 245,                │
│   "success": true,                        │
│   "error": null,                          │
│   "metadata": {                           │
│     "timezone": "IST",                    │
│     "platform": "windows"                 │
│   }                                        │
│ }                                          │
│                                            │
│ {                                          │
│   "timestamp": "2025-11-04T10:31:00Z",    │
│   "user_command": "weather in london",    │
│   "command_type": "weather_query",        │
│   "handler": "weather_handler",           │
│   "response": "It's 15°C in London, ...", │
│   "response_time_ms": 856,                │
│   "success": true,                        │
│   "api_calls": {                          │
│     "openweather": "200 OK"              │
│   }                                        │
│ }                                          │
│                                            │
│ ... (one JSON object per line)            │
│                                            │
└────────────────────────────────────────────┘
```

---

## 🔐 Configuration Architecture

```
┌──────────────────────────────────────────────────────┐
│              Configuration Hierarchy                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1️⃣ Environment Variables (.env)                    │
│     └─ OPENWEATHER_API_KEY                         │
│     └─ GEMINI_API_KEY                              │
│     └─ GEMINI_API_ENDPOINT (optional)              │
│     └─ GEMINI_API_STREAM (optional)                │
│                 │                                   │
│  2️⃣ Application Constants (config/settings.py)     │
│     └─ COMMON_APPS        (25+ applications)      │
│     └─ WEBSITE_MAP         (11+ websites)          │
│     └─ LOCATION_MAP        (6 file locations)      │
│     └─ PROCESS_NAMES       (13 process names)      │
│     └─ KEYWORDS            (exit, thanks, etc)    │
│     └─ CONNECTOR_WORDS     (to, in, on, etc)      │
│     └─ WEATHER_BLACKLIST   (non-city keywords)    │
│                 │                                   │
│  3️⃣ Runtime State (In Memory)                      │
│     └─ Command history                            │
│     └─ Session cache                              │
│     └─ API response cache                         │
│                 │                                   │
│                 ▼                                   │
│    ✅ Fully Configurable System                    │
│    ✅ No hardcoded values                          │
│    ✅ Easy to customize                            │
│    ✅ API keys secured                             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    Deployment Options                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  LOCAL DEVELOPMENT                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ $ python main_refactored.py                             │   │
│  │ • Single-user development                              │   │
│  │ • Full console output                                  │   │
│  │ • Easy debugging                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                    │
│  SERVER DEPLOYMENT (Linux/macOS)                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ $ nohup python main_refactored.py > output.log 2>&1 &  │   │
│  │ • Runs in background                                   │   │
│  │ • Survives SSH disconnection                           │   │
│  │ • Logs output to file                                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                    │
│  CONTAINER DEPLOYMENT (Docker)                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ $ docker build -t echomind .                            │   │
│  │ $ docker run echomind                                   │   │
│  │ • Isolated environment                                 │   │
│  │ • Reproducible builds                                  │   │
│  │ • Easy scaling                                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                    │
│  SYSTEM SERVICE (Windows)                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ > sc create EchoMind ...                                │   │
│  │ • Auto-start on boot                                   │   │
│  │ • System tray integration                              │   │
│  │ • Windows Service Manager                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Performance & Optimization

```
┌────────────────────────────────────────────────────────────┐
│              Performance Optimization                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  COMPONENT          │ TIME    │ OPTIMIZATION             │
│  ─────────────────────────────────────────────────────    │
│  Voice Recognition  │ 2-3s    │ Pre-load model           │
│  Text Processing    │ <10ms   │ Compiled regex           │
│  Handler Matching   │ <50ms   │ Ordered priority         │
│  API Call (Weather) │ 800-1s  │ Cache responses          │
│  Text-to-Speech     │ 0.5-2s  │ Stream audio             │
│  Gemini AI Call     │ 2-5s    │ Streaming responses      │
│  JSON Logging       │ <5ms    │ Async append             │
│  ─────────────────────────────────────────────────────    │
│  TOTAL TIME: 5-12 seconds per command                    │
│                                                            │
│  ✅ Caching Strategy:                                     │
│    • API responses cached for 5 minutes                  │
│    • Handler patterns compiled once                      │
│    • Logger batches writes (async)                       │
│                                                            │
│  ✅ Scalability:                                          │
│    • Can handle 1000+ commands per hour                  │
│    • Thread-safe logging                                │
│    • Non-blocking I/O                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎨 Technology Stack Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    Technology Stack                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  PRESENTATION LAYER (User Interfaces)                   │  │
│  │  ├─ 🎤 Voice Input (Microphone)                        │  │
│  │  └─ 🔊 Voice Output (Speakers)                         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         △                                      │
│                         │                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  APPLICATION LAYER (Core Logic)                         │  │
│  │  ├─ main_refactored.py    (Orchestration)            │  │
│  │  ├─ Handlers (14 modules)  (Command processing)      │  │
│  │  ├─ Utils (6 modules)      (Helper functions)        │  │
│  │  └─ Config (settings.py)   (Configuration)           │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         △                                      │
│                         │                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  LIBRARY LAYER (Python Dependencies)                    │  │
│  │  ├─ speech_recognition      (STT)                      │  │
│  │  ├─ pyttsx3                 (TTS - Windows)            │  │
│  │  ├─ requests                (HTTP)                     │  │
│  │  ├─ python-dotenv           (Env config)             │  │
│  │  ├─ pytz                    (Timezones)              │  │
│  │  └─ google-generativeai     (Gemini API)            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         △                                      │
│                         │                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  API LAYER (External Services)                          │  │
│  │  ├─ 🌤️  OpenWeather API      (Weather data)           │  │
│  │  ├─ 🧠 Gemini API           (AI responses)            │  │
│  │  ├─ 🎙️  Google Cloud Speech  (STT)                    │  │
│  │  └─ 🖥️  System APIs          (App launching)          │  │
│  └─────────────────────────────────────────────────────────┘  │
│                         △                                      │
│                         │                                      │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  INFRASTRUCTURE LAYER (OS & Deployment)                │  │
│  │  ├─ 🪟 Windows              (PowerShell)             │  │
│  │  ├─ 🍎 macOS                (Unix commands)           │  │
│  │  ├─ 🐧 Linux                (Unix commands)           │  │
│  │  └─ 🐳 Docker               (Containerization)        │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

**This architecture document provides a comprehensive overview of EchoMind AI's system design!** 🎉
