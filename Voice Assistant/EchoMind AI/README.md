# EchoMind AI — EchoMind Basic

EchoMind Basic is a beginner-level Python voice assistant that listens to your voice, interprets simple commands, and replies using text-to-speech.

Features
- Listen to voice and convert to text (SpeechRecognition)
- Speak responses (pyttsx3)
- Answer greetings
- Tell the current time and date
- Search Wikipedia for a topic
- Open websites (Google, YouTube) and perform Google searches

Quick start

1. Create and activate a Python environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1    # PowerShell
   # or: .\.venv\Scripts\activate  # cmd.exe
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   If `PyAudio` fails to install on Windows, try:

   ```powershell
   pip install pipwin
   pipwin install pyaudio
   ```

3. Run the assistant:

   ```powershell
   python echomind_basic.py
   ```

   To run in text-only mode (no speech output, useful if your system TTS isn't working or you prefer text responses):

   ```powershell
   python echomind_basic.py --text-only
   ```

Usage notes
- Speak clearly into your microphone. The assistant listens continuously until you say "stop", "quit", or "exit".
- Commands to try: "Hello", "What's the time?", "What's the date?", "Search Wikipedia for Python programming", "Open YouTube", "Search Google for cats".

Troubleshooting
- If the microphone is not found, make sure your OS has granted microphone permission and the device is connected.
- If speech recognition does not work offline, `recognize_google` uses an online service; ensure you have internet access for recognition and Wikipedia searches.

License
- This is a small demo project for learning; adapt and extend as needed.
