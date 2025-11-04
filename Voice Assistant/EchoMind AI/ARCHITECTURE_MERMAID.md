# 🏗️ ECHOMIND AI - ARCHITECTURE IN MERMAID FORMAT

## 1️⃣ SYSTEM ARCHITECTURE OVERVIEW

```mermaid
graph TB
    User["🎤 User<br/>(Voice/Text Input)"]
    Main["main_refactored.py<br/>(Entry Point)"]
    Router["🔀 Command Router<br/>(Priority Queue)"]
    
    subgraph Handlers["14 Command Handlers"]
        G["greeting_handler"]
        T["thank_you_handler"]
        TM["time_handler"]
        D["date_handler"]
        W["weather_handler"]
        WB["web_handler"]
        F["file_handler"]
        A["app_handler"]
        P["personal_handler"]
        V["volume_handler"]
        C["close_app_handler"]
        E["exit_handler"]
        SW["simple_weather_handler"]
        PH["phone_handler"]
    end
    
    subgraph Utils["Utility Modules"]
        VI["voice_io.py<br/>(TTS/STT)"]
        TP["text_processing.py"]
        TU["time_utils.py"]
        WE["weather.py"]
        LG["logger.py"]
    end
    
    subgraph Config["Configuration"]
        SET["settings.py<br/>(Constants)"]
    end
    
    subgraph APIs["External APIs"]
        OW["OpenWeather API"]
        GM["Gemini AI"]
        GCP["Google Cloud<br/>Speech-to-Text"]
    end
    
    subgraph Storage["Data Storage"]
        LOG["logs/assistant.jsonl<br/>(Interaction Logs)"]
        ENV[".env<br/>(Credentials)"]
    end
    
    User -->|Voice Input| Main
    Main -->|Process| Router
    Router -->|Route by<br/>Priority| Handlers
    
    G & T & TM & D & W & WB & F & A & P & V & C & E & SW & PH -->|Use| Utils
    Utils -->|Read Config| SET
    
    G & T & TM & D & SW -->|Local<br/>Responses| LG
    W -->|API Call| OW
    Handlers -->|Fallback| GM
    VI -->|Speech| GCP
    
    LG -->|Store| LOG
    ENV -->|Provide| APIs
    
    Handlers -->|Output to<br/>User| User
```

---

## 2️⃣ REQUEST PROCESSING FLOW

```mermaid
sequenceDiagram
    participant User
    participant Main as main_refactored.py
    participant Router as Command Router
    participant Handler as Handler Module
    participant Utils as Utils
    participant API as External API
    participant Logger as Logger
    participant Output as User Output

    User->>Main: Voice/Text Input
    Main->>Main: Capture & Recognize Speech
    Main->>Main: Convert to Text
    Main->>Router: Extract Keywords & Intent
    Router->>Router: Check Handler Priority
    Router->>Handler: Route to Best Handler
    
    alt Handler is Local
        Handler->>Utils: Use Local Utilities
        Utils->>Utils: Process Request
        Utils-->>Handler: Return Response
    else Handler Needs API
        Handler->>API: Call External API
        API-->>Handler: Get Response
    end
    
    Handler->>Logger: Log Interaction
    Logger->>Logger: Create JSON Entry
    
    Handler->>Main: Return Response
    Main->>Output: Speak/Display Result
    Output-->>User: Deliver Response
```

---

## 3️⃣ HANDLER PRIORITY DECISION TREE

