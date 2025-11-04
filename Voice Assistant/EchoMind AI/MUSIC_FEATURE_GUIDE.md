🎵 MUSIC PLAYBACK FEATURE - QUICK REFERENCE
==========================================

The voice assistant now supports direct music playback on YouTube!

INSTALLATION:
=============
The music feature is already integrated. No additional dependencies required.
It uses the existing Chrome browser and YouTube's search functionality.

USAGE COMMANDS:
===============

1. BASIC PLAY COMMAND:
   Voice: "play bohemian rhapsody"
   Result: Opens YouTube search results for "bohemian rhapsody"

2. PLAY WITH ARTIST:
   Voice: "play imagine by john lennon"
   Result: Searches "imagine by john lennon" on YouTube

3. PLAY MUSIC VARIANT:
   Voice: "play music stairway to heaven"
   Result: Searches "stairway to heaven" on YouTube

4. EXPLICIT YOUTUBE COMMAND:
   Voice: "play thriller on youtube"
   Result: Opens YouTube and plays search results for "thriller"

SUPPORTED PATTERNS:
===================
✓ play [song]
✓ play [song] by [artist]
✓ play music [song]
✓ play [song] on youtube

WHAT HAPPENS:
=============
1. Voice command is recognized
2. Assistant confirms: "Searching for [song] on YouTube"
3. Chrome browser opens automatically
4. YouTube search results page displays matching songs
5. User can click the first result to play

HOW IT WORKS:
=============
File: handlers/music_handler.py

Contains two functions:
- handle_play_music(): Handles basic "play" commands
- handle_play_on_youtube(): Handles explicit YouTube commands

Both functions:
1. Use regex patterns to match and extract song name
2. Build a YouTube search URL
3. Open the URL in Chrome browser
4. Log the interaction

BROWSER REQUIREMENT:
====================
- Windows: Uses Chrome via "start chrome" command
- macOS: Uses Chrome via "open -a" command
- Linux: Uses "google-chrome" command

If Chrome is not available, you can modify the handler to use:
- Firefox: subprocess.Popen(["firefox", url])
- Edge: subprocess.Popen(["msedge", url])
- Default browser: webbrowser.open(url)

EXAMPLE INTERACTIONS:
====================

User: "play shape of you"
Assistant: "Searching for shape of you on YouTube"
Result: YouTube opens with search results

User: "play hotel california by eagles"
Assistant: "Searching for hotel california by eagles on YouTube"
Result: YouTube opens with song search

User: "play music under the bridge"
Assistant: "Searching for under the bridge on YouTube"
Result: YouTube opens with search results

LOGGING:
========
All music requests are logged to logs/assistant.jsonl with:
- Source: "music"
- Command: Original voice command
- Query: Extracted song name

Example log entry:
{
  "timestamp": "2025-11-04T10:30:45.123456",
  "command": "play imagine by john lennon",
  "response": "YouTube search: imagine by john lennon",
  "source": "music"
}

CUSTOMIZATION:
==============
You can modify the handler to:
1. Use different search engines (Google Music, Spotify, etc.)
2. Extract additional metadata (album, year)
3. Add speech confirmation variations
4. Integrate with music streaming APIs

For advanced features, see gemini_client.py for AI integration patterns.
