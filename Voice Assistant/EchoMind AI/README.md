# EchoMind AI Voice Assistant

## Idea: Voice Assistant

## Description:

### For Beginners:
Create a basic voice assistant that can perform simple tasks based on voice commands. Implement features like responding to "Hello" and providing predefined responses, telling the time or date, and searching the web for information based on user queries.

### For Advanced:
Develop an advanced voice assistant with natural language processing capabilities. Enable it to perform tasks such as sending emails, setting reminders, providing weather updates, controlling smart home devices, answering general knowledge questions, and even integrating with third-party APIs for more functionality.

## Key Concepts and Challenges:

- **Speech Recognition:** Learn how to recognize and process voice commands using speech recognition libraries or APIs.
- **Natural Language Processing (for Advanced):** Implement natural language understanding to interpret and respond to user queries.
- **Task Automation (for Advanced):** Integrate with various APIs and services to perform tasks like sending emails or fetching weather data.
- **User Interaction:** Create a user-friendly interaction design that allows users to communicate with the assistant via voice commands.
- **Error Handling:** Handle potential issues with voice recognition, network requests, or task execution.
- **Privacy and Security (for Advanced):** Address security and privacy concerns when handling sensitive tasks or personal information.
- **Customization (for Advanced):** Allow users to personalize the assistant by adding custom commands or integrations.

## Cross-Platform Support

This voice assistant is designed to work on multiple operating systems:

- **Windows:** Uses PowerShell for TTS, cmd start for app launching
- **macOS:** Uses `say` command for TTS, `open` command for apps
- **Linux:** Uses `espeak` or `festival` for TTS, `xdg-open` for apps

## Installation

1. Install Python 3.x
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the project root and add your OpenWeather API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```
4. (Optional) Add your Gemini API key to the `.env` as well:
  ```
  GEMINI_API_KEY=your_gemini_api_key_here
  ```
  - Use `.env.example` as a template. Do NOT commit `.env` to version control.
  - The project includes a `gemini_client.py` template showing where to wire a
    streaming Gemini client. You must implement the provider-specific streaming
    logic there.
   - Optionally set `GEMINI_API_ENDPOINT` in `.env` to point to an HTTP endpoint
     that accepts POST {"prompt": "..."} and returns a JSON response.
     If `GEMINI_API_ENDPOINT` is set the assistant will call it with
     Authorization: Bearer $GEMINI_API_KEY and attempt to extract text from the
     response. Use this if you have a provider or proxy URL for Gemini/Generative
     AI (do not store keys in source control). Example in `.env.example`.
4. Run the assistant: `python main.py`

## Usage

Speak commands like:
- "Hello", "Hi", "Hey" → Greeting response
- "What time is it?", "Current time" → Current time
- "What date is it?", "Today's date" → Current date and day of the week in IST
- "Weather", "Forecast" → Weather information (asks for city)
- "Search for [query]", "Google [query]", "Find [query]" → Web search
- "Open [app name]", "Launch [app name]", "Start [app name]" → Open applications
  - Examples: "open notepad", "launch calculator", "start chrome", "open word", "open camera"
  - Can specify app name directly in command or respond when prompted
- "How are you?" → Personal response
- "What's your name?", "Who are you?" → Introduction
- "Exit", "Quit", "Stop", "Bye" → Exit the program

The assistant uses flexible keyword matching to understand various phrasings of commands.

## Features

- **Time-Based Greetings**: The assistant greets you with "Good morning", "Good afternoon", "Good evening", or "Good night" based on the current time in Indian Standard Time (IST)
- **IST Time & Date**: All time and date responses are provided in Indian Standard Time (Asia/Kolkata timezone)
- **Voice Commands**: Supports flexible voice commands for time, date, weather, web search, and more
- **Text-to-Speech**: Uses pyttsx3 for Windows, system commands for macOS/Linux
- **Weather Integration**: Provides current weather information using OpenWeather API
- **Web Search**: Opens Google search results for user queries
- **App Launcher**: Can open any application installed on your device by name