```mermaid
graph TD
    Input["Input Command"]
    
    Check1{"Greeting<br/>Keywords?"}
    Check2{"Thanks<br/>Keywords?"}
    Check3{"Time<br/>Query?"}
    Check4{"Date<br/>Query?"}
    Check5{"Weather<br/>Keywords?"}
    Check6{"Web<br/>Search?"}
    Check7{"File<br/>Operation?"}
    Check8{"App<br/>Launch?"}
    Check9{"Personal<br/>Data?"}
    Check10{"Volume<br/>Control?"}
    Check11{"Close<br/>App?"}
    Check12{"Exit<br/>App?"}
    
    H1["greeting_handler<br/>Priority: 1"]
    H2["thank_you_handler<br/>Priority: 2"]
    H3["time_handler<br/>Priority: 3"]
    H4["date_handler<br/>Priority: 4"]
    H5["weather_handler<br/>Priority: 5"]
    H6["web_handler<br/>Priority: 6"]
    H7["file_handler<br/>Priority: 7"]
    H8["app_handler<br/>Priority: 8"]
    H9["personal_handler<br/>Priority: 9"]
    H10["volume_handler<br/>Priority: 10"]
    H11["close_app_handler<br/>Priority: 11"]
    H12["exit_handler<br/>Priority: 12"]
    
    Fallback["Gemini AI<br/>(Fallback)<br/>Priority: 13"]
    
    Input -->|Yes| Check1
    Check1 -->|Yes| H1
    Check1 -->|No| Check2
    
    Check2 -->|Yes| H2
    Check2 -->|No| Check3
    
    Check3 -->|Yes| H3
    Check3 -->|No| Check4
    
    Check4 -->|Yes| H4
    Check4 -->|No| Check5
    
    Check5 -->|Yes| H5
    Check5 -->|No| Check6
    
    Check6 -->|Yes| H6
    Check6 -->|No| Check7
    
    Check7 -->|Yes| H7
    Check7 -->|No| Check8
    
    Check8 -->|Yes| H8
    Check8 -->|No| Check9
    
    Check9 -->|Yes| H9
    Check9 -->|No| Check10
    
    Check10 -->|Yes| H10
    Check10 -->|No| Check11
    
    Check11 -->|Yes| H11
    Check11 -->|No| Check12
    
    Check12 -->|Yes| H12
    Check12 -->|No| Fallback
    
    H1 & H2 & H3 & H4 & H5 & H6 & H7 & H8 & H9 & H10 & H11 & H12 & Fallback -->|Response| Output["Output to User"]
```

---

## 4️⃣ MODULE ARCHITECTURE

```mermaid
graph LR
    subgraph Main["Main Entry"]
        M["main_refactored.py"]
    end
    
    subgraph Config["Configuration<br/>📁 config/"]
        S["settings.py<br/>(103 lines)"]
        CONF_INIT["__init__.py"]
    end
    
    subgraph Utils["Utilities<br/>📁 utils/"]
        VI["voice_io.py<br/>(63 lines)"]
        TP["text_processing.py<br/>(34 lines)"]
        TU["time_utils.py<br/>(33 lines)"]
        WE["weather.py<br/>(16 lines)"]
        LG["logger.py<br/>(18 lines)"]
        UTIL_INIT["__init__.py"]
    end
    
    subgraph Handlers["Handlers<br/>📁 handlers/"]
        H1["greeting_handler"]
        H2["thank_you_handler"]
        H3["time_handler"]
        H4["date_handler"]
        H5["weather_handler"]
        H6["web_handler"]
        H7["file_handler"]
        H8["app_handler"]
        H9["personal_handler"]
        H10["volume_handler"]
        H11["close_app_handler"]
        H12["exit_handler"]
        H13["simple_weather_handler"]
        HAND_INIT["__init__.py"]
    end
    
    subgraph External["External Services"]
        OW["🌐 OpenWeather API"]
        GM["🤖 Gemini AI"]
        GCP["🎤 Google Cloud STT"]
    end
    
    M -->|Import| S
    M -->|Import| VI
    M -->|Import| TP
    M -->|Import| TU
    M -->|Import| WE
    M -->|Import| LG
    
    M -->|Route to| H1
    M -->|Route to| H2
    M -->|Route to| H3
    M -->|Route to| H4
    M -->|Route to| H5
    M -->|Route to| H6
    M -->|Route to| H7
    M -->|Route to| H8
    M -->|Route to| H9
    M -->|Route to| H10
    M -->|Route to| H11
    M -->|Route to| H12
    M -->|Route to| H13
    
    H5 -->|Call| OW
    M -->|Fallback| GM
    VI -->|Call| GCP
    
    LG -->|Log| LOG["📝 assistant.jsonl"]
```

---

## 5️⃣ DATA FLOW - EXTERNAL APIs

