# 🎤 EchoMind AI - Extended Documentation

## 📊 Project Architecture

### 🏗️ Directory Structure

```
EchoMind AI/
├── 🎯 ENTRY POINTS
│   ├── main_refactored.py       ← RECOMMENDED (modular & clean)
│   └── main.py                  ← ALTERNATIVE (original)
│
├── ⚙️ CONFIGURATION
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          ← All constants & configs
│   │
│   ├── .env                     ← API keys (create from .env.example)
│   ├── .env.example             ← Config template
│   ├── requirements.txt         ← Python dependencies
│   └── .gitignore               ← Git configuration
│
├── 🔧 UTILITIES (Reusable Functions)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── voice_io.py          ← Voice input/output (TTS & STT)
│   │   ├── text_processing.py   ← Text utilities & symbol conversion
│   │   ├── time_utils.py        ← Time & date functions (IST)
│   │   ├── weather.py           ← Weather API integration
│   │   └── logger.py            ← Interaction logging
│
├── 🎯 HANDLERS (Command Processors)
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── greeting_handler.py              ← Greetings
│   │   ├── thank_you_handler.py             ← Thank you responses
│   │   ├── time_handler.py                  ← Time queries
│   │   ├── date_handler.py                  ← Date queries
│   │   ├── simple_weather_handler.py        ← Simple weather (single city)
│   │   ├── weather_handler.py               ← Complex weather detection
│   │   ├── web_handler.py                   ← Web search & browser
│   │   ├── file_handler.py                  ← File operations
│   │   ├── app_handler.py                   ← App launching
│   │   ├── personal_handler.py              ← Personal Q&A
│   │   ├── volume_handler.py                ← Volume control
│   │   ├── close_app_handler.py             ← Close applications
│   │   └── exit_handler.py                  ← Exit commands
│
├── 🤖 API CLIENT
│   └── gemini_client.py         ← Gemini AI integration
│
├── 📝 LOGS
│   └── logs/
│       └── assistant.jsonl      ← Interaction history
│
└── 📚 DOCUMENTATION
    ├── README.md                ← You are here!
    ├── QUICK_START_FINAL.md     ← Quick start guide
    ├── MODULAR_ARCHITECTURE.md  ← Architecture details
    ├── FILE_REFERENCE.md        ← File descriptions
    └── ... (other docs)
```

---

## 🔄 Command Flow Diagram

```
                    START ECHOMIND AI
                           │
                           ▼
                 🎤 Listen for Command
                           │
                           ▼
                 📝 Convert Symbols
                           │
                           ▼
              🔀 Route to Appropriate Handler
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
    ✅ Handler    ✅ Another Handler    ❓ No Match Found
    Processes    Processes             │
    & Responds   & Responds            ▼
                                    🧠 Gemini AI
                                    Fallback
                                       │
                                       ▼
                                    🤖 Generate Response
                                       │
        ┌──────────────────┬──────────┴───────────┐
        ▼                  ▼                      ▼
    🔊 Speak Result    📝 Log Interaction    ➡️ Next Command
```

---

## 🎯 Handler Priority Order

When you speak a command, handlers are checked in this order:

```
1️⃣  Thank You Handler          → Detects: "thank you", "thanks"
2️⃣  Greeting Handler           → Detects: "hello", "hi", "hey"
3️⃣  Time Handler               → Detects: "what time"
4️⃣  Date Handler               → Detects: "what date", "what's the date"
5️⃣  Simple Weather Handler     → Detects: Single city names
6️⃣  Weather Handler            → Detects: Complex weather requests
7️⃣  Web Handler (Search)       → Detects: "search ... on [browser]"
8️⃣  Web Handler (Website)      → Detects: Direct website opening
9️⃣  File Handler               → Detects: File/folder opening
🔟 App Handler                → Detects: App launching
1️⃣1️⃣ Personal Handler          → Detects: Personal questions
1️⃣2️⃣ Volume Handler            → Detects: Volume control
1️⃣3️⃣ Close App Handler         → Detects: Close applications
1️⃣4️⃣ Exit Handler              → Detects: Exit commands
❓ Gemini Fallback             → If no handler matched
```

---

## 🧠 Handler Details

### ✅ Handler Return Values
- **`True`** - Handler processed the command successfully
- **`False`** - Handler didn't match, try next handler
- **Special case** - Exit handler returns special value to trigger exit

### 📝 Handler Template Structure
```python
def handle_my_command(command):
    """
    Process custom commands
    
    Args:
        command (str): User's spoken command
        
    Returns:
        bool: True if handled, False otherwise
    """
    pattern = r'\b(keyword1|keyword2)\b'
    
    if re.search(pattern, command, re.IGNORECASE):
        response = "My custom response"
        speak(response)
        log_interaction(command, response, source="my_handler")
        return True
    
    return False
```

---

## 📚 Code Modules Overview

### 🎤 `utils/voice_io.py`
- **`speak(text)`** - Convert text to speech (cross-platform)
- **`listen()`** - Capture voice input and convert to text

### 📝 `utils/text_processing.py`
- **`convert_spoken_symbols(text)`** - Convert "question mark" → "?"
- **`is_symbol_only(text)`** - Check if text contains only symbols
- **`clean_connector_words(text)`** - Remove connector words

### ⏰ `utils/time_utils.py`
- **`get_time()`** - Get current time in IST (HH:MM format)
- **`get_date()`** - Get current date in IST (with day name)
- **`get_greeting()`** - Get time-based greeting

### 🌤️ `utils/weather.py`
- **`get_weather(city)`** - Fetch weather from OpenWeather API

### 📝 `utils/logger.py`
- **`log_interaction(user, response, source)`** - Log to JSON file

