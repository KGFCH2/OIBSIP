# 🎙️ EchoMind AI - Voice Assistant

> Advanced Python-based voice assistant with natural language processing, intelligent command routing, and multiple integration features.

**Author:** Babin Bid  
**Repository:** https://github.com/KGFCH2/OIBSIP/tree/main/Voice%20Assistant/EchoMind%20AI  
**License:** MIT License

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Command Features](#-command-features)
3. [Architecture](#️-architecture)
4. [Quick Start](#-quick-start)
5. [Configuration](#️-configuration)
6. [Usage Examples](#-usage-examples)
7. [Project Structure](#-project-structure)
8. [Commands Reference](#-commands-reference)
9. [Handler System](#-handler-system)
10. [Logging](#-logging)
11. [Troubleshooting](#-troubleshooting)
12. [Contributing](#-contributing)
13. [Additional Documentation](#-additional-documentation)
14. [Roadmap](#-roadmap)
15. [FAQ](#-faq)
16. [Support](#-support)
17. [License](#-license)
18. [Credits](#-credits)

---

## ✨ Features

### Core Capabilities

#### 🗣️ Voice I/O
- **Speech Recognition:** Real-time voice input processing
- **Text-to-Speech:** Natural voice feedback using system TTS
- **Streaming Support:** Support for streaming AI responses
- **Multi-language:** English support with extensible architecture

#### 🧠 AI Integration
- **Gemini API:** Advanced AI for unmatched query handling
- **Streaming Responses:** Real-time AI response streaming
- **Smart Fallback:** Automatic fallback to Gemini for unknown commands
- **Context Awareness:** Maintains conversation context

#### 📱 System Integration
- **Windows Search:** App discovery and launching via Windows Search
- **Volume Control:** Voice-controlled speaker volume adjustment
- **Battery Status:** Real-time battery monitoring and alerts
- **USB Detection:** Automatic USB device detection and reporting

---

## 🔧 Command Features

### 📂 File & Folder Management
| Command | Example | Action |
|---------|---------|--------|
| **Open System Folders** | "Open Desktop" | Opens Desktop folder |
| | "Open Downloads" | Opens Downloads folder |
| | "Open Documents" | Opens Documents folder |
| | "Open Pictures" | Opens Pictures folder |
| | "Open Music" | Opens Music folder |
| | "Open Videos" | Opens Videos folder |
| **Open Drives** | "Open drive C" | Opens C:\ drive |
| | "Open drive D" | Opens D:\ drive |
| | "Open drive E" | Opens any connected drive |
| **Close/Eject Drives** | "Close drive C" | Safely ejects C: |
| | "Eject drive D" | Alternative verb |
| | "Unmount drive E" | Another verb option |

### 🌐 Browser & Web
| Command | Example | Action |
|---------|---------|--------|
| **Web Search** | "Search for Python" | Searches in default browser |
| | "Google machine learning" | Google search results |
| **Open Websites** | "Open YouTube" | Opens YouTube.com |
| | "Open GitHub" | Opens GitHub.com |
| **WhatsApp Web** | "Open WhatsApp" | Opens WhatsApp Web |

### 🎵 Multimedia
| Command | Example | Action |
|---------|---------|--------|
| **YouTube Music** | "Play music by artist" | Plays on YouTube |
| | "Play song name" | Searches and plays |
| **Local Music** | "Play music" | Plays local songs |

### 💻 Application Control
| Command | Example | Action |
|---------|---------|--------|
| **Open Apps** | "Open Notepad" | Launches application |
| | "Open Chrome" | Launches browser |
| **Close Apps** | "Close Notepad" | Closes application |
| | "Close Discord" | Closes app instance |
| **Tab Navigation** | "Move to 3rd tab" | Navigates to tab 3 (Ctrl+3) |
| | "Next tab" | Moves to next tab (Ctrl+Tab) |
| | "Previous tab" | Previous tab (Ctrl+Shift+Tab) |
| | "Last tab" | Jump to last tab (Ctrl+9) |
| | "Close current tab" | Closes active tab (Ctrl+W) |

### ⚙️ System Control
| Command | Example | Action |
|---------|---------|--------|
| **Volume** | "Increase volume" | Raises speaker volume |
| | "Decrease volume" | Lowers speaker volume |
| | "Mute" | Mutes audio |
| **Battery** | "Battery status" | Reports battery level |
| | "Check battery" | Battery percentage |
| **USB Devices** | "USB status" | Lists connected USB devices |
| | "Check USB" | Reports USB connections |

### 📝 Utilities
| Command | Example | Action |
|---------|---------|--------|
| **Time** | "What time is it" | Reads current time |
| **Date** | "What's the date" | Reads current date |
| **Weather** | "Weather in London" | Weather information |
| **File Operations** | "Write file" | Creates/writes files |
| **Greeting** | "Hello" | Responds with greeting |
| **Exit** | "Exit" | Closes application |

---

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    subgraph "Voice Input"
        MIC["🎤 Microphone"]
        SR["Speech Recognition<br/>listen()"]
    end
    
    subgraph "Core Processing"
        RM["Request Manager<br/>route_command()"]
        HDB["Handler Database<br/>23+ Handlers"]
    end
    
    subgraph "Handlers"
        H1["Time/Date Handler"]
        H2["Weather Handler"]
        H3["App Handler"]
        H4["Tab Navigation"]
        H5["System Folder Handler"]
        H6["Voice Volume"]
        H7["Gemini Fallback"]
        H8["... More Handlers"]
    end
    
    subgraph "External APIs"
        GEMINI["🤖 Gemini AI"]
        WEATHER["🌤️ Weather API"]
        WINDOWS["🪟 Windows API"]
    end
    
    subgraph "Voice Output"
        TTS["Text-to-Speech<br/>speak()"]
        SPK["🔊 Speaker"]
    end
    
    MIC -->|Audio Stream| SR
    SR -->|Text| RM
    RM -->|Route| HDB
    HDB -->|Dispatch| H1
    HDB -->|Dispatch| H2
    HDB -->|Dispatch| H3
    HDB -->|Dispatch| H4
    HDB -->|Dispatch| H5
    HDB -->|Dispatch| H6
    HDB -->|Dispatch| H7
    HDB -->|Dispatch| H8
    
    H1 -->|Result| RM
    H2 -->|Result| RM
    H3 -->|Result| RM
    H4 -->|Result| RM
    H5 -->|Result| RM
    H6 -->|Result| RM
    H7 -->|Query| GEMINI
    H7 -->|Response| RM
    H2 -->|Query| WEATHER
    H3 -->|System Call| WINDOWS
    
    RM -->|Text/Stream| TTS
    TTS -->|Audio| SPK
    RM -->|Logging| LOG["📊 Logger<br/>assistant.jsonl"]
```

### Command Routing Flow

```mermaid
flowchart TD
    A["👂 User Speaks<br/>Command"] --> B["🎯 listen()<br/>Speech to Text"]
    B --> C["📝 Text Command<br/>Received"]
    C --> D{"Command Type?"}
    
    D -->|Simple Greeting| E["😊 Greeting Handler"]
    D -->|Time/Date| F["⏰ Time/Date Handler"]
    D -->|Weather| G["🌤️ Weather Handler"]
    D -->|File Operation| H["📁 File Handler"]
    D -->|App Operation| I["💻 App Handler"]
    D -->|Tab Navigation| J["📑 Tab Handler"]
    D -->|System Folder| K["📂 Folder Handler"]
    D -->|Drive Operation| K
    D -->|Volume Control| L["🔊 Volume Handler"]
    D -->|Battery Status| M["🔋 Battery Handler"]
    D -->|USB Detection| N["💾 USB Handler"]
    D -->|Unknown Query| O["🤖 Gemini AI<br/>Fallback"]
    
    E --> P["Generate Response"]
    F --> P
    G --> P
    H --> P
    I --> P
    J --> P
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P
    
    P --> Q["✅ Format Response<br/>with ? if question"]
    Q --> R["🔊 speak()<br/>Text to Speech"]
    R --> S["📊 Log to<br/>assistant.jsonl"]
    S --> T["👤 User Hears<br/>Response"]
```

### Handler Priority & Routing

```mermaid
graph LR
    CMD["Command Input"]
    
    CMD --> P1["Priority 1<br/>Text Input<br/>Greeting<br/>Time/Date"]
    P1 --> P2["Priority 2<br/>USB Detection<br/>Search<br/>Website"]
    P2 --> P3["Priority 3<br/>Weather<br/>WhatsApp<br/>File Ops"]
    P3 --> P4["Priority 4<br/>Music<br/>Battery<br/>File Writing"]
    P4 --> P5["Priority 5<br/>System Folder<br/>App Opening"]
    P5 --> P6["Priority 6<br/>Volume<br/>Tab Navigation<br/>App Closing"]
    P6 --> P7["Priority 7<br/>Exit"]
    P7 --> P8["⚠️ Fallback<br/>Gemini AI"]
    
    P1 -.->|Match| DONE1["✅ Done<br/>Return Response"]
    P2 -.->|Match| DONE1
    P3 -.->|Match| DONE1
    P4 -.->|Match| DONE1
    P5 -.->|Match| DONE1
    P6 -.->|Match| DONE1
    P7 -.->|Match| DONE1
    P8 -.->|Match| DONE1
```

### Data Flow Architecture

```mermaid
graph TB
    subgraph "Input Layer"
        A["🎤 Audio Stream"]
        B["🎙️ Speech Recognition"]
        C["📝 Text Command"]
    end
    
    subgraph "Processing Layer"
        D["🔄 Text Normalization"]
        E["🔍 Symbol Conversion"]
        F["✨ Question Mark Detection"]
        G["🧭 Command Routing"]
    end
    
    subgraph "Handler Layer"
        H1["Handler 1"]
        H2["Handler 2"]
        H3["Handler N"]
    end
    
    subgraph "Output Layer"
        I["📄 Format Response"]
        J["🎙️ Text to Speech"]
        K["🔊 Audio Output"]
    end
    
    subgraph "Persistence"
        L["📊 Logging<br/>assistant.jsonl"]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    
    G -->|Route| H1
    G -->|Route| H2
    G -->|Route| H3
    
    H1 -->|Response| I
    H2 -->|Response| I
    H3 -->|Response| I
    
    I --> J
    J --> K
    
    K -.->|Logged| L
    C -.->|Logged| L
    G -.->|Logged| L
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Windows 10/11 (primary support)
- Microphone for voice input
- Speaker for voice output
- Internet connection (for Gemini API & weather)

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd "Voice Assistant/EchoMind AI"
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings:
GEMINI_API_KEY=your_key_here
GEMINI_API_STREAM=true
```

4. **Run Assistant**
```bash
python main_refactored.py
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```ini
# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_STREAM=true          # Enable streaming responses (true/false)

# System Settings
SYSTEM_VOLUME_STEP=5            # Volume change amount per command
BATTERY_CHECK_INTERVAL=30       # Battery check interval in seconds

# Logging
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/assistant.jsonl   # Log file path
```

### Key Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Runtime secrets and API keys (⚠️ Never commit) |
| `.env.example` | Template for .env configuration |
| `config/settings.py` | Application settings and constants |
| `requirements.txt` | Python dependencies |

---

## 📖 Usage Examples

### Basic Usage

```bash
# Start the assistant
python main_refactored.py

# Voice commands
Say: "What time is it?"      → Responds with current time
Say: "Open Desktop"          → Opens Desktop folder
Say: "Close drive E"         → Safely ejects E: drive
Say: "Play music"            → Starts playing music
Say: "Exit"                  → Closes application
```

### Advanced Features

#### Tab Navigation
```
Say: "Move to 5th tab"
Say: "Next tab"
Say: "Previous tab"
Say: "Close current tab"
```

#### Drive Operations
```
Say: "Open drive C"          # Opens C:\ in Explorer
Say: "Close drive D"         # Safely ejects D:
Say: "Eject drive E"         # Alternative syntax
```

#### App Management
```
Say: "Open Notepad"          # Launches Notepad
Say: "Close Chrome"          # Closes Chrome browser
Say: "Search for Python"     # Opens web search
```

---

## 📁 Project Structure

```
EchoMind AI/
├── 📄 .env                        # Environment variables (secrets)
├── 📄 .env.example                # Environment template
├── 📄 .gitignore                  # Git ignore patterns
├── 📄 README.md                   # This file
├── 📄 gemini_client.py            # Gemini AI integration
├── 📄 main_refactored.py          # Main entry point
├── 📄 requirements.txt            # Python dependencies
├── 🗂️ config/                     # Configuration module
│   ├── __init__.py
│   ├── __pycache__/
│   └── settings.py                # Settings & constants
├── 🗂️ handlers/                   # Command handlers (20+)
│   ├── __init__.py
│   ├── __pycache__/
│   ├── app_handler.py             # App opening/launching
│   ├── battery_handler.py         # Battery status monitoring
│   ├── close_app_handler.py       # App closing/tab control
│   ├── date_handler.py            # Date queries
│   ├── exit_handler.py            # Exit command
│   ├── file_handler.py            # File operations
│   ├── file_writing_handler.py    # File writing operations
│   ├── greeting_handler.py        # Greeting responses
│   ├── music_handler.py           # Music playback
│   ├── personal_handler.py        # Personal questions
│   ├── simple_weather_handler.py  # Simple weather queries
│   ├── system_folder_handler.py   # Folder & drive operations
│   ├── tab_navigation_handler.py  # Tab navigation (Ctrl+N)
│   ├── text_input_handler.py      # Text input handling
│   ├── thank_you_handler.py       # Thank you responses
│   ├── time_handler.py            # Time queries
│   ├── usb_detection_handler.py   # USB device detection
│   ├── volume_handler.py          # Volume control
│   ├── weather_handler.py         # Weather queries
│   └── web_handler.py             # Web search & browser
├── 🗂️ logs/                       # Log storage
│   └── assistant.jsonl            # JSON logs of all operations
├── 🗂️ utils/                      # Utility modules
│   ├── __init__.py
│   ├── __pycache__/
│   ├── logger.py                  # Logging utilities
│   ├── text_processing.py         # Text processing & normalization
│   ├── time_utils.py              # Time utility functions
│   ├── voice_io.py                # Voice input/output operations
│   └── weather.py                 # Weather API utilities
└── 🗂️ __pycache__/                # Python bytecode cache
```

---

## 🎮 Commands Reference

### Time & Date
| Say | Response |
|-----|----------|
| "What time is it?" | Current time |
| "What's the time?" | Current time |
| "What date is it?" | Current date |
| "Today's date" | Current date |

### System
| Say | Response |
|-----|----------|
| "Battery status" | Battery percentage & status |
| "USB devices" | List of connected USB |
| "Increase volume" | Raises volume |
| "Decrease volume" | Lowers volume |

### Files & Folders
| Say | Response |
|-----|----------|
| "Open Desktop" | Opens Desktop folder |
| "Open Downloads" | Opens Downloads folder |
| "Open drive C" | Opens C:\ drive |
| "Close drive E" | Safely ejects E: |
| "Write file" | Creates/writes file |

### Browser & Web
| Say | Response |
|-----|----------|
| "Search Python" | Web search in browser |
| "Open YouTube" | Opens YouTube.com |
| "Open GitHub" | Opens GitHub.com |
| "Open WhatsApp" | Opens WhatsApp Web |

### Applications
| Say | Response |
|-----|----------|
| "Open Notepad" | Launches Notepad |
| "Open Chrome" | Launches Chrome browser |
| "Close Discord" | Closes Discord app |
| "Move to 3rd tab" | Navigates to tab 3 |

### General
| Say | Response |
|-----|----------|
| "Hello" | Greeting response |
| "Thank you" | Thank you response |
| "Exit" / "Quit" | Closes application |

---

## 🔍 Handler System

### How Handlers Work

Each handler is a specialized module that:
1. **Detects** specific command patterns (regex matching)
2. **Processes** the command logic
3. **Returns** response or False (if not matched)

### Handler Priority

Commands are checked in this order:
1. Text input mode
2. Greeting & thank you
3. Time & date
4. USB & search
5. Website & weather
6. Battery & media
7. File operations
8. System folders
9. App launching
10. Personal questions
11. Volume control
12. Tab navigation & app closing
13. Exit command
14. **Gemini AI Fallback** (for unmatched queries)

### Adding Custom Handlers

1. Create `handlers/custom_handler.py`:
```python
def handle_custom_command(command):
    if "trigger_word" in command.lower():
        # Process command
        from utils.voice_io import speak
        speak("Custom response")
        return True
    return False
```

2. Add to `main_refactored.py`:
```python
from handlers.custom_handler import handle_custom_command
# ... in handlers list
("Custom feature", handle_custom_command),
```

---

## 📊 Logging

All voice commands and responses are logged to `logs/assistant.jsonl`:

```json
{
  "timestamp": "2025-11-06T10:30:00Z",
  "command": "Open Desktop",
  "response": "Opening Desktop folder",
  "source": "local",
  "status": "success"
}
```

---

## 🐛 Troubleshooting

### Voice Not Recognized
- Check microphone is connected and working
- Speak clearly and in English
- Check system volume is adequate

### Commands Not Working
- Verify .env configuration is correct
- Check logs in `logs/assistant.jsonl`
- Ensure dependencies are installed (`pip install -r requirements.txt`)

### Gemini API Errors
- Verify `GEMINI_API_KEY` in .env is correct
- Check internet connection
- Check API quota/limits

### App Won't Start
- Ensure Python 3.13+ is installed
- Run `pip install -r requirements.txt` 
- Check .env file exists and is configured

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Create a feature branch (`git checkout -b feature/new-feature`)
2. Commit changes (`git commit -am 'Add feature'`)
3. Push to branch (`git push origin feature/new-feature`)
4. Open a Pull Request

---

## 📚 Additional Documentation

For detailed feature documentation, see:

- **Tab Navigation:** `TAB_NAVIGATION_FEATURE.md`
- **System Folders & Drives:** `SYSTEM_FOLDER_DRIVE_OPENING_FEATURE.md`
- **Drive Closing/Ejection:** `DRIVE_CLOSING_FEATURE.md`

---

## 🎯 Roadmap

### Planned Features
- [ ] Multi-language support (Spanish, French, German)
- [ ] Custom voice profiles
- [ ] Smart home integration
- [ ] Email integration
- [ ] Calendar management
- [ ] Task management

### Performance Improvements
- [ ] Command caching
- [ ] Faster speech recognition
- [ ] Offline mode support
- [ ] Response time optimization

---

## ❓ FAQ

**Q: Does it require internet?**
A: Yes, for Gemini AI and weather features. Local commands work offline.

**Q: Can I add custom commands?**
A: Yes! Create a handler in `handlers/` and add to routing in `main_refactored.py`.

**Q: Is it free to use?**
A: Yes, but requires Gemini API key (free tier available).

**Q: What operating systems are supported?**
A: Primary: Windows 10/11. Secondary: macOS (partial), Linux (partial).

**Q: How is my data handled?**
A: All data is logged locally in `logs/assistant.jsonl`. No data sent elsewhere except Gemini API queries.

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review logs in `logs/assistant.jsonl`

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### License Summary

This is **Babin Bid's personal project**. You are free to:
- ✅ Use for personal, educational, or commercial purposes
- ✅ Modify and distribute the code
- ✅ Create derivative works
- ✅ Use commercially

You must:
- 📋 Include the original license and copyright notice
- 📋 Document any significant modifications
- 📋 Provide a copy of the LICENSE file with distributions

### Third-Party Libraries

This project uses several open-source libraries:
- **pyttsx3** - Text-to-speech (Apache License 2.0)
- **SpeechRecognition** - Speech recognition (BSD 3-Clause License)
- **google-generativeai** - Google Gemini AI integration (Apache License 2.0)
- **pyautogui** - GUI automation (BSD 3-Clause License)
- **requests** - HTTP library (Apache License 2.0)
- **python-dotenv** - Environment variable management (BSD 3-Clause License)

See `requirements.txt` and individual package documentation for more details.

---

## 🎉 Credits

Built with Python, integrated with:
- Google Gemini AI
- Windows API
- pyautogui for automation
- pyttsx3 for text-to-speech

**Project Author:** Babin Bid  
**GitHub:** https://github.com/KGFCH2/OIBSIP/tree/main/Voice%20Assistant/EchoMind%20AI

---

**Last Updated:** November 6, 2025
**Version:** 1.0
**Status:** Production Ready ✅

---

<div align="center">

### 📖 [Back to Top](https://github.com/KGFCH2/OIBSIP/tree/main/Voice%20Assistant/EchoMind%20AI) ⬆️

</div>