```mermaid
graph TB
    App["EchoMind AI App"]
    
    subgraph Weather["Weather Handler"]
        WH["weather_handler.py"]
        WU["weather.py"]
    end
    
    subgraph Gemini["Gemini Handler"]
        GH["Fallback Handler"]
        GC["gemini_client.py"]
    end
    
    subgraph STT["Speech to Text"]
        VI["voice_io.py"]
    end
    
    OW_API["OpenWeather API<br/>api.openweathermap.org"]
    GM_API["Google Generative AI<br/>generativelanguage.googleapis.com"]
    GCP_API["Google Cloud Speech-to-Text<br/>speech.googleapis.com"]
    
    APP_ENV[".env File<br/>Stores API Keys"]
    
    App -->|Weather Query| WH
    WH -->|Get Location| WU
    WU -->|HTTP Request| OW_API
    OW_API -->|JSON Response<br/>Temperature, Conditions| WU
    WU -->|Format Response| WH
    
    App -->|Fallback Query| GH
    GH -->|Send Prompt| GC
    GC -->|HTTP Request| GM_API
    GM_API -->|Streaming Response| GC
    GC -->|Process Stream| GH
    
    App -->|Audio Input| VI
    VI -->|Convert to<br/>Bytes| GCP_API
    GCP_API -->|Recognized<br/>Text| VI
    
    APP_ENV -->|Provide API Keys| OW_API
    APP_ENV -->|Provide API Keys| GM_API
    APP_ENV -->|Provide Credentials| GCP_API
    
    style OW_API fill:#fff9e6
    style GM_API fill:#e6f3ff
    style GCP_API fill:#f0e6ff
```

---

## 6️⃣ HANDLER EXECUTION MODEL

```mermaid
graph TD
    Input["User Input<br/>(Text)"]
    
    Step1["Step 1: Extract Keywords<br/>& Normalize Text"]
    Step2["Step 2: Check Handler<br/>Conditions"]
    Step3["Step 3: Execute Handler<br/>Logic"]
    Step4["Step 4: Generate<br/>Response"]
    Step5["Step 5: Log & Output"]
    
    Input -->|Process| Step1
    Step1 -->|Keywords Extracted| Step2
    
    Step2 -->|Condition<br/>Matched| Step3
    Step2 -->|No Match| Fallback["Route to Fallback<br/>(Gemini)"]
    
    Step3 -->|Handler<br/>Logic| Step4
    Fallback -->|AI Response| Step4
    
    Step4 -->|Generated| Step5
    
    Step5 -->|Log Entry| JSONL["JSON Log Entry"]
    Step5 -->|Output| TTS["Text-to-Speech"]
    
    TTS -->|Audio| User["User<br/>(Audio Output)"]
    
    JSONL -->|Save| FILE["assistant.jsonl<br/>(Append)"]
    
    style Input fill:#fff
    style User fill:#fff
    style FILE fill:#f0f0f0
    style Fallback fill:#ffe6e6
```

---

## 7️⃣ CONFIGURATION HIERARCHY

```mermaid
graph TB
    APP[".env File<br/>(Runtime Config)"]
    
    subgraph Settings["settings.py<br/>(103 lines)"]
        COMMON["COMMON_APPS<br/>(25 applications)"]
        WEBSITES["WEBSITE_MAP<br/>(11 websites)"]
        LOCATIONS["LOCATION_MAP<br/>(6 locations)"]
        PROCESS["PROCESS_NAMES<br/>(13 processes)"]
        KEYWORDS["KEYWORDS<br/>(Pattern Dict)"]
        BLACKLIST["BLACKLIST<br/>(Excluded Words)"]
    end
    
    subgraph Runtime["Runtime Variables"]
        API_KEYS["API Keys"]
        USER_DATA["User Data"]
        PREFERENCES["Preferences"]
    end
    
    Handlers["14 Handlers"]
    Utils["Utility Functions"]
    
    APP -->|Load| Runtime
    Runtime -->|Merge with| Settings
    Settings -->|Provide to| Handlers
    Settings -->|Provide to| Utils
    
    COMMON -->|Lists Apps| Handlers
    WEBSITES -->|Lists Sites| Handlers
    LOCATIONS -->|Lists Locations| Utils
    KEYWORDS -->|Pattern Matching| Handlers
    BLACKLIST -->|Filter Words| Utils
    PROCESS -->|Process Names| Handlers
    
    style Settings fill:#f0f0f0
    style Runtime fill:#fff9e6
    style Handlers fill:#e6f3ff
    style Utils fill:#f0e6ff
```