### ⚙️ `config/settings.py`
- **`COMMON_APPS`** - Dictionary of applications
- **`WEBSITE_MAP`** - Dictionary of websites
- **`LOCATION_MAP`** - Dictionary of file locations
- **`PROCESS_NAMES`** - Application process names
- **And more constants...**

---

## 🔌 API Integrations

### 🌤️ OpenWeather API
```python
# Required in .env
OPENWEATHER_API_KEY=your_key_here

# Usage in code
from utils.weather import get_weather
weather_info = get_weather("London")
```

### 🧠 Gemini AI API
```python
# Required in .env
GEMINI_API_KEY=your_key_here

# Optional
GEMINI_API_ENDPOINT=your_endpoint
GEMINI_API_STREAM=true/false

# Usage in code
import gemini_client
response = gemini_client.generate_response(prompt)
```

---

## 🛠️ Customization Guide

### ➕ Add a New Application

Edit `config/settings.py`:
```python
COMMON_APPS = {
    "existing_app": "C:\\path\\to\\app.exe",
    "my_app": "C:\\path\\to\\my_app.exe",  # Add this
}
```

Then speak: "Open my_app"

### ➕ Add a New Website

Edit `config/settings.py`:
```python
WEBSITE_MAP = {
    "existing_site": "https://example.com",
    "mysite": "https://mysite.com",  # Add this
}
```

Then speak: "Open mysite"

### ➕ Create a New Handler

1. Create `handlers/my_feature_handler.py`:
```python
import re
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_my_feature(command):
    """Handle my custom feature"""
    pattern = r'\b(my|keywords)\b'
    
    if re.search(pattern, command, re.IGNORECASE):
        response = "My response"
        speak(response)
        log_interaction(command, response, source="my_feature")
        return True
    
    return False
```

2. Import in `main_refactored.py`:
```python
from handlers.my_feature_handler import handle_my_feature
```

3. Add to handlers list in `route_command()`:
```python
handlers = [
    # ... existing handlers ...
    ("My Feature", handle_my_feature),
]
```

4. Test by speaking your command!

---

## 🐛 Troubleshooting

### ❌ "No module named [module]"
```bash
pip install -r requirements.txt
```

### ❌ Microphone not working
- Check microphone permissions
- Test: `python -c "import speech_recognition; print('OK')"`
- Ensure microphone is not muted

### ❌ API Key errors
- Verify `.env` file exists in project root
- Check keys are not wrapped in quotes
- Keys should look like: `KEY=abc123def456`

### ❌ "GEMINI_API_KEY is not set"
- Add key to `.env`: `GEMINI_API_KEY=your_key`
- Reload the application
- Or set as environment variable

### ❌ Weather returns empty
- Verify `OPENWEATHER_API_KEY` in `.env`
- API key must be valid and active
- City name must be recognized

### ❌ App won't open
- Check app name is in `config/settings.py`
- Verify app is installed on system
- Try full path to executable instead

---

## 📊 Logging

### 📝 Log File Location
```
logs/assistant.jsonl
```

### 📋 Log Entry Format
```json
{
  "timestamp": "2025-11-04T10:30:00Z",
  "user_input": "What time is it?",
  "response": "It's 10:30 AM",
  "handler": "time_handler",
  "status": "success"
}
```

### 📖 Reading Logs
```bash
# View last 10 interactions
tail -10 logs/assistant.jsonl

# Pretty print
python -m json.tool logs/assistant.jsonl

# Search for specific handler
grep "time_handler" logs/assistant.jsonl
```

---

## 🚀 Deployment

### 💻 Local Development
```bash
python main_refactored.py
```

### 🖥️ Run in Background (Linux/macOS)
```bash
nohup python main_refactored.py &
```

### 🪟 Run in Background (Windows)
```powershell
Start-Process python main_refactored.py -WindowStyle Hidden
```

### 🐳 Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main_refactored.py"]
```

Build and run:
```bash
docker build -t echomind-ai .
docker run echomind-ai
```

---

## 📈 Performance Tips

- 🚀 Use `main_refactored.py` (faster startup)
- 📦 Keep `config/settings.py` organized
- 🧹 Clear logs periodically: `rm logs/assistant.jsonl`
- 🔄 Cache API responses when possible
- ⏱️ Set timeouts for API calls

---

## 🔒 Security Best Practices

- 🔑 **Never commit `.env`** to version control
- 🛡️ Use environment variables for sensitive data
- 🔐 Rotate API keys regularly
- 🚫 Don't share `.env` file
- 🔒 Sanitize user input before logging
- ⚠️ Validate API responses before processing

---

## 📚 Learning Resources

- 📖 [Speech Recognition Docs](https://pypi.org/project/SpeechRecognition/)
- 🗣️ [pyttsx3 Documentation](https://pypi.org/project/pyttsx3/)
- ☁️ [OpenWeather API](https://openweathermap.org/api)
- 🤖 [Google Generative AI](https://ai.google.dev/)
- 🐍 [Python Docs](https://docs.python.org/3/)

---

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create your feature branch
3. 💻 Make your changes
4. ✅ Test thoroughly
5. 📝 Commit with clear messages
6. 🚀 Push to your fork
7. 🔄 Create a Pull Request

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🎯 Future Enhancements

- [ ] 🗣️ Multi-language support
- [ ] 📱 Mobile app integration
- [ ] 🏠 Smart home control
- [ ] 📧 Email integration
- [ ] 🔔 Reminder system
- [ ] 🎮 Game integration
- [ ] 📊 Analytics dashboard
- [ ] 👤 User profiles

---

## 💬 Support & Questions

For questions or issues:
1. Check documentation files
2. Review existing handlers
3. Check logs for errors
4. Test in isolation

---

**Happy voice commanding!** 🎉
