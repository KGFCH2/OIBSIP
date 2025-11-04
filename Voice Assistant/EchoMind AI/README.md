# 🎤 EchoMind AI Voice Assistant

> An intelligent, cross-platform voice assistant powered by AI 🤖

## 💡 Idea: Voice Assistant

## 📝 Description:

### 👶 For Beginners:
Create a basic voice assistant that can perform simple tasks based on voice commands. Implement features like responding to "Hello" and providing predefined responses, telling the time or date, and searching the web for information based on user queries.

### 🚀 For Advanced:
Develop an advanced voice assistant with natural language processing capabilities. Enable it to perform tasks such as sending emails, setting reminders, providing weather updates, controlling smart home devices, answering general knowledge questions, and even integrating with third-party APIs for more functionality.

## 🎯 Key Concepts and Challenges:

- 🎙️ **Speech Recognition:** Learn how to recognize and process voice commands using speech recognition libraries or APIs.
- 🧠 **Natural Language Processing (for Advanced):** Implement natural language understanding to interpret and respond to user queries.
- ⚙️ **Task Automation (for Advanced):** Integrate with various APIs and services to perform tasks like sending emails or fetching weather data.
- 💬 **User Interaction:** Create a user-friendly interaction design that allows users to communicate with the assistant via voice commands.
- ⚠️ **Error Handling:** Handle potential issues with voice recognition, network requests, or task execution.
- 🔒 **Privacy and Security (for Advanced):** Address security and privacy concerns when handling sensitive tasks or personal information.
- 🎨 **Customization (for Advanced):** Allow users to personalize the assistant by adding custom commands or integrations.

## 🖥️ Cross-Platform Support

This voice assistant is designed to work on multiple operating systems:

- **🪟 Windows:** Uses PowerShell for TTS, cmd start for app launching
- **🍎 macOS:** Uses `say` command for TTS, `open` command for apps
- **🐧 Linux:** Uses `espeak` or `festival` for TTS, `xdg-open` for apps

## ⚙️ Installation

### 📋 Prerequisites:
- Python 3.8 or higher
- Microphone (for voice input)
- Internet connection (for APIs)

### 🔧 Setup Steps:

1. **📥 Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **🔑 Create Environment Configuration:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env    # macOS/Linux
     copy .env.example .env  # Windows
     ```
   - Add your API keys to `.env`:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - **⚠️ IMPORTANT:** Never commit `.env` to version control!

3. **🤖 Optional Gemini AI Setup:**
   - The project includes `gemini_client.py` template
   - Implement provider-specific streaming logic
   - Set `GEMINI_API_ENDPOINT` in `.env` if using HTTP endpoint:
     ```
     GEMINI_API_ENDPOINT=https://your-provider.com/api
     GEMINI_API_STREAM=true
     ```

4. **🚀 Run the Assistant:**
   ```bash
   python main_refactored.py    # Recommended (modular version)
   # OR
   python main.py               # Alternative (original version)
   ```

## 🎤 Usage

### 📢 Voice Commands:

**🙋 Greetings:**
- "Hello", "Hi", "Hey" → ✅ Greeting response

**⏰ Time & Date:**
- "What time is it?", "Current time" → ⏱️ Current time (IST)
- "What date is it?", "Today's date" → 📅 Current date and day of the week (IST)

**🌤️ Weather:**
- "Weather", "Forecast" → 🌡️ Weather information (asks for city)
- "Weather in London" → Weather for specific city

**🔍 Web Search:**
- "Search for [query]", "Google [query]", "Find [query]" → 🔎 Web search
- "Search Python tutorials on Google" → Opens search in browser

**🎵 Music & YouTube:**
- "Play [song name]" → 🎵 Search and open song on YouTube
- "Play [song name] by [artist]" → Search specific artist's song
- "Play music [song name]" → Alternative music command
- **Examples:**
  - "play imagine by john lennon"
  - "play bohemian rhapsody"
  - "play music stairway to heaven"

**💻 App Launching:**
- "Open [app name]", "Launch [app name]", "Start [app name]" → 🚀 Open applications
- **Examples:** 
  - "open notepad"
  - "launch calculator"
  - "start chrome"
  - "open word"
  - "open camera"

**💬 Personal Questions:**
- "How are you?" → 😊 Personal response
- "What's your name?", "Who are you?" → 🤖 Introduction

**🔊 Volume Control:**
- "Increase volume", "Turn up volume" → 🔉 Volume up
- "Decrease volume", "Turn down volume" → 🔉 Volume down

**📁 File Management:**
- "Open downloads" → 📂 Opens Downloads folder
- "Show documents" → 📂 Opens Documents folder

**🚪 Exit:**
- "Exit", "Quit", "Stop", "Bye", "Goodbye" → 👋 Exit the program

> The assistant uses flexible keyword matching to understand various phrasings of commands.

## ⭐ Features

- 🎉 **Time-Based Greetings:** The assistant greets you with "Good morning", "Good afternoon", "Good evening", or "Good night" based on the current time in Indian Standard Time (IST)
- 🌏 **IST Time & Date:** All time and date responses are provided in Indian Standard Time (Asia/Kolkata timezone)
- 🎤 **Voice Commands:** Supports flexible voice commands for time, date, weather, web search, music, and more
- 🔊 **Text-to-Speech:** Uses pyttsx3 for Windows, system commands for macOS/Linux
- 🌤️ **Weather Integration:** Provides current weather information using OpenWeather API
- 🔍 **Web Search:** Opens Google search results for user queries in your browser
- 🎵 **Music Playback:** Search and play songs directly from YouTube with voice commands
- 🚀 **App Launcher:** Can open any application installed on your device by name
- 🧠 **AI Integration:** Uses Gemini API for intelligent responses to unknown commands
- 📝 **Interaction Logging:** Automatically logs all interactions to `logs/assistant.jsonl`
- 📚 **Modular Architecture:** Clean, organized code structure with specialized handlers
- 🖥️ **Cross-Platform:** Works on Windows, macOS, and Linux with automatic platform detection