---

## 8️⃣ DEPLOYMENT ARCHITECTURE

```mermaid
graph TB
    subgraph Local["Local Development"]
        L["python main_refactored.py<br/>On Your Computer"]
    end
    
    subgraph Server["Server Deployment"]
        S["Flask/FastAPI App<br/>On Cloud Server"]
        WSGI["WSGI Server<br/>(Gunicorn/uWSGI)"]
    end
    
    subgraph Docker["Docker Container"]
        D["Docker Image<br/>Python + Dependencies"]
        CONT["Running Container<br/>Isolated Environment"]
    end
    
    subgraph WindowsService["Windows Service"]
        WS["NSSM Service<br/>Auto-start on Boot"]
    end
    
    subgraph Cloud["Cloud Platforms"]
        GCP_CLOUD["Google Cloud<br/>Compute Engine"]
        AWS["AWS EC2"]
        HEROKU["Heroku/Render"]
    end
    
    Local -->|Run Locally| DEV["Development Mode"]
    
    S -->|Manage| WSGI
    WSGI -->|Run| Server
    
    D -->|Build| CONT
    CONT -->|Run| Docker
    
    WS -->|Background Service| WindowsService
    
    Server -->|Deploy to| GCP_CLOUD
    Server -->|Deploy to| AWS
    Docker -->|Deploy to| HEROKU
    
    DEV & Server & Docker & WindowsService -->|Connect to| APIs["External APIs<br/>Weather, Gemini, etc."]
    
    style DEV fill:#e6ffe6
    style Server fill:#fff9e6
    style Docker fill:#e6f3ff
    style WindowsService fill:#f0e6ff
```

---

## 9️⃣ DATA FLOW - COMPLETE JOURNEY

```mermaid
graph LR
    U["🎤 User"]
    
    subgraph Input["1. INPUT"]
        VI["voice_io.py<br/>Listen & Record"]
        GCP["Google STT<br/>Convert Audio→Text"]
        TEXT["Extract Text"]
    end
    
    subgraph Processing["2. PROCESSING"]
        TP["text_processing.py<br/>Normalize & Clean"]
        KW["Extract Keywords"]
        ROUTER["Command Router<br/>Priority Check"]
    end
    
    subgraph Routing["3. ROUTING"]
        H1["Handler 1"]
        H2["Handler 2"]
        H3["Handler 3"]
        HN["Handler N"]
        FB["Gemini<br/>Fallback"]
    end
    
    subgraph Execution["4. EXECUTION"]
        LOGIC["Execute Handler<br/>Logic"]
        API["Call APIs<br/>if needed"]
        RESP["Generate<br/>Response"]
    end
    
    subgraph Storage["5. STORAGE"]
        LOGGER["logger.py<br/>Create Entry"]
        JSONL["assistant.jsonl<br/>Append Line"]
    end
    
    subgraph Output["6. OUTPUT"]
        TTS["Text-to-Speech<br/>voice_io.py"]
        SPEAK["Speak Response"]
    end
    
    U -->|Speak| VI
    VI -->|Audio Bytes| GCP
    GCP -->|Text| TEXT
    TEXT -->|Normalized| TP
    TP -->|Cleaned Text| KW
    KW -->|Keywords| ROUTER
    
    ROUTER -->|Route| H1
    ROUTER -->|Route| H2
    ROUTER -->|Route| H3
    ROUTER -->|Route| HN
    ROUTER -->|No Match| FB
    
    H1 & H2 & H3 & HN & FB -->|Execute| LOGIC
    LOGIC -->|Call| API
    API -->|Response| RESP
    
    RESP -->|Response| LOGGER
    LOGGER -->|Log Entry| JSONL
    
    RESP -->|Text| TTS
    TTS -->|Audio| SPEAK
    SPEAK -->|Output| U
    
    style U fill:#fff
    style Input fill:#e6f3ff
    style Processing fill:#f0e6ff
    style Routing fill:#fff9e6
    style Execution fill:#e6ffe6
    style Storage fill:#ffe6e6
    style Output fill:#f0f0f0
```

---

## 🔟 TECHNOLOGY STACK

```mermaid
graph TB
    subgraph Language["Programming Language"]
        PY["Python 3.8+"]
    end
    
    subgraph Core["Core Libraries"]
        OS["os - File System"]
        JSON["json - Data Format"]
        TIME["time - Timestamps"]
        SUBPROCESS["subprocess - Process Management"]
        RE["re - Pattern Matching"]
    end
    
    subgraph Voice["Voice Processing"]
        SPEECH["SpeechRecognition<br/>(Speech→Text)"]
        PYTTSX3["pyttsx3<br/>(Text→Speech)"]
        GCP_LIB["google-cloud-speech<br/>(Google STT)"]
    end
    
    subgraph AI["AI & LLM"]
        GENAI["google-generativeai<br/>(Gemini API)"]
    end
    
    subgraph APIs["External APIs"]
        REQUESTS["requests<br/>(HTTP Client)"]
        OPENWEATHER["OpenWeather API<br/>(REST)"]
    end
    
    subgraph Utils["Utilities"]
        DATETIME["datetime<br/>(Date/Time)"]
        PYTZ["pytz<br/>(Timezone)"]
    end
    
    PY --> Core
    PY --> Voice
    PY --> AI
    PY --> APIs
    PY --> Utils
    
    SPEECH & PYTTSX3 & GCP_LIB --> Voice
    GENAI --> AI
    REQUESTS --> APIs
    DATETIME & PYTZ --> Utils
    
    Voice -->|Process Audio| Voice
    AI -->|Generate Responses| AI
    APIs -->|Fetch Data| APIs
    
    style Language fill:#fff9e6
    style Core fill:#e6f3ff
    style Voice fill:#f0e6ff
    style AI fill:#e6ffe6
    style APIs fill:#ffe6e6
    style Utils fill:#f0f0f0
```

---

## 1️⃣1️⃣ ERROR HANDLING & FALLBACK FLOW

```mermaid
graph TD
    Start["User Request"]
    
    Try1["Handler Tries<br/>to Execute"]
    Catch1{"Handler<br/>Error?"}
    
    Yes1["Log Error"]
    Fallback1["Try Gemini<br/>Fallback"]
    
    Try2["Gemini Tries<br/>to Generate"]
    Catch2{"Gemini<br/>Error?"}
    
    Yes2["Log Error"]
    Generic["Return Generic<br/>Response"]
    
    No["Success"]
    Success["Return Response<br/>to User"]
    
    Start --> Try1
    Try1 --> Catch1
    
    Catch1 -->|Yes| Yes1
    Catch1 -->|No| No
    
    Yes1 --> Fallback1
    Fallback1 --> Try2
    
    Try2 --> Catch2
    Catch2 -->|Yes| Yes2
    Catch2 -->|No| No
    
    Yes2 --> Generic
    Generic --> Success
    
    No --> Success
    
    Success -->|Output| User["User"]
    
    style Try1 fill:#e6f3ff
    style Try2 fill:#e6ffe6
    style Catch1 fill:#ffe6e6
    style Catch2 fill:#ffe6e6
    style Success fill:#e6ffe6
    style User fill:#fff
```

---

## 1️⃣2️⃣ FILE STRUCTURE TREE (VISUAL)

```mermaid
graph TD
    ROOT["📁 EchoMind AI<br/>(Project Root)"]
    
    ROOT --> MAIN1["📄 main.py<br/>(Legacy)"]
    ROOT --> MAIN2["📄 main_refactored.py<br/>(Current - 80 lines)"]
    ROOT --> GEMINI["📄 gemini_client.py<br/>(AI Client)"]
    ROOT --> REQ["📄 requirements.txt<br/>(Dependencies)"]
    ROOT --> ENV1["📄 .env<br/>(Credentials)"]
    ROOT --> ENV2["📄 .env.example<br/>(Template)"]
    ROOT --> GIT["📄 .gitignore"]
    
    ROOT --> CONFIG["📁 config/"]
    CONFIG --> C1["⚙️ settings.py<br/>(103 lines)"]
    CONFIG --> C2["📄 __init__.py"]
    
    ROOT --> UTILS["📁 utils/"]
    UTILS --> U1["🎤 voice_io.py<br/>(63 lines)"]
    UTILS --> U2["✂️ text_processing.py<br/>(34 lines)"]
    UTILS --> U3["⏰ time_utils.py<br/>(33 lines)"]
    UTILS --> U4["🌤️ weather.py<br/>(16 lines)"]
    UTILS --> U5["📝 logger.py<br/>(18 lines)"]
    UTILS --> U6["📄 __init__.py"]
    
    ROOT --> HANDLERS["📁 handlers/"]
    HANDLERS --> H1["greeting_handler.py"]
    HANDLERS --> H2["thank_you_handler.py"]
    HANDLERS --> H3["time_handler.py"]
    HANDLERS --> H4["date_handler.py"]
    HANDLERS --> H5["simple_weather_handler.py"]
    HANDLERS --> H6["weather_handler.py"]
    HANDLERS --> H7["web_handler.py"]
    HANDLERS --> H8["file_handler.py"]
    HANDLERS --> H9["app_handler.py"]
    HANDLERS --> H10["personal_handler.py"]
    HANDLERS --> H11["volume_handler.py"]
    HANDLERS --> H12["close_app_handler.py"]
    HANDLERS --> H13["exit_handler.py"]
    HANDLERS --> H14["__init__.py"]
    
    ROOT --> LOGS["📁 logs/"]
    LOGS --> LOG["📊 assistant.jsonl<br/>(Interaction Log)"]
    
    ROOT --> DOCS["📁 Documentation/"]
    DOCS --> D1["📖 README.md"]
    DOCS --> D2["📖 ARCHITECTURE_DETAILED.md"]
    DOCS --> D3["📖 QUICK_START_FINAL.md"]
    
    style ROOT fill:#fff9e6
    style CONFIG fill:#e6f3ff
    style UTILS fill:#f0e6ff
    style HANDLERS fill:#e6ffe6
    style LOGS fill:#ffe6e6
    style DOCS fill:#f0f0f0
```

---

## 1️⃣3️⃣ INTERACTION LOGGING SYSTEM

```mermaid
graph LR
    User["User<br/>Speaks/Types"]
    
    App["EchoMind AI<br/>Processes"]
    
    Handler["Handler<br/>Generates Response"]
    
    Logger["logger.py<br/>log_interaction()"]
    
    Entry["JSON Entry<br/>Created"]
    
    File["assistant.jsonl<br/>JSONL Format"]
    
    User -->|Input| App
    App -->|Process| Handler
    Handler -->|Response| Logger
    
    Logger -->|Create| Entry
    Entry -->|Structure:<br/>ts, user, response, source| File
    
    File -->|Append Mode<br/>One Line per Entry| Storage["📊 File System<br/>logs/ Directory"]
    
    style User fill:#fff
    style App fill:#e6f3ff
    style Handler fill:#e6ffe6
    style Logger fill:#f0e6ff
    style Entry fill:#fff9e6
    style File fill:#ffe6e6
    style Storage fill:#f0f0f0
```

---

## Summary

These 13 Mermaid diagrams provide complete architectural visualization of your EchoMind AI:

1. ✅ **System Overview** - High-level component interaction
2. ✅ **Request Flow** - Sequential request processing
3. ✅ **Handler Priority** - Decision tree for routing
4. ✅ **Module Architecture** - File/folder organization
5. ✅ **API Data Flow** - External service integration
6. ✅ **Handler Execution** - Step-by-step processing
7. ✅ **Configuration** - Settings hierarchy
8. ✅ **Deployment Options** - Different deployment methods
9. ✅ **Complete Data Journey** - Full request lifecycle
10. ✅ **Technology Stack** - Libraries and dependencies
11. ✅ **Error Handling** - Fallback and error management
12. ✅ **File Structure** - Project organization
13. ✅ **Logging System** - Data persistence

All diagrams are production-ready and can be used for documentation, presentations, or developer onboarding! 🎯
